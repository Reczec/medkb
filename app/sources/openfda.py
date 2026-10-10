"""openFDA drug labels (US prescribing information, English) per active ingredient."""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings
from app.schemas import MedicationLabel
from app.sources.cache import SourceUnavailable

LABEL_URL = "https://api.fda.gov/drug/label.json"
ABOUT_URL = "https://open.fda.gov/apis/drug/label/"
MAX_TEXT = 600
MAX_BRANDS = 5
CANDIDATES = 10  # labels fetched per ingredient; the most fitting one is shown


def truncate(text: str | None, limit: int = MAX_TEXT) -> str | None:
    """Collapse whitespace and cut at a word boundary with "…"."""
    if not text:
        return None
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:")
    return f"{cut}…"


def _first(label: dict[str, Any], *fields: str) -> str | None:
    for field in fields:
        values = label.get(field)
        if isinstance(values, list) and values and isinstance(values[0], str):
            return truncate(values[0])
    return None


def _fit(label: dict[str, Any]) -> tuple[bool, bool, bool]:
    """Ranking: single-ingredient before combinations, prescription before OTC/homeopathic,
    labels with an indication before those without."""
    meta = label.get("openfda") or {}
    generic = " ".join(meta.get("generic_name") or []).upper()
    single = bool(generic) and " AND " not in generic and "," not in generic
    prescription = "HUMAN PRESCRIPTION DRUG" in (meta.get("product_type") or [])
    return single, prescription, bool(label.get("indications_and_usage"))


def fetch_label(
    client: httpx.Client, ingredient: str, settings: Settings
) -> MedicationLabel | None:
    """The first FDA label for an active ingredient; None if openFDA has none."""
    try:
        response = client.get(
            LABEL_URL,
            params={"search": f'openfda.generic_name:"{ingredient}"', "limit": CANDIDATES},
        )
        if response.status_code == 404:  # openFDA answers "no matches" with 404 NOT_FOUND
            return None
        response.raise_for_status()
        results = [r for r in response.json()["results"] if isinstance(r, dict)]
        label = max(results, key=_fit)  # max keeps the first of equally fitting labels
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise SourceUnavailable(f"openFDA {ingredient}: {exc}") from exc

    brands = (label.get("openfda") or {}).get("brand_name") or []
    return MedicationLabel(
        ingredient=ingredient,
        brand_names=list(dict.fromkeys(str(b) for b in brands))[:MAX_BRANDS],
        indications=_first(label, "indications_and_usage"),
        warnings=_first(label, "boxed_warning", "warnings_and_cautions", "warnings"),
        adverse_reactions=_first(label, "adverse_reactions"),
        url=ABOUT_URL,
    )
