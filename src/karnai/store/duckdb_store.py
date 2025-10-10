from __future__ import annotations

import duckdb
import os
import json
import time
import hashlib
from pathlib import Path
from typing import Mapping, Any, Iterable

from karnai.contracts import RunStore

_DEFAULT_DIR = Path(".karnai")
_DEFAULT_DB = _DEFAULT_DIR / "karnai.duckdb"

DDL = [
    """CREATE TABLE IF NOT EXISTS run(
        run_id TEXT PRIMARY KEY,
        started_at TIMESTAMP,
        config_json JSON,
        seed BIGINT,
        code_hash TEXT
    );""",
    """CREATE TABLE IF NOT EXISTS episode(
        episode_id TEXT PRIMARY KEY,
        run_id TEXT,
        match_id TEXT,
        started_at TIMESTAMP,
        outcome TEXT
    );""",
    """CREATE TABLE IF NOT EXISTS step(
        episode_id TEXT,
        idx INTEGER,
        ts TIMESTAMP,
        active_player INTEGER,
        reward DOUBLE,
        done BOOLEAN,
        record JSON
    );""",
    """CREATE TABLE IF NOT EXISTS artifact(
        artifact_id TEXT PRIMARY KEY,
        run_id TEXT,
        kind TEXT,
        uri TEXT,
        sha256 TEXT,
        created_at TIMESTAMP
    );""",
]


def _now_ts() -> float:
    return time.time()


def _hash_config(cfg: Mapping[str, Any]) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode("utf-8")).hexdigest()


class DuckDBStore(RunStore):
    def __init__(self, db_path: str | os.PathLike | None = None):
        _DEFAULT_DIR.mkdir(parents=True, exist_ok=True)
        self.path = Path(db_path) if db_path else _DEFAULT_DB
        self.con = duckdb.connect(str(self.path))
        for stmt in DDL:
            self.con.execute(stmt)

    def capabilities(self) -> dict[str, bool]:
        return {"otlp_tracing": False}

    def new_run(self, config: Mapping[str, Any]) -> str:
        run_id = f"run_{int(_now_ts() * 1000)}"
        seed = int(config.get("rng_seed", 0))
        code_hash = _hash_config(config)
        self.con.execute(
            "INSERT INTO run VALUES (?, NOW(), ?, ?, ?)",
            [run_id, json.dumps(config), seed, code_hash],
        )
        return run_id

    def new_episode(self, run_id: str, match_id: str) -> str:
        ep_id = f"ep_{int(_now_ts() * 1000)}"
        self.con.execute(
            "INSERT INTO episode VALUES (?, ?, ?, NOW(), ?)",
            [ep_id, run_id, match_id, "in_progress"],
        )
        return ep_id

    def log_step(self, episode_id: str, idx: int, record: Mapping[str, Any]) -> None:
        active_player = record.get("active_player", -1)
        reward = float(record.get("reward", 0.0))
        done = bool(record.get("done", False))
        self.con.execute(
            "INSERT INTO step VALUES (?, ?, NOW(), ?, ?, ?, ?)",
            [episode_id, idx, active_player, reward, done, json.dumps(record)],
        )

    def end_episode(self, episode_id: str, outcome: str) -> None:
        self.con.execute(
            "UPDATE episode SET outcome=? WHERE episode_id=?",
            [outcome, episode_id],
        )

    def get_episode(self, episode_id: str) -> Iterable[Mapping[str, Any]]:
        cur = self.con.execute(
            "SELECT idx, record FROM step WHERE episode_id = ? ORDER BY idx",
            [episode_id],
        )
        for idx, rec_json in cur.fetchall():
            yield {"idx": idx, **json.loads(rec_json)}

    def put_artifact(self, run_id: str, kind: str, uri: str, sha256: str) -> str:
        art_id = f"art_{int(_now_ts() * 1000)}"
        self.con.execute(
            "INSERT INTO artifact VALUES (?, ?, ?, ?, ?, NOW())",
            [art_id, run_id, kind, uri, sha256],
        )
        return art_id
