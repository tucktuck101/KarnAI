from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def read_replays(paths: Iterable[str | Path]) -> List[Dict[str, Any]]:
    """Return list of events with filename tag for downstream aggregation.
    Each item is a dict with keys: type, idx?, action?, obs?, sha256?, seed?, config?
    """
    rows: List[Dict[str, Any]] = []
    for p in paths:
        p = Path(p)
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                obj["_file"] = str(p)
                rows.append(obj)
    return rows
