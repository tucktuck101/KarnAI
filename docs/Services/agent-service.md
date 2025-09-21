agent-service.txt

Agent Service
=============

Purpose:
--------
The Agent Service is responsible for evaluating game state, receiving available legal actions, and selecting the most strategically appropriate move using reinforcement learning. It is the core decision engine of the AI player in the simulation system.

Core Responsibilities:
----------------------
- Interact with the Simulation Engine via the Agent Hook
- Flatten and evaluate all incoming legal actions
- Query and apply learned policies based on reward shaping and tag data
- Execute the selected action and log metadata for explanation
- Adapt behavior over time through deck identity, meta-awareness, and confidence tracking

Key Functional Components:
--------------------------
1. **Action Evaluator**
   - Receives a list of legal actions from the `agent-hook`
   - For each action:
     - Flattens its tag hierarchy using the CardIR (see: Tag Flattening Logic)
     - Queries historical performance of those tags
     - Applies model inference (e.g., RLlib PPO policy) to assign a confidence-weighted value
     - Applies any relevant heuristic overrides for invalid or detrimental actions

2. **State Encoder**
   - Transforms the game state into a vector format
   - Includes zones, stack, mana availability, threat analysis, and phase context

3. **Policy Inference**
   - Uses reinforcement learning (PPO, A2C, etc.) to evaluate expected reward
   - Can support specialized models per archetype, color identity, or deck class
   - Includes optional shadow policy for self-evaluation

4. **Confidence Scorer**
   - Applies softmax to compute action selection confidence
   - Tracks confidence trends across simulations for convergence and correction

5. **Opponent Model**
   - Maintains a short-term memory of opponent actions, threats, and patterns
   - Informs play-around logic, bluff detection, and tactical evaluations

6. **Deck Archetype Awareness**
   - Aligns decisions with a strategic play pattern based on the deck’s classification
   - Adjusts value functions and action biasing based on archetype identity

7. **Turn Phase Sensitivity**
   - Adjusts reward/priority weighting based on current phase and stack state
   - Prevents phase-inappropriate decisions (e.g., casting Wrath before combat)

8. **Adaptive Exploration**
   - Adjusts the exploration/exploitation ratio dynamically based on:
     - Bayesian convergence levels
     - Novelty of opponents or decks
     - Stale or high-variance reward zones

9. **Staleness Decay & Self-Correction**
   - Detects when learned values no longer align with win rates or confidence
   - Applies decaying value weights to overfit or misaligned policies

10. **Dual-Agent Shadow Policy**
    - A parallel agent trained using the same data
    - Logs diverging decisions or outcomes for error detection and model comparison

Tag Flattening Logic:
---------------------
- Strategic tags stored in `CardIR` and `ActionIR` follow a parent-child hierarchy
- At decision time, each action’s tag structure is flattened into a flat list:
    - Input:
      - `{ "path": ["interaction", "stack_interaction", "counterspell"] }`
      - `{ "path": ["combo", "combo_disruption"] }`
    - Flattened result:
      - `[ "interaction", "stack_interaction", "counterspell", "combo", "combo_disruption" ]`
- Used for:
    - Reward lookups
    - Policy input
    - Action bias filtering
- Flattening is cached per turn for performance

Outputs:
--------
- Chosen action and required targets
- Confidence score
- Flattened tag trace
- Phase and intent metadata
- Optional explanation log

Integration Points:
-------------------
- **`card-ir-registry`**: Card definitions with strategic tags
- **`reward-shaping-agent`**: Tag-based reward adjustments and decay
- **`agent-hook`**: Entry point to simulation
- **`explanation-service`**: Logs strategy trace and intent
- **`bayesian-evaluator`**: Tracks convergence to influence exploration
- **`deck-service`**: Provides deck archetype classification

Conclusion:
-----------
The enhanced Agent Service blends advanced reinforcement learning with context-aware evaluation, opponent tracking, and meta-aware adaptability. By flattening tags at decision time, incorporating strategic specializations, and enabling learning corrections, it forms the backbone of intelligent, strategic gameplay simulation in Commander and beyond.
