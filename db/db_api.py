# db_api.py
from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Dict, Iterable, Optional, Tuple

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, registry

# ---------- connection ----------
# Adjust: server, database, driver
cnxn_url = URL.create(
    "mssql+pyodbc",
    query={
        "odbc_connect": (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=KarnAI;"
            "Trusted_Connection=Yes;"
            "TrustServerCertificate=Yes;"
            "Encrypt=Yes;"
        )
    },
)
engine = create_engine(cnxn_url, pool_pre_ping=True, future=True)

# ---------- automap ----------
mapper_registry = registry()
Base = mapper_registry.generate_base()

# reflect everything in dbo schema (fast and future-proof)
with engine.connect() as conn:
    Base.metadata.reflect(conn, schema="dbo")

# Build a name->mapped class lookup (e.g., "oracle_card" -> class)
TABLE: Dict[str, Any] = {
    tbl.name: type_ for type_ in Base.registry.mappers for tbl in type_.persist_selectable.metadata.tables.values()
}
# The dict above contains duplicates; rebuild cleanly:
TABLE = {name.split(".")[-1]: Base.registry._class_registry[name]  # type: ignore[attr-defined]
         for name in list(Base.registry._class_registry.keys())
         if isinstance(Base.registry._class_registry[name], type)}

# ---------- session helper ----------
@contextmanager
def session_scope() -> Iterable[Session]:
    sess = Session(engine, future=True)
    try:
        yield sess
        sess.commit()
    except Exception:
        sess.rollback()
        raise
    finally:
        sess.close()

# ---------- utilities ----------
def _pk_cols(model) -> Tuple[str, ...]:
    insp = inspect(model)
    return tuple(col.name for col in insp.primary_key)

def _ensure_model(table_name: str):
    try:
        return TABLE[table_name]
    except KeyError:
        raise KeyError(f"Unknown table: {table_name}. Available: {sorted(TABLE.keys())}")

def to_dict(obj) -> Dict[str, Any]:
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

# ---------- CRUD ----------
def create(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    Model = _ensure_model(table)
    with session_scope() as s:
        inst = Model(**data)
        s.add(inst)
        s.flush()  # populates identity/PKs
        return to_dict(inst)

def read_one(table: str, pk: Dict[str, Any]) -> Dict[str, Any]:
    Model = _ensure_model(table)
    with session_scope() as s:
        stmt = select(Model)
        for k, v in pk.items():
            stmt = stmt.where(getattr(Model, k) == v)
        try:
            obj = s.execute(stmt).scalar_one()
        except NoResultFound:
            raise KeyError(f"{table} not found for PK {pk}")
        return to_dict(obj)

def read_many(
    table: str,
    where: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = 100,
    offset: int = 0,
    order_by: Optional[Iterable[str]] = None,
) -> Iterable[Dict[str, Any]]:
    Model = _ensure_model(table)
    with session_scope() as s:
        stmt = select(Model)
        if where:
            for k, v in where.items():
                stmt = stmt.where(getattr(Model, k) == v)
        if order_by:
            stmt = stmt.order_by(*[getattr(Model, col) for col in order_by])
        if limit is not None:
            stmt = stmt.limit(limit).offset(offset)
        return [to_dict(r) for r in s.execute(stmt).scalars().all()]

def update(table: str, pk: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    Model = _ensure_model(table)
    with session_scope() as s:
        stmt = select(Model)
        for k, v in pk.items():
            stmt = stmt.where(getattr(Model, k) == v)
        try:
            obj = s.execute(stmt).scalar_one()
        except NoResultFound:
            raise KeyError(f"{table} not found for PK {pk}")
        for k, v in data.items():
            setattr(obj, k, v)
        s.flush()
        return to_dict(obj)

def delete(table: str, pk: Dict[str, Any]) -> None:
    Model = _ensure_model(table)
    with session_scope() as s:
        stmt = select(Model)
        for k, v in pk.items():
            stmt = stmt.where(getattr(Model, k) == v)
        try:
            obj = s.execute(stmt).scalar_one()
        except NoResultFound:
            raise KeyError(f"{table} not found for PK {pk}")
        s.delete(obj)

# ---------- helpers for PK building ----------
def pk_for(table: str, **kwargs) -> Dict[str, Any]:
    Model = _ensure_model(table)
    keys = _pk_cols(Model)
    missing = [k for k in keys if k not in kwargs]
    if missing:
        raise ValueError(f"Missing PK parts {missing} for {table}")
    return {k: kwargs[k] for k in keys}
