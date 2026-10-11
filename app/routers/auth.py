"""Login endpoints: password login, one-click demo login, current user, public options."""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import CurrentUser, create_token, hash_password, verify_password
from app.config import Settings, get_settings
from app.database import get_db
from app.i18n import RequestLang, message
from app.models import User
from app.schemas import AuthOptions, DemoLoginRequest, LoginRequest, TokenOut, UserOut
from app.users import DEMO_USERS

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Checked against when the username is unknown, so both failures take the same time.
_DUMMY_HASH = hash_password(secrets.token_urlsafe(16))

DbSession = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]


def _token_for(user: User, settings: Settings) -> TokenOut:
    return TokenOut(access_token=create_token(user, settings), user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest, db: DbSession, settings: AppSettings, lang: RequestLang) -> TokenOut:
    user = db.scalar(select(User).where(User.username == data.username))
    # Same message for unknown users and wrong passwords: nothing to learn from the answer.
    valid = verify_password(data.password, user.password_hash if user else _DUMMY_HASH)
    if user is None or not valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, message("invalid_login", lang))
    return _token_for(user, settings)


@router.post("/demo", response_model=TokenOut)
def demo_login(data: DemoLoginRequest, db: DbSession, settings: AppSettings) -> TokenOut:
    if not settings.demo_mode:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Demo-Zugang ist deaktiviert.")
    username = next(name for name, (role, _) in DEMO_USERS.items() if role == data.role)
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Demo-Zugang ist nicht eingerichtet.")
    return _token_for(user, settings)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> User:
    return user


@router.get("/options", response_model=AuthOptions)
def options(settings: AppSettings) -> AuthOptions:
    return AuthOptions(demo_mode=settings.demo_mode)
