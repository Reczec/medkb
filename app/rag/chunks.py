"""Deterministic section chunks, independent of database IDs and reset timestamps."""

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from app.content import SECTION_KEYS
from app.i18n import Lang

VERSION = "sections-v1"
MODEL = "gemini-embedding-001"
DIMENSIONS = 768


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def signature(settings: Any = None) -> str:
    return digest([VERSION, "google-v1beta", MODEL, "RETRIEVAL_DOCUMENT", DIMENSIONS])


@dataclass(frozen=True)
class Chunk:
    key: str
    document_id: int
    fingerprint: str
    lang: Lang
    title: str
    section: str
    text: str
    offset: int

    @property
    def embedding_text(self) -> str:
        return f"{self.title[:200]}\n{self.section}\n{self.text}"


def chunks(document: Any, lang: Lang) -> list[Chunk]:
    title = (document.title_en or document.title) if lang == "en" else document.title
    german = document.sections or {}
    english = (document.sections_en or {}) if lang == "en" else {}
    sections = {key: text for key in SECTION_KEYS if (text := english.get(key) or german.get(key))}
    if not sections:
        sections = {
            "content": (document.content_en or document.content)
            if lang == "en"
            else document.content
        }
    fingerprint = digest([document.title, document.source, lang, title, sections])
    result = []
    for section, text in sections.items():
        start = 0
        while start < len(text):
            end = min(start + 800, len(text))
            if end < len(text):
                boundary = text.rfind(" ", start + 700, end)
                if boundary > start:
                    end = boundary
            part = text[start:end]
            key = digest([signature(), lang, document.title, document.source, title, section, part])
            result.append(Chunk(key, document.id, fingerprint, lang, title, section, part, start))
            if end == len(text):
                break
            start = end - 100
    return result
