"""Role-gated AI assistance; generated drafts never write documents."""

import asyncio
from typing import Annotated, Any, Literal

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.ai import prompts, retrieval, service, store
from app.ai.provider import AIProvider, get_provider
from app.ai.schemas import AskRequest, DraftRequest, StudyRequest
from app.auth import CurrentUser, require_role
from app.config import Settings, get_settings
from app.database import get_db
from app.models import Document
from app.schemas import ClassifyRequest
from app.sources.cache import cached
from app.sources.http import http_client
from app.sources.pubmed import fetch_abstract

router = APIRouter(prefix="/api/ai", tags=["ai"])
Db = Annotated[Session, Depends(get_db)]
Config = Annotated[Settings, Depends(get_settings)]
Provider = Annotated[AIProvider, Depends(get_provider)]
Staff = Annotated[Any, Depends(require_role("admin", "doctor"))]
Admin = Annotated[Any, Depends(require_role("admin"))]


def client_ip(request: Request, settings: Settings) -> str:
    """The visitor's address: the trusted proxy header if configured, else the connection."""
    if settings.client_ip_header:
        forwarded = request.headers.get(settings.client_ip_header, "").split(",")[0].strip()
        if forwarded:
            return forwarded
    return request.client.host if request.client else "unknown"


def identity(request: Request, settings: Settings) -> str:
    return store.client_identity(client_ip(request, settings), settings)


def document_access(feature: str, user: CurrentUser):
    if feature == "summary" and user.role == "patient":
        raise HTTPException(403, "Keine Berechtigung für diese Aktion.")
    return user


@router.post("/documents/{document_id}/{feature}")
async def document_assistance(
    document_id: int,
    feature: Literal["explain", "red-flags", "summary"],
    request: Request,
    db: Db,
    settings: Config,
    user: Annotated[Any, Depends(document_access)],
    provider: Provider,
    stream: bool = False,
):
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(404, "Document not found.")
    if stream and feature == "red-flags":
        raise HTTPException(422, "Diese Funktion unterstützt kein Streaming.")
    return await service.execute(
        db,
        settings,
        provider,
        identity(request, settings),
        feature,
        service.document_inputs(document),
        user.role,
        document_id=document_id,
        stream=stream,
        cache_identity=service.document_cache_identity(document),
    )


@router.post("/ask")
async def ask(
    body: AskRequest,
    request: Request,
    user: CurrentUser,
    db: Db,
    settings: Config,
    provider: Provider,
    stream: bool = False,
):
    documents = retrieval.find(db, body)
    references = [{"index": i, "id": d.id, "title": d.title} for i, d in enumerate(documents, 1)]
    if not documents:
        result = {
            "text": "Es gibt keine passenden Einträge in der Wissensdatenbank. " + prompts.NOTICE,
            "cached": False,
            "citations": [],
        }
        if stream:

            async def events():
                yield service.event("done", result)

            from fastapi.responses import StreamingResponse

            return StreamingResponse(events(), media_type="text/event-stream")
        return result
    inputs = {
        **body.model_dump(),
        "entries": [
            {**ref, "content": doc.content} for ref, doc in zip(references, documents, strict=True)
        ],
    }
    return await service.execute(
        db,
        settings,
        provider,
        identity(request, settings),
        "ask",
        inputs,
        user.role,
        citations=references,
        stream=stream,
    )


@router.post("/draft")
async def draft(
    body: DraftRequest,
    request: Request,
    user: Admin,
    db: Db,
    settings: Config,
    provider: Provider,
    stream: bool = False,
):
    return await service.execute(
        db,
        settings,
        provider,
        identity(request, settings),
        "draft",
        body.model_dump(),
        user.role,
        stream=stream,
    )


@router.post("/classify")
async def classify(
    body: ClassifyRequest,
    request: Request,
    user: Admin,
    db: Db,
    settings: Config,
    provider: Provider,
):
    return await service.execute(
        db,
        settings,
        provider,
        identity(request, settings),
        "classify",
        body.model_dump(),
        user.role,
    )


@router.post("/studies/summarize")
async def study_summary(
    body: StudyRequest,
    request: Request,
    user: Staff,
    db: Db,
    settings: Config,
    provider: Provider,
    client: Annotated[httpx.Client, Depends(http_client)],
):
    # The session is used sequentially: no DB operation overlaps this awaited worker.
    abstract = await asyncio.to_thread(
        cached,
        db,
        f"pubmed-abstract:{body.pmid}",
        settings,
        lambda: fetch_abstract(client, body.pmid, settings),
    )
    if abstract.status == "unavailable":
        raise HTTPException(503, "ai_source_unavailable")
    if not abstract.data:
        raise HTTPException(404, "Kein Abstract verfügbar.")
    return await service.execute(
        db,
        settings,
        provider,
        identity(request, settings),
        "study",
        {"pmid": body.pmid, "abstract": abstract.data},
        user.role,
    )


@router.get("/usage")
def usage(user: Staff, db: Db, settings: Config):
    return {"today": store.usage_today(db), "limit": settings.ai_daily_limit}
