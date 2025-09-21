card-ir-generator.txt

Card IR Generator Service
=========================

Purpose:
--------
The `card-ir-generator` service transforms raw card data (typically in JSON format, such as from Scryfall) into a structured Intermediate Representation (IR) that the simulation engine, reward shaping agent, and AI agents can interpret and act upon.

It also enriches each card with hierarchical strategic tags using NLP and pattern recognition to support reward shaping, action evaluation, and post-game analysis.

Responsibilities:
-----------------
- Parse raw card JSON into domain objects (e.g., name, mana cost, type line, oracle text, set, rarity).
- Use a hybrid NLP + rule-matching engine to identify:
  - Activated and triggered abilities
  - Spell resolution behavior
  - Strategic intent (e.g., removal, ramp, combo-piece)
- Generate CardIR entries that map to IR action primitives, including:
  - Static and triggered abilities
  - Targeting rules
  - Conditional effects
- Generate hierarchical tags (e.g., interaction > removal > exile_effect).
- Embed tag metadata into CardIR in a way that supports flattening at runtime.
- Validate card completeness, ability coverage, and legal format mapping.
- Emit CardIR records to the `card-ir-registry` for persistent access.

Inputs:
-------
- Raw JSON files or API streams (e.g., Scryfall bulk data).
- IR schema definitions (action types, targeting logic, costs).
- Tag taxonomy for NLP mapping (parent-child strategic tag relationships).
- MTG Comprehensive Rules for parsing keyword abilities and logic.

Outputs:
--------
- JSON CardIR objects with:
  - Core metadata (name, mana cost, color identity, etc.)
  - Oracle ability IR definitions
  - Strategic hierarchical tags for reward shaping and agent inference
  - Reward hinting metadata (delayed, immediate, symmetrical, passive, etc.)

Example Tag Output:
-------------------
{
  "tags": [
    { "path": ["interaction", "removal", "exile_effect"] },
    { "path": ["tempo", "low_cost_interaction"] }
  ],
  "flattened_tags": [
    "interaction", "removal", "exile_effect", "tempo", "low_cost_interaction"
  ]
}

Interfaces:
-----------
- Input: Local file store, scheduled API poller, or real-time stream consumer
- Output: Kafka topic → `card.ir.generated` OR direct API → `card-ir-registry`
- Optional: REST validation endpoint (e.g., `POST /ir/validate`) for schema debugging

Communication:
--------------
- Kafka topic: `card.ir.generated`
- REST endpoint (optional): `POST /ir/batch`

Dependencies:
-------------
- NLP engine or ruleset matcher for ability classification
- Comprehensive rulebook or keyword extraction framework
- Access to card data source (e.g., Scryfall API)
- Tag taxonomy (can be stored in config or served by `tag-taxonomy-service`)

Deployment:
-----------
- Triggered during new set releases or bulk reprocessing jobs
- Containerized job can be scheduled (cron/webhook/manual)
- Logs transformation stats, tag coverage, and unresolved abilities

Notes:
------
CardIR is the canonical representation of all cards. It enables modular simulation logic, stable AI interfaces, and reward alignment across all formats. Tag accuracy directly influences simulation quality, making this service critical to agent performance and explainability.
