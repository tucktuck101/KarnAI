# commander_counter_otel.py
import os, sys, csv, re, time, json, argparse, datetime, logging, uuid, math
from itertools import combinations
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from collections import defaultdict, deque


# ---- Minimal console tracing/metrics shim (replaces OpenTelemetry) ----
class _SpanCtx:
    def __init__(self, logger, name, attributes=None):
        self.logger = logger
        self.name = name
        self.attributes = attributes or {}
        self._t0 = None

    def __enter__(self):
        self._t0 = time.perf_counter()
        self.logger.debug("→ %s %s", self.name, self.attributes)
        return self

    def __exit__(self, exc_type, exc, tb):
        dt = time.perf_counter() - self._t0 if self._t0 else 0.0
        self.logger.debug("← %s duration=%.3fs", self.name, dt)

class _Tracer:
    def __init__(self, logger):
        self.logger = logger
    def start_as_current_span(self, name, attributes=None):
        return _SpanCtx(self.logger, name, attributes)

class _Counter:
    def __init__(self, logger, name, unit="", desc=""):
        self.logger = logger; self.name = name; self.unit = unit; self.desc = desc
    def add(self, n: float, attrs=None):
        self.logger.debug("%s += %s %s %s", self.name, n, self.unit, attrs or {})

class _Histogram:
    def __init__(self, logger, name, unit="", desc=""):
        self.logger = logger; self.name = name; self.unit = unit; self.desc = desc
    def record(self, x: float, attrs=None):
        self.logger.debug("%s = %s %s %s", self.name, x, self.unit, attrs or {})

class _Meter:
    def __init__(self, logger):
        self.logger = logger
    def create_counter(self, name, unit="", desc=""):
        return _Counter(self.logger, name, unit, desc)
    def create_histogram(self, name, unit="", desc=""):
        return _Histogram(self.logger, name, unit, desc)

def setup_tracing(run_id: str | None = None):
    import logging
    log = logging.getLogger(__name__)
    tracer = _Tracer(log)
    meter = _Meter(log)
    return tracer, meter
# ---- end shim ----



# -------- OpenTelemetry setup --------

SERVICE_NAME = "commander-counter"
API = "https://api.scryfall.com/cards/search"
UA = {"User-Agent": "CommanderCounter/1.0 (otel)"}

# -------- OTEL --------
def setup_tracing(run_id: str):
    res = Resource.create({
        "service.name": SERVICE_NAME,
        "service.version": "0.3.1",
        "deployment.environment": os.getenv("ENV", "dev"),
        "run.id": run_id,
    })
    # Traces
    tp = TracerProvider(resource=res)
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint + "/v1/traces")))
    else:
        tp.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(tp)
    # Metrics
    readers = []
    if endpoint:
        readers.append(PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint + "/v1/metrics")))
    else:
        readers.append(PeriodicExportingMetricReader(ConsoleMetricExporter()))
    mp = MeterProvider(resource=res, metric_readers=readers)
    metrics.set_meter_provider(mp)
    # Auto-instrument
    return trace.get_tracer(__name__), metrics.get_meter(__name__)

# -------- Logging --------

