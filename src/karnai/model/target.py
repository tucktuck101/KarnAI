from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


class Target(BaseModel):
    selector: Dict[
        str, Any
    ]  # e.g., {"zone":"battlefield","type":"creature","controller":"opponent"}
    chosen_uid: Optional[str] = None
