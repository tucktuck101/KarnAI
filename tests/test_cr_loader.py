from karnai.data.cr_loader import CRLoaderFile


def test_cr_anchor_index_builds():
    loader = CRLoaderFile("tests/fixtures/cr_sample.txt")
    idx = loader.rules_index()
    assert "100" in idx and "101" in idx
    assert any(k.startswith("100") for k in idx.keys())