def setup_logging(level_name: str = "INFO", run_id: str | None = None):
    import sys, logging
    level = getattr(logging, level_name.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    if run_id:
        # Simple adapter that injects run_id into each message prefix
        class _Adapter(logging.LoggerAdapter):
            def process(self, msg, kwargs):
                return f"[run_id={run_id}] {msg}", kwargs
        return _Adapter(logger, {})
    return logger


# -------- Fetch --------
def scry_search(q: str, tracer, REQS, LAT):
    params = urlencode({"q": q, "unique": "oracle", "include_extras": "false", "include_multilingual": "false"})
    url = f"{API}?{params}"
    while url:
        with tracer.start_as_current_span("scryfall.page", attributes={"url": url, "query": q}):
            t0 = time.perf_counter()
            req = Request(url, headers=UA)
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            dur = time.perf_counter() - t0
            REQS.add(1)
            LAT.record(dur)
            for c in data["data"]:
                yield c
            url = data.get("next_page")
            time.sleep(0.05)

# -------- Pairing helpers --------
def by_oracle(cards): 
    return {c["oracle_id"]: c for c in cards}

def index_names(pools):
    name_to_oid = {}
    for pool in pools:
        for oid, c in pool.items():
            name_to_oid[c["name"]] = oid
            for f in c.get("card_faces", []) or []:
                nm = f.get("name")
                if nm:
                    name_to_oid[nm] = oid
    return name_to_oid

def extract_partner_with_pairs(cards_dict, name_to_oid):
    pairs, pat = set(), re.compile(r"Partner with ([^(\n]+)")
    for oid, c in cards_dict.items():
        text = c.get("oracle_text") or ""
        for m in pat.finditer(text):
            partner_name = m.group(1).strip(" .’'“”")
            oid2 = name_to_oid.get(partner_name)
            if oid2 and oid2 != oid:
                pairs.add(frozenset([oid, oid2]))
    return pairs

def extract_friends_forever_pairs(cards_dict):
    oids = list(cards_dict.keys())
    return {frozenset(p) for p in combinations(oids, 2)}

def cartesian_pairs(left_ids, right_ids):
    # exclude degenerate a==b
    return {frozenset({a, b}) for a in left_ids for b in right_ids if a != b}

# -------- Output helpers --------
def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in rows: w.writerow({k: r.get(k, "") for k in fields})

def rows_from_ids(ids, pools):
    order = ["name", "oracle_id", "type_line", "oracle_text"]; out = []
    for oid in ids:
        for pool in pools:
            c = pool.get(oid)
            if c:
                out.append({k: c.get(k, "") for k in order}); break
    return out

def write_pair_csv(path, pairs, pools):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "a_name", "a_oracle_id", "b_name", "b_oracle_id"])
        w.writeheader()
        for p in pairs:
            if len(p) != 2: continue
            a, b = list(p)
            ca = cb = None
            for pool in pools:
                ca = ca or pool.get(a); cb = cb or pool.get(b)
            if not (ca and cb): continue
            w.writerow({"pair": f'{ca["name"]} ⟷ {cb["name"]}', "a_name": ca["name"], "a_oracle_id": a,
                        "b_name": cb["name"], "b_oracle_id": b})

# -------- Combinatorics & Pool --------
COLOR_BITS = {"W": 1, "U": 2, "B": 4, "R": 8, "G": 16}  # colorless = 0
POOL_Q = 'legal:commander game:paper -is:token -is:funny'
STICKER_Q = 'game:paper layout:sticker'

ANY_NUM_PAT = re.compile(r"\bany number of cards named\b", re.I)
UP_TO_PAT   = re.compile(r"\bup to\s+(\d+)\s+cards named\b", re.I)

def ci_mask(colors):
    m = 0
    for c in colors or []:
        m |= COLOR_BITS.get(c, 0)
    return m

def classify_card(c):
    """Return (mask, is_basic, K) where K is max copies (1 default, 99='any number of', bounded=specific)."""
    m = ci_mask(c.get("color_identity") or [])
    tl = (c.get("type_line") or "")
    is_basic = "Basic" in tl and "Land" in tl
    K = 1
    t = (c.get("oracle_text") or "")
    if ANY_NUM_PAT.search(t):
        K = 99
    else:
        m2 = UP_TO_PAT.search(t)
        if m2:
            try: K = int(m2.group(1))
            except Exception: K = 1
    return m, is_basic, K

def fetch_commander_pool(tracer, REQS, LAT):
    """Commander-legal mainboard pool as of now. Excludes stickers and tokens."""
    pool = []
    for c in scry_search(POOL_Q, tracer, REQS, LAT):
        if (c.get("layout") or "").lower() == "sticker":
            continue
        m, is_basic, K = classify_card(c)
        pool.append({
            "oracle_id": c["oracle_id"],
            "name": c["name"],
            "type_line": c.get("type_line", ""),
            "mask": m,
            "is_basic": is_basic,
            "K": K
        })
    return pool

