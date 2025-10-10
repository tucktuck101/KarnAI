from __future__ import annotations
import random
from typing import Mapping, Any


class RandomPolicy:
    """Randomly chooses noop or pass_priority."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def capabilities(self) -> dict[str, bool]:
        return {"stochastic": True}

    def act(self, observation: Mapping[str, Any]):
        if self.rng.random() < 0.5:
            return {"type": "pass_priority"}
        return {"type": "noop"}

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            self.rng.seed(seed)
