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
from app.schemas import DocumentCreate, DocumentOut


def document_inputs(document: Any) -> dict:
    """Bind to semantic content, not timestamps refreshed by an unchanged demo reset."""
    return DocumentOut.model_validate(document).model_dump(
        mode="json", exclude={"created_at", "updated_at"}
    )


def normalize(feature: str, text: str, inputs: Any, citations: list[dict]) -> dict:
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
        result["text"] += "\n\n" + prompts.NOTICE
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
) -> Any:
    references = citations or []
    cacheable = feature not in ("ask", "draft", "classify")
    key = store.cache_key(feature, document_id, inputs, role, settings)
    found = store.read_cache(db, key) if cacheable else None
    if found is not None:
        result = {**found, "cached": True}
        if stream:

            async def cached_events():
                yield event("done", result)

            return StreamingResponse(cached_events(), media_type="text/event-stream")
        return result
    store.reserve(db, identity, settings)
    request_messages = prompts.messages(feature, role, inputs)

    def finish(text: str) -> dict:
        result = normalize(feature, text, inputs, references)
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
                    "message": (
                        "KI-Antwort konnte nicht vollständig erstellt werden. "
                        "Bitte erneut versuchen."
                    ),
                },
            )

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
