from karnai.core.state import Game, Player
from karnai.core.objects import create_object
from karnai.core.zones import move


def test_state_roundtrip():
    g = Game(
        rng_seed=42,
        players=[Player(0, "A"), Player(1, "B"), Player(2, "C"), Player(3, "D")],
    )
    oid = create_object(g, "Grizzly Bears", owner=0, controller=0, zone="HAND")  # type: ignore[arg-type]
    h1 = g.snapshot_hash()
    move(g, oid, "BATTLEFIELD")  # type: ignore[arg-type]
    h2 = g.snapshot_hash()
    assert h1 != h2
