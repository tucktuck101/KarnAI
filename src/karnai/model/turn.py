from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Phase(str, Enum):
    beginning = "beginning"
    precombat_main = "precombat_main"
    combat = "combat"
    postcombat_main = "postcombat_main"
    ending = "ending"


class Step(str, Enum):
    untap = "untap"
    upkeep = "upkeep"
    draw = "draw"
    main = "main"
    begin_combat = "begin_combat"
    declare_attackers = "declare_attackers"
    declare_blockers = "declare_blockers"
    combat_damage = "combat_damage"
    end_combat = "end_combat"
    end = "end"
    cleanup = "cleanup"


class Turn(BaseModel):
    number: int = 1
    phase: Phase = Phase.beginning
    step: Step = Step.untap
    active_player: int = 0
