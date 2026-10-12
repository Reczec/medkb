"""The English version of the bundled entries (spec: Mehrsprachigkeit §3)."""

import re

import pytest
from sqlalchemy import select

from app.models import Document
from app.seed_data import SEED_DOCUMENTS

IDS = [d["title"][:30] for d in SEED_DOCUMENTS]
GERMAN_WORDS = re.compile(
    r"\b(und|oder|der|die|das|nicht|bei|mit|ist|ein|eine|wird|sind|für|von)\b", re.IGNORECASE
)
UMLAUTS = re.compile("[äöüßÄÖÜ]")


def english_texts(entry):
    yield entry["title_en"]
    yield from entry["sections_en"].values()
    yield from entry["keywords_en"]


@pytest.mark.parametrize("entry", SEED_DOCUMENTS, ids=IDS)
def test_entry_has_a_complete_english_version(entry):
    assert entry.get("title_en"), "title_en missing"
    assert entry["sections_en"].keys() == entry["sections"].keys()
    assert all(text.strip() for text in entry["sections_en"].values())
    keywords = entry["keywords_en"]
    assert 5 <= len(keywords) <= 8
    assert len({k.lower() for k in keywords}) == len(keywords)


@pytest.mark.parametrize("entry", SEED_DOCUMENTS, ids=IDS)
def test_english_version_contains_no_german(entry):
    for text in english_texts(entry):
        assert not UMLAUTS.search(text), text
        assert not GERMAN_WORDS.search(text), text


@pytest.mark.parametrize("entry", SEED_DOCUMENTS, ids=IDS)
def test_links_have_english_labels(entry):
    for link in entry["further_reading"]:
        assert link.get("label_en"), link["url"]
        assert "englisch" not in link["label_en"].lower()


def test_english_titles_are_unique():
    titles = [d["title_en"] for d in SEED_DOCUMENTS]
    assert len(titles) == len(set(titles))


def test_seeded_entries_are_found_by_english_terms(client, db_session):
    from app.demo import reset_demo

    reset_demo(db_session)
    migraine = db_session.scalar(select(Document).where(Document.title == "Migräne"))
    assert migraine.title_en and migraine.content_en and migraine.keywords_en
    assert migraine.content_en.startswith("Definition\n")
    found = client.get("/api/documents", params={"q": migraine.title_en.split()[0]}).json()
    assert migraine.id in [d["id"] for d in found["items"]]
