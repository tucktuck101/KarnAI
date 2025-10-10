from __future__ import annotations

import re

from .ir import AbilityIR, AbilityOp

# Simple patterns for demonstration
TAP_ADD_MANA_RE = re.compile(r"^\{T\}:\s*Add\s*\{([WUBRGCS])\}\.?$", re.IGNORECASE)
COUNTER_SPELL_RE = re.compile(r"^Counter target spell\.?$", re.IGNORECASE)


def parse_oracle_text(text: str) -> AbilityIR | None:
    t = text.strip()

    m = TAP_ADD_MANA_RE.match(t)
    if m:
        color = m.group(1).upper()
        return AbilityIR(
            text=text,
            cost={"tap_self": True},
            ops=[AbilityOp(op="add_mana", params={"color": color, "amount": 1})],
        )

    if COUNTER_SPELL_RE.match(t):
        return AbilityIR(
            text=text,
            cost=None,
            ops=[AbilityOp(op="counter_target", params={"target": "spell"})],
        )

    # Unknown for now
    return None
