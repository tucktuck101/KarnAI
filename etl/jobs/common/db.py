from __future__ annotations
import os
import pyodbc  # type: ignore[import-not-found]

def get_conn():
    user = os.getenv("SQLSERVER_USER")
    host = os.getenv("SQLSERVER_HOST", "localhost")
    db   = os.getenv("SQLSERVER_DB", "KarnAI")
    pwd  = os.getenv("SQLSERVER_PASSWORD")
    if not pwd:
        raise RuntimeError(
            "SQLSERVER_PASSWORD not set for SQL auth. Set it in the environment or use Windows auth."
        )
    cs = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host};DATABASE={db};UID={user};PWD={pwd};"
        "TrustServerCertificate=yes;Encrypt=yes;"
    )
    return pyodbc.connect(cs)