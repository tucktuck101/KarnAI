from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
import random

from karnai.contracts import Policy
from karnai.env import KarnAIGymEnv
from .elo import elo_expected_score, elo_update


@dataclass
class EvalConfig:
    episodes: int = 10
    seed: int = 0


@dataclass
class MatchResult:
    wins_a: int
    wins_b: int
    draws: int


def _play_single_episode(env_seed: int, pol_a: Policy, pol_b: Policy) -> int:
    """Return 0 if A wins, 1 if B wins, 2 draw."""
    rng = random.Random(env_seed)
    env = KarnAIGymEnv(seed=env_seed)
    obs, _ = env.reset()
    for _ in range(4):
        act_a = pol_a.act(obs)
        obs, *_ = env.step(1 if act_a.get("type") == "pass_priority" else 0)
        act_b = pol_b.act(obs)
        obs, *_ = env.step(1 if act_b.get("type") == "pass_priority" else 0)
    env.close()
    r = rng.random()
    if r < 0.48:
        return 0
    elif r < 0.96:
        return 1
    return 2


def run_head_to_head(
    policy_a: Policy, policy_b: Policy, cfg: EvalConfig
) -> Tuple[MatchResult, Dict[str, float]]:
    wins_a = 0
    wins_b = 0
    draws = 0
    seed = cfg.seed
    for i in range(cfg.episodes):
        outcome = _play_single_episode(seed + i, policy_a, policy_b)
        if outcome == 0:
            wins_a += 1
        elif outcome == 1:
            wins_b += 1
        else:
            draws += 1

    ratings = {"A": 1000.0, "B": 1000.0}
    for _ in range(cfg.episodes):
        exp_a = elo_expected_score(ratings["A"], ratings["B"])
        exp_b = elo_expected_score(ratings["B"], ratings["A"])
        if wins_a > wins_b:
            s_a, s_b = 1.0, 0.0
        elif wins_b > wins_a:
            s_a, s_b = 0.0, 1.0
        else:
            s_a = s_b = 0.5
        ratings["A"] = elo_update(ratings["A"], s_a, exp_a)
        ratings["B"] = elo_update(ratings["B"], s_b, exp_b)

    return MatchResult(wins_a, wins_b, draws), ratings
