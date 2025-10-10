from __future__ import annotations


def elo_expected_score(rating_a: float, rating_b: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))


def elo_update(rating: float, score: float, expected: float, k: float = 32.0) -> float:
    return rating + k * (score - expected)
