epochs.txt

Training Epochs
===============

Purpose:
--------
This document outlines how training epochs function within the AI simulation system for Magic: The Gathering, including their configuration, lifecycle, and role in progressive agent learning.

Definition:
-----------
An epoch is a defined batch of simulation games used to:
- Train the current policy.
- Evaluate new strategies.
- Recalculate rewards and convergence signals.
- Generate intermediate metrics and confidence scores.

Configuration Parameters:
-------------------------
- `epoch_size`: Number of games per pod in one training pass (e.g., 100 or 1000).
- `confidence_target`: Desired statistical certainty (e.g., 95%, 99%, 99.999%).
- `max_epochs_per_pod`: Cap on retraining cycles for any pod.
- `adaptive_scaling`: Optional feature to dynamically increase epoch size per confidence progress.

Lifecycle:
----------
1. **Initialization**: Matchmaker identifies pods needing more data.
2. **Dispatch**: Simulations are distributed (cloud, local, volunteer).
3. **Execution**: Games are logged, rewards applied, placements tallied.
4. **Review**: Bayesian Evaluator checks if new data changed confidence levels.
5. **Termination**: Pod training ends when confidence reaches threshold or max epochs hit.

Logging:
--------
- Epoch metadata (pod ID, start/end time, # games, configuration) is stored.
- Replay logs and reward summaries are grouped per epoch.
- Useful for visualizing training curves or debugging anomalies.

Benefits of Epoch-Based Training:
---------------------------------
- Allows tracking learning progression over time.
- Supports periodic reward shaping and convergence recalibration.
- Encourages parallelism (each pod runs independently).
- Enables snapshotting for rollback or auditing.

Dynamic Epoch Strategy:
-----------------------
- Start with `epoch_size = 1` to ensure early feedback loops.
- Increase exponentially as confidence builds: 1 → 5 → 20 → 100+
- Optional: Skip training for pods whose confidence has not changed significantly.

Tools:
------
- `pod-meta-controller`: Manages epoch progress and convergence.
- `test-orchestrator`: Validates correctness and reward behavior.
- `bayesian-evaluator`: Calculates convergence thresholds per epoch.

Conclusion:
-----------
Epochs are fundamental to structuring reinforcement learning in a massive multiplayer simulation space, providing both structure and scalability.
