from dataclasses import dataclass
from typing import Any, Mapping

from karnai.eval import EvalConfig, run_head_to_head


@dataclass
class RandomPassPolicy:
    def capabilities(self) -> dict[str, bool]:
        return {"stochastic": True}

    def act(self, observation: Mapping[str, Any]):
        # Always pass_priority to exercise env path
        return {"type": "pass_priority"}

    def reset(self, seed: int | None = None) -> None: ...


def test_eval_determinism_and_ratings():
    pol_a = RandomPassPolicy()
    pol_b = RandomPassPolicy()
    cfg = EvalConfig(episodes=8, seed=123)
    res1, ratings1 = run_head_to_head(pol_a, pol_b, cfg)
    res2, ratings2 = run_head_to_head(pol_a, pol_b, cfg)
    assert res1 == res2
    assert ratings1 == ratings2
    # Ratings near 1000
    assert 900 <= ratings1["A"] <= 1100
    assert 900 <= ratings1["B"] <= 1100
