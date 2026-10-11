"""FastAPI application: REST API under /api, React web UI (frontend/dist) at /."""

from __future__ import annotations

import asyncio
import logging
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import __version__
from app.ai.provider import AIUnavailable
from app.config import get_settings
from app.database import Base, SessionLocal, engine, upgrade_schema
from app.demo import demo_reset_loop, reset_demo
from app.routers import admin, ai, auth, documents, sources, users
from app.seed import seed_if_empty
from app.spa import mount_frontend
from app.users import ensure_users

logger = logging.getLogger("medkb")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    # create_all is enough for this prototype; a real deployment would use migrations (Alembic).
    Base.metadata.create_all(engine)
    upgrade_schema(engine)
    if not settings.jwt_secret:
        # get_settings() is cached, so every request sees this key until the process ends.
        settings.jwt_secret = secrets.token_urlsafe(32)
        logger.warning("JWT_SECRET is not set: using a random key, logins end on restart.")
    elif len(settings.jwt_secret) < 32:
        logger.warning("JWT_SECRET is shorter than 32 characters; use a longer random value.")
    with SessionLocal() as db:
        ensure_users(db, settings)
    reset_task: asyncio.Task[None] | None = None
    if settings.demo_mode:
        with SessionLocal() as db:
            count = reset_demo(db)
        logger.info(
            "Demo mode: %d example entries, reset every %s h.", count, settings.demo_reset_hours
        )
        reset_task = asyncio.create_task(demo_reset_loop(settings))
    elif settings.seed_demo_data:
        with SessionLocal() as db:
            added = seed_if_empty(db)
        if added:
            logger.info("Inserted %d example documents.", added)
    yield
    if reset_task:
        reset_task.cancel()


app = FastAPI(
    title="MedKB – Digital Medical Knowledge Base",
    version=__version__,
    description=(
        "Prototype of a medical knowledge base with keyword search, rule-based classification "
        "and JSON archiving. Contains example data only – not medical advice."
    ),
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(sources.router)
app.include_router(ai.router)


@app.exception_handler(AIUnavailable)
async def ai_unavailable(_request, exc: AIUnavailable):
    code = str(exc) if str(exc) in {"ai_not_configured", "ai_invalid_output"} else "ai_unavailable"
    return JSONResponse(status_code=503, content={"detail": code})


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


# Registered last so that /api/* routes take precedence.
mount_frontend(app, get_settings().frontend_dist)
