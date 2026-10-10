"""Shared HTTP helpers for the source clients."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated, Any

import httpx
from fastapi import Depends

from app.config import Settings, get_settings
from app.sources.cache import SourceUnavailable

USER_AGENT = "MedKB/2 (demo knowledge base; +https://github.com/Reczec/medkb)"


def http_client(settings: Annotated[Settings, Depends(get_settings)]) -> Iterator[httpx.Client]:
    """One client per request, with the configured timeout."""
    with httpx.Client(timeout=settings.sources_timeout, headers={"User-Agent": USER_AGENT}) as c:
        yield c


def get_json(client: httpx.Client, url: str, **kwargs: Any) -> Any:
    """GET and decode JSON; every failure becomes SourceUnavailable."""
    try:
        response = client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise SourceUnavailable(f"{url}: {exc}") from exc
