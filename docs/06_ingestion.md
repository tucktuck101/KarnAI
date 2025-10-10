
# Stage 3 — Data Ingestion (CR + Scryfall)

## Goals
- Load Comprehensive Rules (CR) text and expose an anchor index for lookups.
- Load Scryfall Oracle bulk data from a local JSON file and normalize to `karnai.schemas.Card`.
- Optional caching to Parquet for fast reloads.

## Artifacts
- `karnai/data/cr_loader.py`
- `karnai/data/scryfall_loader.py`
- Tests under `tests/` with small fixtures so CI stays offline.

## Usage
```python
from karnai.data.cr_loader import CRLoaderFile
idx = CRLoaderFile("tests/fixtures/cr_sample.txt").rules_index()

from karnai.data.scryfall_loader import OracleLoaderFile
loader = OracleLoaderFile("tests/fixtures/oracle_sample.json", cache_dir=".cache")
cards = list(loader.load_cards())  # yields normalized dicts matching schemas.Card
```
