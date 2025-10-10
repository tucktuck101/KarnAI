from __future__ import annotations
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field

Color = Literal["W", "U", "B", "R", "G"]


class Cost(BaseModel):
    mana: str = Field(default="")
    life: int = 0
    tap: bool = False
    additional: List[str] = Field(default_factory=list)


class Ability(BaseModel):
    kind: str
    text: str
    params: Dict[str, str] = Field(default_factory=dict)


class Face(BaseModel):
    name: str
    mana_cost: Optional[str] = None
    type_line: str
    oracle_text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None


class Card(BaseModel):
    id: str
    name: str
    faces: List[Face]
    type_line: str
    oracle_text: Optional[str] = None
    colors: List[Color] = Field(default_factory=list)
    color_identity: List[Color] = Field(default_factory=list)
    legal_commander: bool = False
    layout: str = "normal"
    scryfall_id: Optional[str] = None
