"""Shared HTTP helpers for the source clients."""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Any

import httpx
from fastapi import Depends

from app.config import Settings, get_settings
from app.sources.cache import SourceUnavailable

USER_AGENT = "MedKB/2 (demo knowledge base; +https://github.com/Reczec/medkb)"


@lru_cache
def _shared_client(timeout: float) -> httpx.Client:
    # One pooled client per process: creating a client loads the CA bundle (~0.3 s), which
    # would otherwise be paid on every request, cache hits included. httpx.Client is thread-safe.
    return httpx.Client(timeout=timeout, headers={"User-Agent": USER_AGENT})


def http_client(settings: Annotated[Settings, Depends(get_settings)]) -> httpx.Client:
    return _shared_client(settings.sources_timeout)


def get_json(client: httpx.Client, url: str, **kwargs: Any) -> Any:
    """GET and decode JSON; every failure becomes SourceUnavailable."""
    try:
        response = client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise SourceUnavailable(f"{url}: {exc}") from exc
