from karnai.policies import RandomPolicy, ScriptedPassPolicy
from karnai.train_loop import TrainConfig, self_play


def test_scripted_self_play_steps():
    pol = ScriptedPassPolicy()
    out = self_play(pol, TrainConfig(episodes=3, seed=7))
    assert out["episodes"] == 3 and out["steps"] > 0


def test_random_policy_reseeds():
    pol = RandomPolicy(seed=1)
    a1 = [pol.act({"turn": 1}) for _ in range(5)]
    pol.reset(seed=1)
    a2 = [pol.act({"turn": 1}) for _ in range(5)]
    assert a1 == a2
