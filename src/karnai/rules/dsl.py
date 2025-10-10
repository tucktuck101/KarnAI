import karnai.rules.registry as _autoload  # noqa: F401

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Callable, Protocol


class ExecCtx(Protocol):
    pass


@dataclass
class Effect:
    op: str
    args: Dict[str, Any]

    def execute(self, ctx: ExecCtx) -> None:
        raise NotImplementedError


_REGISTRY: Dict[str, Callable[[Dict[str, Any]], Effect]] = {}


def register(
    op: str,
) -> Callable[[Callable[[Dict[str, Any]], Effect]], Callable[[Dict[str, Any]], Effect]]:
    def deco(
        f: Callable[[Dict[str, Any]], Effect],
    ) -> Callable[[Dict[str, Any]], Effect]:
        _REGISTRY[op] = f
        return f

    return deco


def build_effect(spec: Dict[str, Any]) -> Effect:
    op = spec.get("op")
    if op not in _REGISTRY:
        raise KeyError(f"No handler for op={op}")
    return _REGISTRY[op](spec.get("args", {}))


