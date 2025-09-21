deployment.txt

Deployment and Infrastructure
=============================

Overview:
---------
This document outlines the deployment architecture and DevOps strategy for the MTG AI simulation system. It is designed to be run in both local development and scalable production environments, including support for distributed volunteer computing.

Containerization:
-----------------
- All microservices are containerized using Docker.
- Images are built via GitHub Actions CI/CD pipelines and stored in a secure container registry.
- Environment configuration is handled through .env files and Helm charts for K8s deployments.

Kubernetes Orchestration:
-------------------------
- Production workloads are orchestrated using Azure Kubernetes Service (AKS).
- Autoscaling is configured for services that handle simulation, AI inference, and replays.
- Internal load balancing routes traffic between simulation pods, databases, and logging services.
- Node pools are segmented by workload type (CPU-bound, GPU-accelerated, storage-heavy).

Persistent Storage:
-------------------
- **PostgreSQL** (Azure Database for PostgreSQL): Stores game logs, placements, deck metadata.
- **MongoDB Atlas**: Stores Card IRs, metadata, price cache, value indexing data.
- **Neo4j Aura**: Handles graph-based analysis and play pattern indexing.

Message Bus and Streaming:
--------------------------
- Apache Kafka handles all asynchronous communication:
  - Simulation job queues
  - Agent request/response pairs
  - Replay log streaming
  - Result aggregation
- Kafka topics are namespaced by service group and retention is tuned for log compliance.

Observability Stack:
--------------------
- **Prometheus**: Metrics collection across all services.
- **Grafana**: Custom dashboards for performance, latency, and game throughput.
- **Loki**: Log aggregation with structured filters for simulation sessions.
- **OpenTelemetry**: Distributed tracing between services, with correlation IDs.

Environment Types:
------------------
- **Local (Dev)**:
  - Docker Compose or Minikube
  - In-memory or SQLite data stores
  - Simulation runs in small batches for development/testing

- **Staging (CI)**:
  - Hosted cloud runner with test decks and agent mocks
  - Used for CI integration, unit testing, and system validation

- **Production (Cloud + Distributed)**:
  - Azure-hosted backend services
  - Supports volunteer clients running remote simulations
  - Optional GPU node pool for agent models
  - Monitoring and convergence controllers run continuously

Distributed Volunteer Simulation:
---------------------------------
- `volunteer-coordinator` issues jobs to external clients (via signed requests)
- Jobs run the simulation-engine locally using a secure build
- Results are uploaded and verified (signed with job ID + seed)
- Contributor statistics are tracked and published to a public leaderboard

Frontend and Public Access:
---------------------------
- `ui-client` and `public-webpage` are hosted via CDN/static hosting
- API access is routed through `api-gateway` with rate limiting
- Replays can be visualized using `replay-viewer` directly in-browser
- Deck submission and predictions are publicly accessible

Security and Scaling:
---------------------
- Secrets are managed via Kubernetes secrets and optionally Azure Key Vault
- Ingress is managed with HTTPS termination, firewall rules, and optional OAuth
- Worker nodes scale based on job queue length (simulations pending)

Backup and Recovery:
--------------------
- All databases have daily backups and failover instances
- Kafka supports log compaction and persistent offset tracking
- Replay logs are deduplicated and compressed for long-term storage

This deployment model balances high throughput, modularity, and public interaction with sustainable cost scaling and low operational risk.
