from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field

_ZONE_PATTERN = r"^(library|hand|battlefield|graveyard|exile|stack|command|ante)$"


class Zone(BaseModel):
    name: str = Field(pattern=_ZONE_PATTERN)
    cards: List[str] = []
