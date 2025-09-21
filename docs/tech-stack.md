tech-stack.txt

Technology Stack
================

Overview:
---------
The system is designed with modularity, observability, and high-performance simulation in mind. Technologies were selected based on suitability for distributed AI training, simulation orchestration, large-scale data handling, and web interoperability.

Languages:
----------
- **Python**: Primary language for AI services, IR pipeline, REST APIs, and orchestration logic.
- **Rust**: (Planned) High-performance implementation of the rules engine for production.
- **JavaScript (HTML/CSS)**: Frontend browser-based client (`ui-client`, `replay-viewer`).
- **SQL**: For structured data, replay logs, and metadata.
- **JSON/JSONL**: For IR objects, replays, logs, and inter-service payloads.

AI and Reinforcement Learning:
------------------------------
- **PyTorch**: Training models and real-time inference.
- **Ray/RLlib**: Distributed agent execution and hyperparameter tuning.
- **NumPy/Pandas**: Data processing, reward aggregation, and simulation metadata analysis.
- **Bayesian Modeling (Scipy/Scikit/Custom)**: Pod convergence evaluation logic.

Simulation Infrastructure:
--------------------------
- **Docker**: Containerization of every service.
- **Kubernetes (AKS)**: Orchestration of microservices and AI workloads.
- **Kafka**: Event bus for simulation job routing, replay event streaming, and logging.
- **Redis**: Low-latency cache for IR lookups, active pods, and replay access.
- **Helm**: Infrastructure as code for deployment and environment consistency.

Databases:
----------
- **PostgreSQL**: Replay logs, results, deck metadata, simulation metrics.
- **MongoDB**: Card IR objects, configuration state, cached price data.
- **Neo4j**: Card interaction graphs, replay decision paths, play pattern indexing.

External APIs and Tools:
------------------------
- **Scryfall API**: Card metadata ingestion.
- **TCGPlayer / CardMarket APIs**: For market price data via `price-ingestor`.
- **OAuth Providers**: For optional identity integration via `auth-service`.

Frontend:
---------
- **HTML5 + JS/Canvas/SVG**: Interactive replay visualization.
- **Vue.js or React (optional)**: For `public-webpage` dashboard components.
- **WebSockets/HTTP Streaming**: Real-time game interaction from `ui-client`.

CI/CD and DevOps:
-----------------
- **GitHub Actions**: Build, test, and deploy workflows.
- **Prometheus + Grafana**: Metrics collection and visualization.
- **Loki**: Log aggregation.
- **OpenTelemetry**: Tracing simulation requests across services.

Other Enhancements:
-------------------
- **Replay-Viewer**: Web-based visual log inspector for human consumption.
- **Value-Index-Service**: Compares in-game value with secondary market price.
- **Volunteer-Coordinator**: Distributed node registry and workload dispatcher.
- **Replay-Indexer**: Enables searching replays across decks, cards, actions.
- **Test-Orchestrator**: Maintains quality through automated multi-service testing.

This stack supports simulation-scale training, distributed reinforcement learning, real-time replay introspection, and public-facing analytics for the Magic: The Gathering Commander format and beyond.
