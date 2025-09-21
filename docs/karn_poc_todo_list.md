Karn.ai 

PHASE 1 – DECK & CARD DATA PIPELINE
Objective: Parse and validate 5 Commander decklists from raw card data

[ ] Load and store raw card data (e.g. Scryfall JSON dump)
[ ] Build card-ir-generator to transform card JSON → IR format
[ ] Build card-ir-registry to store and version IRs
[ ] Implement deck-service to:
    [ ] Validate Commander legality (100 cards, 1 commander)
    [ ] Resolve cards to IRs
    [ ] Store and index canonical decklists
[ ] Add 5 sample Commander decks to test
[ ] Run full validation pipeline on all 5 decks

Acceptance Criteria:
- All 5 decks successfully parse and validate to IR
- Decks can be loaded for use in simulations
- IR registry contains all referenced cards with consistent formatting

PHASE 2 – SIMULATION ENGINE CORE
Objective: Simulate a full 4-player game using parsed IR decks

[ ] Build simulation-engine that includes:
    [ ] Turn structure and priority passing
    [ ] Phase and step resolution (draw, main, combat, etc.)
    [ ] Combat mechanics: attack/block/damage
    [ ] Game end conditions (life loss, poison, concession, decking out)
[ ] Implement zone system: hand, library, battlefield, graveyard, exile, stack
[ ] Create logic to load 4 decks from IR and assign to players
[ ] Enable deterministic seeding and debug mode
[ ] Generate and store a structured game log (JSON or plaintext)

Acceptance Criteria:
- A full game runs start to finish with valid state transitions
- 4-player pods operate using IR-based decks
- Simulation logs all turns, actions, and outcomes

PHASE 3 – AGENT ACTION INTEGRATION
Objective: Integrate basic AI agent to play legal turns

[ ] Build agent-hook to expose game state and receive actions
[ ] Create agent-service with:
    [ ] PPO model stub or baseline random-action agent
    [ ] Legal action generation logic
[ ] Integrate agent into game loop
[ ] Validate that agents play basic actions:
    [ ] Play lands, cast spells, declare attacks

Acceptance Criteria:
- All four players can be controlled by agent services
- Agent actions are legal and trigger correct game responses
- Simulation completes without human input

PHASE 4 – POD SIMULATION CONTROL
Objective: Automate pod formation and run multiple simulations

[ ] Build matchmaker to:
    [ ] Randomly select 4 unique decks from the 5 available
    [ ] Track pod combinations for repeatability
[ ] Create a script or queue to run batches of simulations
[ ] Dispatch each pod to simulation engine

Acceptance Criteria:
- Multiple pods can be formed from 5 decks
- Games simulate end-to-end without manual setup
- Pod metadata (decks, winner, game length) is logged per game

PHASE 5 – REPLAY LOGGING & ANALYSIS
Objective: Store and inspect replays for debugging and agent training

[ ] Implement replay-logger to:
    [ ] Capture complete game logs in structured format
    [ ] Tag replays by decks, outcomes, actions
[ ] Build CLI or HTML tool to:
    [ ] Load and step through replays
    [ ] Visualize turn summaries and decisions

Acceptance Criteria:
- Every simulation generates a valid, readable replay file
- Replays can be searched and filtered by deck combination or winner
- Developers can manually inspect agent decisions and outcomes

PHASE 6 –  REWARD SHAPING
Objective: Shape reward signals for future AI training

[ ] Build reward-shaping-agent to:
    [ ] Assign simple binary rewards (win/loss)
    [ ] Tag actions with strategic utility (e.g., tempo, removal)
[ ] Log rewards in replay or training data output

Acceptance Criteria:
- Agents receive shaped feedback per game
- Reward signal aligns with strategic gameplay traits
- System can be extended later for training loop integration

POC EXIT CRITERIA
[ ] System can simulate 100+ full Commander games using combinations of 5 IR decks
[ ] All game actions and results are stored and replayable
[ ] Agents legally play through full games with no human input
[ ] Architecture supports expansion to more decks and eventual training pipeline