def fetch_sticker_pool_size(tracer, REQS, LAT, fallback=48):
    try:
        ids = set()
        for c in scry_search(STICKER_Q, tracer, REQS, LAT):
            ids.add(c.get("oracle_id"))
        return len(ids) or fallback
    except Exception:
        return fallback

def build_pool_index(pool):
    """
    Index by color-identity mask.
      singles[s]  = count of 1-copy cards (incl. nonbasic lands)
      bounded[s]  = dict K->count for max_copies=K (2..99)
      basics[s]   = set of basic land names
    """
    singles = defaultdict(int)
    bounded = defaultdict(lambda: defaultdict(int))
    basics  = defaultdict(set)
    for x in pool:
        s = x["mask"]
        if x["is_basic"]:
            basics[s].add(x["name"])
            continue
        K = x["K"]
        if K == 1: singles[s] += 1
        else:      bounded[s][K] += 1
    return singles, bounded, basics

def submasks(mask):
    s = mask
    while True:
        yield s
        if s == 0: break
        s = (s - 1) & mask

def count_for_mask(mask, M, singles_idx, bounded_idx, basics_idx, exclude_singletons=0):
    """Exact count of mainboard lists for CI mask and size M. Excludes `exclude_singletons` commanders from pool."""
    n_single = sum(singles_idx.get(s, 0) for s in submasks(mask))
    k_counts = {}
    for s in submasks(mask):
        for K, cnt in bounded_idx.get(s, {}).items():
            k_counts[K] = k_counts.get(K, 0) + cnt
    basic_names = set()
    for s in submasks(mask):
        basic_names |= basics_idx.get(s, set())
    B = len(basic_names)

    n_single = max(0, n_single - exclude_singletons)

    ways = [0] * (M + 1)
    ways[0] = 1

    # (1+x)^{n_single}
    for _ in range(n_single):
        for t in range(M, 0, -1):
            ways[t] += ways[t - 1]

    # multiply by (1 + x + ... + x^K) for each bounded card
    def apply_bounded(ways, K):
        new = [0] * (M + 1)
        s = 0
        dq = deque()
        for t in range(0, M + 1):
            s += ways[t]; dq.append(ways[t])
            if len(dq) > K + 1:
                s -= dq.popleft()
            new[t] = s
        return new

    for K, cnt in sorted(k_counts.items()):
        for _ in range(cnt):
            ways = apply_bounded(ways, min(K, M))

    # fill remaining with basics: compositions into B unlimited types
    total = 0
    for m in range(0, M + 1):
        remaining = M - m
        if B == 0:
            if remaining == 0: total += ways[m]
            continue
        total += ways[m] * math.comb(B + remaining - 1, remaining)
    return total, {"n_single": n_single, "k_counts": k_counts, "B": B}

def sticker_multiplier(pool_size, k_min=10, k_max=None):
    if k_max is None or k_max > pool_size:
        k_max = pool_size
    return sum(math.comb(pool_size, k) for k in range(k_min, k_max + 1))

