from pathlib import Path

from karnai.env import KarnAIGymEnv
from karnai.replay import ReplayLogger, iter_replay, render_text


def test_replay_roundtrip(tmp_path: Path):
    env = KarnAIGymEnv(seed=9)
    obs, _ = env.reset()
    path = tmp_path / "ep.replay.jsonl"
    rl = ReplayLogger.create(path, seed=9, config={})
    for i in range(5):
        obs, rew, term, trunc, info = env.step(1)  # pass_priority
        rl.append_step(i, {"type": "pass_priority"}, obs)
    sha = rl.close_with_footer(env.engine)
    env.close()

    evts = list(iter_replay(path))
    assert evts[0]["type"] == "header"
    assert evts[-1]["type"] == "footer" and evts[-1]["sha256"] == sha
    txt = render_text(path, limit=3)
    assert "[HEADER]" in txt and "[STEP]" in txt
