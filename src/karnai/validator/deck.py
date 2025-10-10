from __future__ import annotations
from typing import List
from karnai.models.card import Card

BANNED: List[str] = []


def validate_commander_deck(cards: List[Card]) -> List[str]:
    errs: List[str] = []
    names = [c.name for c in cards]
    if len(names) != len(set(names)):
        errs.append("singleton violation")
    for c in cards:
        if c.name in BANNED:
            errs.append(f"banned: {c.name}")
    return errs
