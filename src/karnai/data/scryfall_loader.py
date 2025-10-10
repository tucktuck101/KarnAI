from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pyarrow as pa
import pyarrow.parquet as pq

from karnai.schemas import Card, OracleFace


class OracleLoaderFile:
    """
    Loads normalized Scryfall Oracle data from a local JSON file.
    The file can be a JSON array or JSON Lines (one card per line).
    Optional Parquet caching for faster reloads.
    """

    def __init__(self, path: str | Path, cache_dir: str | Path | None = None):
        self.path = Path(path)
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def capabilities(self) -> dict[str, bool]:
        return {"parquet_cache": self.cache_dir is not None}

    def load_cards(self) -> Iterable[Dict[str, Any]]:
        cached = self._maybe_read_cache()
        if cached is not None:
            for row in cached:
                yield row
            return

        rows: List[Dict[str, Any]] = []
        for raw in self._iter_json(self.path):
            norm = self._normalize_card(raw)
            if norm is not None:
                rows.append(norm)

        if self.cache_dir:
            self._write_cache(rows)

        for r in rows:
            yield r

    def _iter_json(self, path: Path):
        txt = path.read_text(encoding="utf-8").strip()
        if txt.startswith("["):
            data = json.loads(txt)
            for item in data:
                yield item
        else:
            for line in txt.splitlines():
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)

    def _normalize_card(self, raw: Dict[str, Any]) -> Dict[str, Any] | None:
        name = raw.get("name")
        if not name:
            return None

        mana_value = float(raw.get("cmc", 0.0))
        colors = raw.get("colors", []) or []
        color_identity = raw.get("color_identity", []) or []
        type_line = raw.get("type_line", "") or ""
        types = type_line.split("—")[0].strip().split() if type_line else []
        subtypes = None
        if "—" in type_line:
            subtypes = [t.strip() for t in type_line.split("—", 1)[1].split()]

        faces = None
        if raw.get("card_faces"):
            faces = []
            for face in raw["card_faces"]:
                f_type = face.get("type_line", "") or ""
                faces.append(
                    OracleFace(
                        name=face.get("name", name),
                        oracle_text=face.get("oracle_text", "") or "",
                        mana_cost=face.get("mana_cost"),
                        power=face.get("power"),
                        toughness=face.get("toughness"),
                        loyalty=face.get("loyalty"),
                        types=f_type.split("—")[0].strip().split() if f_type else None,
                        subtypes=[t.strip() for t in f_type.split("—", 1)[1].split()]
                        if ("—" in f_type)
                        else None,
                    ).model_dump()
                )
        oracle_text = raw.get("oracle_text", "") or ""

        card = Card(
            id=str(raw.get("id", name)),
            name=name,
            mana_cost=raw.get("mana_cost"),
            mana_value=mana_value,
            colors=colors,
            color_identity=color_identity,
            types=types or [],
            subtypes=subtypes,
            oracle_text=oracle_text,
            faces=faces,
        ).model_dump()

        return card

    def _cache_path(self) -> Path | None:
        if not self.cache_dir:
            return None
        return self.cache_dir / "oracle_cards.parquet"

    def _maybe_read_cache(self):
        cp = self._cache_path()
        if not cp or not cp.exists():
            return None
        table = pq.read_table(cp)
        return table.to_pylist()

    def _write_cache(self, rows: list[dict[str, Any]]) -> None:
        cp = self._cache_path()
        if not cp:
            return
        table = pa.Table.from_pylist(rows)
        pq.write_table(table, cp)
