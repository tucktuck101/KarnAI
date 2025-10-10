from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List

Handler = Callable[[Dict[str, Any]], None]


class EventBus:
    """Simple synchronous pub/sub for engine events."""

    def __init__(self) -> None:
        self._subs: DefaultDict[str, List[Handler]] = defaultdict(list)

    def on(self, topic: str, handler: Handler) -> None:
        self._subs[topic].append(handler)

    def emit(self, topic: str, payload: Dict[str, Any]) -> None:
        for h in self._subs.get(topic, []):
            h(payload)
