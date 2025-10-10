# Functional Requirements (FR)

| ID | Requirement | Description | Priority |
|----|--------------|--------------|-----------|
| FR1 | Game Simulation | The system shall simulate complete 4-player Commander matches using legal decks. | High |
| FR2 | Rules Compliance | The simulation shall enforce MTG Comprehensive Rules without ambiguity. | High |
| FR3 | Data Ingestion | The system shall parse and normalize Scryfall Oracle data and Commander decklists. | High |
| FR4 | Deck Power Evaluation | The system shall calculate power indices from simulated outcomes. | High |
| FR5 | Reinforcement-Learning API | The system shall expose a Gymnasium-compatible interface (reset/step/observation/action). | High |
| FR6 | Logging & Replay | The system shall record deterministic replays for every match. | High |
| FR7 | Distributed Simulation | The system shall support batch execution across multiple workers. | Medium |
| FR8 | Explainability Layer | The system shall generate interpretable reasoning logs for agent actions. | Medium |
| FR9 | User CLI | The system shall provide a CLI for launching, replaying, and training. | Medium |
| FR10 | Plugin Framework | The system shall allow external extensions for cards, heuristics, and rewards. | Low |
