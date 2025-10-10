from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, Dict, Iterable


def summarize_replays(paths: Iterable[str]) -> Dict[str, Any]:
    from .ingest import read_replays

    events = read_replays(paths)
    if not events:
        return {
            "replays": 0,
            "total_steps": 0,
            "avg_steps_per_replay": 0.0,
            "determinism_rate": 1.0,
            "unique_sha": 0,
        }

    # Group events by file
    files = sorted({e["_file"] for e in events})
    steps_per_file = {f: 0 for f in files}
    footer_sha = {}
    seeds = {}
    cfgs = {}
    for e in events:
        f = e["_file"]
        if e.get("type") == "step":
            steps_per_file[f] += 1
        elif e.get("type") == "footer":
            footer_sha[f] = e.get("sha256")
        elif e.get("type") == "header":
            seeds[f] = int(e.get("seed", 0))
            cfgs[f] = json.dumps(e.get("config", {}), sort_keys=True)

    total_steps = sum(steps_per_file.values())
    replays = len(files)
    avg_steps = float(total_steps) / replays if replays else 0.0

    # Determinism: within groups with same (seed,cfg), all SHA equal
    groups = defaultdict(list)
    for f in files:
        key = (seeds.get(f, 0), cfgs.get(f, "{}"))
        groups[key].append(footer_sha.get(f))
    det_ok = 0
    det_total = 0
    for key, shas in groups.items():
        # consider only groups with >=2 replays
        if len(shas) >= 2:
            det_total += 1
            # all non-None and all equal
            if shas[0] is not None and all(s == shas[0] for s in shas[1:]):
                det_ok += 1
    determinism_rate = 1.0 if det_total == 0 else det_ok / det_total

    unique_sha = len(set([s for s in footer_sha.values() if s is not None]))

    return {
        "replays": replays,
        "total_steps": total_steps,
        "avg_steps_per_replay": round(avg_steps, 3),
        "determinism_rate": round(determinism_rate, 3),
        "unique_sha": unique_sha,
    }
