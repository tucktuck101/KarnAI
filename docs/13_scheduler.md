# Stage 7b — Tournament Scheduler

Initial capabilities:
- Deterministic shuffling by seed.
- Round-robin pod assignment for Commander (default pod size = 4).
- Emits matches as dictionaries via `Scheduler.schedule(config)` per contract.

Config keys:
- `players`: list of player identifiers (e.g., deck names or IDs)
- `rounds`: number of rounds to schedule
- `pod_size`: default 4
- `seed`: optional int for deterministic assignment
