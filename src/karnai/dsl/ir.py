from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AbilityOp(BaseModel):
    op: str
    params: Dict[str, Any] = {}


class AbilityIR(BaseModel):
    text: str
    cost: Optional[Dict[str, Any]] = None
    ops: List[AbilityOp] = []
