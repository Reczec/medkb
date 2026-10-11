"""Execute reserved requests; publish/cache only complete, validated results."""

import asyncio
import json
import re
from typing import Any

from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ai import prompts, store
from app.ai.provider import AIProvider, AIUnavailable
from app.ai.schemas import Classification
from app.config import Settings
from app.i18n import Lang, message
from app.schemas import DocumentCreate, DocumentOut
from app.seed_data import SEED_DOCUMENTS, SOURCE

SEED_TITLES = frozenset(item["title"] for item in SEED_DOCUMENTS)


ENGLISH_FIELDS = {"title_en", "content_en", "sections_en", "keywords_en"}


def document_inputs(document: Any, lang: Lang = "de") -> dict:
    """Bind to semantic content, not timestamps refreshed by an unchanged demo reset.

    The German shape is exactly what it was before the English version existed, so cache keys
    of warmed German answers stay valid. English requests use the English text field by field,
    falling back to German.
    """
    out = DocumentOut.model_validate(document)
    data = out.model_dump(mode="json", exclude={"id", "created_at", "updated_at"} | ENGLISH_FIELDS)
    english_links = [link.label_en or link.label for link in out.further_reading]
    data["further_reading"] = [
        {"label": link["label"], "url": link["url"]} for link in data["further_reading"]
    ]
    if lang == "en":
        data["title"] = out.title_en or out.title
        data["content"] = out.content_en or out.content
        data["sections"] = out.sections_en or out.sections
        data["keywords"] = out.keywords_en or out.keywords
        for link, label in zip(data["further_reading"], english_links, strict=True):
            link["label"] = label
    return data


def document_cache_identity(document: Any) -> str | None:
    # Seed IDs change on PostgreSQL reset. Content still independently binds the cache key;
    # a changed/restored/imitated seed title cannot receive another content snapshot's answer.
    if document.source == SOURCE and document.title in SEED_TITLES:
        return "seed:" + document.title
    return None


def normalize(
    feature: str, text: str, inputs: Any, citations: list[dict], lang: Lang = "de"
) -> dict:
    try:
        if not text.strip() or len(text) > 20_000:
            raise ValueError("Invalid output size")
        result: dict = {"text": text.strip(), "cached": False, "citations": citations}
        if feature in ("draft", "classify"):
            raw = text.strip()
            if raw.startswith("```json\n") and raw.endswith("```"):
                raw = raw[8:-3].strip()
            data = json.loads(raw)
            if feature == "draft":
                allowed = {
                    "content",
                    "sections",
                    "doc_type",
                    "term_en",
                    "icd11_code",
                    "medications",
                    "keywords",
                }
                draft = DocumentCreate.model_validate(
                    {
                        **{k: v for k, v in data.items() if k in allowed},
                        "title": inputs["title"],
                        "ai_generated": True,
                    }
                )
                result["draft"] = draft.model_dump(mode="json")
                result["text"] = draft.content
            else:
                result["classification"] = Classification.model_validate(data).model_dump()
                result["text"] = result["classification"]["reasoning"]
        if feature == "ask":
            marks = [int(n) for n in re.findall(r"\[(\d+)\]", text)]
            if not marks or any(n < 1 or n > len(citations) for n in marks):
                raise ValueError("Unverifiable citation")
        result["text"] += "\n\n" + message("notice", lang)
        return result
    except (ValueError, TypeError, AttributeError, ValidationError) as exc:
        raise AIUnavailable("ai_invalid_output") from exc


def event(name: str, data: dict) -> str:
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def execute(
    db: Session,
    settings: Settings,
    provider: AIProvider,
    identity: str,
    feature: str,
    inputs: Any,
    role: str,
    document_id: int | None = None,
    citations: list[dict] | None = None,
    stream: bool = False,
    cache_identity: str | None = None,
    lang: Lang = "de",
) -> Any:
    references = citations or []
    cacheable = feature not in ("ask", "draft", "classify")
    key = store.cache_key(feature, cache_identity or document_id, inputs, role, settings, lang)
    found = store.read_cache(db, key) if cacheable else None
    if found is not None:
        result = {**found, "cached": True}
        if stream:

            async def cached_events():
                yield event("done", result)

            return StreamingResponse(cached_events(), media_type="text/event-stream")
        return result
    store.reserve(db, identity, settings, lang)
    request_messages = prompts.messages(feature, role, inputs, lang)

    def finish(text: str) -> dict:
        result = normalize(feature, text, inputs, references, lang)
        if cacheable:
            store.write_cache(db, key, feature, document_id, settings, result)
        return result

    if not stream:
        text = await asyncio.to_thread(provider.complete, request_messages)
        return finish(text)

    async def events():
        text = ""
        try:
            async for token in provider.stream(request_messages):
                text += token
                if len(text) > 20_000:
                    raise AIUnavailable("ai_invalid_output")
                yield event("token", {"text": token})
            yield event("done", finish(text))
        except AIUnavailable as exc:
            yield event(
                "error",
                {
                    "code": str(exc),
                    "message": message("ai_incomplete", lang),
                },
            )

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
