from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class Player(BaseModel):
    pid: int = Field(ge=0, le=3)
    name: str
    life: int = 40
    mana_pool: Dict[str, int] = {}
    commander_ids: List[str] = []  # card ids of commander/partners
    monarch: bool = False

    def add_mana(self, symbol: str, amount: int = 1) -> None:
        self.mana_pool[symbol] = self.mana_pool.get(symbol, 0) + amount

    def spend_mana(self, symbol: str, amount: int = 1) -> bool:
        if self.mana_pool.get(symbol, 0) >= amount:
            self.mana_pool[symbol] -= amount
            return True
        return False
