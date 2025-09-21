volunteer-coordinator.txt

Volunteer Coordinator
=====================

Purpose:
--------
The `volunteer-coordinator` enables distributed simulation by allowing community members to donate compute resources. It manages authentication, job dispatch, validation, and contributor tracking for remote clients running training games.

Responsibilities:
-----------------
- Register volunteer nodes and verify client integrity.
- Dispatch simulation jobs to approved volunteers with signed payloads.
- Receive and verify simulation results.
- Maintain statistics on contributions per user or node.
- Prevent duplicate or invalid simulations from polluting the dataset.

Key Features:
-------------
- Lightweight client support (runs simulation-engine with minimal dependencies).
- Secure job signing with job IDs and seeds.
- Leaderboard tracking for contributors.
- Configurable throttle rate and priority handling.

Inputs:
-------
- Active job queue from `matchmaker`
- Pod configuration and seed
- Volunteer client registration and identity
- Convergence metadata from `pod-meta-controller`

Outputs:
--------
- Result payloads to `result-aggregator`
- Replay logs to `replay-logger`
- Contributor metrics to public leaderboard
- Optional anomaly flags or rejection logs

Execution Flow:
---------------
1. Register or authenticate new volunteer node
2. Dispatch job with simulation spec (decklist, config, seed)
3. Wait for game result or timeout
4. Validate result hash, turn count, and metadata
5. Log contribution and submit data to pipeline

Integration Points:
-------------------
- Works with:
   - `matchmaker` for job dispatch
   - `result-aggregator` for outcome storage
   - `replay-logger` for game trace collection
   - `auth-service` for identity management
   - `public-webpage` for contributor stats

Deployment:
-----------
- Python service with secure job queue API
- Can be exposed via a public registration endpoint
- Load balanced to handle concurrent volunteers
- Stores node metadata in PostgreSQL or Redis

The `volunteer-coordinator` empowers the MTG community to accelerate training and deck evaluation by safely contributing compute power from their own devices.
