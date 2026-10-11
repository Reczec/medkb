"""Structured sections, English term, ICD-11 code, medications, further reading (v2 §4)."""

import pytest

from tests.conftest import make_doc

LINK = {"label": "Migräne – Gesundheitsportal", "url": "https://www.gesundheit.gv.at/x.html"}


def post(client, **fields):
    payload = {"title": "Strukturierter Eintrag", "doc_type": "Diagnose", **fields}
    return client.post("/api/documents", json=payload)


def test_create_with_sections_composes_content(client):
    response = post(client, sections={"definition": "A", "symptoms": "B"})
    assert response.status_code == 201, response.text
    doc = response.json()
    assert doc["content"] == "Definition\nA\n\nSymptome\nB"
    assert doc["sections"]["definition"] == "A"
    assert doc["sections"]["symptoms"] == "B"
    assert doc["auto_classified"] is True


def test_create_needs_content_or_sections(client):
    assert post(client).status_code == 422


def test_new_fields_roundtrip(client):
    response = post(
        client,
        content="Migräne ist eine anfallsartige Kopfschmerzerkrankung.",
        term_en="Migraine",
        icd11_code="8a80.1",
        medications=["Sumatriptan", "sumatriptan", "Ibuprofen"],
        further_reading=[LINK],
    )
    assert response.status_code == 201, response.text
    doc = client.get(f"/api/documents/{response.json()['id']}").json()
    assert doc["term_en"] == "Migraine"
    assert doc["icd11_code"] == "8A80.1"
    assert doc["medications"] == ["sumatriptan", "ibuprofen"]
    assert doc["further_reading"] == [{**LINK, "label_en": None}]
    assert doc["ai_generated"] is False


def test_plain_document_has_empty_new_fields(client):
    doc = make_doc(client)
    assert doc["sections"] is None
    assert doc["term_en"] is None and doc["icd11_code"] is None
    assert doc["medications"] == [] and doc["further_reading"] == []


@pytest.mark.parametrize(
    "fields",
    [
        {"icd11_code": "8A80.123"},
        {"term_en": 'x" OR 1'},
        {"medications": ["1abc"]},
        {"further_reading": [{"label": "x", "url": "javascript:alert(1)"}]},
        {"further_reading": [LINK] * 9},
        {"sections": {}},
        {"sections": {"definition": "   "}},
    ],
    ids=["icd", "term", "medication", "link-scheme", "too-many-links", "no-sections", "blank"],
)
def test_invalid_fields_are_rejected(client, fields):
    response = post(client, content="Genug Inhalt für einen gültigen Eintrag.", **fields)
    assert response.status_code == 422, response.text


def test_patch_content_drops_sections(client):
    doc = post(client, sections={"definition": "Erst gegliedert."}).json()
    response = client.patch(f"/api/documents/{doc['id']}", json={"content": "Jetzt Freitext."})
    assert response.status_code == 200, response.text
    assert response.json()["sections"] is None
    assert response.json()["content"] == "Jetzt Freitext."


def test_patch_sections_recomposes_content_without_reclassifying(client):
    doc = post(client, content="Ein Eintrag mit manueller Kategorie.", category="HNO").json()
    response = client.patch(
        f"/api/documents/{doc['id']}",
        json={"sections": {"definition": "Migräne", "therapy": "Ruhe"}},
    )
    assert response.status_code == 200, response.text
    updated = response.json()
    assert updated["content"] == "Definition\nMigräne\n\nTherapie\nRuhe"
    assert updated["sections"]["therapy"] == "Ruhe"
    assert updated["category"] == "HNO"


def test_patch_can_clear_term_and_code(client):
    doc = post(
        client, content="Inhalt mit Fachbegriff.", term_en="Migraine", icd11_code="8A80"
    ).json()
    updated = client.patch(
        f"/api/documents/{doc['id']}", json={"term_en": None, "icd11_code": None}
    ).json()
    assert updated["term_en"] is None and updated["icd11_code"] is None


def test_ai_generated_defaults_false_and_is_not_patchable(client):
    doc = make_doc(client)
    response = client.patch(
        f"/api/documents/{doc['id']}", json={"title": "Neu", "ai_generated": True}
    )
    assert response.status_code == 200
    assert response.json()["ai_generated"] is False


def test_classify_accepts_sections(client):
    response = client.post(
        "/api/classify",
        json={
            "title": "Ohr",
            "sections": {"definition": "Tinnitus", "diagnostics": "Trommelfell ansehen"},
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["category"] == "HNO"


def test_classify_needs_content_or_sections(client):
    assert client.post("/api/classify", json={"title": "Ohr"}).status_code == 422


# ------------------------------------------------------------- English version (i18n)

DE_TEXT = "Deutscher Inhalt für den Test mit genügend Zeichen."


def post_en(client, **fields):
    payload = {"title": "Erkältung", "content": DE_TEXT, "doc_type": "Beschreibung", **fields}
    return client.post("/api/documents", json=payload)


def test_english_sections_compose_english_content(client):
    response = post_en(
        client,
        title_en="Common cold",
        sections_en={"definition": "A viral infection.", "symptoms": "Runny nose."},
        keywords_en=["Cold", "cold", "Virus"],
    )
    assert response.status_code == 201, response.text
    doc = response.json()
    assert doc["content"] == DE_TEXT  # German stays canonical
    assert doc["content_en"] == "Definition\nA viral infection.\n\nSymptoms\nRunny nose."
    assert doc["title_en"] == "Common cold"
    assert doc["keywords_en"] == ["Cold", "Virus"]


def test_documents_without_english_have_empty_english_fields(client):
    doc = make_doc(client)
    assert doc["title_en"] is None and doc["content_en"] is None
    assert doc["sections_en"] is None and doc["keywords_en"] == []


def test_patch_content_en_drops_sections_en(client):
    doc = post_en(client, sections_en={"definition": "Structured English."}).json()
    updated = client.patch(
        f"/api/documents/{doc['id']}", json={"content_en": "Now free text in English."}
    ).json()
    assert updated["sections_en"] is None
    assert updated["content_en"] == "Now free text in English."


def test_patch_title_en_null_clears_only_the_title(client):
    doc = post_en(
        client, title_en="Common cold", content_en="A viral infection of the nose."
    ).json()
    updated = client.patch(f"/api/documents/{doc['id']}", json={"title_en": None}).json()
    assert updated["title_en"] is None
    assert updated["content_en"] == "A viral infection of the nose."


def test_patch_sections_en_recomposes_and_leaves_german_alone(client):
    doc = post_en(client, content_en="Old English text here.").json()
    updated = client.patch(
        f"/api/documents/{doc['id']}", json={"sections_en": {"therapy": "Rest and fluids."}}
    ).json()
    assert updated["content_en"] == "Therapy\nRest and fluids."
    assert updated["content"] == DE_TEXT and updated["title"] == "Erkältung"


@pytest.mark.parametrize(
    "fields",
    [
        {"title_en": "ab"},
        {"sections_en": {}},
        {"content_en": "short"},
        {"keywords_en": [f"k{i}" for i in range(21)]},
    ],
    ids=["short-title", "no-sections", "short-content", "too-many-keywords"],
)
def test_invalid_english_fields_are_rejected(client, fields):
    assert post_en(client, **fields).status_code == 422
