from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal, Tuple, cast

ZoneName = Literal[
    "LIBRARY", "HAND", "BATTLEFIELD", "GRAVEYARD", "EXILE", "STACK", "COMMAND", "ANTE"
]
ZONES: Tuple[ZoneName, ...] = cast(
    Tuple[ZoneName, ...],
    (
        "LIBRARY",
        "HAND",
        "BATTLEFIELD",
        "GRAVEYARD",
        "EXILE",
        "STACK",
        "COMMAND",
        "ANTE",
    ),
)


@dataclass
class ObjectRef:
    oid: int


@dataclass
class Player:
    pid: int
    name: str
    life: int = 40
    commander_ref: Optional[ObjectRef] = None
    commander_tax: int = 0
    monarch: bool = False
    initiative: bool = False


@dataclass
class CardObject:
    oid: int
    name: str
    owner: int
    controller: int
    zone: ZoneName
    counters: Dict[str, int] = field(default_factory=dict)
    summoning_sick: bool = False


@dataclass
class Game:
    rng_seed: int
    players: List[Player]
    objects: Dict[int, CardObject] = field(default_factory=dict)
    zones: Dict[ZoneName, List[int]] = field(
        default_factory=lambda: {z: [] for z in ZONES}
    )
    turn: int = 0
    priority_player: int = 0

    def snapshot_hash(self) -> str:
        from hashlib import sha256

        keys = sorted(self.objects.keys())
        zone_sig = {z: tuple(self.zones[z]) for z in sorted(self.zones.keys())}
        payload = (
            f"{self.rng_seed}|{self.turn}|{self.priority_player}|{keys}|{zone_sig}"
        )
        return sha256(payload.encode()).hexdigest()
