card-ir-registry.txt

Card IR Registry Service
========================

Purpose:
--------
The `card-ir-registry` service stores, indexes, and serves Intermediate Representations (IR) of cards for the simulation engine and agent training systems. It acts as the canonical source of truth for how each card functions in a structured, machine-readable format.

Responsibilities:
-----------------
- Accept CardIR entries via API or Kafka topic.
- Validate CardIR against schema definitions.
- Assign unique IR identifiers and index by oracle ID, card name, and type.
- Support versioning of IR entries as card definitions evolve.
- Provide fast, queryable access to IR records for:
  - Simulation engine
  - Agent decision systems
  - Replay validator
  - Pattern recognition tools

Inputs:
-------
- Kafka: `card.ir.generated` topic
- REST: `POST /ir` endpoint (optional)
- Local batch loader for migration or bootstrap

Outputs:
--------
- Indexed, queryable CardIR documents in MongoDB
- Version tags and schema compatibility metadata
- API responses for IR lookup

Interfaces:
-----------
- REST API:
  - `GET /ir/{oracle_id}`
  - `GET /ir/search?name=X`
  - `POST /ir` (admin only)
- Kafka consumer for async IR ingestion
- Internal gRPC or REST endpoint for simulation engine access

Communication:
--------------
- Receives data from `card-ir-generator`
- Serves requests from `simulation-engine`, `deck-service`, `replay-logger`, `rsa`

Dependencies:
-------------
- MongoDB instance
- IR schema definition files
- Card metadata indexing service (optional)

Deployment:
-----------
- Runs persistently in all environments
- Caches recent IR lookups in Redis (optional)
- Automatically garbage collects unused/deprecated IR versions (if flagged)

Notes:
------
This service is central to ensuring deterministic, explainable, and versioned gameplay across millions of simulations. Changes to CardIR should trigger downstream revalidation of decks and may require replay regeneration if critical behavior shifts.
