"""Documents, search, classification, statistics. Reading needs a login; writing is admin-only."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import services
from app.auth import current_user, require_role
from app.classifier import CATEGORIES, DEFAULT_CATEGORY, classify
from app.database import get_db
from app.models import Document, User
from app.schemas import (
    ClassifyRequest,
    ClassifyResponse,
    DocType,
    DocumentCreate,
    DocumentList,
    DocumentOut,
    DocumentUpdate,
    MetaOut,
    StatsOut,
)

router = APIRouter(prefix="/api", tags=["documents"], dependencies=[Depends(current_user)])

DbSession = Annotated[Session, Depends(get_db)]
Staff = Annotated[User, Depends(require_role("admin", "doctor"))]
Admin = Annotated[User, Depends(require_role("admin"))]


def _get_or_404(db: Session, document_id: int) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found.")
    return document


@router.get("/meta", response_model=MetaOut)
def meta() -> MetaOut:
    return MetaOut(
        categories=CATEGORIES,
        doc_types=[t.value for t in DocType],
        default_category=DEFAULT_CATEGORY,
    )


@router.post("/classify", response_model=ClassifyResponse)
def classify_text(data: ClassifyRequest, _user: Staff) -> ClassifyResponse:
    """Preview the automatic category and keywords without saving anything."""
    result = classify(data.title, data.content)
    return ClassifyResponse(
        category=result.category,
        confidence=result.confidence,
        fallback=result.fallback,
        scores=result.scores,
        matched_terms=result.matched_terms,
        keywords=result.keywords,
    )


@router.get("/documents", response_model=DocumentList)
def list_documents(
    db: DbSession,
    q: Annotated[
        str | None, Query(max_length=200, description="Search terms (all must match)")
    ] = None,
    category: Annotated[str | None, Query(max_length=50)] = None,
    doc_type: Annotated[str | None, Query(max_length=30)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> DocumentList:
    items, total = services.search_documents(db, q, category, doc_type, limit, offset)
    return DocumentList(
        items=[DocumentOut.model_validate(d) for d in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def create_document(data: DocumentCreate, db: DbSession, user: Admin) -> Document:
    return services.create_document(db, data, actor=user.username)


@router.get("/documents/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: DbSession) -> Document:
    return _get_or_404(db, document_id)


@router.patch("/documents/{document_id}", response_model=DocumentOut)
def update_document(document_id: int, data: DocumentUpdate, db: DbSession, user: Admin) -> Document:
    return services.update_document(db, _get_or_404(db, document_id), data, actor=user.username)


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: DbSession, user: Admin) -> Response:
    services.delete_document(db, _get_or_404(db, document_id), actor=user.username)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/stats", response_model=StatsOut)
def stats(db: DbSession) -> StatsOut:
    return services.get_stats(db)
