# Stage 11 — RL Training Core

Purpose: Provide minimal, dependency-light RL adapters and a self-play orchestrator
so experiments run end-to-end without external RL libs.

Components
- `rl.adapters` — `PPOAdapter`, `DQNAdapter` stubs that satisfy the `Policy` contract.
- `rl.selfplay` — multi-episode self-play orchestration against mirrors or opponents.

Notes
- Adapters are lightweight and *do not* require third-party libs.
- They wrap a tiny logistic bandit over two actions: `noop` vs `pass_priority`.
- Deterministic with seeds for reproducibility.
