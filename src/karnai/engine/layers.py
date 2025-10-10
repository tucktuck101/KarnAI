from __future__ import annotations
from typing import Dict, Any

LAYER_ORDER = [
    "copy",
    "control",
    "text",
    "type",
    "color",
    "abilities",
    "power_toughness",
]


def apply_layers(state_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(state_snapshot)
    for _ in LAYER_ORDER:
        pass
    return out
