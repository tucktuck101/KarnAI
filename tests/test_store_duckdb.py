from pathlib import Path

from karnai.store import DuckDBStore


def test_store_write_read(tmp_path: Path):
    db = tmp_path / "test.duckdb"
    store = DuckDBStore(db_path=db)
    run_id = store.new_run({"rng_seed": 123, "config": {"x": 1}})
    ep_id = store.new_episode(run_id, match_id="m1")

    # write 10 steps
    for i in range(10):
        store.log_step(ep_id, i, {"active_player": i % 4, "reward": 0.0, "done": False})

    store.end_episode(ep_id, outcome="p0_wins")
    steps = list(store.get_episode(ep_id))
    assert len(steps) == 10 and steps[0]["idx"] == 0

    art_id = store.put_artifact(run_id, "replay", "file://replay.bin", "deadbeef")
    assert art_id.startswith("art_")
