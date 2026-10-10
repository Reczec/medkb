"""Login: password hashing, JWT tokens and the role dependencies used by the routers."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from app.config import Settings
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
