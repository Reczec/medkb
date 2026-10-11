"""Demo mode: put the example data back regularly, so a public demo can't be broken for good."""

from __future__ import annotations

import asyncio
import logging
from typing import Protocol

from sqlalchemy import delete, text
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
    One transaction: readers see the old or the new state, never an empty knowledge base, and a
    failure part-way leaves the old state in place.
    """
    try:
        if db.get_bind().dialect.name == "postgresql":
            # A second reset (a new instance starting during a deploy) waits instead of
            # inserting its examples next to ours. Readers are not blocked.
            db.execute(text("LOCK TABLE documents IN SHARE ROW EXCLUSIVE MODE"))
        db.execute(delete(Document))
        db.flush()
        count = seed_if_empty(db, force=True, commit=False)
        db.flush()  # the seed's own audit entries must exist before the log is cleared
        db.execute(delete(AuditLog))
        log_audit(
            db, "demo_reset", None, f"Beispieldaten wiederhergestellt ({count} Einträge)", "system"
        )
        db.commit()
    except BaseException:
        db.rollback()
        raise
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
