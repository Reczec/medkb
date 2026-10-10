"""FastAPI application: REST API under /api, React web UI (frontend/dist) at /."""

from __future__ import annotations

import logging
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __version__
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import admin, auth, documents
from app.seed import seed_if_empty
from app.spa import mount_frontend
from app.users import ensure_users

logger = logging.getLogger("medkb")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    # create_all is enough for this prototype; a real deployment would use migrations (Alembic).
    Base.metadata.create_all(engine)
    if not settings.jwt_secret:
        # get_settings() is cached, so every request sees this key until the process ends.
        settings.jwt_secret = secrets.token_urlsafe(32)
        logger.warning("JWT_SECRET is not set: using a random key, logins end on restart.")
    elif len(settings.jwt_secret) < 32:
        logger.warning("JWT_SECRET is shorter than 32 characters; use a longer random value.")
    with SessionLocal() as db:
        ensure_users(db, settings)
    if not settings.admin_token:
        logger.warning("ADMIN_TOKEN is not set: archive and audit endpoints are disabled.")
    if settings.seed_demo_data:
        with SessionLocal() as db:
            added = seed_if_empty(db)
        if added:
            logger.info("Inserted %d example documents.", added)
    yield


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

# Registered last so that /api/* routes take precedence.
mount_frontend(app, get_settings().frontend_dist)
