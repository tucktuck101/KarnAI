from __future__ import annotations

from typing import Any, Mapping, Protocol


class Policy(Protocol):
    """Agent policy interface."""

    def capabilities(self) -> dict[str, bool]: ...
    def act(self, observation: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def reset(self, seed: int | None = None) -> None: ...
