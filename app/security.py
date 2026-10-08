"""Admin access via a shared secret token (header ``X-Admin-Token``)."""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.config import Settings, get_settings


def require_admin(
    settings: Annotated[Settings, Depends(get_settings)],
    x_admin_token: Annotated[str | None, Header()] = None,
) -> None:
    if not settings.admin_token:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Admin functions are disabled: set the ADMIN_TOKEN environment variable.",
        )
    if not x_admin_token or not secrets.compare_digest(
        x_admin_token.encode(), settings.admin_token.encode()
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing admin token.")
