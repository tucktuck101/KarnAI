from __future__ import annotations
from typing import Dict, Any, Tuple
import gymnasium as gym
from gymnasium import spaces
from karnai.engine import RulesEngineImpl


class KarnAIGymEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(self, seed: int = 0, config: Dict[str, Any] | None = None):
        super().__init__()
        self.engine = RulesEngineImpl()
        self.seed_val = seed
        self.config = config or {}
        self.action_space = spaces.Discrete(2)  # 0 = noop, 1 = pass_priority
        self.observation_space = spaces.Dict(
            {
                "turn": spaces.Discrete(1000),
                "active_player": spaces.Discrete(4),
                "priority_player": spaces.Discrete(4),
            }
        )
        self.obs = None

    def reset(self, seed: int | None = None, options: Dict[str, Any] | None = None):
        s = seed if seed is not None else self.seed_val
        self.obs = self.engine.reset(seed=s, config=self.config)
        return self.obs, {}

    def step(
        self, action: int
    ) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        act = {"type": "pass_priority"} if action == 1 else {"type": "noop"}
        obs = self.engine.step(act)
        reward = 0.0
        terminated = False
        truncated = False
        info = {"turn": obs["turn"]}
        return obs, reward, terminated, truncated, info

    def render(self):
        if self.obs:
            turn = self.obs["turn"]
            ap = self.obs["active_player"]
            pp = self.obs["priority_player"]
            return f"Turn {turn} | Active: {ap} | Priority: {pp}"

    def close(self):
        pass
