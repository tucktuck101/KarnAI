agent-hook.txt

Agent Hook
==========

Purpose:
--------
The `agent-hook` is the interface between the `simulation-engine` and the AI agents responsible for decision-making during games. It abstracts away the simulation internals and presents a normalized, interpretable game state to the agents.

Responsibilities:
-----------------
- Translate current game state into an agent-observable input format.
- Send decision requests to the `agent-service` (or human override via `ui-client`).
- Receive and validate agent decisions (card names, stack targets, phases, combat steps, etc.).
- Fallback to default/pass behavior in case of invalid actions or timeouts.
- Operate transparently for up to 4 agents simultaneously in multiplayer pods.

Key Features:
-------------
- Stateless transformation layer for real-time agent interaction.
- Consistent action encoding scheme.
- Timeout fallback for slow or stalled agents.
- Can be run in headless or visualized mode.

Inputs:
-------
- Current turn game state from `simulation-engine`
- Active agent ID and priority phase
- Valid action space (defined by simulation rules)
- Simulation seed and agent configuration

Outputs:
--------
- Chosen action (encoded command string or ID)
- Optional metadata (probabilities, confidence, explanation hook)

Execution Flow:
---------------
1. Receive game state snapshot and action space
2. Format observation into agent-readable state
3. Send inference request to `agent-service`
4. Wait for agent decision (with timeout)
5. Validate and return chosen action to simulation engine

Interfaces:
-----------
- Requests decisions from `agent-service`
- Optionally integrates with `ui-client` for human decisions
- Logs inference metadata for traceability (optional: `explanation-service`)
- Provides formatted state view to agents via shared schema

Supported Decision Types:
-------------------------
- Play card from hand
- Activate ability
- Choose attack targets/blockers
- Stack resolution order
- Mulligans and keep decisions
- Phase skips and passes

Deployment:
-----------
- Bundled with `simulation-engine`
- Headless mode for training pods
- Debug mode with state printer for development
- Replay mode enabled via `replay-logger` for post-hoc trace

This service ensures modularity and future agent compatibility while enabling dynamic, context-aware gameplay from both AI and human players.
