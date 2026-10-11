"""WHO ICD-11 API (MMS linearization): OAuth2 client credentials, code lookup, entity details."""

from __future__ import annotations

import threading
import time
from typing import Any

import httpx

from app.config import Settings
from app.schemas import Icd11Entry
from app.sources.cache import SourceUnavailable
from app.sources.http import get_json

TOKEN_URL = "https://icdaccessmanagement.who.int/connect/token"
API = "https://id.who.int/icd/release/11/{release}/mms"
TOKEN_MARGIN_SECONDS = 60

# (client id, access token, expiry as time.monotonic()); shared by all requests of the process.
_token: tuple[str, str, float] | None = None
_token_lock = threading.Lock()


def reset_token_cache() -> None:
    global _token
    _token = None


def is_configured(settings: Settings) -> bool:
    return bool(settings.icd_client_id and settings.icd_client_secret)


def _access_token(client: httpx.Client, settings: Settings) -> str:
    global _token
    with _token_lock:
        if _token and _token[0] == settings.icd_client_id and time.monotonic() < _token[2]:
            return _token[1]
        try:
            response = client.post(
                TOKEN_URL,
                data={
                    "client_id": settings.icd_client_id,
                    "client_secret": settings.icd_client_secret,
                    "scope": "icdapi_access",
                    "grant_type": "client_credentials",
                },
            )
            response.raise_for_status()
            body = response.json()
            token = str(body["access_token"])
            lifetime = float(body.get("expires_in", 3600))
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
            raise SourceUnavailable(f"ICD-11 token: {exc}") from exc
        _token = (settings.icd_client_id, token, time.monotonic() + lifetime - TOKEN_MARGIN_SECONDS)
        return token


def _headers(token: str, language: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "API-Version": "v2",
        "Accept-Language": language,
        "Accept": "application/json",
    }


def _value(field: Any) -> str | None:
    if isinstance(field, dict):
        value = field.get("@value")
        return str(value).strip() or None if value else None
    return None


def lookup_code(
    client: httpx.Client, code: str, settings: Settings, language: str | None = None
) -> Icd11Entry | None:
    """Title and definition for an MMS code in ``language`` (default: settings.icd_language);
    None if the code does not exist."""
    requested = language or settings.icd_language
    headers = _headers(_access_token(client, settings), requested)
    base = API.format(release=settings.icd_release)
    try:
        info = client.get(f"{base}/codeinfo/{code}", headers=headers)
    except httpx.HTTPError as exc:
        raise SourceUnavailable(f"ICD-11 codeinfo: {exc}") from exc
    if info.status_code == 404:
        return None
    if info.status_code == 401:
        reset_token_cache()
    try:
        info.raise_for_status()
        stem_id = str(info.json()["stemId"])
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise SourceUnavailable(f"ICD-11 codeinfo: {exc}") from exc

    entity = get_json(client, stem_id.replace("http://", "https://", 1), headers=headers)
    title = _value(entity.get("title")) if isinstance(entity, dict) else None
    if not title:
        raise SourceUnavailable("ICD-11 entity without title")
    language = entity["title"].get("@language") or requested
    entity_id = stem_id.split("/mms/", 1)[-1]
    try:
        return Icd11Entry(
            code=str(entity.get("code") or code),
            title=title,
            definition=_value(entity.get("definition")),
            url=f"https://icd.who.int/browse/{settings.icd_release}/mms/{language}#{entity_id}",
            release=settings.icd_release,
            language=language,
        )
    except ValueError as exc:
        raise SourceUnavailable(f"unexpected ICD-11 entity: {exc}") from exc
