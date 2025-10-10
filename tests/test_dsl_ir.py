from karnai.dsl import compile_ir_to_callable, parse_oracle_text


def test_parse_tap_add_g():
    ir = parse_oracle_text("{T}: Add {G}.")
    assert ir is not None
    assert ir.cost == {"tap_self": True}
    assert ir.ops[0].op == "add_mana"
    assert ir.ops[0].params["color"] == "G"


def test_parse_counterspell():
    ir = parse_oracle_text("Counter target spell.")
    assert ir is not None
    assert ir.cost is None
    assert ir.ops[0].op == "counter_target"
    fn = compile_ir_to_callable(ir)
    out = fn({"stack_top": "spell"})
    assert out["applied"] is True and out["ops"][0]["op"] == "counter_target"
