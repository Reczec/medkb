"""Database engine and session handling (SQLite and PostgreSQL from one code base)."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from sqlalchemy import Engine, create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def normalize_url(url: str) -> str:
    """Accept common PostgreSQL URL spellings and map them to the psycopg 3 driver."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix) :]
    return url


def _json_serializer(value: Any) -> str:
    # Keep umlauts readable in the stored JSON so that text search on keywords works.
    return json.dumps(value, ensure_ascii=False)


def make_engine(url: str) -> Engine:
    url = normalize_url(url)
    kwargs: dict[str, Any] = {"json_serializer": _json_serializer}
    is_sqlite = url.startswith("sqlite")

    if is_sqlite:
        kwargs["connect_args"] = {"check_same_thread": False}
        if url in {"sqlite://", "sqlite:///:memory:"}:
            kwargs["poolclass"] = StaticPool  # one shared in-memory database
    else:
        # Serverless Postgres (Neon) suspends after a few idle minutes and drops pooled
        # connections: test each one before use and replace connections older than 4 minutes.
        kwargs["pool_pre_ping"] = True
        kwargs["pool_recycle"] = 240

    engine = create_engine(url, **kwargs)

    if is_sqlite:

        @event.listens_for(engine, "connect")
        def _unicode_lower(dbapi_connection: Any, _record: Any) -> None:
            # SQLite's built-in lower() only handles ASCII, so "Übelkeit" would not match
            # "übelkeit". Replace it with Python's Unicode-aware version.
            dbapi_connection.create_function(
                "lower", 1, lambda v: v.lower() if isinstance(v, str) else v, deterministic=True
            )

    return engine


engine = make_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Columns added after the first release: (table, column, SQL type). create_all() only creates
# missing tables, so existing databases get these via ALTER TABLE. A real deployment would use
# Alembic; this keeps the prototype's existing SQLite/PostgreSQL databases working.
ADDED_COLUMNS = [
    ("audit_log", "actor", "VARCHAR(50)"),
    ("documents", "term_en", "VARCHAR(200)"),
    ("documents", "icd11_code", "VARCHAR(20)"),
    ("documents", "medications", "JSON DEFAULT '[]'"),
    ("documents", "sections", "JSON"),
    ("documents", "further_reading", "JSON DEFAULT '[]'"),
    ("documents", "ai_generated", "BOOLEAN DEFAULT FALSE"),
    ("documents", "title_en", "VARCHAR(200)"),
    ("documents", "content_en", "TEXT"),
    ("documents", "sections_en", "JSON"),
    ("documents", "keywords_en", "JSON DEFAULT '[]'"),
]


def upgrade_schema(target: Engine) -> None:
    inspector = inspect(target)
    with target.begin() as conn:
        for table, column, sql_type in ADDED_COLUMNS:
            if not inspector.has_table(table):
                continue
            if column not in {c["name"] for c in inspector.get_columns(table)}:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {sql_type}"))
