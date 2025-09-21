# Karn.ai: Commander AI Simulation & Ranking Platform

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Proof-of-Concept](https://img.shields.io/badge/status-active-lightgrey)
![CI/CD](https://img.shields.io/github/actions/workflow/status/your-repo/karnai-ci.yml)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

## Overview

**Karn.ai** is a modular, microservice-based AI simulation system designed for _Magic: The Gathering's_ Commander (EDH) format. It simulates 4-player pods, trains reinforcement learning agents, and evaluates decks based on strategic tag impact and win condition alignment.

The platform supports:
- Distributed simulation across internal and community-hosted clients
- Advanced AI training using RLlib (PPO, A2C) with reward shaping and Bayesian convergence
- Archetype-aware decision making and deck performance ranking
- Fully indexed, replayable game logs for education and transparency

> _Train Commander agents. Rank decks. Understand strategy._

---

## Key Features

- 🧠 **Reinforcement Learning Agents**: Tag-aware, archetype-biased decision models using PPO/A2C
- 📊 **Bayesian Convergence Tracking**: Confidently halt training when results stabilize (99.999%)
- 🧩 **Modular Microservice Architecture**: Built for Kubernetes with Redis, Kafka, PostgreSQL, MongoDB, Neo4j
- 🧾 **Card IR System**: Parses card JSON into a game-agnostic intermediate representation
- 🔁 **Replay & Annotation System**: Logs every game action for training, transparency, and review
- 🔄 **Distributed Simulation Support**: Volunteer compute clients run pods at scale
- 💰 **Value Indexing**: Evaluate card efficiency relative to its market price

---

## Tech Stack

| Layer            | Technology                                      |
|------------------|-------------------------------------------------|
| **Languages**    | Python(prototyping), Rust (planned rules engine), TypeScript |
| **Data**         | PosMSSQL, Redis, MongoDB, Neo4j               |
| **Infrastructure** | Docker, Kubernetes (AKS), GitHub Actions       |
| **Observability** | Prometheus, Grafana, Loki, OpenTelemetry        |
| **AI Framework** | RLlib (Ray), NumPy, Pandas                      |
| **Web**          | HTML/CSS/JS (UI Client), Replay Viewer          |
| **APIs**         | RESTful JSON APIs, OpenAPI spec                 |

---

## Architecture

Karn.ai consists of over 20 independently deployable services:

- `simulation-engine`: Core rule-aware game engine
- `agent-service`: RLlib agent training and serving
- `reward-shaping-agent`: Strategic utility & tag-aware feedback
- `matchmaker`: Builds pods, dispatches simulations
- `card-ir-generator` / `registry`: Converts and stores Intermediate Representations
- `deck-service`: Validates and manages decklists
- `replay-logger`, `replay-viewer`: Game log management and visualization
- `value-index-service`: Evaluates gameplay efficiency vs. market value
- `bayesian-evaluator`: Detects convergence, halts redundant training
- `volunteer-coordinator`: Distributes jobs to external simulation clients

See [`/docs`](./docs) for full service descriptions and system diagrams.

---

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-org/karn.ai.git
   cd karn.ai
   ```

2. **Run Setup Script**
   ```bash
   bash setup.sh
   ```
   This will:
   - Prompt for environment config (e.g., DB URIs)
   - Download simulation resources (excluding large assets like NLTK/Scryfall bulk)
   - Save secrets to `.env` and auto-generate commit (excluding large/sensitive files)


---

## Project Goals

- 🧪 _Simulate 5-Deck Proof of Concept_ for foundational training
- 📈 _Achieve accurate performance rankings_ per Commander archetype
- 🌐 _Launch a public-facing dashboard_ similar to EDHREC with replays and metrics
- ♻️ _Comply with WOTC Fan Content Policy_ and support ethical, community-based monetization

---

## Roadmap

- [x] Card IR Parsing & Registry
- [x] Simulation Engine MVP
- [x] RL Agent Training Loop (PPO/A2C)
- [ ] Deck Archetype Classifier
- [ ] Replay Indexer + Viewer
- [ ] Value Index Score Integration
- [ ] Distributed Volunteer Support
- [ ] Web Dashboard.

For full development milestones, see [`docs/roadmap.txt`](./docs/roadmap.txt)

---

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

## Acknowledgements

- Based on Magic: The Gathering by Wizards of the Coast
- DISCLAIMER:

This project is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC.
This project may use the trademarks and other intellectual property of Wizards of the Coast LLC, which is permitted under Wizards’ Fan Content Policy.
For more information about Wizards of the Coast or any of Wizards' trademarks or other intellectual property, please visit https://company.wizards.com.
- Inspired by EDHREC, Moxfield, and the MTG community

---

> _“104.3a A player can concede the game at any time. A player who concedes leaves the game immediately. That player loses the game.”_
