agent-architecture.txt

Agent Architecture
==================

Overview:
---------
The agent architecture describes the structural components, decision logic, and learning strategies utilized by the AI player during simulation. It integrates reinforcement learning (RL), strategic tagging, opponent modeling, and Bayesian-informed exploration to create a highly adaptive and strategically robust decision-making process.

Core Components:
----------------

1. Action Evaluator:
   - Receives legal actions and associated CardIR from the simulation environment via `agent-hook`.
   - Flattens strategic tags from hierarchical structures for rapid evaluation.
   - Utilizes reinforcement learning (RLlib PPO/A2C) models to estimate expected action values.
   - Applies heuristic overrides to eliminate invalid or clearly disadvantageous moves.

2. State Encoder:
   - Converts game states into vectorized inputs for RL models.
   - Captures critical state information:
     - Player life totals and resources (mana, cards, board state)
     - Stack contents, available responses, and known threats
     - Game phase context (e.g., main phase, combat step, upkeep)
     - Deck archetype identity to inform strategy alignment

3. Opponent Modeling:
   - Maintains short-term memory of opponent actions, threats, and observable patterns.
   - Provides context for bluff detection, strategic counterplay, and anticipatory actions.
   - Optionally integrates historical data from past simulations or meta-analysis.

4. Confidence & Exploration Tuning:
   - Uses Bayesian convergence data to adjust exploration-exploitation ratios dynamically.
   - Reduces exploration in highly converged environments, increases exploration against novel or uncertain pods.

5. Shadow Policy Comparison:
   - Trains a secondary "shadow" agent in parallel with similar inputs but independent policy updates.
   - Monitors divergence between main and shadow policies to detect overfitting, staleness, or policy instability.

6. Reward Integration & Tagging:
   - Interacts with the `reward-shaping-agent` to receive tag-specific reward updates and decay signals.
   - Uses flattened tags to streamline learning from reward structures, generalizing insights across similar actions or scenarios.

7. Decay & Correction Mechanisms:
   - Implements reward staleness decay based on Bayesian evaluator convergence signals and performance regression.
   - Adjusts policy weights when historical strategies become consistently suboptimal or detrimental.

8. Deck Archetype Specialization:
   - Incorporates predefined deck archetypes from `deck-service`.
   - Biases actions to fit the deck's strategic identity (e.g., Aggro, Combo, Control).

Data Flow:
----------
- Game state and legal actions → State Encoder → Action Evaluator → RL model inference → Confidence Scorer → Decision Output
- Historical/observed opponent actions → Opponent Modeling → Action Evaluator context
- Flattened tags and rewards → RL model updates via `reward-shaping-agent` interactions
- Bayesian convergence feedback → Exploration tuning and reward decay logic adjustments

Training Strategy:
------------------
- Uses multi-epoch, adaptive epoch-sizing based on Bayesian convergence to optimize training efficiency.
- Employs composite rewards (immediate, delayed, strategic tag-based, placement-based) for nuanced policy learning.
- Regularly audits and validates strategic tags and reward alignment with shadow policy benchmarks.

Integration Points:
-------------------
- Receives actions via `agent-hook` and CardIR/tag data from `card-ir-registry`.
- Sends action choices and metadata to `simulation-engine` and `replay-logger`.
- Receives reward and decay updates from `reward-shaping-agent`.
- Adjusts exploration parameters based on signals from `bayesian-evaluator`.
- Provides flattened tags and strategic reasoning metadata to `explanation-service`.

Deployment & Scalability:
-------------------------
- Agent inference service is containerized for Kubernetes-based deployment.
- Scales horizontally to support parallel simulation pods and distributed training.
- Optimized for GPU-accelerated inference and training via Ray/RLlib or TensorFlow/PyTorch integration.

Conclusion:
-----------
The enhanced agent architecture provides comprehensive decision-making sophistication through strategic tagging, adaptive learning, and Bayesian-informed exploration. Its modular design allows continuous refinement, deep explainability, and robust, context-aware gameplay across the full scope of Magic: The Gathering Commander and future formats.
