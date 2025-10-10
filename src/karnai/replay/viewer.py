from __future__ import annotations
from pathlib import Path
import json


def render_text(path: str | Path, limit: int | None = None) -> str:
    p = Path(path)
    out = []
    count = 0
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            if limit is not None and count >= limit:
                break
            s = line.strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except json.JSONDecodeError:
                out.append(s)
                count += 1
                continue
            t = obj.get("type")
            if t == "header":
                out.append("[HEADER] " + s)
            elif t == "step":
                out.append("[STEP] " + s)
            elif t == "footer":
                out.append("[FOOTER] " + s)
            else:
                out.append(s)
            count += 1
    return "\n".join(out)
