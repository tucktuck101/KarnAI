from __future__ import annotations
from typing import Iterable, Mapping, Any
import random

from karnai.contracts import Scheduler


def _chunks(lst: list[Any], n: int) -> list[list[Any]]:
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def round_robin_pods(
    players: list[Any],
    rounds: int = 1,
    pod_size: int = 4,
    seed: int | None = None,
):
    rng = random.Random(seed)
    players = list(players)
    n = len(players)
    if n < pod_size:
        yield [players]
        return
    for _ in range(rounds):
        rng.shuffle(players)
        pods = _chunks(players, pod_size)
        yield pods


class RoundRobinScheduler(Scheduler):
    def capabilities(self) -> dict[str, bool]:
        return {"distributed": False, "deterministic": True}

    def schedule(self, config: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
        players = list(config.get("players", []))
        rounds = int(config.get("rounds", 1))
        pod_size = int(config.get("pod_size", 4))
        seed = config.get("seed")
        for rnd, pods in enumerate(
            round_robin_pods(players, rounds=rounds, pod_size=pod_size, seed=seed),
            start=1,
        ):
            for i, pod in enumerate(pods, start=1):
                yield {
                    "round": rnd,
                    "pod": i,
                    "players": list(pod),
                    "match_id": f"r{rnd}_p{i}",
                }
