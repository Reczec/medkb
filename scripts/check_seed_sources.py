"""Check the example entries against the real sources (needs network; not part of CI).

    python scripts/check_seed_sources.py

Fetches every further-reading URL and fails if one does not answer 200. With ICD_CLIENT_ID and
ICD_CLIENT_SECRET set, it also resolves every ICD-11 code through the WHO API.
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.seed_data import SEED_DOCUMENTS  # noqa: E402

HEADERS = {"User-Agent": "medkb-linkcheck/1.0 (+https://github.com/Reczec/medkb)"}


def check_link(url: str) -> tuple[str, int | str]:
    try:
        response = httpx.get(url, follow_redirects=True, timeout=10, headers=HEADERS)
        return url, response.status_code
    except httpx.HTTPError as exc:
        return url, type(exc).__name__


def check_links() -> bool:
    urls = sorted({link["url"] for doc in SEED_DOCUMENTS for link in doc["further_reading"]})
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(check_link, urls))
    for url, status in results:
        print(f"{status}  {url}")
    broken = [url for url, status in results if status != 200]
    print(f"{len(urls) - len(broken)}/{len(urls)} links OK")
    return not broken


def check_icd_codes() -> bool:
    try:
        from app.sources.icd11 import lookup_code

        from app.config import get_settings
    except ImportError:
        return True  # the ICD-11 client is added in a later step
    settings = get_settings()
    if not (settings.icd_client_id and settings.icd_client_secret):
        print("ICD-11: no API keys set, codes not checked")
        return True
    ok = True
    with httpx.Client(timeout=settings.sources_timeout) as client:
        for doc in SEED_DOCUMENTS:
            code = doc.get("icd11_code")
            if not code:
                continue
            entry = lookup_code(client, code, settings)
            print(f"{code:8} {'?' if entry is None else entry.title}  ({doc['title']})")
            ok = ok and entry is not None
    return ok


if __name__ == "__main__":
    links_ok = check_links()
    codes_ok = check_icd_codes()
    sys.exit(0 if links_ok and codes_ok else 1)
