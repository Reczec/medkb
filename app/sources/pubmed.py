"""PubMed via the NCBI E-utilities: esearch for the newest PMIDs, esummary for their details."""

from __future__ import annotations

import html
import re
import threading
import time
from typing import Any

import httpx

from app.config import Settings
from app.schemas import Study
from app.sources.cache import SourceUnavailable

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
MAX_AUTHORS = 3
# NCBI allows 3 requests per second without an API key and 10 with one; it counts strictly,
# so keep a margin, and retry once after a pause if it still answers 429.
MIN_INTERVAL = 0.4
MIN_INTERVAL_WITH_KEY = 0.12
RETRY_AFTER_429 = 1.0

_last_request = 0.0
_rate_lock = threading.Lock()

# MeSH heading per specialty for the dashboard tile "Neueste Studien".
CATEGORY_TERMS: dict[str, str] = {
    "HNO": "Otorhinolaryngologic Diseases",
    "Augenheilkunde": "Eye Diseases",
    "Neurologie": "Nervous System Diseases",
    "Kardiologie": "Cardiovascular Diseases",
    "Pneumologie": "Lung Diseases",
    "Gastroenterologie": "Gastrointestinal Diseases",
    "Endokrinologie": "Endocrine System Diseases",
    "Urologie": "Urologic Diseases",
    "Gynäkologie": "Genital Diseases, Female",
    "Dermatologie": "Skin Diseases",
    "Orthopädie": "Musculoskeletal Diseases",
    "Pädiatrie": "Pediatrics",
    "Psychiatrie": "Mental Disorders",
    "Infektiologie": "Communicable Diseases",
    "Innere Medizin": "Internal Medicine",
    "Allgemeinmedizin": "General Practice",
}

_TAG_RE = re.compile(r"<[^>]+>")
_YEAR_RE = re.compile(r"\b(\d{4})\b")


def document_query(term_en: str) -> str:
    return f'"{term_en}" AND hasabstract'


def category_query(category: str) -> str:
    return f'"{CATEGORY_TERMS[category]}"[MeSH Major Topic] AND hasabstract'


def throttle(settings: Settings) -> None:
    """Space NCBI requests of this process so that bursts (e.g. the dashboard tile) stay
    within the rate limit instead of failing with 429."""
    global _last_request
    interval = MIN_INTERVAL_WITH_KEY if settings.ncbi_api_key else MIN_INTERVAL
    with _rate_lock:
        wait = _last_request + interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()


def _ncbi_get(
    client: httpx.Client, endpoint: str, params: dict[str, Any], settings: Settings
) -> Any:
    for attempt in (1, 2):
        throttle(settings)
        try:
            response = client.get(EUTILS + endpoint, params=params)
        except httpx.HTTPError as exc:
            raise SourceUnavailable(f"{endpoint}: {exc}") from exc
        if response.status_code == 429 and attempt == 1:
            time.sleep(RETRY_AFTER_429)
            continue
        try:
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SourceUnavailable(f"{endpoint}: {exc}") from exc
    raise AssertionError("unreachable")


def _params(settings: Settings, **extra: Any) -> dict[str, Any]:
    params = {"db": "pubmed", "retmode": "json", "tool": "medkb", **extra}
    if settings.ncbi_api_key:
        params["api_key"] = settings.ncbi_api_key
    return params


def _clean(text: str) -> str:
    # Titles can carry markup such as <i>…</i> and HTML entities.
    return " ".join(html.unescape(_TAG_RE.sub("", text)).split())


def _study(pmid: str, item: dict[str, Any]) -> Study:
    authors = [
        a["name"]
        for a in item.get("authors") or []
        if a.get("name") and a.get("authtype", "Author") == "Author"
    ]
    year = _YEAR_RE.search(item.get("pubdate") or "")
    return Study(
        pmid=pmid,
        title=_clean(item.get("title") or "") or "(ohne Titel)",
        journal=item.get("fulljournalname") or item.get("source") or None,
        year=int(year.group(1)) if year else None,
        authors=authors[:MAX_AUTHORS],
        more_authors=len(authors) > MAX_AUTHORS,
        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    )


def search_studies(client: httpx.Client, query: str, settings: Settings, limit: int) -> list[Study]:
    """The newest PubMed articles for ``query``, newest first. Raises SourceUnavailable."""
    # No sort parameter: PubMed's default "most recent" order, newest additions first.
    # (sort=pub_date ranks issues dated in the future first.)
    found = _ncbi_get(client, "esearch.fcgi", _params(settings, term=query, retmax=limit), settings)
    try:
        ids = [str(pmid) for pmid in found["esearchresult"]["idlist"]]
    except (KeyError, TypeError) as exc:
        raise SourceUnavailable(f"unexpected esearch answer: {exc}") from exc
    if not ids:
        return []

    summary = _ncbi_get(client, "esummary.fcgi", _params(settings, id=",".join(ids)), settings)
    try:
        result = summary["result"]
        return [_study(pmid, result[pmid]) for pmid in ids if isinstance(result.get(pmid), dict)]
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        raise SourceUnavailable(f"unexpected esummary answer: {exc}") from exc
