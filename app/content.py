"""Structured entries: the fixed sections and how they become the full-text ``content``."""

from __future__ import annotations

from collections.abc import Mapping

from app.i18n import Lang

SECTION_KEYS = ("definition", "symptoms", "causes", "diagnostics", "therapy", "red_flags")

SECTION_LABELS: dict[Lang, dict[str, str]] = {
    "de": {
        "definition": "Definition",
        "symptoms": "Symptome",
        "causes": "Ursachen",
        "diagnostics": "Diagnostik",
        "therapy": "Therapie",
        "red_flags": "Warnzeichen",
    },
    "en": {
        "definition": "Definition",
        "symptoms": "Symptoms",
        "causes": "Causes",
        "diagnostics": "Diagnostics",
        "therapy": "Therapy",
        "red_flags": "Warning signs",
    },
}


def compose_content(sections: Mapping[str, str | None], lang: Lang = "de") -> str:
    """Full text for search and classification: one "label, newline, text" block per section."""
    labels = SECTION_LABELS[lang]
    blocks = [
        f"{labels[key]}\n{text.strip()}"
        for key in SECTION_KEYS
        if (text := sections.get(key)) and text.strip()
    ]
    return "\n\n".join(blocks)
