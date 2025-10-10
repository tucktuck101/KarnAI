# Stage 7 — Deck Intake & Legality (Commander)

Checks implemented:
- 100 cards total including commander(s).
- Singleton: max 1 copy of any non-basic card.
- Color identity: every card's color identity ⊆ commander's color identity (or union for partners).
- Banlist check.

Basic lands allowed in any quantity:
Plains, Island, Swamp, Mountain, Forest, Wastes, Snow-Covered variants.

Inputs:
- `Decklist` (from schemas).
- `color_lookup(name_or_id) -> list[str]`: returns color identity for a card.

Output:
- `DeckValidationResult`: `is_valid`, `issues` list.
