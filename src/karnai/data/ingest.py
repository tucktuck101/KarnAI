from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Tuple, Dict, Any, List

from pydantic import BaseModel
from karnai.models.card import Card

DATA_DIR = Path(os.environ.get("KARNAI_DATA_DIR", "data/processed")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Provenance(BaseModel):
    source: str
    input_hash: str
    count: int


def _hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _mock_oracle() -> List[Dict[str, Any]]:
    return [
        {
            "id": "demo-0001",
            "name": "Grizzly Bears",
            "type_line": "Creature - Bear",
            "oracle_text": "",
            "colors": ["G"],
            "color_identity": ["G"],
            "legal_commander": True,
            "faces": [
                {
                    "name": "Grizzly Bears",
                    "type_line": "Creature - Bear",
                    "mana_cost": "{1}{G}",
                    "oracle_text": "-",
                    "power": "2",
                    "toughness": "2",
                }
            ],
        }
    ]


def normalize(raw: List[Dict[str, Any]]) -> Tuple[List[Card], Provenance]:
    cards = [Card(**r) for r in raw]
    payload = json.dumps(raw, sort_keys=True).encode("utf-8")
    prov = Provenance(
        source="mock:scryfall_oracle",
        input_hash=_hash_bytes(payload),
        count=len(cards),
    )
    return cards, prov


def persist(cards: List[Card], prov: Provenance) -> Dict[str, str]:
    cards_path = DATA_DIR / "cards.jsonl"
    with cards_path.open("w", encoding="utf-8") as f:
        for c in cards:
            f.write(c.model_dump_json() + "\n")
    prov_path = DATA_DIR / "provenance.json"
    prov_path.write_text(prov.model_dump_json(indent=2), encoding="utf-8")
    return {"cards": str(cards_path), "provenance": str(prov_path)}


def refresh() -> Dict[str, str]:
    raw = _mock_oracle()
    cards, prov = normalize(raw)
    return persist(cards, prov)
