# KarnAI ETL

This folder adds an ETL pipeline without changing your existing repo layout.
Place this `etl/` folder at the repository root.

## Key ideas
- JSON Schemas gate raw inputs before staging.
- Idempotent MERGE scripts load into your existing dbo tables.
- Every run is tracked in `etl_run`, with per-table stats and change logs.
- Working directories live under `etl/storage/` and should be gitignored by default.

## Make targets
```
make -C etl db-seed     # seed core dimension tables
make -C etl scryfall    # fetch + validate + stage + load core Scryfall entities
make -C etl edhrec      # ingest EDHREC commander snapshot stubs
```
