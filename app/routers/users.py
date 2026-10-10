"""Admin: list the login accounts."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import require_role
from app.database import get_db
from app.models import User
from app.schemas import UserListItem

router = APIRouter(prefix="/api", tags=["admin"], dependencies=[Depends(require_role("admin"))])


@router.get("/users", response_model=list[UserListItem])
def list_users(db: Annotated[Session, Depends(get_db)]) -> list[User]:
    return list(db.scalars(select(User).order_by(User.role, User.username)).all())
