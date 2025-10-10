from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Mapping

# Match: 100. , 100 , 100.1 , 100.1a
_RULE_ANCHOR_RE = re.compile(r"^(?P<anchor>(\d{3})(?:\.\d+)*(?:[a-z])?)(?=[\s\.])")


class CRLoaderFile:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def capabilities(self) -> dict[str, bool]:
        return {"anchors": True}

    def load_text(self) -> str:
        return self.path.read_text(encoding="utf-8", errors="ignore")

    def rules_index(self) -> Mapping[str, int]:
        index: Dict[str, int] = {}
        with self.path.open("rb") as f:
            offset = 0
            for raw_line in f:
                line = raw_line.decode("utf-8", errors="ignore")
                s = line.strip()
                if not s:
                    offset += len(raw_line)
                    continue
                m = _RULE_ANCHOR_RE.match(s)
                if m:
                    anchor = m.group("anchor").rstrip(".")
                    index[anchor] = offset
                offset += len(raw_line)
        return index
