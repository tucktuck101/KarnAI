from __future__ import annotations

from typing import Any, Mapping, Protocol


class RulesEngine(Protocol):
    """Deterministic rules engine core."""

    def capabilities(self) -> dict[str, bool]: ...
    def reset(self, seed: int, config: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def step(self, action: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def snapshot(self) -> bytes: ...  # deterministic replay bytes
