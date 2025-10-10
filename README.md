# Karn.AI

**Open-source Gym-style environment for training AI to play Magic: The Gathering – Commander (EDH).**

Karn.AI provides a reproducible simulation platform for researchers, hobbyists, and developers who want to explore reinforcement learning, decision theory, and AI gameplay in a complex, rules-rich card game.

📄 [Vision](./KarnAI_Vision.md) | 📄 [POC Scope](./KarnAI_POC_Scope.md)

---

## Status: Proof of Concept (POC)

This repository currently delivers the **Milestone 0 POC**, designed to:

- Run locally on limited hardware (no paid cloud infra required).
- Provide a Gym-compatible API (`reset()`, `step()`, `seed()`, `render()`).
- Simulate deterministic test games with seeded randomness.
- Track in/out of scope features explicitly.

Future goals (e.g., distributed simulations, dashboards, cloud scale-out) are deferred to the roadmap.

---

## Why Karn.AI?

- **Reproducibility:** Deterministic simulations with seeded randomness.
- **Research Utility:** Gym API integration for RL agents.
- **MTG Accuracy:** Compliance with the Magic: The Gathering Comprehensive Rules.
- **Community:** Open-source, modular, and contributor-friendly.

---

## Quickstart

### Prerequisites
- Python 3.10+
- pip, uv, or poetry for dependency management
- Works on Linux, macOS, and Windows

### Installation
```bash
git clone https://github.com/YOUR_ORG/karn.ai.git
cd karn.ai
pip install -e .
```

### Run a Smoke Test
```python
from karnai.env import KarnAIEnv

# Create environment
env = KarnAIEnv()

# Reset with seed for determinism
obs = env.reset(seed=42)

# Take a dummy action (replace with legal one from env.action_space)
obs, reward, done, info = env.step(env.action_space.sample())

print("Observation:", obs)
print("Reward:", reward)
print("Done:", done)
```

Run tests:
```bash
pytest
```

---

## Scope: What’s In / Out

### In Scope (POC)
- Gym API (reset/step/seed/render).
- Action & observation spaces for MTG zones, stack, life, commanders, mana, priority, damage tracking.
- Legal-action masking.
- Deterministic bots for reproducible smoke tests.
- Replay logging.

### Out of Scope (POC)
- Paid cloud infrastructure.
- Advanced RL pipelines.
- Multi-node distributed simulation.
- Full card database & keyword abilities (beyond test subset).
- Production dashboards.

(See [POC Scope](./KarnAI_POC_Scope.md) for full details.)

---

## Success Criteria

The POC is successful if it:
- Implements all rules required for test games to complete without illegal states.
- Provides working Gym API integration.
- Passes automated test scripts in CI.
- Allows seeded reproducible runs.

---

## Roadmap (Future)

- Distributed simulation (multi-node, volunteer clients).
- Integration with cloud data pipelines and dashboards.
- Expanded card/keyword coverage.
- Advanced RL benchmarks.

---

## Contributing

We use **GitHub issue templates** to structure work into:
- **Epics** (CR top-level sections or core components).
- **Features** (subsections of rules / functional modules).
- **Tasks** (implementation, docs, tests, observability).

👉 Start small: pick a Task, run tests, and open a PR.

---

## Data & Compliance

- Uses **Scryfall bulk data** (permitted under their API license).
- Complies with **Wizards of the Coast Fan Content Policy**.
- Licensed under **MIT** (see LICENSE).

---

## Acknowledgements

- [OpenAI Gym](https://www.gymlibrary.dev/) for the environment spec.
- [Scryfall](https://scryfall.com) for card data.
- Magic: The Gathering Comprehensive Rules as the rules source.
