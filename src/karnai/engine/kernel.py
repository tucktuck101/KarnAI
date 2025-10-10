from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Dict, List
import json
import hashlib
import random

from karnai.contracts import RulesEngine
from .events import EventBus


@dataclass
class EngineState:
    seed: int
    turn: int
    active_player: int
    priority_player: int
    log: List[Dict[str, Any]]


class RulesEngineImpl(RulesEngine):
    def __init__(self) -> None:
        self.bus = EventBus()
        self._rng = random.Random()
        self._state: EngineState | None = None

    def capabilities(self) -> dict[str, bool]:
        return {"replay_bytes": True, "deterministic_step": True}

    def reset(self, seed: int, config: Mapping[str, Any]) -> Mapping[str, Any]:
        self._rng.seed(seed)
        self._state = EngineState(
            seed=seed,
            turn=1,
            active_player=0,
            priority_player=0,
            log=[{"event": "reset", "seed": seed}],
        )
        self.bus.emit("reset", {"seed": seed})
        return self._obs()

    def step(self, action: Mapping[str, Any]) -> Mapping[str, Any]:
        assert self._state is not None, "Engine not reset"
        a_type = str(action.get("type", "pass_priority"))
        st = self._state

        if a_type == "pass_priority":
            st.log.append({"event": "pass_priority", "player": st.priority_player})
            st.priority_player = (st.priority_player + 1) % 4
            if st.priority_player == st.active_player:
                st.turn += 1
                st.active_player = (st.active_player + 1) % 4
                st.priority_player = st.active_player
                st.log.append(
                    {
                        "event": "advance_turn",
                        "turn": st.turn,
                        "active": st.active_player,
                    }
                )
        else:
            st.log.append({"event": "noop", "detail": a_type})

        self.bus.emit("step", {"action": a_type, "turn": st.turn})
        return self._obs()

    def snapshot(self) -> bytes:
        assert self._state is not None, "Engine not reset"
        payload = {
            "seed": self._state.seed,
            "turn": self._state.turn,
            "active_player": self._state.active_player,
            "priority_player": self._state.priority_player,
            "log": self._state.log,
        }
        data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
        h = hashlib.sha256(data).hexdigest()
        return json.dumps({"sha256": h, "data": payload}, sort_keys=True).encode(
            "utf-8"
        )

    def _obs(self) -> Mapping[str, Any]:
        assert self._state is not None
        return {
            "turn": self._state.turn,
            "active_player": self._state.active_player,
            "priority_player": self._state.priority_player,
            "events": len(self._state.log),
        }
