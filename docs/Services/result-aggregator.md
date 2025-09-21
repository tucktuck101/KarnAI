result-aggregator.txt

Result Aggregator
=================

Purpose:
--------
The `result-aggregator` collects final simulation outcomes from the `simulation-engine` and compiles match results, deck performance statistics, convergence metrics, and meta analytics. It forms the backbone of quantitative performance evaluation in the system.

Responsibilities:
-----------------
- Store placement data (1st–4th) and game statistics for each pod.
- Track per-deck and per-archetype win rates, match counts, and performance deltas.
- Aggregate replay hashes and simulation counts.
- Notify convergence evaluators (e.g. `bayesian-evaluator`) with summary data.
- Provide data for financial analysis (`value-index-service`) and public metrics.

Key Features:
-------------
- Handles high throughput of end-of-game messages.
- Aggregates by deck, pod, commander, archetype, color identity, and strategy tag.
- Normalizes results to support fair comparisons.
- Publishes summaries to internal databases and dashboard layers.

Inputs:
-------
- Final game state packet (placements, turns, events) from `simulation-engine`
- Replay metadata and identifiers from `replay-logger`
- Deck ID and session metadata from `matchmaker` or `pod-meta-controller`

Outputs:
--------
- Aggregated win/placement data (PostgreSQL)
- Pod-level summaries (used by `bayesian-evaluator`)
- Simulation count trackers per deck
- Input to `value-index-service` and `replay-indexer`
- Convergence progress and alerts

Execution Flow:
---------------
1. Receive simulation result event
2. Validate and normalize result
3. Update statistical records by deck and pod
4. Emit summary to:
   - `bayesian-evaluator` for convergence check
   - `replay-indexer` for searchable replay metadata
   - `value-index-service` for value computation
   - SQL for persistent storage

Integration Points:
-------------------
- Kafka consumer of simulation results
- Writes to `db-service` (PostgreSQL)
- Signals `bayesian-evaluator` and `pod-meta-controller`
- Feeds public dashboard with updated rankings and meta

Deployment:
-----------
- Python or Go service optimized for high write throughput
- Containerized and autoscalable under Kubernetes
- Uses batched writes and stream processing for real-time updates

This service ensures the system continuously learns from simulation outcomes, updates performance rankings, and provides a data foundation for strategic AI training and player-facing insights.
