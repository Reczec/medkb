"""SQLAlchemy models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Document(Base):
    """One entry of the knowledge base (symptom, diagnosis, description, ...)."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), index=True)
    doc_type: Mapped[str] = mapped_column(String(30), index=True)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    source: Mapped[str | None] = mapped_column(String(200), default=None)
    # True while the category was chosen by the classifier, False once a user set it.
    auto_classified: Mapped[bool] = mapped_column(default=True)
    # English term for the external sources (PubMed search, openFDA), e.g. "Migraine".
    term_en: Mapped[str | None] = mapped_column(String(200), default=None)
    icd11_code: Mapped[str | None] = mapped_column(String(20), default=None)
    # Active ingredients (English, lower case) for openFDA.
    medications: Mapped[list[str]] = mapped_column(JSON, default=list)
    # {definition, symptoms, causes, diagnostics, therapy, red_flags}; None = free text only.
    sections: Mapped[dict[str, str | None] | None] = mapped_column(JSON, default=None)
    further_reading: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list)
    # True if the entry started as an AI draft (stage 4).
    ai_generated: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class User(Base):
    """A login. Roles: admin (everything), doctor and patient (read only)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(10))
    display_name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class SourceCache(Base):
    """Answers from external sources, keyed by source and query (kept across demo resets)."""

    __tablename__ = "source_cache"

    key: Mapped[str] = mapped_column(String(300), primary_key=True)
    payload: Mapped[Any] = mapped_column(JSON, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditLog(Base):
    """Traceability: who changed what and when (no personal data, only document titles)."""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    action: Mapped[str] = mapped_column(String(30))
    # Username of who did it ("system" for automatic actions); None in logs from before v2.
    actor: Mapped[str | None] = mapped_column(String(50), default=None)
    # No foreign key on purpose: log entries must survive deletion of the document.
    document_id: Mapped[int | None] = mapped_column(Integer, default=None)
    detail: Mapped[str] = mapped_column(String(255), default="")
