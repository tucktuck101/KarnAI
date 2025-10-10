from __future__ import annotations
import datetime
from typing import Optional
from .db import get_conn

def start_run(source_name: str, bulk_type: str, bulk_url: str, file_sha256_hex: str) -> None:
    sql = (
        "INSERT INTO dbo.audit_runs "
        "(source_name, bulk_type, bulk_url, file_sha256_hex, started_at_utc, status) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    source_name,
                    bulk_type,
                    bulk_url,
                    file_sha256_hex,
                    datetime.datetime.utcnow(),
                    "running",
                ),
            )

def finish_run(file_sha256_hex: str, status: str, message: Optional[str] = None) -> None:
    sql = (
        "UPDATE dbo.audit_runs SET finished_at_utc = ?, status = ?, message = ? "
        "WHERE file_sha256_hex = ?"
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (datetime.datetime.utcnow(), status, message, file_sha256_hex))