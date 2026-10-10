"""Login: password hashing, JWT tokens and the role dependencies used by the routers."""

from __future__ import annotations

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
from app.models import User

Role = Literal["admin", "doctor", "patient"]
ROLES: tuple[Role, ...] = ("admin", "doctor", "patient")
ALGORITHM = "HS256"

_hasher = PasswordHash((BcryptHasher(),))


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return _hasher.verify(password, hashed)
    except ValueError:  # malformed hash
        return False


def create_token(user: User, settings: Settings) -> str:
    expires = datetime.now(UTC) + timedelta(hours=settings.jwt_hours)
    claims = {"sub": str(user.id), "role": user.role, "exp": expires}
    return jwt.encode(claims, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str, settings: Settings) -> dict[str, Any]:
    """Raises jwt.InvalidTokenError for expired, tampered or foreign tokens."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])


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

    def check(user: CurrentUser) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Keine Berechtigung für diese Aktion.")
        return user

    return check
