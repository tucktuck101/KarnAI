from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel


class StackItem(BaseModel):
    source_uid: str
    controller: int
    text: str
    targets: List[Dict[str, Any]] = []  # generic selectors


class Stack(BaseModel):
    items: List[StackItem] = []

    def push(self, item: StackItem) -> None:
        self.items.append(item)

    def pop(self) -> StackItem:
        return self.items.pop()

    def __len__(self) -> int:
        return len(self.items)
