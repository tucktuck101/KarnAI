from __future__ import annotations
from dataclasses import dataclass
from karnai.core.state import Game


@dataclass
class PrioritySystem:
    def pass_priority(self, game: Game) -> None:
        game.priority_player = (game.priority_player + 1) % len(game.players)
