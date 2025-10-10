# scryfall_fetch.py
# Config-driven fetcher for Scryfall catalogs and bulk files.
# Uses JSON sidecar metadata. Supports gzip detect, preview, checksum, and cache cleaning.

import os, json, gzip, argparse, hashlib, requests, datetime, shutil, time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

# -------------------- config --------------------
def load_cfg(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def cfg_fetch_lists(cfg: dict) -> tuple[List[str], List[str]]:
    f = cfg.get("fetch", {})
    # catalogs
    cat = []
    ovr = (f.get("catalogs", {}) or {}).get("override", []) or []
    if ovr:
        cat = list(dict.fromkeys(ovr))
    elif (f.get("catalogs", {}) or {}).get("from_catalog_mappings", False):
        # derive from top-level catalogs[] entries
        cat = [c.get("name") for c in (cfg.get("catalogs") or []) if c.get("name")]
    else:
        # fallback to a safe default set
        cat = [
            "card-names","artist-names","word-bank","supertypes","card-types",
            "artifact-types","battle-types","creature-types","enchantment-types",
            "land-types","planeswalker-types","spell-types","powers","toughnesses",
            "loyalties","keyword-abilities","keyword-actions","ability-words",
            "flavor-words","watermarks",
        ]
    # bulks
    bulks = (f.get("bulks") or {}).get("types", ["default_cards","oracle_cards","rulings"])
    return cat, bulks

def cfg_http(cfg: dict):
    f = cfg.get("fetch", {})
    h = f.get("http", {}) or {}
    tout = (h.get("timeout_connect_sec", 10), h.get("timeout_read_sec", 600))
    ua = h.get("user_agent", "KarnAI/1.0 (+github.com/tucktuck101/karnai)")
    retries = int(h.get("retries", 3))
    backoff = float(h.get("backoff_factor", 0.5))
    proxies = h.get("proxies", {}) or {}
    return ua, tout, retries, backoff, proxies

def cfg_paths(cfg: dict):
    f = cfg.get("fetch", {})
    outdir = Path(f.get("outdir", "etl/cache"))
    tmpl = (f.get("download", {}) or {}).get("filename_template", "{type}_{id}.jsonl.gz")
    return outdir, tmpl

def cfg_flags(cfg: dict):
    f = cfg.get("fetch", {})
    d = f.get("download", {}) or {}
    return {
        "detect_gzip": bool(d.get("detect_gzip", True)),
        "preview": bool(d.get("preview_first_line", True)),
        "sha256": bool(d.get("compute_sha256", True)),
        "chunk_bytes": int(d.get("chunk_bytes", 1024 * 1024)),
        "use_sidecar_meta": bool(f.get("use_sidecar_meta", True)),
    }

def cfg_clean(cfg: dict):
    cl = (cfg.get("fetch", {}) or {}).get("clean", {}) or {}
    patterns = cl.get("patterns", [
        "catalog_*.meta.json","catalogs/*.json","bulk/*.jsonl","bulk/*.jsonl.gz","bulk/*.meta.json",
    ])
    empty_dirs = cl.get("remove_empty_dirs", ["catalogs","bulk"])
    return patterns, empty_dirs

# -------------------- session + retry --------------------
def make_session(ua: str, proxies: Dict[str,str]) -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": ua})
    if proxies:
        s.proxies.update(proxies)
    return s

def with_retry(fn, retries: int, backoff: float):
    for i in range(retries):
        try:
            return fn()
        except requests.RequestException as e:
            if i == retries - 1:
                raise
            time.sleep(backoff * (2 ** i))

# -------------------- meta helpers --------------------
def utc_now() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

def is_gzip(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(2) == b"\x1f\x8b"
    except FileNotFoundError:
        return False

def sha256_hex(path: Path, chunk_size: int) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()

def load_meta(meta_path: Path) -> dict:
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_meta(meta_path: Path, meta: dict) -> None:
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def headers_with_meta(meta_path: Path) -> Dict[str, str]:
    meta = load_meta(meta_path)
    et = meta.get("etag") or ""
    return {"If-None-Match": et} if et else {}

# -------------------- IO --------------------
def fetch_json(session: requests.Session, url: str, meta_path: Path, timeout, retries, backoff) -> Optional[dict]:
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    def _call():
        return session.get(url, headers=headers_with_meta(meta_path), timeout=timeout)
    r = with_retry(_call, retries, backoff)
    if r.status_code == 304:
        print(f"[304] {url}")
        return None
    r.raise_for_status()
    data = r.json()
    meta = load_meta(meta_path)
    meta.update({
        "url": url,
        "etag": r.headers.get("ETag", ""),
        "content_type": r.headers.get("Content-Type", ""),
        "fetched_at_utc": utc_now(),
        "size_bytes": len(r.content),
    })
    save_meta(meta_path, meta)
    return data

def save_json_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[write] {path}")

def stream_download(session: requests.Session, url: str, target: Path, meta_path: Path,
                    timeout, retries, backoff, chunk_bytes: int) -> Tuple[bool, Path]:
    def _call():
        return session.get(url, headers=headers_with_meta(meta_path), stream=True, timeout=timeout)
    r = with_retry(_call, retries, backoff)
    if r.status_code == 304:
        print(f"[304] {target.name}")
        return False, target
    r.raise_for_status()
    tmp = target.with_suffix(target.suffix + ".part")
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(tmp, "wb") as f:
        for chunk in r.iter_content(chunk_bytes):
            if chunk:
                f.write(chunk)
    os.replace(tmp, target)
    meta = load_meta(meta_path)
    meta.update({
        "url": url,
        "etag": r.headers.get("ETag", ""),
        "content_type": r.headers.get("Content-Type", ""),
        "fetched_at_utc": utc_now(),
        "size_bytes": target.stat().st_size,
        "saved_as": str(target),
    })
    save_meta(meta_path, meta)
    print(f"[get ] {target.name}  {target.stat().st_size:,} bytes")
    return True, target

# -------------------- workflows --------------------
def fetch_catalogs(session, outdir: Path, names: List[str], timeout, retries, backoff):
    cat_dir = outdir / "catalogs"
    for name in names:
        url = f"https://api.scryfall.com/catalog/{name}"
        meta = outdir / f"catalog_{name}.meta.json"
        data = fetch_json(session, url, meta, timeout, retries, backoff)
        if data is not None:
            save_json_file(cat_dir / f"{name}.json", data)

def bulk_index(session, timeout, retries, backoff) -> dict:
    def _call():
        return session.get("https://api.scryfall.com/bulk-data", timeout=timeout)
    r = with_retry(_call, retries, backoff)
    r.raise_for_status()
    return r.json()

def select_bulks(index: dict, types: List[str]) -> Dict[str, dict]:
    found: Dict[str, dict] = {}
    for item in index.get("data", []):
        t = item.get("type")
        if t in types:
            found[t] = item
    missing = [t for t in types if t not in found]
    if missing:
        raise RuntimeError(f"Bulk types not found: {missing}")
    return found

def fetch_bulks(session, outdir: Path, types: List[str], timeout, retries, backoff, flags, fname_tmpl: str):
    idx = bulk_index(session, timeout, retries, backoff)
    chosen = select_bulks(idx, types)
    for t, meta in chosen.items():
        uri = meta["download_uri"]; bid = meta["id"]
        raw_name = fname_tmpl.format(type=t, id=bid)
        out = outdir / "bulk" / raw_name
        meta_path = out.with_suffix(out.suffix + ".meta.json")

        _, saved = stream_download(session, uri, out, meta_path, timeout, retries, backoff, flags["chunk_bytes"])

        gz = is_gzip(saved) if flags["detect_gzip"] else saved.suffix == ".gz"
        if flags["detect_gzip"] and (not gz) and saved.suffix == ".gz":
            new_path = saved.with_suffix("")  # drop .gz
            os.replace(saved, new_path)
            saved = new_path

        if flags["preview"]:
            try:
                if gz:
                    with gzip.open(saved, "rt", encoding="utf-8") as f: _ = f.readline()
                else:
                    with open(saved, "rt", encoding="utf-8", errors="replace") as f: _ = f.readline()
                print(f"[ok  ] {t} preview")
            except OSError:
                print(f"[warn] {t} preview failed")

        digest = ""
        if flags["sha256"]:
            digest = sha256_hex(saved, flags["chunk_bytes"])
            print(f"[sha ] {t} {digest}")

        side = load_meta(meta_path)
        side.update({
            "bulk_type": t,
            "bulk_id": bid,
            "final_path": str(saved),
            **({"sha256": digest} if digest else {}),
        })
        save_meta(meta_path, side)

# -------------------- cleaner --------------------
def clear_cache(outdir: Path, patterns: List[str], empty_dirs: List[str], dry_run: bool) -> None:
    if not outdir.exists():
        print(f"[skip] {outdir} does not exist"); return
    removed = 0
    for pat in patterns:
        for p in outdir.glob(pat):
            if p.is_file():
                print(("[del ]" if not dry_run else "[dry ]") + f" {p}")
                if not dry_run:
                    try:
                        p.unlink(); removed += 1
                    except FileNotFoundError:
                        pass
    for sub in empty_dirs:
        d = outdir / sub
        if d.exists():
            try:
                if dry_run:
                    print(f"[dry ] rmdir {d}")
                else:
                    shutil.rmtree(d); print(f"[rmdir] {d}")
            except FileNotFoundError:
                pass
    print(f"[done] files removed: {removed} (dry-run={dry_run})")

# -------------------- CLI --------------------
def main():
    ap = argparse.ArgumentParser(description="Fetch Scryfall catalogs and bulk files using etl/config.yml.")
    ap.add_argument("--config", default="etl/config.yml", help="Path to YAML config")
    ap.add_argument("--catalogs", action="store_true", help="Fetch catalogs")
    ap.add_argument("--bulks", action="store_true", help="Fetch bulk files")
    ap.add_argument("--all", action="store_true", help="Fetch both")
    ap.add_argument("--clear-cache", action="store_true", help="Delete cached files under outdir")
    ap.add_argument("--dry-run", action="store_true", help="With --clear-cache, show what would be deleted")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        raise SystemExit(f"config not found: {cfg_path}")
    cfg = load_cfg(cfg_path)

    outdir, fname_tmpl = cfg_paths(cfg)
    outdir.mkdir(parents=True, exist_ok=True)
    patterns, empty_dirs = cfg_clean(cfg)
    flags = cfg_flags(cfg)
    ua, timeout, retries, backoff, proxies = cfg_http(cfg)
    session = make_session(ua, proxies)

    cats, bulk_types = cfg_fetch_lists(cfg)

    if args.clear_cache:
        clear_cache(outdir, patterns, empty_dirs, dry_run=args.dry_run)
        return

    if not (args.catalogs or args.bulks or args.all):
        ap.print_help(); return

    if args.all or args.catalogs:
        fetch_catalogs(session, outdir, cats, timeout, retries, backoff)
    if args.all or args.bulks:
        fetch_bulks(session, outdir, bulk_types, timeout, retries, backoff, flags, fname_tmpl)

if __name__ == "__main__":
    main()
