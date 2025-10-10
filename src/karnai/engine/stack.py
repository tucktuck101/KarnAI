from __future__ import annotations
from karnai.core.state import Game


def push(game: Game, oid: int) -> None:
    game.zones["STACK"].append(oid)


def resolve_top(game: Game) -> int:
    if not game.zones["STACK"]:
        raise RuntimeError("stack empty")
    return game.zones["STACK"].pop()
