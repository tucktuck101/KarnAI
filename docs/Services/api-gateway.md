api-gateway.txt

API Gateway
===========

Purpose:
--------
The `api-gateway` acts as the unified entry point for all HTTP requests to backend services, including simulation management, result queries, deck predictions, authentication, and replay access. It provides routing, rate limiting, and access control.

Responsibilities:
-----------------
- Route external and internal API calls to the correct service.
- Provide versioned, RESTful endpoints for user-facing features.
- Enforce authentication and authorization policies.
- Apply rate limits and request throttling.
- Provide health checks and monitoring for all services.

Key Features:
-------------
- Centralized endpoint for all frontend and tool access.
- Configurable route proxying to microservices (e.g., deck, replay, agent, prediction).
- Extensible routing map for new public services.
- Integrated logging and request tracing for observability.

Exposed Endpoints (Initial):
----------------------------
- `/predict` → Predict win rates from a submitted decklist
- `/decks/{id}` → Fetch metadata about a registered deck
- `/replays/{id}` → Stream or download a specific replay
- `/leaderboard` → Display volunteer simulation contributors
- `/auth` → Identity and session management
- `/submit` → Submit a decklist for evaluation
- `/health` → Health check and uptime status

Inputs:
-------
- HTTP requests from `ui-client`, `public-webpage`, developer tools
- Auth tokens (via `auth-service`)
- Service availability information

Outputs:
--------
- Response JSON from target services
- Load balancing and retry behavior
- Tracing headers for OpenTelemetry stack

Integration Points:
-------------------
- Forwards requests to:
   - `deck-service`
   - `result-aggregator`
   - `replay-indexer`
   - `replay-viewer`
   - `auth-service`
- Observability integrated with `Prometheus`, `Grafana`, and `OpenTelemetry`

Deployment:
-----------
- Reverse proxy (e.g., FastAPI, NGINX, or Kong)
- Optional middleware for JWT token parsing, logging, and retries
- Runs in front of all external services and frontend clients

The `api-gateway` provides a secure, traceable, and consistent interface for all service interactions, enabling robust integration across public and internal use cases.
