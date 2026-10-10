"""24 h cache for external sources, keyed by source and query (not by document id)."""

from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from typing import Any

from pydantic_core import to_jsonable_python
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import Settings
from app.models import SourceCache, utcnow
from app.schemas import SourceResult, as_utc


class SourceUnavailable(Exception):
    """The source did not answer usably (timeout, HTTP error, unexpected format)."""


def is_empty(payload: Any) -> bool:
    return payload is None or payload == [] or payload == {}


def store(db: Session, key: str, payload: Any) -> None:
    """Insert or replace a cache entry; a parallel request writing the same key is not an error."""
    now = utcnow()
    db.add(SourceCache(key=key, payload=payload, fetched_at=now))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        db.execute(
            update(SourceCache)
            .where(SourceCache.key == key)
            .values(payload=payload, fetched_at=now)
        )
        db.commit()


def lookup(db: Session, key: str, settings: Settings) -> SourceCache | None:
    row = db.get(SourceCache, key)
    if row is None:
        return None
    if as_utc(row.fetched_at) < utcnow() - timedelta(hours=settings.source_cache_hours):
        return None
    return row


def cached(
    db: Session, key: str, settings: Settings, fetch: Callable[[], Any]
) -> SourceResult[Any]:
    """Serve a fresh cache entry, or call ``fetch`` and cache its (JSON-able) answer.

    ``ok`` and ``empty`` answers are cached; ``unavailable`` is not, so the next request retries.
    """
    row = lookup(db, key, settings)
    if row is None:
        try:
            payload = to_jsonable_python(fetch())
        except SourceUnavailable:
            return SourceResult(status="unavailable")
        store(db, key, payload)
        row = db.get(SourceCache, key)
        assert row is not None
    status = "empty" if is_empty(row.payload) else "ok"
    return SourceResult(status=status, fetched_at=row.fetched_at, data=row.payload or None)
