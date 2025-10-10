from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
from karnai.contracts import Policy
from karnai.env import KarnAIGymEnv


@dataclass
class SelfPlayConfig:
    episodes: int = 10
    steps_per_episode: int = 16
    seed: int = 0
    reward_per_pass: float = 0.0
    reward_per_turn_advance: float = 0.1


def run_self_play(policy: Policy, cfg: SelfPlayConfig) -> Dict[str, Any]:
    env = KarnAIGymEnv(seed=cfg.seed)
    total_steps = 0
    total_reward = 0.0
    for ep in range(cfg.episodes):
        obs, _ = env.reset(seed=cfg.seed + ep)
        policy.reset(seed=cfg.seed + ep)
        batch = []
        prev_turn = obs.get("turn", 1)
        for _ in range(cfg.steps_per_episode):
            act = policy.act(obs)
            step_arg = 1 if act.get("type") == "pass_priority" else 0
            obs, rew, term, trunc, info = env.step(step_arg)
            r = cfg.reward_per_pass if act.get("type") == "pass_priority" else 0.0
            if obs.get("turn", prev_turn) > prev_turn:
                r += cfg.reward_per_turn_advance
                prev_turn = obs["turn"]
            total_reward += r
            total_steps += 1
            batch.append((obs, act, r))
        if hasattr(policy, "train_batch"):
            policy.train_batch(batch)  # type: ignore[attr-defined]
    env.close()
    return {"episodes": cfg.episodes, "steps": total_steps, "reward": total_reward}
