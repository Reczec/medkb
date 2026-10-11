"""Content-bound cache and atomic per-client/global UTC-day reservations."""

from __future__ import annotations

import hashlib
import hmac
import json
from datetime import timedelta
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import Settings
from app.models import AICache, AIUsage, utcnow

GLOBAL = "global"
PROMPT_VERSION = "stage4-v2"


def day() -> str:
    return utcnow().date().isoformat()


def client_identity(ip: str, settings: Settings) -> str:
    return hmac.new(settings.jwt_secret.encode(), ip.encode(), hashlib.sha256).hexdigest()


def cache_key(
    feature: str, document_id: int | str | None, inputs: Any, role: str, settings: Settings
) -> str:
    identity = [
        PROMPT_VERSION,
        feature,
        document_id,
        inputs,
        role,
        settings.ai_model,
        settings.ai_base_url.rstrip("/"),
    ]
    return hashlib.sha256(
        json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def read_cache(db: Session, key: str) -> dict[str, Any] | None:
    row = db.get(AICache, key)
    return row.output if row else None


def write_cache(
    db: Session,
    key: str,
    feature: str,
    document_id: int | None,
    settings: Settings,
    result: dict[str, Any],
) -> None:
    values = {
        "feature": feature,
        "document_id": document_id,
        "model": settings.ai_model,
        "output": result,
        "created_at": utcnow(),
    }
    try:
        with db.begin_nested():
            db.add(AICache(key=key, **values))
            db.flush()
    except IntegrityError:
        db.execute(update(AICache).where(AICache.key == key).values(**values))
    db.commit()


def _ensure_row(db: Session, identity: str, today: str) -> None:
    try:
        with db.begin_nested():
            db.add(AIUsage(client_id=identity, day=today, count=0))
            db.flush()
    except IntegrityError:
        pass  # another request (or earlier reservation) created it


def reserve(db: Session, identity: str, settings: Settings) -> None:
    """Reserve once before contacting a provider. Failed attempts still cost an API call.

    Lock/update global before client in every request; either both increments commit or neither.
    """
    today = day()
    for client, limit in (
        (GLOBAL, settings.ai_daily_limit),
        (identity, settings.ai_client_daily_limit),
    ):
        _ensure_row(db, client, today)
        changed = db.execute(
            update(AIUsage)
            .where(AIUsage.client_id == client, AIUsage.day == today, AIUsage.count < limit)
            .values(count=AIUsage.count + 1)
        )
        if changed.rowcount != 1:
            db.rollback()
            now = utcnow()
            midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            retry = max(1, int((midnight - now).total_seconds()))
            raise HTTPException(
                429,
                "KI-Tageslimit erreicht. Bitte morgen erneut versuchen.",
                headers={"Retry-After": str(retry)},
            )
    db.commit()


def usage_today(db: Session) -> int:
    return (
        db.scalar(select(AIUsage.count).where(AIUsage.client_id == GLOBAL, AIUsage.day == day()))
        or 0
    )
