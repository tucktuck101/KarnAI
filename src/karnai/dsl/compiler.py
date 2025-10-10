from __future__ import annotations

from typing import Any, Callable, Dict

from .ir import AbilityIR


def compile_ir_to_callable(ir: AbilityIR) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Return a stub effect callable that records intended operation.
    This is a placeholder to integrate with the engine later.
    """

    def effect(context: Dict[str, Any]) -> Dict[str, Any]:
        # Echo IR for now; engine will interpret ops later.
        return {
            "applied": True,
            "cost": ir.cost,
            "ops": [op.model_dump() for op in ir.ops],
            "context_keys": sorted(context.keys()),
        }

    return effect
