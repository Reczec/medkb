"""Structured entries: the fixed sections and how they become the full-text ``content``."""

from __future__ import annotations

from collections.abc import Mapping

SECTION_KEYS = ("definition", "symptoms", "causes", "diagnostics", "therapy", "red_flags")

SECTION_LABELS: dict[str, str] = {
    "definition": "Definition",
    "symptoms": "Symptome",
    "causes": "Ursachen",
    "diagnostics": "Diagnostik",
    "therapy": "Therapie",
    "red_flags": "Warnzeichen",
}


def compose_content(sections: Mapping[str, str | None]) -> str:
    """Full text for search and classification: one "label, newline, text" block per section."""
    blocks = [
        f"{SECTION_LABELS[key]}\n{text.strip()}"
        for key in SECTION_KEYS
        if (text := sections.get(key)) and text.strip()
    ]
    return "\n\n".join(blocks)
