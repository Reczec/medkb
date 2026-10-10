"""JSON archive: export all documents to a file, list archives, restore from one."""

from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import Document
from app.schemas import ArchiveEntry, ArchiveInfo, DocumentOut
from app.services import log_audit

ARCHIVE_FORMAT_VERSION = 1
# Only names produced by this module are accepted (prevents path traversal).
ARCHIVE_NAME_RE = re.compile(r"^archive_\d{8}_\d{6}(?:_[a-z0-9-]{1,30})?\.json$")


class ArchiveError(Exception):
    """Raised for unknown or unreadable archives; the API maps it to 4xx responses."""

    def __init__(self, message: str, *, not_found: bool = False) -> None:
        super().__init__(message)
        self.not_found = not_found


def _info_from_file(path: Path) -> ArchiveInfo:
    stat = path.stat()
    try:
        count = int(json.loads(path.read_text(encoding="utf-8")).get("document_count", 0))
    except (OSError, ValueError, AttributeError):
        count = 0
    return ArchiveInfo(
        name=path.name,
        created_at=datetime.fromtimestamp(stat.st_mtime, tz=UTC),
        size_bytes=stat.st_size,
        document_count=count,
    )


def create_archive(
    db: Session, archive_dir: Path, suffix: str | None = None, actor: str | None = None
) -> ArchiveInfo:
    """Write every document (content, metadata, keywords) into a new JSON file."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    documents = db.scalars(select(Document).order_by(Document.id)).all()
    now = datetime.now(UTC)

    payload = {
        "format_version": ARCHIVE_FORMAT_VERSION,
        "created_at": now.isoformat(),
        "document_count": len(documents),
        "documents": [
            DocumentOut.model_validate(d).model_dump(mode="json", exclude={"id"}) for d in documents
        ],
    }

    stamp = f"archive_{now:%Y%m%d_%H%M%S}"
    path = archive_dir / (f"{stamp}_{suffix}.json" if suffix else f"{stamp}.json")
    counter = 2
    while path.exists():  # two archives within the same second
        tag = f"{suffix}-{counter}" if suffix else str(counter)
        path = archive_dir / f"{stamp}_{tag}.json"
        counter += 1

    # Write atomically: a crash must never leave a half-written archive behind.
    fd, tmp_name = tempfile.mkstemp(dir=archive_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise

    log_audit(db, "archive_create", None, f"{path.name} ({len(documents)} documents)", actor)
    db.commit()
    return _info_from_file(path)


def list_archives(archive_dir: Path) -> list[ArchiveInfo]:
    if not archive_dir.is_dir():
        return []
    files = [p for p in archive_dir.iterdir() if ARCHIVE_NAME_RE.match(p.name) and p.is_file()]
    infos = [_info_from_file(p) for p in files]
    return sorted(infos, key=lambda info: info.name, reverse=True)


def resolve_archive(archive_dir: Path, name: str) -> Path:
    if not ARCHIVE_NAME_RE.match(name):
        raise ArchiveError("Invalid archive name.")
    path = archive_dir / name
    if not path.is_file():
        raise ArchiveError("Archive not found.", not_found=True)
    return path


def _read_entries(path: Path) -> list[ArchiveEntry]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        documents = raw["documents"]
        if raw.get("format_version") != ARCHIVE_FORMAT_VERSION or not isinstance(documents, list):
            raise ValueError("unsupported format")
        return [ArchiveEntry.model_validate(item) for item in documents]
    except (OSError, ValueError, KeyError, TypeError, ValidationError) as exc:
        raise ArchiveError(f"Archive is corrupt or has an unsupported format: {exc}") from exc


def restore_archive(
    db: Session, archive_dir: Path, name: str, actor: str | None = None
) -> tuple[int, ArchiveInfo]:
    """Replace all documents with the content of an archive.

    The archive is fully validated first. Before anything is deleted, the current state is
    saved as an automatic "pre-restore" archive. Document ids are not preserved.
    """
    entries = _read_entries(resolve_archive(archive_dir, name))
    backup = create_archive(db, archive_dir, suffix="pre-restore", actor=actor)

    db.execute(delete(Document))
    for entry in entries:
        db.add(
            Document(
                title=entry.title,
                content=entry.content,
                category=entry.category,
                doc_type=entry.doc_type.value,
                keywords=entry.keywords,
                source=entry.source,
                auto_classified=entry.auto_classified,
                term_en=entry.term_en,
                icd11_code=entry.icd11_code,
                medications=entry.medications,
                sections=entry.sections.model_dump() if entry.sections else None,
                further_reading=[link.model_dump() for link in entry.further_reading],
                ai_generated=entry.ai_generated,
                created_at=entry.created_at,
                updated_at=entry.updated_at,
            )
        )
    log_audit(db, "archive_restore", None, f"{name} ({len(entries)} documents)", actor)
    db.commit()
    return len(entries), backup
