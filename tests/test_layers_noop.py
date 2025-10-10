from karnai.engine.layers import apply_layers


def test_layers_noop():
    s = {"x": 1}
    out = apply_layers(s)
    assert out == s
