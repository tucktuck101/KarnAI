reward-shaping.txt

Reward Shaping
==============

Purpose:
--------
This document defines how reward signals are calculated and adjusted during training simulations to guide reinforcement learning agents toward strategic, competitive, and rules-compliant behavior in Commander format.

Overview:
---------
Reward shaping involves assigning scalar feedback to actions based on their effectiveness, legality, and long-term value. This system uses both turn-based and post-hoc rewards.

Reward Sources:
---------------
1. **Immediate Impact**:
   - Drawing cards
   - Removing threats
   - Deploying mana or resources
   - Attacking effectively

2. **Delayed Impact**:
   - Triggered abilities (e.g., Rhystic Study)
   - Board control effects
   - Stack interactions

3. **Outcome-Based**:
   - Game placement (1st, 2nd, etc.)
   - Opponent elimination
   - Bluff success or tempo advantage

4. **Negative Rewards**:
   - Inefficient plays (e.g., wasting mana)
   - Overcommitting into wipes
   - Infinite loops or illegal actions
   - Repetitive non-impact actions (penalized with timers)

Reward Value Structure:
-----------------------
Each action has up to four perspectives:
- `player_value`: reward to self
- `opponent1_value`, `opponent2_value`, `opponent3_value`: penalty or mirror impact

This allows modeling interaction and multiplayer dynamics fairly.

Shaping Tools:
--------------
- `reward-shaping-agent`: Core engine for reward assignment
- `card-ir-registry`: Provides card-level impact estimates
- `replay-logger`: Flags potential reward-relevant actions
- `annotation-service`: Allows manual feedback and tuning

Post-Hoc Adjustments:
---------------------
- Rewards updated after game using placement-based bonus
- Strategic evaluations like combo success or bluff success added
- Game log reviewed for missed impact (e.g., triggers not paid for)

Win Placement Bonuses:
----------------------
- 1st: +1.0
- 2nd: +0.6
- 3rd: +0.2
- 4th: 0.0

Advanced Features:
------------------
- Delayed impact decay factor (credit action 2–3 turns later)
- Inverted reward for opponent effects
- Archetype-aware shaping (e.g., aggro vs. control rewards)
- Anomaly detection to trigger reward policy audit

Conclusion:
-----------
Reward shaping is essential for helping unsupervised agents learn good behavior in complex multiplayer environments. It evolves over time with feedback, convergence, and expert tuning.
