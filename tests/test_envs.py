from karnai.env import KarnAIAECEnv, KarnAIGymEnv


def test_aec_env_cycle():
    env = KarnAIAECEnv(seed=1)
    obs = env.reset()
    assert isinstance(obs, dict)
    for _ in range(8):
        obs, rew, done, info = env.step({"type": "pass_priority"})
        assert "turn" in obs and isinstance(rew, float)
    env.close()


def test_gym_env_basic():
    env = KarnAIGymEnv(seed=2)
    obs, _ = env.reset()
    assert "turn" in obs
    obs, rew, term, trunc, info = env.step(1)
    assert isinstance(obs, dict)
    assert term is False and trunc is False
    assert "turn" in info
    s = env.render()
    assert isinstance(s, str)
    env.close()
