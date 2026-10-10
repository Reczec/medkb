"""Rules for the bundled example entries (spec §7)."""

from collections import Counter
from urllib.parse import urlparse

import pytest

from app.classifier import CATEGORIES
from app.schemas import DocumentCreate
from app.seed_data import SEED_DOCUMENTS, SOURCE

TRUSTED_HOSTS = {
    "www.gesundheit.gv.at",
    "register.awmf.org",
    "www.awmf.org",
    "www.who.int",
    "medlineplus.gov",
    "www.nih.gov",
    "www.ninds.nih.gov",
    "www.niddk.nih.gov",
    "www.nei.nih.gov",
    "www.nhlbi.nih.gov",
}
DOCUMENT_FIELDS = (
    "title",
    "doc_type",
    "term_en",
    "icd11_code",
    "medications",
    "sections",
    "further_reading",
)
IDS = [d["title"][:30] for d in SEED_DOCUMENTS]


def test_entry_count_and_specialty_coverage():
    assert 44 <= len(SEED_DOCUMENTS) <= 48
    per_category = Counter(d["expected_category"] for d in SEED_DOCUMENTS)
    assert set(per_category) == set(CATEGORIES)
    assert min(per_category.values()) >= 2


def test_source_marks_editorial_demo_content():
    assert SOURCE == "Redaktionelle Demo-Inhalte auf Lehrbuchniveau – keine medizinische Beratung"


@pytest.mark.parametrize("doc", SEED_DOCUMENTS, ids=IDS)
def test_every_entry_validates(doc):
    DocumentCreate(**{k: doc[k] for k in DOCUMENT_FIELDS if k in doc}, source=SOURCE)


@pytest.mark.parametrize("doc", SEED_DOCUMENTS, ids=IDS)
def test_section_coverage(doc):
    filled = [key for key, text in doc["sections"].items() if text and text.strip()]
    if doc["doc_type"] in ("Diagnose", "Symptom"):
        assert len(filled) == 6, doc["title"]
    else:
        assert len(filled) >= 2, doc["title"]


@pytest.mark.parametrize("doc", SEED_DOCUMENTS, ids=IDS)
def test_every_entry_has_term_en_and_disease_entries_an_icd_code(doc):
    assert doc["term_en"]
    if doc["doc_type"] in ("Diagnose", "Symptom"):
        assert doc.get("icd11_code"), doc["title"]


@pytest.mark.parametrize("doc", SEED_DOCUMENTS, ids=IDS)
def test_further_reading_only_from_trusted_hosts(doc):
    assert doc["further_reading"], doc["title"]
    for link in doc["further_reading"]:
        assert urlparse(link["url"]).hostname in TRUSTED_HOSTS, link["url"]


def test_titles_are_unique():
    titles = [d["title"] for d in SEED_DOCUMENTS]
    assert len(titles) == len(set(titles))


def test_seeding_stores_all_fields(client, db_session):
    from app.demo import reset_demo

    reset_demo(db_session)
    items = client.get("/api/documents", params={"q": "Migräne", "limit": 5}).json()["items"]
    migraine = next(d for d in items if d["title"] == "Migräne")
    assert migraine["sections"]["definition"]
    assert migraine["term_en"] == "Migraine"
    assert migraine["icd11_code"] == "8A80"
    assert "sumatriptan" in migraine["medications"]
    assert migraine["further_reading"]
