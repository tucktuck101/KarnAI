from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ContinuousEffect(BaseModel):
    layer: int = Field(ge=1, le=7)  # 613.x top-level layers 1..7
    text: str
    duration: str = "until_end_of_turn"  # or "permanent"
    params: Optional[Dict[str, Any]] = None
