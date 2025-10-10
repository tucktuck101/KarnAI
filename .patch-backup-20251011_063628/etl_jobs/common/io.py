from __future__ annotations
import pathlib

def ensure_dirs() -> None:
    for d in [
        "etl/storage/landing",
        "etl/storage/staging",
        "etl/storage/quarantine",
        "etl/storage/logs",
    ]:
        pathlib.Path(d).mkdir(parents=True, exist_ok=True)