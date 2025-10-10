from __future__ import annotations

from typing import Any, Iterable, Mapping, Protocol


class Scheduler(Protocol):
    """Tournament and self-play scheduler."""

    def capabilities(self) -> dict[str, bool]: ...
    def schedule(self, config: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]: ...
