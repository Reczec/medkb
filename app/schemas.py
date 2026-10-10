"""Pydantic schemas (request validation and API responses)."""

from __future__ import annotations

import re
from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Annotated, Any, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.classifier import CATEGORIES
from app.content import compose_content


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


MAX_MEDICATIONS = 10
MAX_FURTHER_READING = 8
MAX_SECTION_LENGTH = 5000
TERM_EN_RE = re.compile(r"^[A-Za-z0-9 ,'()\-]+$")
ICD11_CODE_RE = re.compile(r"^[0-9A-Z]{4}(\.[0-9A-Z]{1,2})?$")
MEDICATION_RE = re.compile(r"^[a-z][a-z \-]+$")

TermEn = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=200)]


def _check_term_en(value: str | None) -> str | None:
    if value is not None and not TERM_EN_RE.match(value):
        raise ValueError("term_en may only contain letters, digits, spaces and , ' ( ) -")
    return value


def _check_icd11_code(value: str | None) -> str | None:
    if value is None:
        return None
    code = value.strip().upper()
    if not ICD11_CODE_RE.match(code):
        raise ValueError("Not an ICD-11 stem code such as 'BA00' or '8A80.1'.")
    return code


def _clean_medications(values: list[str] | None) -> list[str] | None:
    if values is None:
        return None
    cleaned: list[str] = []
    for value in values:
        name = " ".join(value.split()).lower()
        if not (2 <= len(name) <= 60 and MEDICATION_RE.match(name)):
            raise ValueError(f"'{value}' is not a valid active ingredient name.")
        if name not in cleaned:
            cleaned.append(name)
    if len(cleaned) > MAX_MEDICATIONS:
        raise ValueError(f"At most {MAX_MEDICATIONS} active ingredients are allowed.")
    return cleaned


class Sections(BaseModel):
    """Structured content. Empty sections are stored as null; at least one must have text."""

    model_config = ConfigDict(extra="forbid")

    definition: str | None = Field(default=None, max_length=MAX_SECTION_LENGTH)
    symptoms: str | None = Field(default=None, max_length=MAX_SECTION_LENGTH)
    causes: str | None = Field(default=None, max_length=MAX_SECTION_LENGTH)
    diagnostics: str | None = Field(default=None, max_length=MAX_SECTION_LENGTH)
    therapy: str | None = Field(default=None, max_length=MAX_SECTION_LENGTH)
    red_flags: str | None = Field(default=None, max_length=MAX_SECTION_LENGTH)

    @field_validator("*", mode="before")
    @classmethod
    def _blank_is_none(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip() or None
        return value

    @model_validator(mode="after")
    def _not_empty(self) -> Self:
        if not any(self.model_dump().values()):
            raise ValueError("At least one section needs text.")
        return self


class FurtherReadingLink(BaseModel):
    label: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    url: Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]

    @field_validator("url")
    @classmethod
    def _https(cls, value: str) -> str:
        if not value.startswith("https://") or any(c.isspace() for c in value):
            raise ValueError("Links must be https:// URLs.")
        return value


FurtherReading = Annotated[list[FurtherReadingLink], Field(max_length=MAX_FURTHER_READING)]


def as_utc(value: datetime) -> datetime:
    # SQLite returns naive datetimes; everything is stored in UTC.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


class DocumentCreate(BaseModel):
    title: Title
    # Required unless sections are given; with sections it is composed from them.
    content: Content | None = None
    doc_type: DocType
    # None -> chosen by the classifier. A value -> manual choice, never overwritten.
    category: str | None = None
    # None or [] -> generated automatically.
    keywords: list[str] | None = None
    source: Source | None = None
    term_en: TermEn | None = None
    icd11_code: str | None = None
    medications: list[str] = Field(default_factory=list)
    sections: Sections | None = None
    further_reading: FurtherReading = Field(default_factory=list)
    ai_generated: bool = False

    @field_validator("category")
    @classmethod
    def _category(cls, value: str | None) -> str | None:
        return _check_category(value)

    @field_validator("keywords")
    @classmethod
    def _keywords(cls, value: list[str] | None) -> list[str] | None:
        return _clean_keywords(value)

    @field_validator("term_en")
    @classmethod
    def _term_en(cls, value: str | None) -> str | None:
        return _check_term_en(value)

    @field_validator("icd11_code")
    @classmethod
    def _icd11_code(cls, value: str | None) -> str | None:
        return _check_icd11_code(value)

    @field_validator("medications")
    @classmethod
    def _medications(cls, value: list[str]) -> list[str]:
        return _clean_medications(value) or []

    @model_validator(mode="after")
    def _content_or_sections(self) -> Self:
        if self.sections is not None:
            self.content = compose_content(self.sections.model_dump())
        elif self.content is None:
            raise ValueError("Either 'content' or 'sections' is required.")
        return self


