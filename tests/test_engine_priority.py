from karnai.core.state import Game, Player
from karnai.engine.priority import PrioritySystem
from karnai.engine.turns import advance_turn


def test_priority_turns():
    g = Game(
        rng_seed=1,
        players=[Player(0, "A"), Player(1, "B"), Player(2, "C"), Player(3, "D")],
    )
    p = PrioritySystem()
    start = g.priority_player
    p.pass_priority(g)
    assert g.priority_player == (start + 1) % 4
    advance_turn(g)
    assert g.turn == 1
