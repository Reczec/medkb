"""PubMed via the NCBI E-utilities: esearch for the newest PMIDs, esummary for their details."""

from __future__ import annotations

import html
import re
from typing import Any

import httpx

from app.config import Settings
from app.schemas import Study
from app.sources.cache import SourceUnavailable
from app.sources.http import get_json

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
MAX_AUTHORS = 3

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
    found = get_json(
        client,
        EUTILS + "esearch.fcgi",
        params=_params(settings, term=query, sort="pub_date", retmax=limit),
    )
    try:
        ids = [str(pmid) for pmid in found["esearchresult"]["idlist"]]
    except (KeyError, TypeError) as exc:
        raise SourceUnavailable(f"unexpected esearch answer: {exc}") from exc
    if not ids:
        return []

    summary = get_json(client, EUTILS + "esummary.fcgi", params=_params(settings, id=",".join(ids)))
    try:
        result = summary["result"]
        return [_study(pmid, result[pmid]) for pmid in ids if isinstance(result.get(pmid), dict)]
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        raise SourceUnavailable(f"unexpected esummary answer: {exc}") from exc
