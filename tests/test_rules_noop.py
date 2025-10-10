from karnai.rules.dsl import build_effect


def test_rules_registry_noop():
    eff = build_effect({"op": "noop", "args": {"k": 1}})
    assert eff.op == "noop"
