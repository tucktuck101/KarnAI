from karnai.schemas import GameState


def test_minimal_gamestate_shape():
    gs = GameState(
        players=["p0", "p1", "p2", "p3"],
        active_player=0,
        turn=1,
        phase="beginning",
        rng_seed=42,
    )
    assert gs.turn == 1 and gs.active_player == 0
