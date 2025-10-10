# Stage 4 — Domain Model

Goal: pure data objects that represent the MTG game world. These models are
framework-agnostic and safe to serialize. They will back the rules engine.

## Modules
- `player.py` — life, mana pool, identity
- `card_instance.py` — per-instance state (tapped, counters, controller)
- `zones.py` — per-player zones and shared zones
- `stack.py` — LIFO stack of spells/abilities
- `effects.py` — continuous effects metadata (layer, duration)
- `turn.py` — turn counter and phase/step enums
- `target.py` — generic target selectors

## Invariants (initial)
- Players start at 40 life in Commander by default.
- Stack is LIFO; `pop()` removes the last pushed item.
- Zone transfer updates the card instance `zone` field to match.
- Models are Pydantic v2 and round-trip via `model_dump_json`.
