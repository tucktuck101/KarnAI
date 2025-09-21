ui-client.txt

UI Client
=========

Purpose:
--------
The `ui-client` is a browser-based interface that allows human players to participate in games alongside AI agents. It provides a full Commander gameplay experience with real-time simulation feedback and action selection.

Responsibilities:
-----------------
- Display the current game state to a human user.
- Accept inputs and choices (e.g., card plays, attacks, priority passes).
- Communicate decisions to the `agent-hook` via WebSocket or API.
- Support full Commander game flow (priority, stack, phases).
- Provide live feedback and UI indicators for game progress.

Key Features:
-------------
- Action menu dynamically populated by `agent-hook`.
- Fully functional card interaction and battlefield zones.
- Stack viewer, graveyard inspector, life total HUD.
- Turn timer and auto-pass options.
- Built-in log viewer for transparency.

Inputs:
-------
- Game state updates from `simulation-engine` (via `agent-hook`)
- Valid action space for current decision point
- Card data and images from `card-ir-registry`

Outputs:
--------
- Player action selection (e.g., card name, targets, mode)
- UI logs (optional)
- Replay metadata (for later playback or debugging)

Execution Flow:
---------------
1. Player is assigned a seat in a 4-player pod
2. Game state updates are pushed to browser
3. Player selects an action or passes priority
4. Action is validated and sent to `agent-hook`
5. Game continues with mixed AI/human play

Integration Points:
-------------------
- Reads card metadata from `card-ir-registry`
- Communicates with `agent-hook` for decision cycles
- May export replays to `replay-logger`
- Supports annotation tagging in collaboration with `annotation-service`

Deployment:
-----------
- Served as a React/Vue/Svelte app
- Hosted behind `api-gateway`
- Integrated into staging or live sandbox games
- Optional player login via `auth-service`

The `ui-client` enables humans to directly interact with the AI simulation system, supporting hybrid pods, public events, educational use cases, and training data enrichment.
