deck-service.txt

Deck Service
============

Purpose:
--------
The `deck-service` handles ingestion, validation, and management of Commander-format decklists. It ensures decks meet legality requirements, references only valid CardIR objects, and are properly indexed for matchmaking and simulation scheduling.

Responsibilities:
-----------------
- Accept deck submissions in plain text, JSON, or list format.
- Validate decks against Commander rules (singleton, 100 cards, valid commander).
- Cross-reference all cards against the Card IR Registry.
- Store validated decks with metadata and indexing for performance.
- Generate deck fingerprints for tracking usage across simulations.

Inputs:
-------
- Plain text or JSON decklists (user or system-submitted)
- IR data from the `card-ir-registry`
- Format metadata and legality flags (from schema or Scryfall)

Outputs:
--------
- Validated, canonicalized deck objects
- Indexed deck records by commander, archetype (optional), and hash
- Errors for illegal cards, formatting issues, or unrecognized entries

Interfaces:
-----------
- REST API:
  - `POST /decks/validate`
  - `GET /decks/{deck_id}`
  - `GET /decks?commander=X`
- Kafka topic (optional): for new deck broadcasts to the matchmaker
- Internal utility for deck fingerprinting and clustering

Communication:
--------------
- Reads IR from `card-ir-registry`
- Sends validated decks to `matchmaker` and metadata to `db-service`
- Flags invalid decks to a moderation queue or admin dashboard (future)

Dependencies:
-------------
- Access to IR registry
- Legal card flags by format
- Scryfall-based card metadata loader or cache

Deployment:
-----------
- Persistent service
- Can run on local Docker or Kubernetes
- Scales horizontally for public submission load

Notes:
------
This service is foundational for pod formation, simulation reproducibility, and long-term analytics. Deck versioning may be introduced in the future to support evolution tracking or user-submitted updates.
