pod-meta-controller.txt

Pod Meta Controller
===================

Purpose:
--------
The `pod-meta-controller` manages metadata for all active and historical pods, including their simulation progress, convergence status, retry counts, and experimental parameters. It coordinates training flow across services and helps prevent unnecessary recomputation.

Responsibilities:
-----------------
- Track simulation counts and game outcomes for each 4-player pod.
- Coordinate with `matchmaker` and `bayesian-evaluator` to determine when pods should be retired.
- Prevent duplicate pod dispatch once convergence is reached.
- Monitor and store training parameters (epoch size, seed, flags).
- Maintain retry records for failed or incomplete simulations.

Key Features:
-------------
- Stores convergence state per pod in durable cache or DB.
- Works alongside Bayesian inference to throttle job creation.
- Supports training lifecycle insights (active vs. archived pods).
- Optional expiration and reset logic for evolving training conditions.

Inputs:
-------
- Pod definitions (deck IDs, seed, config) from `matchmaker`
- Convergence signals from `bayesian-evaluator`
- Simulation metadata and result triggers

Outputs:
--------
- Pod status updates (ready, active, converged, archived)
- Control signals to `matchmaker` to skip/queue pods
- Epoch and iteration statistics
- Optional training trace export

Execution Flow:
---------------
1. Receive new pod info from `matchmaker`
2. Track simulation runs and placement consistency
3. Wait for convergence signal from `bayesian-evaluator`
4. Mark pod as complete and signal to downstream services
5. Archive pod metadata or reset as needed

Integration Points:
-------------------
- Communicates with:
   - `matchmaker` (to block/allow job creation)
   - `result-aggregator` (for result context)
   - `bayesian-evaluator` (for convergence tracking)
   - `replay-indexer` and dashboards (for status metrics)

Deployment:
-----------
- Stateless or semi-stateful Python service
- Uses Redis, MongoDB, or PostgreSQL for pod metadata
- Deployable as a background process or Kafka consumer

The `pod-meta-controller` forms the backbone of intelligent training orchestration, reducing redundant simulations and providing detailed insight into system progression and data confidence.
