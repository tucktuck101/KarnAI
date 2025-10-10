from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any
import math
import random

from karnai.contracts import Policy


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


@dataclass
class _Bandit:
    w0: float = 0.0
    w_turn: float = 0.0
    w_active: float = 0.0
    w_priority: float = 0.0
    lr: float = 0.05
    rng_seed: int = 0

    def prob_pass(self, obs: Mapping[str, Any]) -> float:
        x = (
            self.w0
            + self.w_turn * float(obs.get("turn", 0))
            + self.w_active * float(obs.get("active_player", 0))
            + self.w_priority * float(obs.get("priority_player", 0))
        )
        return _sigmoid(x)

    def update(self, obs: Mapping[str, Any], action_pass: bool, reward: float) -> None:
        p = self.prob_pass(obs)
        a = 1.0 if action_pass else 0.0
        g = (a - p) * reward
        self.w0 += self.lr * g * 1.0
        self.w_turn += self.lr * g * float(obs.get("turn", 0))
        self.w_active += self.lr * g * float(obs.get("active_player", 0))
        self.w_priority += self.lr * g * float(obs.get("priority_player", 0))


class _BanditPolicy(Policy):
    def __init__(self, seed: int = 0):
        self.bandit = _Bandit(rng_seed=seed)
        self.rng = random.Random(seed)

    def capabilities(self) -> dict[str, bool]:
        return {"stochastic": True}

    def act(self, observation: Mapping[str, Any]):
        p = self.bandit.prob_pass(observation)
        return {"type": "pass_priority"} if self.rng.random() < p else {"type": "noop"}

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            self.rng.seed(seed)

    def train_batch(
        self,
        batch: list[tuple[Mapping[str, Any], Mapping[str, Any], float]],
    ) -> None:
        for obs, act, rew in batch:
            self.bandit.update(obs, act.get("type") == "pass_priority", rew)


class PPOAdapter(_BanditPolicy):
    pass


class DQNAdapter(_BanditPolicy):
    pass
