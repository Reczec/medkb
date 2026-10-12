"""Resumable operator-built index. Public reads never generate document embeddings."""

import time
from dataclasses import dataclass

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ai.provider import AIUnavailable
from app.ai.store import reserve
from app.config import Settings
from app.i18n import Lang
from app.models import Document, Embedding
from app.rag.chunks import Chunk, chunks, signature
from app.rag.embeddings import EmbeddingProvider, normalize


@dataclass(frozen=True)
class IndexStatus:
    total: int
    ready: int


@dataclass(frozen=True)
class BuildReport(IndexStatus):
    failed: int = 0
    requests: int = 0


def corpus(db: Session, settings: Settings, langs: tuple[Lang, ...] = ("de", "en")) -> list[Chunk]:
    result: list[Chunk] = []
    for doc in db.scalars(select(Document).order_by(Document.id)):
        for lang in langs:
            result.extend(chunks(doc, lang))
            if len(result) > settings.rag_max_chunks:
                raise ValueError("RAG corpus exceeds configured chunk bound")
    return result


def vectors(db: Session, current: list[Chunk]) -> dict[str, list[float]]:
    keys = sorted({chunk.key for chunk in current})
    result = {}
    for start in range(0, len(keys), 256):
        for row in db.scalars(
            select(Embedding).where(Embedding.key.in_(keys[start : start + 256]))
        ):
            if row.signature != signature():
                continue
            try:
                result[row.key] = normalize(row.vector)
            except AIUnavailable:
                continue
    return result


def load_current(
    db: Session, settings: Settings, lang: Lang
) -> list[tuple[Chunk, list[float]]] | None:
    current = corpus(db, settings, (lang,))
    stored = vectors(db, current)
    if any(chunk.key not in stored for chunk in current):
        return None
    return [(chunk, stored[chunk.key]) for chunk in current]


def _write(db: Session, chunk: Chunk, vector: list[float]) -> None:
    try:
        with db.begin_nested():
            db.add(Embedding(key=chunk.key, signature=signature(), vector=vector))
            db.flush()
    except IntegrityError:
        # Also repairs a corrupt stored row. A concurrent valid vector remains valid.
        db.execute(
            update(Embedding)
            .where(Embedding.key == chunk.key)
            .values(signature=signature(), vector=vector)
        )


def build_index(
    db: Session,
    settings: Settings,
    provider: EmbeddingProvider,
    pause: float = 4,
    cleanup: bool = False,
    limit_documents: int | None = None,
) -> BuildReport:
    if pause < 0 or (limit_documents is not None and limit_documents < 1):
        raise ValueError("Invalid index options")
    if cleanup and limit_documents is not None:
        raise ValueError("Cleanup requires the complete corpus")
    current = corpus(db, settings)
    if limit_documents is not None:
        ids = list(dict.fromkeys(chunk.document_id for chunk in current))[:limit_documents]
        current = [chunk for chunk in current if chunk.document_id in ids]
    unique = {chunk.key: chunk for chunk in current}
    stored = vectors(db, current)
    missing = [chunk for key, chunk in unique.items() if key not in stored]
    trusted = settings.model_copy(update={"ai_client_daily_limit": settings.ai_daily_limit})
    failed = requests = 0
    for start in range(0, len(missing), 16):
        if requests and pause:
            time.sleep(pause)
        batch = missing[start : start + 16]
        reserve(db, "rag-index", trusted)
        requests += 1
        try:
            returned = provider.embed([chunk.embedding_text for chunk in batch], "document")
            if len(returned) != len(batch):
                raise AIUnavailable("embedding_unavailable")
            valid = [normalize(vector) for vector in returned]
        except AIUnavailable:
            failed += len(batch)
            continue
        # Refresh identities after the remote call; never publish stale ready coverage.
        db.expire_all()
        live = {chunk.key for chunk in corpus(db, settings)}
        try:
            for chunk, vector in zip(batch, valid, strict=True):
                if chunk.key in live:
                    _write(db, chunk, vector)
            db.commit()
        except Exception:
            db.rollback()
            raise
    db.expire_all()
    final = corpus(db, settings)
    if limit_documents is not None:
        final = [chunk for chunk in final if chunk.document_id in ids]
    if cleanup:
        keep = {chunk.key for chunk in final}
        # Bounded deletion per row avoids SQLite parameter limits on large indexes.
        for key in db.scalars(select(Embedding.key)):
            if key not in keep:
                db.execute(delete(Embedding).where(Embedding.key == key))
        db.commit()
    return BuildReport(len({c.key for c in final}), len(vectors(db, final)), failed, requests)
