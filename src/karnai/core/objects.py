from __future__ import annotations
from .state import Game, CardObject, ZoneName


def create_object(
    game: Game, name: str, owner: int, controller: int, zone: ZoneName
) -> int:
    oid = 1 + (max(game.objects.keys()) if game.objects else 0)
    game.objects[oid] = CardObject(
        oid=oid, name=name, owner=owner, controller=controller, zone=zone
    )
    game.zones[zone].append(oid)
    return oid
