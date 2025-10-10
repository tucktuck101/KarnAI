# etl_stage.py
# Stage Scryfall bulk files into MSSQL using etl/config.yml mappings.
# Reads bulk "type" -> "stage_table" from YAML. Streams JSONL and JSONL.GZ.

import argparse, gzip
from pathlib import Path
import pyodbc, yaml

def latest_file(cache_dir: Path, prefix: str) -> Path | None:
    cands = list(cache_dir.glob(f"{prefix}_*.jsonl")) + list(cache_dir.glob(f"{prefix}_*.jsonl.gz"))
    if not cands: return None
    return max(cands, key=lambda p: p.stat().st_mtime)

def line_iter(path: Path):
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f: 
                ln = line.rstrip("\n")
                if ln: yield ln
    else:
        with open(path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                ln = line.rstrip("\n")
                if ln: yield ln

def stage_one(cn, table: str, bulk_path: Path, truncate: bool, chunk: int):
    cur = cn.cursor()
    if truncate:
        cur.execute(f"IF OBJECT_ID('{table}','U') IS NOT NULL TRUNCATE TABLE {table};")
    else:
        # ensure table exists
        cur.execute(f"""
IF OBJECT_ID('{table}','U') IS NULL
BEGIN
    DECLARE @sch sysname = PARSENAME('{table}',2);
    IF @sch IS NOT NULL AND NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name=@sch)
        EXEC('CREATE SCHEMA ' + QUOTENAME(@sch));
    EXEC('CREATE TABLE {table} (raw NVARCHAR(MAX) NOT NULL)');
END
""")
    cur.fast_executemany = True

    batch, total = [], 0
    for ln in line_iter(bulk_path):
        batch.append((ln,))
        if len(batch) >= chunk:
            cur.executemany(f"INSERT INTO {table}(raw) VALUES (?)", batch)
            total += len(batch); batch.clear()
    if batch:
        cur.executemany(f"INSERT INTO {table}(raw) VALUES (?)", batch)
        total += len(batch)

    print(f"[stage] {table}: {total:,} rows from {bulk_path.name}")

def load_cfg(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def build_conn_str(args, cfg_sql) -> str:
    server   = args.server   or cfg_sql.get("server")   or ""
    database = args.database or cfg_sql.get("database") or ""
    auth     = "trusted" if args.trusted else (cfg_sql.get("auth","trusted").lower())
    if auth == "trusted":
        return (
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server={server};Database={database};Trusted_Connection=yes;"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )
    user = args.username or cfg_sql.get("username") or ""
    pwd  = args.password or cfg_sql.get("password") or ""
    return (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={server};Database={database};UID={user};PWD={pwd};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )

def resolve_types(cfg: dict, types_arg: list[str] | None, all_flag: bool) -> list[tuple[str,str]]:
    bulks = cfg.get("bulks", [])
    type_to_stage = {b["type"]: b["stage_table"] for b in bulks if "type" in b and "stage_table" in b}
    if not type_to_stage:
        raise SystemExit("No bulks with type+stage_table found in config.")
    if all_flag or not types_arg:
        return [(t, type_to_stage[t]) for t in sorted(type_to_stage)]
    out = []
    for t in types_arg:
        if t not in type_to_stage:
            raise SystemExit(f"Bulk type not in config: {t}")
        out.append((t, type_to_stage[t]))
    return out

def main():
    ap = argparse.ArgumentParser(description="Stage Scryfall bulk files into MSSQL from YAML config.")
    ap.add_argument("--config", default="etl/config.yml", help="Path to YAML config")
    ap.add_argument("--cache-dir", default="etl/cache/bulk", help="Directory of downloaded bulk files")
    ap.add_argument("--types", nargs="*", help="Bulk types to stage (e.g. default_cards rulings). Omit with --all.")
    ap.add_argument("--all", action="store_true", help="Stage all types defined in config")
    ap.add_argument("--no-truncate", action="store_true", help="Do not TRUNCATE stage tables")
    ap.add_argument("--chunk", type=int, default=10_000, help="Batch size for inserts")
    # connection overrides
    ap.add_argument("--server")
    ap.add_argument("--database")
    ap.add_argument("--trusted", action="store_true")
    ap.add_argument("--username")
    ap.add_argument("--password")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        raise SystemExit(f"config not found: {cfg_path}")
    cfg = load_cfg(cfg_path)

    cache_dir = Path(args.cache_dir)
    if not cache_dir.exists():
        raise SystemExit(f"cache dir not found: {cache_dir}")

    targets = resolve_types(cfg, args.types, args.all)
    conn_str = build_conn_str(args, cfg.get("sql", {}))

    with pyodbc.connect(conn_str, autocommit=False) as cn:
        for bulk_type, stage_table in targets:
            f = latest_file(cache_dir, bulk_type)
            if not f:
                raise SystemExit(f"{bulk_type} file not found in cache: {cache_dir}")
            stage_one(cn, stage_table, f, truncate=not args.no_truncate, chunk=args.chunk)
            cn.commit()
    print("[done] staging complete")

if __name__ == "__main__":
    main()