# -------- Orchestrate deckspace counting --------
def compute_all_counts(all_cmd, gen_partner_pairs, with_pairs, ff_pairs, bg_pairs, doc_pairs, tracer, REQS, LAT, out_dir):
    pool = fetch_commander_pool(tracer, REQS, LAT)
    singles_idx, bounded_idx, basics_idx = build_pool_index(pool)
    sticker_pool = fetch_sticker_pool_size(tracer, REQS, LAT, fallback=48)
    stick_mult = sticker_multiplier(sticker_pool, k_min=10, k_max=None)

    def commander_mask(oid):
        c = all_cmd.get(oid)
        return ci_mask(c.get("color_identity") or []) if c else 0

    results = []

    # Singles
    for oid in all_cmd.keys():
        M = 99
        m = commander_mask(oid)
        base, meta = count_for_mask(m, M, singles_idx, bounded_idx, basics_idx, exclude_singletons=1)
        total = base * stick_mult
        results.append({"kind": "single", "a": oid, "b": "", "M": M, "mask": m, "total": total, "meta": meta})

    # Pairs helper
    def add_pairs(pairs, kind, exclude_count=2):
        for p in pairs:
            a, b = list(p)
            M = 98
            m = commander_mask(a) | commander_mask(b)
            base, meta = count_for_mask(m, M, singles_idx, bounded_idx, basics_idx, exclude_singletons=exclude_count)
            total = base * stick_mult
            results.append({"kind": kind, "a": a, "b": b, "M": M, "mask": m, "total": total, "meta": meta})

    add_pairs(gen_partner_pairs, "generic_partner", exclude_count=2)
    add_pairs(with_pairs, "partner_with", exclude_count=2)
    add_pairs(ff_pairs, "friends_forever", exclude_count=2)
    add_pairs(bg_pairs, "background", exclude_count=2)
    add_pairs(doc_pairs, "doctors_companion", exclude_count=2)

    # Write CSV
    rows = []
    for r in results:
        rows.append({
            "kind": r["kind"],
            "a_oracle_id": r["a"],
            "b_oracle_id": r["b"],
            "mask": r["mask"],
            "mainboard_size": r["M"],
            "n_single_after_exclusion": r["meta"]["n_single"],
            "B_basic_names": r["meta"]["B"],
            "exceptions_json": json.dumps(r["meta"]["k_counts"], separators=(",", ":")),
            "sticker_pool": sticker_pool,
            "sticker_multiplier": stick_mult,
            "deckspace_total": str(r["total"])
        })
    write_csv(os.path.join(out_dir, "7_deckspace_counts.csv"), rows, [
        "kind", "a_oracle_id", "b_oracle_id", "mask", "mainboard_size",
        "n_single_after_exclusion", "B_basic_names", "exceptions_json",
        "sticker_pool", "sticker_multiplier", "deckspace_total"
    ])
    return results

