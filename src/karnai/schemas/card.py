from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class OracleFace(BaseModel):
    name: str
    oracle_text: str
    mana_cost: Optional[str] = None
    power: Optional[Union[str, int]] = None
    toughness: Optional[Union[str, int]] = None
    loyalty: Optional[Union[str, int]] = None
    types: Optional[List[str]] = None
    subtypes: Optional[List[str]] = None


class Ability(BaseModel):
    id: str
    kind: str = Field(pattern=r"^(activated|triggered|static|keyword)$")
    text: str
    cost: Optional[str] = None
    effect_ir: Optional[Dict[str, Any]] = None


class Card(BaseModel):
    id: str
    name: str
    mana_cost: Optional[str] = None
    mana_value: float
    colors: List[str]
    color_identity: Optional[List[str]] = None
    types: List[str]
    subtypes: Optional[List[str]] = None
    supertypes: Optional[List[str]] = None
    oracle_text: str
    faces: Optional[List[OracleFace]] = None
