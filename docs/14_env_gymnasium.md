# Stage 8 — Gymnasium & PettingZoo Environment

Purpose:
Provide a minimal but working Gymnasium-compatible and PettingZoo AEC-compatible environment wrapper around the RulesEngineImpl.

Implements:
- `KarnAIAECEnv`: multi-agent PettingZoo AEC API
- `KarnAIGymEnv`: single-agent Gymnasium API facade

Features:
- Deterministic stepping via RulesEngineImpl
- Minimal observation dicts (turn, active_player, priority_player)
- Random or scripted actions for baseline testing
