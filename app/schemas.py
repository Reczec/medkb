"""Pydantic schemas (request validation and API responses)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.classifier import CATEGORIES


class DocType(StrEnum):
    SYMPTOM = "Symptom"
    DIAGNOSE = "Diagnose"
    BESCHREIBUNG = "Beschreibung"
    ANAMNESE = "Anamnese"
    BEFUND = "Befund"
    LEITLINIE = "Leitlinie"


Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=200)]
Content = Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=50_000)]
Source = Annotated[str, StringConstraints(strip_whitespace=True, max_length=200)]

MAX_KEYWORDS_PER_DOCUMENT = 20
MAX_KEYWORD_LENGTH = 50


def _clean_keywords(values: list[str] | None) -> list[str] | None:
    if values is None:
        return None
    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values:
        word = value.strip()
        if not word:
            continue
        if len(word) > MAX_KEYWORD_LENGTH:
            raise ValueError(f"A keyword may have at most {MAX_KEYWORD_LENGTH} characters.")
        if word.lower() not in seen:
            seen.add(word.lower())
            cleaned.append(word)
    if len(cleaned) > MAX_KEYWORDS_PER_DOCUMENT:
        raise ValueError(f"At most {MAX_KEYWORDS_PER_DOCUMENT} keywords are allowed.")
    return cleaned


def _check_category(value: str | None) -> str | None:
    if value is not None and value not in CATEGORIES:
        raise ValueError(f"Unknown category '{value}'. Allowed: {', '.join(CATEGORIES)}")
    return value


def as_utc(value: datetime) -> datetime:
    # SQLite returns naive datetimes; everything is stored in UTC.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


class DocumentCreate(BaseModel):
    title: Title
    content: Content
    doc_type: DocType
    # None -> chosen by the classifier. A value -> manual choice, never overwritten.
    category: str | None = None
    # None or [] -> generated automatically.
    keywords: list[str] | None = None
    source: Source | None = None

    @field_validator("category")
    @classmethod
    def _category(cls, value: str | None) -> str | None:
        return _check_category(value)

    @field_validator("keywords")
    @classmethod
    def _keywords(cls, value: list[str] | None) -> list[str] | None:
        return _clean_keywords(value)


class DocumentUpdate(BaseModel):
    """Partial update: only the fields that are sent are changed."""

    title: Title | None = None
    content: Content | None = None
    doc_type: DocType | None = None
    category: str | None = None
    keywords: list[str] | None = None  # [] -> regenerate automatically
    source: Source | None = None  # null clears the source
    reclassify: bool = False  # re-run the classifier for category (and keywords)

    @field_validator("category")
    @classmethod
    def _category(cls, value: str | None) -> str | None:
        return _check_category(value)

    @field_validator("keywords")
    @classmethod
    def _keywords(cls, value: list[str] | None) -> list[str] | None:
        return _clean_keywords(value)

    @model_validator(mode="after")
    def _check_fields(self) -> Self:
        sent = self.model_fields_set
        for name in ("title", "content", "doc_type", "category", "keywords"):
            if name in sent and getattr(self, name) is None:
                raise ValueError(f"'{name}' must not be null.")
        if not sent:
            raise ValueError("No fields to update.")
        return self


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    category: str
    doc_type: str
    keywords: list[str]
    source: str | None
    auto_classified: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return as_utc(value)


class DocumentList(BaseModel):
    items: list[DocumentOut]
    total: int
    limit: int
    offset: int


class ClassifyRequest(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    content: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50_000)
    ]


class ClassifyResponse(BaseModel):
    category: str
    confidence: float = Field(description="Share of the winning score in the total score (0-1).")
    fallback: bool = Field(description="True if no category reached the minimum score.")
    scores: dict[str, int]
    matched_terms: list[str]
    keywords: list[str]


class MetaOut(BaseModel):
    categories: list[str]
    doc_types: list[str]
    default_category: str


class CountItem(BaseModel):
    name: str
    count: int


class RecentItem(BaseModel):
    id: int
    title: str
    category: str
    updated_at: datetime

    @field_validator("updated_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return as_utc(value)


class DayCount(BaseModel):
    date: date
    count: int


class StatsOut(BaseModel):
    total: int
    auto_classified: int
    categories: list[CountItem]
    doc_types: list[CountItem]
    recent: list[RecentItem]
    activity: list[DayCount] = Field(
        description="Changes (audit log entries) per UTC day, last 30 days, oldest first."
    )


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    action: str
    actor: str | None = None
    document_id: int | None
    detail: str

    @field_validator("timestamp")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return as_utc(value)


class ArchiveInfo(BaseModel):
    name: str
    created_at: datetime
    size_bytes: int
    document_count: int


class RestoreResult(BaseModel):
    restored: int
    backup: ArchiveInfo = Field(description="Automatic backup of the state before the restore.")


class ArchiveEntry(BaseModel):
    """One document inside an archive file (validated again when restoring)."""

    title: Title
    content: Content
    category: str
    doc_type: DocType
    keywords: list[str] = Field(default_factory=list)
    source: str | None = None
    auto_classified: bool = True
    created_at: datetime
    updated_at: datetime

    @field_validator("category")
    @classmethod
    def _category(cls, value: str) -> str:
        checked = _check_category(value)
        assert checked is not None
        return checked


class LoginRequest(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=200)]


class DemoLoginRequest(BaseModel):
    role: Literal["admin", "doctor", "patient"]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    role: str


class UserListItem(UserOut):
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return as_utc(value)


class TokenOut(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: UserOut


class AuthOptions(BaseModel):
    demo_mode: bool
