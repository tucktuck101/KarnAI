# Stage 8b — Evaluation Harness and Benchmarks

Purpose: Run reproducible head-to-head evaluations and produce ratings.

Components:
- `elo.py`: simple Elo update utilities.
- `harness.py`: deterministic evaluation loop over the environment using Policy contracts.

Notes:
- This stage ships a minimal random policy in tests for smoke and determinism.
- Real bots arrive in Stage 10.
