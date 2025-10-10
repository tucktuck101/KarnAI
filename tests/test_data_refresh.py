from pathlib import Path
from karnai.data import refresh


def test_refresh_writes_files(tmp_path, monkeypatch):
    monkeypatch.setenv("KARNAI_DATA_DIR", str(tmp_path / "processed"))
    out = refresh()
    assert Path(out["cards"]).exists()
    assert Path(out["provenance"]).exists()
