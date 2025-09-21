architecture.txt

System Architecture
===================

Overview:
---------
The system uses a microservice-based architecture to simulate Magic: The Gathering Commander games using AI agents. It is designed for horizontal scalability, cloud-native deployment, modular development, and robust observability.

Simulation Architecture:
------------------------
- A central simulation engine processes 4-player pods using game rules defined by Intermediate Representations (IR).
- Agents interact with the game via the agent hook, using real-time decision making and reward-informed inference.
- Simulations are dispatched either to internal compute nodes or to trusted volunteer clients.
- Game state, replays, tag traces, and action logs are emitted and stored for post-processing, reward shaping, and visualization.

Core Layers and Services:
-------------------------

1. Simulation & Game Execution
   - `simulation-engine`: Runs the full game loop, stack resolution, priority passing, triggers, and rule enforcement.
   - `agent-hook`: Interfaces between the game engine and the AI decision system.
   - `replay-logger`: Captures all game states and transitions, including flattened strategic tags and context.
   - `matchmaker`: Builds 4-player pods and routes them for execution.
   - `pod-meta-controller`: Tracks pod configurations, active match counts, and convergence.
   - `volunteer-coordinator`: Dispatches simulation jobs to trusted volunteer clients and tracks leaderboard stats.

2. AI, Reward, and Convergence
   - `agent-service`: Hosts reinforcement learning models and strategic logic. Evaluates actions based on flattened tag structures, deck archetype, phase awareness, opponent modeling, and dynamic exploration. Supports shadow agents for validation and decay tracking.
   - `reward-shaping-agent`: Adjusts and refines reward weights after each game using post-hoc outcomes and tag performance. Handles reward decay for stale or misaligned values.
   - `bayesian-evaluator`: Evaluates pod convergence confidence (e.g., 99.999%) to determine when to retire simulations. Feeds convergence data into agent exploration logic.
   - `explanation-service`: Optional tracing for transparency of agent decision paths, action tags, and strategic justification.

3. Card and Deck Services
   - `card-ir-generator`: Converts raw JSON card data into structured IR with hierarchical tag metadata via NLP pipelines.
   - `card-ir-registry`: Stores and indexes IR by card ID, type, strategic tags, and functionality.
   - `deck-service`: Validates Commander decklists against format rules and known card IRs. Supplies deck identity profiles to agents for archetype-aligned behavior.
   - `value-index-service`: Computes the ratio of in-game impact to market price for financial efficiency analysis.
   - `price-ingestor`: Fetches and updates secondary market pricing data for use by the value indexer.

4. Result Handling and Indexing
   - `result-aggregator`: Updates win/loss data, convergence metrics, and meta statistics.
   - `replay-indexer`: Indexes replay logs with tag metadata for searching, filtering, and pattern identification.
   - `db-service`: Writes to and queries relational, document, and graph databases.
   - `test-orchestrator`: Coordinates CI/CD testing across services, including model behavior, reward consistency, and shadow agent comparisons.

5. Public Interface and Visualization
   - `ui-client`: Enables human-vs-AI or mixed pods in a browser-based game client.
   - `replay-viewer`: Visualizes replay logs interactively, with tag overlays and decision confidence heatmaps.
   - `public-webpage`: EDHREC-style dashboard for replay exploration, meta trends, and deck predictions.
   - `api-gateway`: Exposes internal and public APIs across all services.
   - `auth-service`: Handles user identity and authentication for leaderboard, annotations, or submissions.

Data Flow and Coordination:
---------------------------
- Kafka is the primary message bus for simulation job coordination and result streaming.
- Redis provides fast lookup caching for IRs, pod metadata, and deck info.
- PostgreSQL, MongoDB, and Neo4j serve different data roles:
  - Structured logs and deck data (PostgreSQL)
  - IRs and metadata, including tag hierarchies (MongoDB)
  - Replay patterns and card interactions (Neo4j)

Deployment and Scaling:
-----------------------
- Each service is containerized via Docker and orchestrated with Kubernetes.
- Azure AKS and spot instances support high-throughput, parallel simulation workloads.
- Volunteer nodes are securely verified and signed, contributing to public simulations at scale.

The architecture is modular, explainable, and designed for research, gameplay innovation, and scalable Commander AI training at the full Magic ruleset level.
