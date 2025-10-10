from __future__ import annotations
from .state import Game, ZoneName


def move(game: Game, oid: int, to: ZoneName) -> None:
    for _, lst in game.zones.items():
        if oid in lst:
            lst.remove(oid)
    game.zones[to].append(oid)
