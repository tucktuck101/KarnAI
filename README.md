# KarnAI

An AI-driven Commander (EDH) simulation and training environment built around deterministic rule enforcement and Gymnasium compliance.

## Quick Start

```bash
git clone https://github.com/tucktuck101/karnai.git
cd karnai
python -m venv .venv
.\.venv\Scripts\pip install -e .[dev]
.\.venv\Scripts\pytest -q
```

## Design Philosophy

- Deterministic core (same seed → same game)
- Modular Gymnasium environment
- PettingZoo AEC compatibility
- Schema-first data exchange (Pydantic)
- Rule-driven validation from Comprehensive Rules (CR)

## Project Stages

| Stage | Description |
|-------|--------------|
| 0–1   | Vision, setup, repo scaffolding |
| 2–4   | Contracts, schemas, data loaders |
| 5–8   | Engine kernel → Gymnasium environment |
| 9–11  | CLI, bots, RL core |
| 12–13 | Replay, metrics, dashboards |
| 14+   | Docs, Sphinx, orchestration |

## Licensing

Open source (MIT) pending full CR compliance verification.
