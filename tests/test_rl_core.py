from karnai.rl import DQNAdapter, PPOAdapter, SelfPlayConfig, run_self_play


def test_self_play_runs_and_updates():
    pol = PPOAdapter(seed=7)
    out = run_self_play(pol, SelfPlayConfig(episodes=3, steps_per_episode=8, seed=11))
    assert out["episodes"] == 3 and out["steps"] == 24
    # Run again and ensure determinism given same seeds
    pol2 = PPOAdapter(seed=7)
    out2 = run_self_play(pol2, SelfPlayConfig(episodes=3, steps_per_episode=8, seed=11))
    assert out == out2


def test_dqn_adapter_compat():
    pol = DQNAdapter(seed=123)
    out = run_self_play(pol, SelfPlayConfig(episodes=2, steps_per_episode=4, seed=5))
    assert out["steps"] == 8
