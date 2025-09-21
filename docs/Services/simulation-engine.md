simulation-engine.txt

Simulation Engine
=================

Purpose:
--------
The `simulation-engine` is the core component responsible for executing full Commander games using the rules of Magic: The Gathering. It is designed for determinism, IR-based rule interpretation, reinforcement learning compatibility, and replay generation. It can simulate pods composed of human, AI, or hybrid players.

Responsibilities:
-----------------
- Enforce the rules of Magic: The Gathering using an Intermediate Representation (IR) system.
- Execute Commander-format multiplayer games.
- Interface with the `agent-hook` to request decisions from AI models.
- Emit game state transitions to the `replay-logger`.
- Evaluate win conditions and track placements.
- Handle triggered abilities, the stack, priority passing, state-based actions, and replacement effects.

Key Features:
-------------
- Deterministic execution for training reproducibility.
- Modular support for various MTG formats (future support: Standard, Draft, Modern, etc.).
- Pluggable rule modules per format (Commander, Oathbreaker, Pauper, etc.).
- Turn timeouts to avoid infinite combos or slow play.
- Supports both internal training and external volunteer node execution.

Inputs:
-------
- Card IRs (from `card-ir-registry`)
- Validated decklists (from `deck-service`)
- Pod metadata (from `matchmaker`)
- Configuration flags (turn timeout, debug mode, format type)
- Actions from AI via `agent-hook` or human players via `ui-client`

Outputs:
--------
- Full replay log (JSONL format) to `replay-logger`
- Final game state (placements, damage, life, turn counts)
- Result packet to `result-aggregator`
- Optional debug trace to `explanation-service`

Execution Flow:
---------------
1. Load decklists and IRs
2. Initialize pod state, random seed, and life totals
3. Enter game loop:
   - Begin turn phase → Upkeep → Main → Combat → Second Main → End
   - Handle stack resolution and triggers
   - Request agent/human input for decision points
   - Enforce state-based actions
4. End game when a player wins or all others lose
5. Emit replay and game summary

Interfaces:
-----------
- Reads IRs and decks from storage/cache
- Exchanges decisions with `agent-hook` or `ui-client`
- Publishes replay events to `replay-logger`
- Sends results to `result-aggregator` and `pod-meta-controller`

Configuration Flags:
--------------------
- Replay debug mode (enables verbose output for replay inspection)
- Turn timeout (e.g. 60s per player, failsafe for infinite loops)
- Random seed (enforces reproducible games)
- Game mode (Commander, Draft, Sealed, etc.)
- Headless mode (for training vs. interactive vs. visualized)

Deployment:
-----------
- Python prototype for rapid iteration
- Rust production engine for performance and memory safety
- Supports containerized execution for local, cloud, or volunteer nodes

Future Format Support:
----------------------
The engine is designed to support all MTG formats with minimal code changes:
- 60-card 1v1 formats (Standard, Modern, Legacy, etc.)
- Draft and Sealed for AI card selection and deck building
- Cube and Brawl formats via pluggable rulesets
- Multiplayer variants like Archenemy or Two-Headed Giant

Notes:
------
The simulation-engine is the foundation of the system, enabling competitive AI development, reproducible training experiments, deck evaluation at scale, and public replay introspection.
