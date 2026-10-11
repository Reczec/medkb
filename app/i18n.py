"""Request language and the few texts the server itself writes (everything else is data)."""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import Depends, Request

Lang = Literal["en", "de"]
LANGS: tuple[Lang, ...] = ("en", "de")
DEFAULT_LANG: Lang = "en"

MESSAGES: dict[str, dict[Lang, str]] = {
    "invalid_login": {
        "en": "Wrong username or password",
        "de": "Benutzername oder Passwort falsch",
    },
    "forbidden": {
        "en": "You are not allowed to do this.",
        "de": "Keine Berechtigung für diese Aktion.",
    },
    "ai_limit": {
        "en": "Daily AI limit reached. Please try again tomorrow.",
        "de": "KI-Tageslimit erreicht. Bitte morgen erneut versuchen.",
    },
    "ai_incomplete": {
        "en": "The AI answer could not be completed. Please try again.",
        "de": "KI-Antwort konnte nicht vollständig erstellt werden. Bitte erneut versuchen.",
    },
    "ai_no_entries": {
        "en": "There are no matching entries in the knowledge base.",
        "de": "Es gibt keine passenden Einträge in der Wissensdatenbank.",
    },
    "ai_no_streaming": {
        "en": "This feature does not support streaming.",
        "de": "Diese Funktion unterstützt kein Streaming.",
    },
    "ai_no_abstract": {
        "en": "No abstract available.",
        "de": "Kein Abstract verfügbar.",
    },
    "not_signed_in": {
        "en": "Not signed in or the session has expired.",
        "de": "Nicht angemeldet oder Sitzung abgelaufen.",
    },
    "demo_disabled": {
        "en": "Demo access is switched off.",
        "de": "Demo-Zugang ist deaktiviert.",
    },
    "demo_missing": {
        "en": "Demo access is not set up.",
        "de": "Demo-Zugang ist nicht eingerichtet.",
    },
    "notice": {
        "en": "Prototype with example data – not medical advice.",
        "de": "Prototyp mit Beispieldaten – keine medizinische Beratung.",
    },
}


def parse_language(header: str | None) -> Lang:
    """Only the first entry of Accept-Language counts, and only its primary subtag."""
    if not header:
        return DEFAULT_LANG
    primary = header.split(",")[0].split(";")[0].strip().lower().split("-")[0]
    return primary if primary in LANGS else DEFAULT_LANG  # type: ignore[return-value]


def request_language(request: Request) -> Lang:
    return parse_language(request.headers.get("accept-language"))


RequestLang = Annotated[Lang, Depends(request_language)]


def message(code: str, lang: Lang) -> str:
    return MESSAGES[code][lang]
