"""Create the login accounts the configuration asks for."""

from __future__ import annotations

import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.config import Settings
from app.models import User

# username -> (role, display name). Their passwords are random: they log in only via demo login.
DEMO_USERS = {
    "demo-admin": ("admin", "Admin"),
    "demo-doctor": ("doctor", "Dr. Demo"),
    "demo-patient": ("patient", "Patient Demo"),
}


def _upsert(db: Session, username: str, role: str, display_name: str, password: str | None):
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        user = User(
            username=username,
            role=role,
            display_name=display_name,
            password_hash=hash_password(password or secrets.token_urlsafe(32)),
        )
        db.add(user)
    elif password is not None:
        user.password_hash = hash_password(password)
    return user


def ensure_users(db: Session, settings: Settings) -> None:
    """Idempotent: demo accounts in demo mode, and an "admin" login if ADMIN_PASSWORD is set."""
    if settings.demo_mode:
        for username, (role, display_name) in DEMO_USERS.items():
            _upsert(db, username, role, display_name, None)
    if settings.admin_password:
        _upsert(db, "admin", "admin", "Admin", settings.admin_password)
    db.commit()
