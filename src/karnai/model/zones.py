from __future__ import annotations
from typing import Dict, List
from pydantic import BaseModel, Field


def _four_dict() -> Dict[int, List[str]]:
    return {i: [] for i in range(4)}


class Zones(BaseModel):
    library: Dict[int, List[str]] = Field(default_factory=_four_dict)
    hand: Dict[int, List[str]] = Field(default_factory=_four_dict)
    battlefield: Dict[int, List[str]] = Field(default_factory=_four_dict)
    graveyard: Dict[int, List[str]] = Field(default_factory=_four_dict)
    exile: Dict[int, List[str]] = Field(default_factory=_four_dict)
    command: Dict[int, List[str]] = Field(default_factory=_four_dict)
    stack: List[str] = Field(default_factory=list)

    def transfer(
        self,
        uid: str,
        src: Dict[int, List[str]],
        dst: Dict[int, List[str]],
        pid: int,
    ) -> bool:
        if uid in src.get(pid, []):
            src[pid].remove(uid)
            dst[pid].append(uid)
            return True
        return False
