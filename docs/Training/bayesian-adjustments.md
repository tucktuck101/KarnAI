bayesian-adjustments.txt

Bayesian Adjustments
====================

Purpose:
--------
This document explains how Bayesian methods are used to guide simulation and training efficiency, determine convergence, and adaptively reallocate resources for pod evaluation in Commander AI simulations.

Core Concept:
-------------
Bayesian inference allows the system to update its belief about a deck’s performance using new simulation data without starting from scratch each time.

Use Cases:
----------
1. **Convergence Detection**:
   - Posterior confidence intervals help determine when a pod is "solved."

2. **Smart Resampling**:
   - Bayesian uncertainty is used to prioritize pods with volatile or low-confidence matchups.

3. **Reward Auditing**:
   - Bayesian anomalies in reward effectiveness flag potential policy errors.

4. **Meta Monitoring**:
   - After new cards are released or rules change, Bayesian delta scores trigger retraining only where needed.

Key Features:
-------------
- Probabilistic modeling of 1st–4th placement probabilities.
- Confidence intervals tracked over epochs.
- Optional Dirichlet-Multinomial model for multinomial placements.
- Decay of stale data if meta shifts (e.g., using exponential decay factor).

Integration Points:
-------------------
- `bayesian-evaluator`: Main service responsible for computation.
- `result-aggregator`: Supplies historical outcome data per pod.
- `pod-meta-controller`: Stores and tracks convergence scores.
- `reward-shaping-agent`: May query confidence to adjust reward policy scope.

Example Adjustment Flow:
------------------------
1. Pod finishes 100 games → placements: [40, 30, 20, 10]
2. Posterior updated with new samples → Confidence = 98%
3. Pod added to “slow mode” for light resampling
4. Another deck is buffed → system detects outdated placement confidence
5. Bayesian delta triggers retraining of affected pods

Benefits:
---------
- Efficient use of computational resources.
- Quantifiable learning progress per deck.
- Avoids overtraining on converged pods.
- Adapts gracefully to environmental or card pool changes.

Conclusion:
-----------
Bayesian adjustments provide a mathematically grounded method for evaluating training progress and prioritizing simulation jobs with maximum value for learning and stability.
