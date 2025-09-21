db-service.txt

Database Service
================

Purpose:
--------
The `db-service` provides a unified abstraction layer over the three types of databases used in the system: relational (SQL), document (NoSQL), and graph. It handles all reads and writes of simulation data, card IRs, replays, annotations, and convergence metadata.

Responsibilities:
-----------------
- Handle SQL interactions for game results, deck metadata, and logs.
- Store and retrieve Card IRs and reward logs in a document store.
- Query and update card interaction graphs and play patterns in a graph database.
- Serve data to all dependent services through a consistent interface.

Key Features:
-------------
- Integrates PostgreSQL, MongoDB, and Neo4j into a unified access API.
- Supports sharding, caching, and connection pooling.
- Includes schema validation and automatic indexing for large datasets.
- Optional analytics queries exposed to downstream services.

Datastore Roles:
----------------
- **PostgreSQL**: Game logs, placements, deck registration, user accounts.
- **MongoDB**: Card IRs, replay logs, reward shaping, annotations.
- **Neo4j**: Game interaction graphs, combo patterns, deckline graphs.

Inputs:
-------
- Card data from `card-ir-generator`
- Simulation outcomes from `result-aggregator`
- Replay logs and annotations from `replay-logger` and `annotation-service`
- Reward and convergence data from `reward-shaping-agent` and `bayesian-evaluator`

Outputs:
--------
- Structured data to `public-webpage` and `api-gateway`
- IR lookups for `simulation-engine`, `agent-service`, and `replay-viewer`
- Pre-processed data for visualization, pattern recognition, and convergence tracking

Integration Points:
-------------------
- Writes data from nearly all services
- Queried by:
   - `deck-service`
   - `value-index-service`
   - `reward-shaping-agent`
   - `replay-viewer`
   - `public-webpage`

Deployment:
-----------
- Hosted database cluster (self-managed or via cloud providers)
- Access managed via connection pool and role-based auth
- Read replicas and caching available for high-throughput queries

This service decouples storage concerns from simulation and AI logic, allowing the system to scale, persist, and analyze data efficiently across multiple formats and workloads.
