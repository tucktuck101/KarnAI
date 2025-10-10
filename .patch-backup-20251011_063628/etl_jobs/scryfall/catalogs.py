from __future__ annotations
from typing import Dict, List, Tuple
import requests
from etl.jobs.common.db import get_conn

ENDPOINTS: Dict[str, str] = {
    "artifact-types": "https://api.scryfall.com/catalog/artifact-types",
    "creature-types": "https://api.scryfall.com/catalog/creature-types",
    "enchantment-types": "https://api.scryfall.com/catalog/enchantment-types",
}

def fetch(name: str, url: str) -> List[Tuple[str, str]]:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    j = r.json()
    if j.get("object") != "catalog" or "data" not in j:
        raise RuntimeError(f"Unexpected catalog payload for {name}")
    return [(name, v) for v in j["data"]]

def load_all() -> int:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
IF OBJECT_ID('dbo.stg_catalog') IS NULL
  CREATE TABLE dbo.stg_catalog(
    catalog NVARCHAR(64) NOT NULL,
    value   NVARCHAR(200) NOT NULL
  );
"""
        )
        cur.execute("TRUNCATE TABLE dbo.stg_catalog;")
        rows: List[Tuple[str, str]] = []
        for name, url in ENDPOINTS.items():
            rows.extend(fetch(name, url))
        cur.fast_executemany = True
        cur.executemany(
            "INSERT INTO dbo.stg_catalog(catalog, value) VALUES (?, ?)",
            rows,
        )
        return len(rows)

if __name__ == "__main__":
    print(f"Inserted {load_all()} catalog rows.")