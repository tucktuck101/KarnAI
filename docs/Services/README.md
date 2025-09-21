README.txt

Services Overview
=================

This directory contains documentation for all microservices that power the MTG Commander AI simulation system. Services are grouped by function across simulation, AI, indexing, frontend, and coordination layers.

Simulation and Game Control
---------------------------
- simulation-engine.txt — Core MTG engine that simulates Commander games with IR-based rules.
- agent-hook.txt — Interface between AI agent decisions and the simulation loop.
- agent-service.txt — Hosts the reinforcement learning agents for action selection.
- matchmaker.txt — Builds pods of 4 decks and dispatches simulation jobs.
- pod-meta-controller.txt — Tracks pod convergence status and manages scheduling metadata.
- test-orchestrator.txt — Runs automated tests and service validation routines.

Card and Deck Services
----------------------
- card-ir-generator.txt — Parses card JSON into Intermediate Representation (IR) format.
- card-ir-registry.txt — Stores, versions, and indexes all generated Card IRs.
- deck-service.txt — Validates decklists, enforces format rules, and stores canonical decks.
- price-ingestor.txt — Gathers market prices for cards from external APIs.
- value-index-service.txt — Calculates efficiency scores of cards based on performance and price.

AI Post-Processing and Evaluation
---------------------------------
- reward-shaping-agent.txt — Assigns and adjusts rewards based on game logs.
- bayesian-evaluator.txt — Analyzes win distribution to determine when pods have converged.
- explanation-service.txt — Traces and explains agent decisions.
- annotation-service.txt — Allows users to add replay feedback for training and diagnostics.

Replay and Result Handling
--------------------------
- replay-logger.txt — Captures game actions, transitions, and results for each match.
- result-aggregator.txt — Consolidates simulation outcomes into statistical formats.
- replay-indexer.txt — Indexes replays for searching by deck, card, or action.

Distributed Simulation and Volunteering
---------------------------------------
- volunteer-coordinator.txt — Manages compute contributions from community-run clients.
- auth-service.txt — Handles user identity and leaderboard tracking for volunteers.

Public Platform Services
------------------------
- ui-client.txt — Browser-based game client for mixed human/AI pod play.
- replay-viewer.txt — Renders replays interactively in the browser.
- public-webpage.txt — Provides the EDHREC-style dashboard, deck lookup, and stats.
- api-gateway.txt — Routes and secures all internal and public API requests.

Database Layer
--------------
- db-service.txt — Interface to SQL, NoSQL, and graph databases (PostgreSQL, MongoDB, Neo4j).

This README is maintained to reflect the growing modular architecture and allows contributors to quickly locate documentation for each part of the system.
