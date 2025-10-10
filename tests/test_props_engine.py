import json
from hypothesis import given, strategies as st
from karnai.engine import RulesEngineImpl

actions = st.lists(
    st.sampled_from([{"type": "pass_priority"}, {"type": "noop"}]),
    min_size=0,
    max_size=50,
)
seeds = st.integers(min_value=0, max_value=10_000)


@given(seed=seeds, seq=actions)
def test_deterministic_snapshots(seed, seq):
    eng1 = RulesEngineImpl()
    eng1.reset(seed=seed, config={})
    for a in seq:
        eng1.step(a)
    s1 = json.loads(eng1.snapshot())["sha256"]

    eng2 = RulesEngineImpl()
    eng2.reset(seed=seed, config={})
    for a in seq:
        eng2.step(a)
    s2 = json.loads(eng2.snapshot())["sha256"]

    assert s1 == s2


@given(seq=st.lists(st.just({"type": "pass_priority"}), min_size=1, max_size=32))
def test_priority_rotation(seq):
    eng = RulesEngineImpl()
    o0 = eng.reset(seed=0, config={})
    prev_events = o0["events"]
    for i, a in enumerate(seq, start=1):
        o = eng.step(a)
        assert o["events"] >= prev_events
        prev_events = o["events"]
        assert 0 <= o["active_player"] <= 3
        assert 0 <= o["priority_player"] <= 3
