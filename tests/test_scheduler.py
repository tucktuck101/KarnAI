from karnai.scheduler import RoundRobinScheduler, round_robin_pods


def test_round_robin_determinism():
    players = [f"d{i}" for i in range(8)]
    pods1 = list(round_robin_pods(players, rounds=3, pod_size=4, seed=123))
    pods2 = list(round_robin_pods(players, rounds=3, pod_size=4, seed=123))
    assert pods1 == pods2 and len(pods1) == 3
    assert all(len(rnd) == 2 and all(len(p) == 4 for p in rnd) for rnd in pods1)


def test_scheduler_yields_matches():
    sched = RoundRobinScheduler()
    matches = list(
        sched.schedule(
            {
                "players": ["a", "b", "c", "d", "e", "f"],
                "rounds": 2,
                "pod_size": 3,
                "seed": 42,
            }
        )
    )
    assert len(matches) == 4
    matches2 = list(
        sched.schedule(
            {
                "players": ["a", "b", "c", "d", "e", "f"],
                "rounds": 2,
                "pod_size": 3,
                "seed": 42,
            }
        )
    )
    assert matches == matches2
