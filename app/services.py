"""Business logic: CRUD, search, statistics and audit log."""

from __future__ import annotations

import operator
from functools import reduce

from sqlalchemy import String, case, cast, func, or_, select
from sqlalchemy.orm import Session

from app.classifier import CATEGORIES, classify
from app.models import AuditLog, Document
from app.schemas import (
    CountItem,
    DocType,
    DocumentCreate,
    DocumentUpdate,
    RecentItem,
    StatsOut,
)

MAX_SEARCH_TERMS = 8
MAX_TERM_LENGTH = 100

# Relevance weights: a hit in the title counts more than one in the keywords or the content.
WEIGHT_TITLE = 3
WEIGHT_KEYWORDS = 2
WEIGHT_CONTENT = 1


def log_audit(db: Session, action: str, document_id: int | None, detail: str) -> None:
    db.add(AuditLog(action=action, document_id=document_id, detail=detail[:255]))


# --------------------------------------------------------------------------- CRUD


def create_document(db: Session, data: DocumentCreate) -> Document:
    suggestion = classify(data.title, data.content)
    manual_category = data.category is not None

    document = Document(
        title=data.title,
        content=data.content,
        doc_type=data.doc_type.value,
        category=data.category if manual_category else suggestion.category,
        keywords=data.keywords or suggestion.keywords,
        source=data.source or None,
        auto_classified=not manual_category,
    )
    db.add(document)
    db.flush()  # assigns the id for the audit entry
    log_audit(db, "create", document.id, document.title)
    db.commit()
    return document


def update_document(db: Session, document: Document, data: DocumentUpdate) -> Document:
    changes = data.model_dump(exclude_unset=True)
    reclassify = changes.pop("reclassify", False)
    changed_fields = list(changes)

    if "title" in changes:
        document.title = changes["title"]
    if "content" in changes:
        document.content = changes["content"]
    if "doc_type" in changes:
        document.doc_type = changes["doc_type"].value
    if "source" in changes:
        document.source = changes["source"] or None

    if "category" in changes:
        document.category = changes["category"]
        document.auto_classified = False
    elif reclassify:
        suggestion = classify(document.title, document.content)
        document.category = suggestion.category
        document.auto_classified = True
        changed_fields.append("reclassify")
        if "keywords" not in changes:
            document.keywords = suggestion.keywords

    if "keywords" in changes:
        if changes["keywords"]:
            document.keywords = changes["keywords"]
        else:  # an empty list asks for automatic keywords
            document.keywords = classify(document.title, document.content).keywords

    log_audit(db, "update", document.id, f"{document.title} ({', '.join(changed_fields)})")
    db.commit()
    return document


def delete_document(db: Session, document: Document) -> None:
    log_audit(db, "delete", document.id, document.title)
    db.delete(document)
    db.commit()


# ------------------------------------------------------------------------- search


def _term_condition_and_score(term: str):
    in_title = Document.title.icontains(term, autoescape=True)
    in_keywords = cast(Document.keywords, String).icontains(term, autoescape=True)
    in_content = Document.content.icontains(term, autoescape=True)
    score = (
        case((in_title, WEIGHT_TITLE), else_=0)
        + case((in_keywords, WEIGHT_KEYWORDS), else_=0)
        + case((in_content, WEIGHT_CONTENT), else_=0)
    )
    return or_(in_title, in_keywords, in_content), score


def search_documents(
    db: Session,
    q: str | None = None,
    category: str | None = None,
    doc_type: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Document], int]:
    """Keyword search over title, content and keywords, with optional filters.

    Every search term must match somewhere (AND). Results are ordered by relevance
    (title > keywords > content), then by most recently updated.
    """
    terms = [t[:MAX_TERM_LENGTH] for t in (q or "").split()][:MAX_SEARCH_TERMS]

    conditions = []
    scores = []
    for term in terms:
        condition, score = _term_condition_and_score(term)
        conditions.append(condition)
        scores.append(score)
    if category:
        conditions.append(Document.category == category)
    if doc_type:
        conditions.append(Document.doc_type == doc_type)

    filtered = select(Document).where(*conditions)
    total = db.scalar(select(func.count()).select_from(filtered.subquery())) or 0

    order_by = [Document.updated_at.desc(), Document.id.desc()]
    if scores:
        order_by.insert(0, reduce(operator.add, scores).desc())
    items = db.scalars(filtered.order_by(*order_by).limit(limit).offset(offset)).all()
    return list(items), total


# ---------------------------------------------------------------------- statistics


def get_stats(db: Session) -> StatsOut:
    total = db.scalar(select(func.count(Document.id))) or 0
    auto = db.scalar(select(func.count(Document.id)).where(Document.auto_classified.is_(True)))

    category_rows = db.execute(
        select(Document.category, func.count()).group_by(Document.category)
    ).all()
    type_rows = db.execute(
        select(Document.doc_type, func.count()).group_by(Document.doc_type)
    ).all()
    by_category = {name: count for name, count in category_rows}
    by_type = {name: count for name, count in type_rows}

    recent = db.scalars(
        select(Document).order_by(Document.updated_at.desc(), Document.id.desc()).limit(5)
    ).all()

    return StatsOut(
        total=total,
        auto_classified=auto or 0,
        # All known categories/types are listed, also those with 0 entries (stable dashboard).
        categories=[CountItem(name=c, count=by_category.get(c, 0)) for c in CATEGORIES],
        doc_types=[CountItem(name=t.value, count=by_type.get(t.value, 0)) for t in DocType],
        recent=[
            RecentItem(id=d.id, title=d.title, category=d.category, updated_at=d.updated_at)
            for d in recent
        ],
    )


def list_audit(db: Session, limit: int = 50) -> list[AuditLog]:
    return list(db.scalars(select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)).all())
