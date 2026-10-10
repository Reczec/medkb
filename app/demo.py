"""Demo mode: put the example data back regularly, so a public demo can't be broken for good."""

from __future__ import annotations

import asyncio
import logging
from typing import Protocol

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import AuditLog, Document
from app.seed import seed_if_empty
from app.services import log_audit

logger = logging.getLogger("medkb")


class _ResetSettings(Protocol):
    demo_reset_hours: float


def reset_demo(db: Session) -> int:
    """Replace all entries with the example entries and start a fresh change log.

    Logins and archives are kept. Returns the number of entries.
    """
    db.execute(delete(Document))
    db.commit()
    count = seed_if_empty(db, force=True)
    db.execute(delete(AuditLog))
    log_audit(
        db, "demo_reset", None, f"Beispieldaten wiederhergestellt ({count} Einträge)", "system"
    )
    db.commit()
    return count


def _reset_in_new_session() -> int:
    with SessionLocal() as db:
        return reset_demo(db)


async def demo_reset_loop(settings: _ResetSettings) -> None:
    """Run reset_demo every `demo_reset_hours` until cancelled."""
    while True:
        await asyncio.sleep(settings.demo_reset_hours * 3600)
        try:
            count = await asyncio.to_thread(_reset_in_new_session)
            logger.info("Demo reset: %d example entries restored.", count)
        except Exception:  # keep the loop alive; the next run tries again
            logger.exception("Demo reset failed.")
