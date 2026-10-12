"""Bounded hybrid retrieval with explicit lexical fallback and no forced nearest neighbor."""

import asyncio
import re
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.ai import retrieval as lexical
from app.ai.provider import AIUnavailable
from app.ai.schemas import AskRequest
from app.ai.store import reserve
from app.config import Settings
from app.i18n import Lang
from app.rag.chunks import Chunk, chunks
from app.rag.embeddings import EmbeddingProvider, get_embeddings, normalize
from app.rag.index import load_current


@dataclass
class RetrievalResult:
    citations: list[dict]
    entries: list[dict]
    mode: str
    reason: str | None = None
    indexed_chunks: int = 0

    @property
    def metadata(self) -> dict:
        data = {"mode": self.mode, "indexed_chunks": self.indexed_chunks}
        if self.reason:
            data["reason"] = self.reason
        return data


def evidence(
    selected: list[Chunk], mode: str, reason: str | None = None, indexed_chunks: int = 0
) -> RetrievalResult:
    references: list[dict] = []
    entries: list[dict] = []
    budget = 6000
    for chunk in selected:
        title = chunk.title[:200]
        available = budget - len(title) - len(chunk.section)
        if available <= 0:
            break
        text = chunk.text[: min(800, available)]
        budget -= len(title) + len(chunk.section) + len(text)
        ref = {
            "index": len(references) + 1,
            "id": chunk.document_id,
            "title": title,
            "section": chunk.section,
            "excerpt": text,
        }
        references.append(ref)
        entries.append(
            {
                "index": ref["index"],
                "id": ref["id"],
                "title": title,
                "section": chunk.section,
                "content": text,
            }
        )
    return RetrievalResult(references, entries, mode, reason, indexed_chunks)


def fallback(db: Session, body: AskRequest, lang: Lang, reason: str) -> RetrievalResult:
    focus = lexical.query(body).split()
    words = set(re.findall(r"[^\W_]+", body.question.lower()))
    intent = {
        section
        for section, terms in {
            "therapy": (
                "treat treated treating treatment therapy hilft helfen "
                "behandlung behandelt therapie"
            ),
            "diagnostics": (
                "diagnose diagnosed diagnosis diagnostics diagnostic "
                "untersucht untersuchung diagnostik diagnostiziert"
            ),
            "red_flags": "warning warnings emergency urgent warnzeichen notfall gefährlich",
            "symptoms": "symptom symptoms symptome beschwerden",
            "causes": "cause causes ursache ursachen",
        }.items()
        if words.intersection(terms.split())
    }
    selected = []
    for doc in lexical.find(db, body):
        candidates = chunks(doc, lang)
        candidates.sort(
            key=lambda c: (
                c.section not in intent,
                -sum(t in c.text.lower() for t in focus),
                c.offset,
            )
        )
        selected.extend(candidates[:2])
    return evidence(selected, "lexical", reason)


async def retrieve_async(*args) -> RetrievalResult:
    """Keep the request session owned until its bounded DB worker actually finishes."""
    worker = asyncio.create_task(asyncio.to_thread(retrieve, *args))
    try:
        return await asyncio.shield(worker)
    except asyncio.CancelledError:
        while not worker.done():
            try:
                await asyncio.shield(worker)
            except asyncio.CancelledError:
                continue
            except Exception:
                break
        if not worker.cancelled():
            worker.exception()  # consume a failed abandoned result; never start completion
        raise


def retrieve(
    db: Session,
    body: AskRequest,
    lang: Lang,
    settings: Settings,
    provider: EmbeddingProvider | None,
    client_id: str,
) -> RetrievalResult:
    if not lexical.query(body):
        return RetrievalResult([], [], "hybrid" if settings.rag_enabled else "lexical")
    if not settings.rag_enabled:
        return fallback(db, body, lang, "disabled")
    try:
        indexed = load_current(db, settings, lang)
    except ValueError:
        indexed = None
    if not indexed:
        return fallback(db, body, lang, "index_incomplete")
    question = body.question
    if not lexical.terms(question):
        question += "\nPrevious topic: " + lexical.query(body)
    reserve(db, client_id, settings, lang)
    try:
        embedder = provider or get_embeddings(settings)
        returned = embedder.embed([question[:800]], "query")
        if len(returned) != 1:
            raise AIUnavailable("embedding_unavailable")
        vector = normalize(returned[0])
    except AIUnavailable:
        return fallback(db, body, lang, "embedding_unavailable")
    # The provider request may overlap an edit/reset. Rebind only to the current corpus.
    db.expire_all()
    try:
        indexed = load_current(db, settings, lang)
    except ValueError:
        indexed = None
    if not indexed:
        return fallback(db, body, lang, "index_incomplete")
    ranked = sorted(
        [
            (sum(a * b for a, b in zip(vector, stored, strict=True)), chunk)
            for chunk, stored in indexed
        ],
        key=lambda item: (-item[0], item[1].document_id, item[1].section, item[1].offset),
    )
    qualified = [(score, chunk) for score, chunk in ranked if score >= settings.rag_min_similarity]
    semantic_ids = list(dict.fromkeys(chunk.document_id for _, chunk in qualified))
    lexical_ids = [doc.id for doc in lexical.find(db, body)]
    scores = {doc_id: 1 / (60 + rank) for rank, doc_id in enumerate(semantic_ids, 1)}
    for rank, doc_id in enumerate(lexical_ids, 1):
        if doc_id in scores:
            scores[doc_id] += 1 / (60 + rank)
    documents = sorted(scores, key=lambda doc_id: (-scores[doc_id], doc_id))[:5]
    selected = []
    for doc_id in documents:
        selected.extend([chunk for _, chunk in qualified if chunk.document_id == doc_id][:2])
    return evidence(selected, "hybrid", indexed_chunks=len(indexed))
