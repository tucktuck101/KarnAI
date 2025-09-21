annotation-service.txt

Annotation Service
==================

Purpose:
--------
The `annotation-service` enables manual or semi-automated tagging of replays with structured feedback, explanations, observations, or errors. It is used to augment agent training data, identify edge cases, and create human-aided insights for post-hoc review.

Responsibilities:
-----------------
- Accept annotations for game actions or sequences based on replay logs.
- Store tags, comments, corrections, and ratings associated with specific replay events.
- Support structured annotation formats (e.g., usefulness, missed triggers, risk).
- Provide review tools for expert users to audit or flag behaviors for analysis.

Key Features:
-------------
- Allows replay review and tagging by format, agent, archetype, or card.
- Stores annotation logs in JSONL or database format.
- Can influence future reward shaping or model retraining.
- Supports collaborative annotation by multiple reviewers with identity logging.

Inputs:
-------
- Replay logs (from `replay-logger` or `replay-indexer`)
- Annotation schema templates
- User submissions (via API or UI)

Outputs:
--------
- `replay-annotations` log (JSONL or DB)
- Structured tags attached to replay events
- Audit log of who submitted annotations and when
- Optional feedback for `reward-shaping-agent` or `explanation-service`

Execution Flow:
---------------
1. User selects a replay via `public-webpage` or API
2. Log is parsed and displayed (via `replay-viewer`)
3. Reviewer adds annotations to specific turn, card, or action
4. Annotations are validated and stored
5. Optionally used to retrain agents or highlight problem areas

Annotation Types:
-----------------
- Play Quality (e.g., suboptimal, greedy, efficient)
- Rule Accuracy (e.g., correct interaction, missed resolution)
- Strategic Tags (e.g., combo setup, tempo shift, bluff)
- Training Value (e.g., highlight for reinforcement or regression)

Integration Points:
-------------------
- Works with:
   - `replay-viewer` (visual UI for tagging)
   - `reward-shaping-agent` (feedback loop)
   - `explanation-service` (to validate or expand reasoning)
- Stores data via `db-service` in MongoDB or PostgreSQL

Deployment:
-----------
- Python service exposed via REST API
- Secured with optional OAuth from `auth-service`
- Optional rate limits and moderation queues for public submissions

The annotation-service connects expert review to AI development, offering a feedback-rich environment for improving model reasoning and community transparency.
