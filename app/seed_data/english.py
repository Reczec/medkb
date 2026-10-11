"""English version of the example entries, merged into the German canonical ones."""

from __future__ import annotations

from typing import Any


def with_english(
    entries: list[dict[str, Any]], translations: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Add ``title_en``, ``sections_en`` and ``keywords_en`` to each entry by German title.

    Every entry needs a translation and every translation an entry, so a renamed German title
    fails at import instead of silently leaving an entry untranslated.
    """
    titles = {entry["title"] for entry in entries}
    unknown = set(translations) - titles
    missing = titles - set(translations)
    if unknown or missing:
        raise ValueError(f"translations out of sync: unknown={unknown} missing={missing}")
    return [{**entry, **translations[entry["title"]]} for entry in entries]
