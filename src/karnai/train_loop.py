from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from karnai.env import KarnAIGymEnv


@dataclass
class TrainConfig:
    episodes: int = 10
    seed: int = 0


def self_play(policy, cfg: TrainConfig) -> Dict[str, Any]:
    env = KarnAIGymEnv(seed=cfg.seed)
    total_steps = 0
    for ep in range(cfg.episodes):
        obs, _ = env.reset(seed=cfg.seed + ep)
        policy.reset(seed=cfg.seed + ep)
        for _ in range(8):
            act = policy.act(obs)
            step_arg = 1 if act.get("type") == "pass_priority" else 0
            obs, rew, term, trunc, info = env.step(step_arg)
            total_steps += 1
    env.close()
    return {"episodes": cfg.episodes, "steps": total_steps}
