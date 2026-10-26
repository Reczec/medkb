"""Example entries: structured, general textbook-level descriptions. No patient data.

One module per specialty. Each entry has ``sections`` (the full text ``content`` is composed
from them, as the API does), ``term_en`` for the external sources, an ICD-11 code for diseases
and symptoms, active ingredients where sensible, and checked further-reading links.

``expected_category`` is what the rule-based classifier is expected to choose; the test suite
checks this, which doubles as a small accuracy check of the classifier.
"""

from typing import Any

from app.content import compose_content
from app.seed_data import (
    allgemeinmedizin,
    augenheilkunde,
    dermatologie,
    endokrinologie,
    gastroenterologie,
    gynaekologie,
    hno,
    infektiologie,
    innere_medizin,
    kardiologie,
    neurologie,
    orthopaedie,
    paediatrie,
    pneumologie,
    psychiatrie,
    urologie,
)

SOURCE = "Redaktionelle Demo-Inhalte auf Lehrbuchniveau – keine medizinische Beratung"

_MODULES = (
    hno,
    augenheilkunde,
    neurologie,
    kardiologie,
    pneumologie,
    gastroenterologie,
    endokrinologie,
    urologie,
    gynaekologie,
    dermatologie,
    orthopaedie,
    paediatrie,
    psychiatrie,
    infektiologie,
    innere_medizin,
    allgemeinmedizin,
)

# The first release's entries (ENTRIES) come first and keep ids 1..47 across resets; entries added
# later (EXTRA of each module) follow in the same specialty order.
SEED_DOCUMENTS: list[dict[str, Any]] = [
    {**entry, "content": compose_content(entry["sections"])}
    for attribute in ("ENTRIES", "EXTRA")
    for module in _MODULES
    for entry in getattr(module, attribute, [])
]
