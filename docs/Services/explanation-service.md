explanation-service.txt

Explanation Service
===================

Purpose:
--------
The `explanation-service` provides interpretable insights into why AI agents took specific actions during a simulation. It supports transparency, trust, debugging, and human-guided improvement of agent behavior.

Responsibilities:
-----------------
- Collect and serve decision-making traces from agents.
- Analyze policy outputs (logits, confidence, attention) and correlate with replay context.
- Generate structured explanations (e.g., “played card for tempo”, “held up counterspell”).
- Support comparisons across agents, archetypes, or decision epochs.

Key Features:
-------------
- Compatible with supervised and unsupervised RL agents.
- Integrates with attention or saliency maps (if model supports).
- Stores explanations for each decision point in a game.
- Enables post-game review and debugging of learned behavior.

Inputs:
-------
- Inference metadata from `agent-service` or `agent-hook`
- Replay logs (via `replay-logger`)
- Card IRs (from `card-ir-registry`)
- Optional user annotations (from `annotation-service`)

Outputs:
--------
- Explanation logs (per turn, action, or agent)
- Human-readable summaries and reasoning trees
- Comparison heatmaps across agents or episodes
- Flagged anomalies for training inspection

Execution Flow:
---------------
1. Receive action and metadata from `agent-service`
2. Parse state context and valid options
3. Match decision patterns to known explanation templates or generate dynamically
4. Store explanation with replay ID and action ID
5. Optional: augment with annotations or agent debug info

Explanation Types:
------------------
- Value-maximizing (e.g., “generated 2 mana, gained 1 card”)
- Strategic (e.g., “bluffed threat”, “played around wipe”)
- Tactical (e.g., “removed key combo piece”)
- Randomized (e.g., “coin flip outcome: tails”)

Integration Points:
-------------------
- Receives metadata from `agent-service` and `replay-logger`
- Accesses IRs via `card-ir-registry`
- Supports visualization via `replay-viewer`
- Linked with `annotation-service` for validation

Deployment:
-----------
- Python service with REST API
- Explanation records stored in document DB or as JSONL logs
- Can be queried by replay ID, deck ID, or action ID
- May support frontend tooltips or breakdown panels on `public-webpage`

The explanation-service enhances transparency, supports fairness auditing, and enables the system to not only act—but justify and refine its actions in a human-understandable way.
