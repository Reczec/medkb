"""Live data from external sources for doctors and admins. Always 200; see ``status``."""

from __future__ import annotations

from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth import require_role
from app.config import Settings, get_settings
from app.database import get_db
from app.i18n import RequestLang
from app.models import Document
from app.schemas import Icd11Entry, LatestStudies, MedicationsOut, SourceResult, Study
from app.sources import icd11, openfda, pubmed
from app.sources.cache import cached
from app.sources.http import http_client

router = APIRouter(
    prefix="/api/sources",
    tags=["sources"],
    dependencies=[Depends(require_role("admin", "doctor"))],
)

DbSession = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]
Client = Annotated[httpx.Client, Depends(http_client)]

DOCUMENT_STUDIES = 5
LATEST_CATEGORIES = 2
LATEST_STUDIES = 3


def _document(db: Session, document_id: int) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found.")
    return document


def _studies(
    db: Session, client: httpx.Client, settings: Settings, query: str, limit: int
) -> SourceResult[Any]:
    return cached(
        db,
        f"pubmed:{query}:{limit}",
        settings,
        lambda: pubmed.search_studies(client, query, settings, limit),
    )


@router.get("/documents/{document_id}/studies", response_model=SourceResult[list[Study]])
def document_studies(
    document_id: int, db: DbSession, settings: AppSettings, client: Client
) -> SourceResult[Any]:
    """The newest PubMed articles for the entry's English term."""
    document = _document(db, document_id)
    if not document.term_en:
        return SourceResult(status="empty")
    return _studies(db, client, settings, pubmed.document_query(document.term_en), DOCUMENT_STUDIES)


@router.get("/latest-studies", response_model=SourceResult[list[LatestStudies]])
def latest_studies(db: DbSession, settings: AppSettings, client: Client) -> SourceResult[Any]:
    """Newest PubMed articles for the specialties with the most entries (dashboard tile)."""
    counts = dict(
        db.execute(select(Document.category, func.count()).group_by(Document.category)).all()
    )
    # Ties keep the classifier's specialty order, so the choice is stable.
    filled = [c for c in pubmed.CATEGORY_TERMS if counts.get(c)]
    largest = sorted(filled, key=lambda c: -counts[c])[:LATEST_CATEGORIES]

    groups: list[dict[str, Any]] = []
    fetched: list[Any] = []
    for category in largest:
        result = _studies(db, client, settings, pubmed.category_query(category), LATEST_STUDIES)
        if result.status == "unavailable":
            return SourceResult(status="unavailable")
        fetched.append(result.fetched_at)
        if result.data:
            groups.append({"category": category, "studies": result.data})
    if not groups:
        return SourceResult(status="empty")
    return SourceResult(status="ok", fetched_at=min(fetched), data=groups)


@router.get("/documents/{document_id}/icd11", response_model=SourceResult[Icd11Entry])
def document_icd11(
    document_id: int, db: DbSession, settings: AppSettings, client: Client, lang: RequestLang
) -> SourceResult[Any]:
    """Title and definition of the entry's ICD-11 code from the WHO API."""
    document = _document(db, document_id)
    if not icd11.is_configured(settings):
        return SourceResult(status="not_configured")
    if not document.icd11_code:
        return SourceResult(status="empty")
    code = document.icd11_code
    key = f"icd11:{settings.icd_release}:{lang}:{code}"
    return cached(db, key, settings, lambda: icd11.lookup_code(client, code, settings, lang))


@router.get("/documents/{document_id}/medications", response_model=SourceResult[MedicationsOut])
def document_medications(
    document_id: int, db: DbSession, settings: AppSettings, client: Client
) -> SourceResult[Any]:
    """FDA label excerpts for the entry's active ingredients, cached per ingredient."""
    document = _document(db, document_id)
    if not document.medications:
        return SourceResult(status="empty")

    found: list[Any] = []
    missing: list[str] = []
    fetched: list[Any] = []
    for ingredient in document.medications:
        result = cached(
            db,
            f"openfda:{ingredient}",
            settings,
            lambda ingredient=ingredient: openfda.fetch_label(client, ingredient, settings),
        )
        if result.status == "unavailable":
            return SourceResult(status="unavailable")
        fetched.append(result.fetched_at)
        if result.data:
            found.append(result.data)
        else:
            missing.append(ingredient)
    return SourceResult(
        status="ok", fetched_at=min(fetched), data={"found": found, "missing": missing}
    )
