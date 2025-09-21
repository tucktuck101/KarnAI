matchmaker.txt

Matchmaker
==========

Purpose:
--------
The `matchmaker` service is responsible for creating Commander game pods (groups of four decks) and dispatching them to be simulated. It ensures that all eligible decks are tested against others fairly, and maintains load balance across the simulation infrastructure.

Responsibilities:
-----------------
- Select 4 unique decklists from the deck pool.
- Ensure matchups are diverse and consistent with tournament-style pairing logic.
- Avoid reusing recently-converged pods.
- Dispatch simulation jobs to either internal workers or volunteer clients.
- Track match job queue saturation for scaling and optimization.

Key Features:
-------------
- Deterministic pod composition via seeding (for reproducibility).
- Flexible pod formation logic (round-robin, MMR-pairing, exhaustive pairings).
- Optional override for manual deck combinations (used in testing).
- Integrated with confidence convergence logic to prevent redundant pairings.

Inputs:
-------
- Active deck pool (via `deck-service`)
- Pod history and convergence status (via `pod-meta-controller`)
- Volunteer availability and compute status (via `volunteer-coordinator`)
- Training session configuration (epoch size, random seed, mode flags)

Outputs:
--------
- Simulation job packets (decklist IDs + seed + config)
- Event to Kafka queue (for `simulation-engine` or remote client)
- Optional: log for audit trail and experiment traceability

Execution Flow:
---------------
1. Check for eligible decks and non-converged pod combinations
2. Select 4-deck pod (random, balanced, or targeted)
3. Generate seed and simulation configuration
4. Dispatch job to:
   - `simulation-engine` (internal)
   - `volunteer-coordinator` (external)
5. Log and track pod activity

Integration Points:
-------------------
- Reads deck data from `deck-service`
- Reads convergence info from `pod-meta-controller`
- Dispatches jobs via Kafka for `simulation-engine`
- Can route jobs to `volunteer-coordinator` when external support is enabled

Deployment:
-----------
- Stateless Python service
- Can be run as a scheduler or Kafka consumer loop
- Configurable for pod size, deck selection strategy, and job priority

The matchmaker ensures training coverage across decks and formats while controlling system load, enabling scalable, reproducible, and fair training environments.
