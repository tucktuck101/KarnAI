replay-logger.txt

Replay Logger Service
=====================

Purpose:
--------
The `replay-logger` captures comprehensive game state transitions, actions, and metadata during simulations. It generates detailed logs to facilitate replay visualization, strategic analysis, reward shaping, agent training, and human auditing.

Responsibilities:
-----------------
- Continuously logs all actions, state transitions, and triggered abilities during simulation.
- Records flattened strategic tags associated with each action for clarity and rapid analysis.
- Stores game state context including player resources, life totals, game phase, and stack status.
- Provides structured logs that are easily searchable and indexable by downstream services.

Key Features:
-------------
- Detailed state and action logging with precise timing and sequencing.
- Integration of strategic tags and metadata from `agent-service` and CardIR data.
- Captures decision confidence and Bayesian convergence metrics influencing actions.
- Supports both full replays and targeted state/action log searches.

Inputs:
-------
- Game state data and player actions from `simulation-engine`.
- Flattened strategic tags and agent metadata via `agent-hook` and `agent-service`.
- Optional Bayesian convergence feedback and shadow policy metadata.

Outputs:
--------
- JSONL-formatted structured replay logs.
- Comprehensive metadata logs (strategic tags, player states, confidence scores).
- Indexed data for efficient retrieval and analysis by `replay-indexer`.

Log Structure Example:
----------------------
{
  "turn": 5,
  "phase": "combat",
  "active_player": "Player 2",
  "action": {
    "player": "Player 2",
    "card_played": "Swords to Plowshares",
    "target": "Opponent's Thassa's Oracle",
    "flattened_tags": ["interaction", "removal", "instant_speed"],
    "confidence": 0.87,
    "shadow_policy_action": "Fierce Guardianship",
    "shadow_confidence": 0.75
  },
  "state": {
    "player_life_totals": {"P1": 40, "P2": 27, "P3": 33, "P4": 19},
    "stack": ["Demonic Consultation (P4)", "Swords to Plowshares (P2)"],
    "mana_pool": {"P2": ["1 Plains (untapped)"]},
    "board_state_summary": "Opponent controls Thassa's Oracle, Player 2 controls Commander."
  }
}

Integration Points:
-------------------
- Receives game state and actions from `simulation-engine` and `agent-hook`.
- Logs metadata received from `agent-service`, including flattened tags and confidence scores.
- Provides replay data to `reward-shaping-agent`, `bayesian-evaluator`, and `explanation-service`.
- Indexed by `replay-indexer` for easy retrieval and detailed analysis.

Deployment:
-----------
- Lightweight Python service optimized for real-time logging performance.
- Containerized and horizontally scalable for parallel pod simulations.
- Stores logs in structured file storage (JSONL) or object storage for durability and fast indexing.

Use Cases:
----------
- Strategic tag and reward shaping analysis by `reward-shaping-agent`.
- Bayesian convergence evaluation and strategic effectiveness auditing.
- Replay visualizations in `replay-viewer` for human review, education, or public display.
- Detailed explanation tracing through `explanation-service`.

Conclusion:
-----------
The Replay Logger Service ensures detailed and structured logging of gameplay simulations, strategic contexts, and agent decisions. It provides critical data to multiple downstream services, enhancing strategic analysis, reward shaping accuracy, and overall system transparency and auditability.
