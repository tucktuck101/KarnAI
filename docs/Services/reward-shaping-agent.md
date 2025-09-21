reward-shaping-agent.txt

Reward Shaping Agent (RSA)
==========================

Purpose:
--------
The `reward-shaping-agent` analyzes game replays and assigns training rewards to actions taken by the AI. It dynamically adjusts these rewards based on strategic tags, game phase, outcomes, delayed effects, opponent response, and historical convergence confidence.

Responsibilities:
-----------------
- Parse replay logs and extract sequences of actions by each agent.
- Evaluate actions using flattened strategic tags derived from CardIR.
- Apply tag-weighted reward functions with support for parent-child inheritance.
- Incorporate post-hoc adjustments based on game result (placement).
- Apply delayed impact tracking for persistent/passive effects (e.g., Rhystic Study).
- Decay stale reward values over time if their associated actions underperform.
- Optionally emit reward anomalies to be audited or flagged by a human or shadow agent.

Key Features:
-------------
- Fully unsupervised reward interpretation with tag-based reasoning.
- Supports composite reward functions (per turn, per tag, per game, per pod).
- Supports flattened tags for fast access, while maintaining hierarchical lineage for audit.
- Implements reward decay for staleness and poor convergence.
- Compatible with Bayesian convergence scores for adaptive confidence tracking.
- Allows agent explanation outputs for debugging and reward trace validation.

Inputs:
-------
- Game replay log (JSONL format from `replay-logger`)
- Final placement data (from `result-aggregator`)
- Flattened and hierarchical tags (via `card-ir-registry`)
- Reward policy configuration or decay thresholds

Outputs:
--------
- Updated reward log (JSON or database)
- Action-tagged reward sequences with flattened tag traces
- Reward inheritance map and decay stats
- Optional anomaly log or shadow divergence report

Execution Flow:
---------------
1. Load and parse the replay log and outcome.
2. For each player:
   - Identify actions and passive triggers.
   - Flatten all tags associated with the action using CardIR.
   - For each tag:
     - Score the short-term impact (tempo, resources, threat)
     - Inherit reward if tag has no history but parent does
     - Apply placement modifier post-hoc (1st–4th normalized bonus)
     - Adjust weights up/down based on game result and convergence trends
3. Apply decay if the tag’s performance is statistically stale or inversely correlated with win rate.
4. Emit updated reward entries and optionally log anomalies or divergence with a shadow policy.

Reward Components:
------------------
- Resource gain/loss (mana, cards, life)
- Opponent denial (e.g., exile, discard)
- Stack interaction (e.g., counterspells, triggers)
- Passive utility effects (e.g., taxation, control-locks)
- Strategic timing (e.g., pre-combat removal, upkeep stack actions)
- Win/placement bonus (tiered by pod outcome)
- Tag-based generalization for new cards or unseen abilities

Integration Points:
-------------------
- Pulls IRs and tag hierarchies from `card-ir-registry`
- Receives logs from `replay-logger`
- Optionally interacts with `bayesian-evaluator` to track tag convergence and guide decay
- Logs to `reward-log-schema.json` and optional audit trail via `explanation-service`

Deployment:
-----------
- Python module with configuration-driven tag policies
- Can run in batch mode post-replay or streaming mode for per-action updates
- Tuned for large-scale processing with low memory overhead
- Containerized for execution in distributed replay analysis pipelines

Notes:
------
The reward shaping agent ensures every action is analyzed and reinforced in a way that reflects both tactical impact and strategic relevance. With tag inheritance, adaptive decay, and alignment with convergence metrics, it provides a highly flexible foundation for robust AI training and behavior alignment across all formats.
