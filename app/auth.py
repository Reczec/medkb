"""Login: password hashing, JWT tokens and the role dependencies used by the routers."""

from __future__ import annotations

import base64
import hashlib
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.i18n import RequestLang, message
from app.models import User

Role = Literal["admin", "doctor", "patient"]
ROLES: tuple[Role, ...] = ("admin", "doctor", "patient")
ALGORITHM = "HS256"

_hasher = PasswordHash((BcryptHasher(),))


def _prehash(password: str) -> str:
    # bcrypt only reads 72 bytes and bcrypt 5 rejects longer input; a SHA-256 digest keeps every
    # character significant and the input short.
    return base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()


def hash_password(password: str) -> str:
    return _hasher.hash(_prehash(password))


def verify_password(password: str, hashed: str) -> bool:
    try:
        return _hasher.verify(_prehash(password), hashed)
    except ValueError:  # malformed hash
        return False


def create_token(user: User, settings: Settings) -> str:
    expires = datetime.now(UTC) + timedelta(hours=settings.jwt_hours)
    claims = {"sub": str(user.id), "role": user.role, "exp": expires}
    return jwt.encode(claims, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str, settings: Settings) -> dict[str, Any]:
    """Raises jwt.InvalidTokenError for expired, tampered or foreign tokens."""
    return jwt.decode(
        token, settings.jwt_secret, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]}
    )


_bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Nicht angemeldet oder Sitzung abgelaufen.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        claims = decode_token(credentials.credentials, settings)
        user = db.get(User, int(claims["sub"]))
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise unauthorized from None
    if user is None:
        raise unauthorized
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def require_role(*roles: Role):
    """Dependency: the logged-in user must have one of the given roles (else 403)."""

    def check(user: CurrentUser, lang: RequestLang) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, message("forbidden", lang))
        return user

    return check
