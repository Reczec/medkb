"""Business logic: CRUD, search, statistics and audit log."""

from __future__ import annotations

import operator
from collections import Counter
from datetime import UTC, datetime, time, timedelta
from functools import reduce

from sqlalchemy import String, case, cast, false, func, or_, select
from sqlalchemy.orm import Session

from app.classifier import CATEGORIES, classify
from app.content import compose_content
from app.models import AuditLog, Document
from app.schemas import (
    CountItem,
    DayCount,
    DocType,
    DocumentCreate,
    DocumentUpdate,
    RecentItem,
    StatsOut,
    as_utc,
)

MAX_SEARCH_TERMS = 8
MAX_TERM_LENGTH = 100

# Relevance weights: a hit in the title counts more than one in the keywords or the content.
WEIGHT_TITLE = 3
WEIGHT_KEYWORDS = 2
WEIGHT_CONTENT = 1

ACTIVITY_DAYS = 30


def log_audit(
    db: Session, action: str, document_id: int | None, detail: str, actor: str | None = None
) -> None:
    db.add(AuditLog(action=action, actor=actor, document_id=document_id, detail=detail[:255]))


# --------------------------------------------------------------------------- CRUD


def create_document(
    db: Session,
    data: DocumentCreate,
    actor: str | None = None,
    commit: bool = True,
    document_id: int | None = None,
) -> Document:
    """Insert one entry. ``commit=False`` leaves the transaction open (atomic demo reset);
    ``document_id`` pins the id (example entries keep theirs across resets)."""
    content = data.content or ""  # the schema guarantees content (or composes it from sections)
    suggestion = classify(data.title, content)
    manual_category = data.category is not None

    document = Document(
        id=document_id,
        title=data.title,
        content=content,
        doc_type=data.doc_type.value,
        category=data.category if manual_category else suggestion.category,
        keywords=data.keywords or suggestion.keywords,
        source=data.source or None,
        auto_classified=not manual_category,
        term_en=data.term_en,
        icd11_code=data.icd11_code,
        medications=data.medications,
        sections=data.sections.model_dump() if data.sections else None,
        further_reading=[link.model_dump() for link in data.further_reading],
        ai_generated=data.ai_generated,
    )
    db.add(document)
    db.flush()  # assigns the id for the audit entry
    log_audit(db, "create", document.id, document.title, actor)
    if commit:
        db.commit()
    return document


def update_document(
    db: Session, document: Document, data: DocumentUpdate, actor: str | None = None
) -> Document:
    changes = data.model_dump(exclude_unset=True)
    reclassify = changes.pop("reclassify", False)
    changed_fields = list(changes)

    if "title" in changes:
        document.title = changes["title"]
    if changes.get("sections") is not None:
        # Structured entries keep their full text in sync with the sections.
        document.sections = changes["sections"]
        document.content = compose_content(changes["sections"])
    elif "content" in changes:
        document.content = changes["content"]
        document.sections = None  # edited as free text from now on
    elif "sections" in changes:  # explicit null: keep the text, drop the structure
        document.sections = None
    if "doc_type" in changes:
        document.doc_type = changes["doc_type"].value
    if "source" in changes:
        document.source = changes["source"] or None
    for name in ("term_en", "icd11_code", "medications", "further_reading"):
        if name in changes:
            setattr(document, name, changes[name])

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

    log_audit(db, "update", document.id, f"{document.title} ({', '.join(changed_fields)})", actor)
    db.commit()
    return document


def delete_document(db: Session, document: Document, actor: str | None = None) -> None:
    log_audit(db, "delete", document.id, document.title, actor)
    db.delete(document)
    db.commit()


# ------------------------------------------------------------------------- search


# Keywords are searched in their JSON text, so these characters would match its syntax.
JSON_SYNTAX = frozenset('"[],' + "\\")


def _term_condition_and_score(term: str):
    in_title = Document.title.icontains(term, autoescape=True)
    in_content = Document.content.icontains(term, autoescape=True)
    if JSON_SYNTAX.isdisjoint(term):
        in_keywords = cast(Document.keywords, String).icontains(term, autoescape=True)
    else:
        in_keywords = false()
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
        activity=_activity(db),
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


def _activity(db: Session) -> list[DayCount]:
    """Audit log entries per UTC day for the last ACTIVITY_DAYS days, oldest first.

    Counted in Python so that it behaves the same on SQLite and PostgreSQL.
    """
    today = datetime.now(UTC).date()
    first_day = today - timedelta(days=ACTIVITY_DAYS - 1)
    start = datetime.combine(first_day, time.min, tzinfo=UTC)
    timestamps = db.scalars(select(AuditLog.timestamp).where(AuditLog.timestamp >= start)).all()
    counts = Counter(as_utc(ts).date() for ts in timestamps)
    return [
        DayCount(date=day, count=counts.get(day, 0))
        for day in (first_day + timedelta(days=i) for i in range(ACTIVITY_DAYS))
    ]


def list_audit(db: Session, limit: int = 50) -> list[AuditLog]:
    return list(db.scalars(select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)).all())
