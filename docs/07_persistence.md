# Stage 3b — Persistence & Results DB

Goal: store runs, episodes, steps, and artifacts with fast local reads.

Backend: **DuckDB** file (default: `.karnai/karnai.duckdb`) + URIs for large artifacts (e.g., replays, parquet).

## Tables
- `run(run_id TEXT PRIMARY KEY, started_at TIMESTAMP, config_json JSON, seed BIGINT, code_hash TEXT)`
- `episode(episode_id TEXT PRIMARY KEY, run_id TEXT, match_id TEXT, started_at TIMESTAMP, outcome TEXT)`
- `step(episode_id TEXT, idx INTEGER, ts TIMESTAMP, active_player INTEGER, reward DOUBLE, done BOOLEAN, record JSON)`
- `artifact(artifact_id TEXT PRIMARY KEY, run_id TEXT, kind TEXT, uri TEXT, sha256 TEXT, created_at TIMESTAMP)`

## Notes
- URIs may be `file://...` or `s3://...` in the future.
- All writes are idempotent on primary keys.
