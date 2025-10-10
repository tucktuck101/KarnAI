import json

from karnai.engine import RulesEngineImpl


def test_reset_step_snapshot_deterministic():
    eng = RulesEngineImpl()
    obs0 = eng.reset(seed=123, config={})
    assert obs0["turn"] == 1 and obs0["active_player"] == 0

    # Pass priority around table once to advance turn
    for _ in range(4):
        eng.step({"type": "pass_priority"})
    obs1 = eng.step({"type": "pass_priority"})
    assert obs1["turn"] >= 2

    snap1 = eng.snapshot()
    eng2 = RulesEngineImpl()
    eng2.reset(seed=123, config={})
    for _ in range(5):
        eng2.step({"type": "pass_priority"})
    snap2 = eng2.snapshot()

    j1 = json.loads(snap1)
    j2 = json.loads(snap2)
    assert j1["sha256"] == j2["sha256"]
