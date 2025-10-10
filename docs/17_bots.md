# Stage 10 — Bot Policies

Baseline agents implementing the `Policy` contract:

- `RandomPolicy`: chooses between noop and pass_priority randomly.
- `ScriptedPassPolicy`: always passes priority.

Utilities:
- `train_loop.py`: simple loop to run N episodes with a policy against itself
  to validate end-to-end wiring before RL integration.
