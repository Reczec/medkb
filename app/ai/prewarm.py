"""Explicit trusted CLI warmup; no startup calls and no invented offline output."""

import argparse
import asyncio

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.provider import AIProvider, AIUnavailable, get_provider
from app.ai.service import document_cache_identity, document_inputs, execute
from app.ai.store import client_identity
from app.config import Settings, get_settings
from app.database import Base, SessionLocal, engine, upgrade_schema
from app.i18n import Lang
from app.models import Document


async def prewarm(
    db: Session,
    settings: Settings,
    provider: AIProvider,
    limit: int | None = None,
    pause: float = 0,
    lang: Lang = "de",
) -> dict[str, int]:
    """Warm every role/feature variant. ``pause`` seconds between calls keeps a free provider
    tier under its per-minute limit (failed calls still use the daily budget)."""
    # This explicit operator job may use the global budget; public client quotas stay unchanged.
    trusted = settings.model_copy(update={"ai_client_daily_limit": settings.ai_daily_limit})
    documents = db.scalars(select(Document).order_by(Document.id).limit(limit)).all()
    counts = {"completed": 0, "failed": 0}
    first = True
    for document in documents:
        inputs = document_inputs(document, lang)
        for role in ("admin", "doctor", "patient"):
            features = (
                ("explain", "red-flags", "summary")
                if role != "patient"
                else ("explain", "red-flags")
            )
            for feature in features:
                if pause and not first:
                    await asyncio.sleep(pause)
                first = False
                try:
                    await execute(
                        db,
                        trusted,
                        provider,
                        client_identity("prewarm", settings),
                        feature,
                        inputs,
                        role,
                        document_id=document.id,
                        cache_identity=document_cache_identity(document),
                        lang=lang,
                    )
                    counts["completed"] += 1
                except (AIUnavailable, HTTPException):
                    counts["failed"] += 1
                    db.rollback()
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Number of documents to warm")
    parser.add_argument(
        "--pause", type=float, default=0, help="Seconds between calls (free tiers: about 4)"
    )
    parser.add_argument(
        "--lang", choices=("de", "en", "both"), default="de", help="Language(s) to warm"
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    settings = get_settings()
    if not settings.ai_api_key:
        print("AI not configured; no requests made.")
        return
    Base.metadata.create_all(engine)
    upgrade_schema(engine)
    with SessionLocal() as db:
        provider = get_provider(settings)
        languages: list[Lang] = ["de", "en"] if args.lang == "both" else [args.lang]
        for lang in languages:
            result = asyncio.run(prewarm(db, settings, provider, args.limit, args.pause, lang))
            print(lang, result)


if __name__ == "__main__":
    main()
