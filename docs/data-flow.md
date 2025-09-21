data-flow.txt

System Data Flow
================

Overview:
---------
This document describes the primary flow of data between microservices within the AI simulation system, emphasizing strategic tagging, agent decision-making, reward shaping, Bayesian convergence integration, and overall data lifecycle.

Core Data Flow Sequence:
------------------------

1. Card Data Ingestion:
   - Raw card JSON (Scryfall API) → `card-ir-generator`.
   - Generated CardIR with hierarchical strategic tags emitted to Kafka and stored in `card-ir-registry`.

2. Deck and Pod Initialization:
   - User-submitted decklists validated by `deck-service` using CardIR data.
   - `matchmaker` composes pods of 4 decks and dispatches pods to `simulation-engine` via Kafka.

3. Simulation Execution:
   - `simulation-engine` initiates game instance, handling rules enforcement and game logic.
   - Game states and actions continuously emitted to `agent-hook`.

4. Agent Decision-Making:
   - `agent-hook` passes state and legal actions to `agent-service`.
   - `agent-service` encodes state, flattens tags from CardIR, queries reinforcement learning models.
   - Action decisions returned to `simulation-engine` and logged by `replay-logger`.

5. Replay and Log Generation:
   - All actions, states, flattened tags, and metadata captured by `replay-logger`.
   - Replay logs stored in JSONL format and indexed by `replay-indexer`.

6. Result Aggregation:
   - Post-game results (placements, scores, convergence metrics) processed by `result-aggregator`.
   - Results published to Kafka, consumed by `bayesian-evaluator`.

7. Bayesian Convergence Evaluation:
   - `bayesian-evaluator` uses placement results to compute convergence confidence.
   - Convergence feedback sent to `pod-meta-controller`, `matchmaker`, `reward-shaping-agent`, and `agent-service`.

8. Reward Shaping and Adjustment:
   - `reward-shaping-agent` receives replay logs, placement data, and Bayesian feedback.
   - Rewards adjusted based on strategic tags, delayed outcomes, and convergence confidence.
   - Reward updates emitted back to training pipelines and stored in reward log schema.

9. Training and Policy Updates:
   - Updated rewards and replay data consumed by RL training pipelines (`agent-service` models).
   - Policy improvements reflected in subsequent simulation epochs.

10. Explanation and Annotation (optional):
    - `explanation-service` captures agent decision metadata, strategic tags, and reasoning.
    - Human reviewers annotate replays through `annotation-service` for audit or training validation.

Data Persistence and Storage:
-----------------------------
- Relational Data (PostgreSQL): Structured logs, placements, decklists.
- Document Store (MongoDB): Card IR data, hierarchical tags, deck archetypes.
- Graph Database (Neo4j): Interaction patterns, replay metadata for strategic analysis.
- Redis Cache: Quick retrieval of frequently accessed IR metadata, pod status, and configuration settings.

Message Coordination:
---------------------
- Kafka serves as the central message bus for asynchronous inter-service communication:
  - Topics: card.ir.generated, simulation.results, pod.dispatch, convergence.status, rewards.updated.

Deployment and Scalability:
---------------------------
- Data flows designed to be containerized and orchestrated via Kubernetes.
- Elastic scaling through Azure Kubernetes Service (AKS), supporting parallel processing and real-time streaming data ingestion.

Integration Highlights:
-----------------------
- Flattened strategic tags streamline agent action evaluation and reward shaping.
- Bayesian convergence integration ensures training efficiency and adaptive exploration.
- Continuous feedback loops between convergence evaluation, reward shaping, and agent policy updates ensure robust learning.

Conclusion:
-----------
This comprehensive data flow structure underpins the robust and efficient operation of the entire AI simulation ecosystem. By explicitly connecting strategic tags, agent learning, Bayesian convergence, and reward shaping, it maintains consistent data integrity, high performance, and deep strategic adaptability.
