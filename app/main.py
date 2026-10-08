"""FastAPI application: REST API under /api, static web UI at /."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import admin, documents
from app.seed import seed_if_empty

logger = logging.getLogger("medkb")
STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    # create_all is enough for this prototype; a real deployment would use migrations (Alembic).
    Base.metadata.create_all(engine)
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

app.include_router(documents.router)
app.include_router(admin.router)

# Mounted last so that /api/* routes take precedence.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
