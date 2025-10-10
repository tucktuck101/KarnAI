from __future__ import annotations

from typing import Any, Mapping, Protocol


class Renderer(Protocol):
    """Text/CLI rendering interface."""

    def capabilities(self) -> dict[str, bool]: ...
    def render(self, state: Mapping[str, Any]) -> str: ...
