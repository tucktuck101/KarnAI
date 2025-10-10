# etl_load.py
# Load staged Scryfall data into SQL Server using etl/config.yml mappings.
# Supports: flat rows, array_from, object_from, derive_type_line specials, and face_image_uris special.

import argparse
from pathlib import Path
import yaml, pyodbc
from typing import Any, Dict, List, Union

JsonPath = str

# -------- YAML helpers --------
def load_cfg(cfg_path: Path) -> dict:
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

def conn_str_from_args(args, cfg_sql: dict) -> str:
    server   = args.server   or cfg_sql.get("server")   or ""
    database = args.database or cfg_sql.get("database") or ""
    auth     = "trusted" if args.trusted else (cfg_sql.get("auth","trusted").lower())
    if auth == "trusted":
        return (
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server={server};Database={database};Trusted_Connection=yes;"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )
    user = args.username or cfg_sql.get("username") or ""
    pwd  = args.password or cfg_sql.get("password") or ""
    return (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={server};Database={database};UID={user};PWD={pwd};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )

# -------- SQL builders --------
def cast_expr(base_sql: str, cast: str|None) -> str:
    if not cast: return base_sql
    if cast == "date":  return f"TRY_CONVERT(date, {base_sql})"
    if cast == "int":   return f"TRY_CONVERT(int, {base_sql})"
    if cast == "bit":   return f"TRY_CONVERT(bit, {base_sql})"
    if cast == "float": return f"TRY_CONVERT(float, {base_sql})"
    return base_sql

def json_value_from(source: str, path: JsonPath) -> str:
    # source is table alias: 'raw' for parent, or a JSON column like kv.value, arr.value
    if source == "raw":
        return f"JSON_VALUE(raw, '{path}')"
    # nested JSON column
    return f"JSON_VALUE({source}, '{path}')"

def build_select_flat(load: dict, stage_table: str) -> str:
    cols = []
    for c in load["columns"]:
        expr = json_value_from("raw", c["json"])
        expr = cast_expr(expr, c.get("cast"))
        cols.append(f"{expr} AS {c['col']}")
    return f"SELECT {', '.join(cols)} FROM {stage_table} WHERE ISJSON(raw)=1"

def build_select_array(load: dict, stage_table: str) -> str:
    arr = load["array_from"]
    select_cols = []
    # We CROSS APPLY OPENJSON to get [key], value
    from_clause = f"{stage_table} CROSS APPLY OPENJSON(JSON_QUERY(raw, '{arr}')) AS arr"
    for c in load["columns"]:
        jp = c["json"]
        if c.get("from_parent"):
            expr = json_value_from("raw", jp)
        elif jp == "$.__value__":
            expr = "arr.value"
        elif jp == "$.__index__":
            expr = "TRY_CONVERT(int, arr.[key])"
        elif jp.startswith("$.__value__."):
            # nested field from array element object
            expr = json_value_from("arr.value", "$." + jp.split(".",1)[1])
        else:
            # allow direct JSON_VALUE on parent if needed
            expr = json_value_from("raw", jp)
        expr = cast_expr(expr, c.get("cast"))
        select_cols.append(f"{expr} AS {c['col']}")
    return f"SELECT {', '.join(select_cols)} FROM {from_clause} WHERE ISJSON(raw)=1"

def build_select_object(load: dict, stage_table: str) -> str:
    obj = load["object_from"]
    from_clause = f"{stage_table} CROSS APPLY OPENJSON(JSON_QUERY(raw, '{obj}')) AS kv"
    select_cols = []
    for c in load["columns"]:
        jp = c["json"]
        if c.get("from_parent"):
            expr = json_value_from("raw", jp)
        elif jp == "$.__key__":
            expr = "kv.[key]"
        elif jp == "$.__value__":
            expr = "kv.value"
        elif jp.startswith("$.__value__."):
            expr = json_value_from("kv.value", "$." + jp.split(".",1)[1])
        else:
            expr = json_value_from("raw", jp)
        expr = cast_expr(expr, c.get("cast"))
        select_cols.append(f"{expr} AS {c['col']}")
    return f"SELECT {', '.join(select_cols)} FROM {from_clause} WHERE ISJSON(raw)=1"

def build_select_derive_typeline(which: str, stage_table: str) -> str:
    # Split `type_line` into super / types / sub using em dash or hyphen fallback.
    # PARSENAME trick expects dot; replace separators with '-'.
    base_cte = f"""
WITH base AS (
  SELECT JSON_VALUE(raw,'$.id') AS card_id,
         JSON_VALUE(raw,'$.type_line') AS type_line
  FROM {stage_table}
  WHERE ISJSON(raw)=1
), norm AS (
  SELECT card_id, REPLACE(type_line, '—', '-') AS tl
  FROM base
)
"""
    if which == "types":
        # center part (3rd from right) approximated by taking the "type" chunk
        return base_cte + """
SELECT card_id, value AS card_type
FROM (
  SELECT card_id,
         ISNULL(PARSENAME(REPLACE(REPLACE(tl,' — ','-'),' ',' . '),3),'') AS type_chunk
  FROM norm
) t
CROSS APPLY OPENJSON(CONCAT('["', REPLACE(type_chunk,' . ','","'), '"]'))
WHERE value <> ''
"""
    if which == "subtypes":
        return base_cte + """
SELECT card_id, value AS subtype
FROM (
  SELECT card_id,
         ISNULL(PARSENAME(REPLACE(REPLACE(tl,' — ','-'),' ',' . '),2),'') AS sub_chunk
  FROM norm
) t
CROSS APPLY OPENJSON(CONCAT('["', REPLACE(sub_chunk,' . ','","'), '"]'))
WHERE value <> ''
"""
    if which == "supertypes":
        return base_cte + """
SELECT card_id, value AS supertype
FROM (
  SELECT card_id,
         ISNULL(PARSENAME(REPLACE(REPLACE(tl,' — ','-'),' ',' . '),4),'') AS super_chunk
  FROM norm
) t
CROSS APPLY OPENJSON(CONCAT('["', REPLACE(super_chunk,' . ','","'), '"]'))
WHERE value <> ''
"""
    raise ValueError("unknown derive_type_line")

def build_select(load: dict, stage_table: str) -> str:
    if "array_from" in load:   return build_select_array(load, stage_table)
    if "object_from" in load:  return build_select_object(load, stage_table)
    if "derive_type_line" in load:
        return build_select_derive_typeline(load["derive_type_line"], stage_table)
    # flat
    return build_select_flat(load, stage_table)

def normalize_keys(key: Union[str, List[str]]) -> List[str]:
    return key if isinstance(key, list) else [key]

def build_merge(load: dict, stage_table: str) -> str:
    tgt = load["target"]
    key_cols = normalize_keys(load["key"])
    sel_sql = build_select(load, stage_table)

    # Determine columns produced by SELECT.
    if "columns" in load and load["columns"]:
        select_cols = [c["col"] for c in load["columns"]]
    else:
        # derive_type_line emits known names for each case
        if load.get("derive_type_line") == "types":
            select_cols = ["card_id","card_type"]
        elif load.get("derive_type_line") == "subtypes":
            select_cols = ["card_id","subtype"]
        elif load.get("derive_type_line") == "supertypes":
            select_cols = ["card_id","supertype"]
        else:
            select_cols = key_cols[:]  # fallback

    # INSERT set
    ins_names = ", ".join(select_cols)
    ins_vals  = ", ".join([f"s.{c}" for c in select_cols])

    # UPDATE set only for non-key columns if present
    non_keys = [c for c in select_cols if c not in key_cols]
    set_clause = ", ".join([f"t.{c} = s.{c}" for c in non_keys])

    on_clause = " AND ".join([f"t.{k} = s.{k}" for k in key_cols])

    return f"""
MERGE {tgt} AS t
USING (
{sel_sql}
) AS s
ON {on_clause}
WHEN NOT MATCHED BY TARGET THEN
  INSERT ({ins_names}) VALUES ({ins_vals})
{"WHEN MATCHED THEN UPDATE SET " + set_clause if set_clause else ""}
;"""

# Special post-step: per-face image URIs that require joining card_face
FACE_IMAGE_SQL = """
;WITH faces AS (
  SELECT
    JSON_VALUE(raw,'$.id') AS card_id,
    f.[key]                AS face_index,
    f.value                AS face_json
  FROM stg.stg_default_cards
  CROSS APPLY OPENJSON(JSON_QUERY(raw,'$.card_faces')) AS f
),
uris AS (
  SELECT
    CAST(f.face_index AS int) AS face_index,
    f.card_id,
    kv.[key]  AS uri_kind,
    kv.value  AS uri
  FROM faces f
  CROSS APPLY OPENJSON(JSON_QUERY(f.face_json,'$.image_uris')) AS kv
)
MERGE dbo.face_image_uri AS t
USING (
  SELECT cf.face_id, u.uri_kind, u.uri
  FROM uris u
  JOIN dbo.card_face cf
    ON cf.card_id = u.card_id AND cf.face_index = u.face_index
) AS s
ON t.face_id = s.face_id AND t.uri_kind = s.uri_kind
WHEN NOT MATCHED BY TARGET THEN
  INSERT (face_id, uri_kind, uri) VALUES (s.face_id, s.uri_kind, s.uri)
WHEN MATCHED AND ISNULL(t.uri,'') <> ISNULL(s.uri,'') THEN
  UPDATE SET t.uri = s.uri
;"""

def exec_sql(cur, sql: str):
    for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
        cur.execute(stmt + ";")

# -------- load driver --------
def run_load(conn, cfg: dict, only_types: List[str]|None = None):
    bulks = cfg.get("bulks", [])
    # Turn list into dict type -> block (handles multiple entries like default_cards + rulings)
    per_type = {}
    for b in bulks:
        t = b.get("type")
        if not t: continue
        per_type.setdefault(t, []).append(b)

    target_types = list(per_type.keys()) if not only_types else only_types
    cur = conn.cursor()

    # Ensure stg schema exists (loader reads FROM stg.*)
    cur.execute("IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='stg') EXEC('CREATE SCHEMA stg');")
    conn.commit()

    for t in target_types:
        blocks = per_type.get(t, [])
        if not blocks: continue
        # stage table per block
        for blk in blocks:
            stage_table = blk.get("stage_table")
            if not stage_table:
                raise SystemExit(f"Missing stage_table for bulk type {t}")

            loads = blk.get("loads", [])

            # Execute in YAML order: parents first
            for load in loads:
                if load.get("special") == "face_image_uris":
                    # run after card_face exists
                    print(f"[load] special face_image_uris -> dbo.face_image_uri")
                    exec_sql(cur, FACE_IMAGE_SQL)
                    conn.commit()
                    continue

                sql = build_merge(load, stage_table)
                print(f"[load] {load['name']} -> {load['target']}")
                cur.execute(sql)
                conn.commit()

# -------- CLI --------
def main():
    ap = argparse.ArgumentParser(description="Load staged Scryfall data into SQL Server from YAML config.")
    ap.add_argument("--config", default="etl/config.yml")
    ap.add_argument("--types", nargs="*", help="Bulk types to load (e.g. default_cards rulings). Default: all in config.")
    # connection overrides
    ap.add_argument("--server")
    ap.add_argument("--database")
    ap.add_argument("--trusted", action="store_true")
    ap.add_argument("--username")
    ap.add_argument("--password")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        raise SystemExit(f"config not found: {cfg_path}")
    cfg = load_cfg(cfg_path)

    conn_str = conn_str_from_args(args, cfg.get("sql", {}))
    with pyodbc.connect(conn_str, autocommit=False) as conn:
        run_load(conn, cfg, args.types)
    print("[done] load complete")

if __name__ == "__main__":
    main()
