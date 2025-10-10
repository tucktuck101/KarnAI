from typing import Mapping, Any
from dataclasses import dataclass
from karnai.contracts import Scheduler, RulesEngine, GymEnvFacade, RunStore


@dataclass
class DummySched(Scheduler):
    def capabilities(self) -> dict[str, bool]:
        return {}

    def schedule(self, config):
        yield {"ok": True}


@dataclass
class DummyEngine(RulesEngine):
    def capabilities(self) -> dict[str, bool]:
        return {}

    def reset(self, seed, config):
        return {"ok": True}

    def step(self, action):
        return {"ok": True}

    def snapshot(self):
        return b"ok"


@dataclass
class DummyGym(GymEnvFacade):
    def __init__(self):
        self.called = False

    def reset(self, seed=None, options=None):
        return {"ok": True}, {}

    def step(self, action):
        self.called = True
        return {"ok": True}, 0.0, False, False, {}

    def render(self):
        return "ok"

    def close(self):
        pass


@dataclass
class DummyStore(RunStore):
    def capabilities(self) -> dict[str, bool]:
        return {}

    def new_run(self, config):
        return "run_1"

    def new_episode(self, run_id, match_id):
        return "ep_1"

    def log_step(
        self, episode_id: str, idx: int, record: Mapping[str, Any]
    ) -> None: ...
    def get_episode(self, episode_id: str):
        yield {"idx": 0}

    def put_artifact(self, run_id: str, kind: str, uri: str, sha256: str) -> str:
        return "art_1"

    def end_episode(self, episode_id: str, outcome: str) -> None: ...


def test_contracts_smoke():
    s = DummySched()
    e = DummyEngine()
    g = DummyGym()
    assert list(s.schedule({})) and e.reset(42, {}) and isinstance(e.step({}), dict)
    o, r, d, info = g.step({"type": "pass"})
    g.close()
    assert r == 0.0 and d is False


def test_engine_snapshot_bytes():
    eng = DummyEngine()
    s = eng.reset(42, {})
    out = eng.step({"noop": True})
    snap = eng.snapshot()
    assert s["ok"] and isinstance(out, dict) and isinstance(snap, (bytes, bytearray))
