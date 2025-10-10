# Stage 13 — Metrics Pipeline & Dashboard

Scope:
- Parse replay `.jsonl` files.
- Compute core KPIs offline with Pandas/DuckDB.
- Emit a compact text dashboard for CI logs.

KPIs:
- `replays`: count
- `total_steps`: sum of step records
- `avg_steps_per_replay`
- `determinism_rate`: for identical `(seed, config_json)` groups, all footers' SHA must match.
- `unique_sha`: number of unique footer hashes

APIs:
- `karnai.metrics.summarize_replays(paths)` → dict
- `karnai.metrics.render_dashboard(summary)` → str

CLI hook idea (future):
- `karnai train ... --emit-metrics out.json`