class DocumentUpdate(BaseModel):
    """Partial update: only the fields that are sent are changed."""

    title: Title | None = None
    content: Content | None = None
    doc_type: DocType | None = None
    category: str | None = None
    keywords: list[str] | None = None  # [] -> regenerate automatically
    source: Source | None = None  # null clears the source
    term_en: TermEn | None = None  # null clears
    icd11_code: str | None = None  # null clears
    medications: list[str] | None = None
    # New sections recompose the content; content sent without sections makes it free text.
    sections: Sections | None = None
    further_reading: FurtherReading | None = None
    reclassify: bool = False  # re-run the classifier for category (and keywords)

    @field_validator("category")
    @classmethod
    def _category(cls, value: str | None) -> str | None:
        return _check_category(value)

    @field_validator("keywords")
    @classmethod
    def _keywords(cls, value: list[str] | None) -> list[str] | None:
        return _clean_keywords(value)

    @field_validator("term_en")
    @classmethod
    def _term_en(cls, value: str | None) -> str | None:
        return _check_term_en(value)

    @field_validator("icd11_code")
    @classmethod
    def _icd11_code(cls, value: str | None) -> str | None:
        return _check_icd11_code(value)

    @field_validator("medications")
    @classmethod
    def _medications(cls, value: list[str] | None) -> list[str] | None:
        return _clean_medications(value)

    @model_validator(mode="after")
    def _check_fields(self) -> Self:
        sent = self.model_fields_set
        not_null = (
            "title",
            "content",
            "doc_type",
            "category",
            "keywords",
            "medications",
            "further_reading",
        )
        for name in not_null:
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
    term_en: str | None = None
    icd11_code: str | None = None
    medications: list[str] = Field(default_factory=list)
    sections: dict[str, str | None] | None = None
    further_reading: list[FurtherReadingLink] = Field(default_factory=list)
    ai_generated: bool = False
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return as_utc(value)

    @field_validator("medications", "further_reading", mode="before")
    @classmethod
    def _null_list(cls, value: Any) -> Any:
        # Rows from before v2 stage 3 can hold NULL in the added columns.
        return [] if value is None else value

    @field_validator("ai_generated", mode="before")
    @classmethod
    def _null_false(cls, value: Any) -> Any:
        return False if value is None else value


class DocumentList(BaseModel):
    items: list[DocumentOut]
    total: int
    limit: int
    offset: int


class ClassifyRequest(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    content: Annotated[str, StringConstraints(strip_whitespace=True, max_length=50_000)] = ""
    # Structured entries are classified on their composed full text.
    sections: Sections | None = None

    @model_validator(mode="after")
    def _content_or_sections(self) -> Self:
        if self.sections is not None:
            self.content = compose_content(self.sections.model_dump())
        if not self.content:
            raise ValueError("Either 'content' or 'sections' is required.")
        return self


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
    # Added in v2 stage 3; archives written before that restore with these defaults.
    term_en: TermEn | None = None
    icd11_code: str | None = None
    medications: list[str] = Field(default_factory=list)
    sections: Sections | None = None
    further_reading: FurtherReading = Field(default_factory=list)
    ai_generated: bool = False
    created_at: datetime
    updated_at: datetime

    @field_validator("category")
    @classmethod
    def _category(cls, value: str) -> str:
        checked = _check_category(value)
        assert checked is not None
        return checked

    @field_validator("term_en")
    @classmethod
    def _term_en(cls, value: str | None) -> str | None:
        return _check_term_en(value)

    @field_validator("icd11_code")
    @classmethod
    def _icd11_code(cls, value: str | None) -> str | None:
        return _check_icd11_code(value)

    @field_validator("medications")
    @classmethod
    def _medications(cls, value: list[str]) -> list[str]:
        return _clean_medications(value) or []


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
