from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel


class CardInstance(BaseModel):
    uid: str  # unique per instance
    card_id: str  # scryfall id or canonical id
    owner: int  # player id
    controller: int  # player id
    zone: str  # 'library','hand','battlefield','graveyard','exile','command','stack'
    tapped: bool = False
    summoning_sick: bool = False
    counters: Dict[str, int] = {}

    def move_to(self, zone: str, controller: Optional[int] = None) -> None:
        self.zone = zone
        if controller is not None:
            self.controller = controller
