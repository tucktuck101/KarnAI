from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any, Iterator
from pathlib import Path
import json
import time

from karnai.engine import RulesEngineImpl


@dataclass
class ReplayLogger:
    path: Path

    @classmethod
    def create(
        cls,
        path: str | Path,
        seed: int,
        config: Mapping[str, Any],
    ) -> "ReplayLogger":
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            header = {
                "type": "header",
                "seed": int(seed),
                "config": dict(config),
                "created_at": time.time(),
            }
            f.write(json.dumps(header) + "\n")
        return cls(p)

    def append_step(
        self,
        idx: int,
        action: Mapping[str, Any],
        obs: Mapping[str, Any],
    ) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            rec = {
                "type": "step",
                "idx": int(idx),
                "action": dict(action),
                "obs": dict(obs),
            }
            f.write(json.dumps(rec, separators=(",", ":")) + "\n")

    def close_with_footer(self, engine: RulesEngineImpl) -> str:
        snap = engine.snapshot()
        j = json.loads(snap)
        sha = j["sha256"]
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"type": "footer", "sha256": sha}) + "\n")
        return sha


def iter_replay(path: str | Path) -> Iterator[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