# -------- Main --------
def run(out_dir="out", log_level=logging.INFO):
    run_id = str(uuid.uuid4())
    tracer, meter = setup_tracing(run_id)
    log, _ = setup_logging(level=log_level, run_id=run_id)

    # Metrics
    REQS = meter.create_counter("scryfall_requests_total", "count", "Scryfall requests")
    LAT  = meter.create_histogram("scryfall_request_seconds", "s", "Scryfall request latency")
    CARDS = meter.create_counter("cards_fetched_total", "count", "Cards fetched")
    PAIRS = meter.create_counter("pairs_built_total", "count", "Pairs built")

    # Queries
    ALL_Q = "legal:commander is:commander game:paper -is:funny"
    GEN_PARTNER_Q = ('legal:commander is:commander game:paper keyword:"partner" -o:"partner with" -o:"friends forever" -is:funny')
    WITH_Q = 'legal:commander is:commander game:paper o:"partner with" -is:funny'
    FF_Q = 'legal:commander is:commander game:paper o:"friends forever" -is:funny'
    CHOOSE_BG_Q = 'legal:commander is:commander game:paper o:"choose a Background" -is:funny'
    BG_Q = 'legal:commander type:Background is:legendary game:paper -is:funny'
    DOC_COMP_Q = 'legal:commander is:commander game:paper o:"Doctor’s companion" -is:funny'
    DOCTORS_Q = 'legal:commander is:commander game:paper type:"Legendary Creature" type:Doctor -is:funny'

    with tracer.start_as_current_span("fetch_buckets"):
        all_cmd = by_oracle(scry_search(ALL_Q, tracer, REQS, LAT)); CARDS.add(len(all_cmd))
        gen_partner = by_oracle(scry_search(GEN_PARTNER_Q, tracer, REQS, LAT)); CARDS.add(len(gen_partner))
        partner_with = by_oracle(scry_search(WITH_Q, tracer, REQS, LAT)); CARDS.add(len(partner_with))
        friends_forever = by_oracle(scry_search(FF_Q, tracer, REQS, LAT)); CARDS.add(len(friends_forever))
        choose_bg = by_oracle(scry_search(CHOOSE_BG_Q, tracer, REQS, LAT)); CARDS.add(len(choose_bg))
        backgrounds = by_oracle(scry_search(BG_Q, tracer, REQS, LAT)); CARDS.add(len(backgrounds))
        doctors_companions = by_oracle(scry_search(DOC_COMP_Q, tracer, REQS, LAT)); CARDS.add(len(doctors_companions))
        doctors = by_oracle(scry_search(DOCTORS_Q, tracer, REQS, LAT)); CARDS.add(len(doctors))

    log.info("Counts | all:%d gen_partner:%d with:%d ff:%d choose_bg:%d backgrounds:%d doctors:%d companions:%d",
             len(all_cmd), len(gen_partner), len(partner_with), len(friends_forever),
             len(choose_bg), len(backgrounds), len(doctors), len(doctors_companions))

    singles = set(all_cmd) - set(backgrounds)
    name_to_oid = index_names([all_cmd, backgrounds, choose_bg])

    with tracer.start_as_current_span("build_pairs"):
        gen_partner_pairs = {frozenset(p) for p in combinations(gen_partner.keys(), 2)}; PAIRS.add(len(gen_partner_pairs), {"type": "generic_partner"})
        with_pairs = extract_partner_with_pairs(partner_with, name_to_oid); PAIRS.add(len(with_pairs), {"type": "partner_with"})
        ff_pairs = extract_friends_forever_pairs(friends_forever); PAIRS.add(len(ff_pairs), {"type": "friends_forever"})

        # remove commander/background overlaps before pairing
        bg_overlap = set(choose_bg.keys()) & set(backgrounds.keys())
        left  = set(choose_bg.keys()) - bg_overlap
        right = set(backgrounds.keys()) - bg_overlap
        bg_pairs = cartesian_pairs(left, right); PAIRS.add(len(bg_pairs), {"type": "background"})

        doc_pairs = cartesian_pairs(doctors.keys(), doctors_companions.keys()); PAIRS.add(len(doc_pairs), {"type": "doctors_companion"})

    # Validate pair cardinality
    for label, s in [("bg_pairs", bg_pairs), ("with_pairs", with_pairs),
                     ("ff_pairs", ff_pairs), ("gen_partner_pairs", gen_partner_pairs)]:
        bad = [p for p in s if len(p) != 2]
        if bad:
            log.error("%s invalid entries: %d; example=%s", label, len(bad), next(iter(bad)))
            raise SystemExit(1)

    # Output: CSVs of identities/pairs
    with tracer.start_as_current_span("write_outputs", attributes={"out_dir": out_dir}):
        os.makedirs(out_dir, exist_ok=True)
        pools = [all_cmd, backgrounds, choose_bg, doctors, doctors_companions]
        write_csv(os.path.join(out_dir, "1_singles.csv"), rows_from_ids(singles, [all_cmd]),
                  ["name", "oracle_id", "type_line", "oracle_text"])
        write_pair_csv(os.path.join(out_dir, "2_generic_partner_pairs.csv"), gen_partner_pairs, pools)
        write_pair_csv(os.path.join(out_dir, "3_partner_with_pairs.csv"), with_pairs, pools)
        write_pair_csv(os.path.join(out_dir, "4_friends_forever_pairs.csv"), ff_pairs, pools)
        write_pair_csv(os.path.join(out_dir, "5_background_pairs.csv"), bg_pairs, pools)
        write_pair_csv(os.path.join(out_dir, "6_doctor_companion_pairs.csv"), doc_pairs, pools)

    # Compute deckspace counts and write summary
    compute_all_counts(all_cmd, gen_partner_pairs, with_pairs, ff_pairs, bg_pairs, doc_pairs, tracer, REQS, LAT, out_dir)

    total = len(singles) + len(gen_partner_pairs) + len(with_pairs) + len(ff_pairs) + len(bg_pairs) + len(doc_pairs)
    log.info("Totals | singles:%d partner:%d partner_with:%d friends:%d backgrounds:%d doctors_comp:%d | ALL:%d",
             len(singles), len(gen_partner_pairs), len(with_pairs), len(ff_pairs), len(bg_pairs), len(doc_pairs), total)
    log.info("CSV outputs: %s", os.path.abspath(out_dir))

# -------- CLI --------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Count legal Commander deck spaces with OpenTelemetry.")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = ap.parse_args()
    run(out_dir=args.out_dir, log_level=getattr(logging, args.log_level))
