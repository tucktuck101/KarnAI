from __future__ import annotations
from karnai.core.state import Game

PHASES = ["BEGIN", "PRECOMBAT_MAIN", "COMBAT", "POSTCOMBAT_MAIN", "END"]


def advance_turn(game: Game) -> None:
    game.turn += 1
    game.priority_player = game.turn % len(game.players)
