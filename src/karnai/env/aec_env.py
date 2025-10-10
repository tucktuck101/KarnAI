from __future__ import annotations

from typing import Any, Dict

from karnai.engine import RulesEngineImpl


class KarnAIAECEnv:
    """Minimal multi-agent PettingZoo-style AEC environment."""

    metadata = {"name": "KarnAI-AEC", "players": 4}

    def __init__(self, seed: int = 0, config: Dict[str, Any] | None = None):
        self.engine = RulesEngineImpl()
        self.seed = seed
        self.config = config or {}
        self.obs = None
        self.agents = [f"player_{i}" for i in range(4)]
        self.agent_iter = iter(self.agents)
        self.active_agent = next(self.agent_iter)
        self.done_flags = {a: False for a in self.agents}

    def reset(self, seed: int | None = None, options: Dict[str, Any] | None = None):
        s = seed if seed is not None else self.seed
        self.obs = self.engine.reset(seed=s, config=self.config)
        self.agent_iter = iter(self.agents)
        self.active_agent = next(self.agent_iter)
        self.done_flags = {a: False for a in self.agents}
        return self.obs

    def observe(self, agent: str) -> Dict[str, Any]:
        return dict(self.obs)

    def step(self, action: Dict[str, Any] | None = None):
        if self.done_flags[self.active_agent]:
            return self.obs, 0.0, True, {}
        self.obs = self.engine.step(action or {"type": "pass_priority"})
        rew = 0.0
        done = False
        info = {"turn": self.obs["turn"]}
        try:
            self.active_agent = next(self.agent_iter)
        except StopIteration:
            self.agent_iter = iter(self.agents)
            self.active_agent = next(self.agent_iter)
        return self.obs, rew, done, info

    def close(self):
        pass
