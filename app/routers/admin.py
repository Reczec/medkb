"""Admin API: archives (export / list / download / restore) and the audit log."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import services
from app.archive import (
    ArchiveError,
    create_archive,
    list_archives,
    resolve_archive,
    restore_archive,
)
from app.config import Settings, get_settings
from app.database import get_db
from app.schemas import ArchiveInfo, AuditOut, RestoreResult
from app.security import require_admin

router = APIRouter(prefix="/api", tags=["admin"], dependencies=[Depends(require_admin)])

DbSession = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]


def _http_error(exc: ArchiveError) -> HTTPException:
    code = status.HTTP_404_NOT_FOUND if exc.not_found else status.HTTP_400_BAD_REQUEST
    return HTTPException(code, str(exc))


@router.post("/archives", response_model=ArchiveInfo, status_code=status.HTTP_201_CREATED)
def make_archive(db: DbSession, settings: AppSettings) -> ArchiveInfo:
    return create_archive(db, settings.archive_dir)


@router.get("/archives", response_model=list[ArchiveInfo])
def get_archives(settings: AppSettings) -> list[ArchiveInfo]:
    return list_archives(settings.archive_dir)


@router.get("/archives/{name}")
def download_archive(name: str, settings: AppSettings) -> FileResponse:
    try:
        path = resolve_archive(settings.archive_dir, name)
    except ArchiveError as exc:
        raise _http_error(exc) from exc
    return FileResponse(path, media_type="application/json", filename=name)


@router.post("/archives/{name}/restore", response_model=RestoreResult)
def restore(name: str, db: DbSession, settings: AppSettings) -> RestoreResult:
    try:
        restored, backup = restore_archive(db, settings.archive_dir, name)
    except ArchiveError as exc:
        raise _http_error(exc) from exc
    return RestoreResult(restored=restored, backup=backup)


@router.get("/audit", response_model=list[AuditOut])
def audit_log(db: DbSession, limit: Annotated[int, Query(ge=1, le=200)] = 50) -> list:
    return services.list_audit(db, limit)
