from __future__ import annotations

from typing import Any, Mapping


class ScriptedPassPolicy:
    """Always passes priority to exercise env path predictably."""

    def capabilities(self) -> dict[str, bool]:
        return {"stochastic": False}

    def act(self, observation: Mapping[str, Any]):
        return {"type": "pass_priority"}

    def reset(self, seed: int | None = None) -> None:
        return None
