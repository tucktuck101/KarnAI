from __future__ import annotations
from typing import Dict, Any
from .dsl import Effect, register


class _Noop(Effect):
    def execute(self, ctx) -> None:  # type: ignore[override]
        return None


@register("noop")
def _noop(args: Dict[str, Any]) -> Effect:
    return _Noop(op="noop", args=args)
