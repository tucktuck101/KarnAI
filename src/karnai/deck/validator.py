from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, List, Dict, Set
from karnai.schemas import Decklist

BASIC_LANDS: Set[str] = {
    "Plains",
    "Island",
    "Swamp",
    "Mountain",
    "Forest",
    "Wastes",
    "Snow-Covered Plains",
    "Snow-Covered Island",
    "Snow-Covered Swamp",
    "Snow-Covered Mountain",
    "Snow-Covered Forest",
}

DEFAULT_BANNED: Set[str] = {
    "Shahrazad",
    "Sundering Titan",
    "Tinker",
    "Hullbreacher",
    "Paradox Engine",
    "Golos, Tireless Pilgrim",
    "Iona, Shield of Emeria",
    "Primeval Titan",
}


@dataclass
class DeckValidationResult:
    is_valid: bool
    issues: List[str]


class DeckValidationError(Exception):
    pass


# returns color identity symbols like ["G","U"]
CardColorLookup = Callable[[str], Iterable[str]]


class DeckValidator:
    def __init__(self, banned: Iterable[str] | None = None):
        self.banned = set(banned) if banned is not None else set(DEFAULT_BANNED)

    def validate(
        self,
        deck: Decklist,
        color_lookup: CardColorLookup,
    ) -> DeckValidationResult:
        issues: List[str] = []

        commander_ci = set([c.upper() for c in color_lookup(deck.commander)])
        if deck.partner:
            commander_ci |= set([c.upper() for c in color_lookup(deck.partner)])

        total_cards = 1 + (1 if deck.partner else 0) + len(deck.cards)
        if total_cards != 100:
            issues.append(
                (
                    "Deck must contain exactly 100 cards including commander(s). "
                    f"Found {total_cards}."
                )
            )

        counts: Dict[str, int] = {}
        for name in deck.cards:
            counts[name] = counts.get(name, 0) + 1
        dupes = [n for n, c in counts.items() if c > 1 and n not in BASIC_LANDS]
        if dupes:
            issues.append("Non-singleton cards found: " + ", ".join(sorted(dupes)))

        all_names = (
            [deck.commander]
            + ([deck.partner] if deck.partner else [])
            + list(deck.cards)
        )
        banned_hits = [n for n in all_names if n in self.banned]
        if banned_hits:
            issues.append(
                "Banned cards present: " + ", ".join(sorted(set(banned_hits)))
            )

        for name in all_names:
            ci = set([c.upper() for c in color_lookup(name)])
            if not ci.issubset(commander_ci):
                lhs = f"{name} has {sorted(ci)}"
                rhs = f"not subset of commander {sorted(commander_ci)}"
                issues.append("Color identity violation: " + lhs + " " + rhs)
        return DeckValidationResult(is_valid=(len(issues) == 0), issues=issues)
