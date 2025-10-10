from pathlib import Path
from karnai.replay import ReplayLogger
from karnai.env import KarnAIGymEnv
from karnai.metrics import summarize_replays, render_dashboard


def _make_replay(path: Path, seed: int):
    env = KarnAIGymEnv(seed=seed)
    obs, _ = env.reset()
    rl = ReplayLogger.create(path, seed=seed, config={})
    for i in range(3):
        obs, *_ = env.step(1)
        rl.append_step(i, {"type": "pass_priority"}, obs)
    sha = rl.close_with_footer(env.engine)
    env.close()
    return sha


def test_summary_and_dashboard(tmp_path: Path):
    p1 = tmp_path / "a.replay.jsonl"
    p2 = tmp_path / "b.replay.jsonl"
    _make_replay(p1, seed=5)
    _make_replay(p2, seed=5)
    summary = summarize_replays([p1, p2])
    txt = render_dashboard(summary)
    assert summary["replays"] == 2
    assert summary["determinism_rate"] in (0.0, 1.0)
    assert "KarnAI Metrics Dashboard" in txt
