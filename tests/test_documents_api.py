import pytest

from tests.conftest import make_doc

# ----------------------------------------------------------------------------- basics


def test_health_and_meta(client):
    assert client.get("/api/health").json() == {"status": "ok"}
    meta = client.get("/api/meta").json()
    assert "HNO" in meta["categories"]
    assert "Symptom" in meta["doc_types"]
    assert meta["default_category"] == "Allgemeinmedizin"


def test_web_ui_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "MedKB" in response.text


# ------------------------------------------------------------------------------- create


def test_create_classifies_automatically(client):
    doc = make_doc(
        client,
        title="Ohrenschmerzen",
        content="Starke Ohrenschmerzen und ein gerötetes Trommelfell bei Otitis media.",
    )
    assert doc["id"] > 0
    assert doc["category"] == "HNO"
    assert doc["auto_classified"] is True
    assert "Ohrenschmerzen" in doc["keywords"]
    assert doc["created_at"].endswith("Z") or "+00:00" in doc["created_at"]


def test_create_with_manual_category_and_keywords(client):
    doc = make_doc(client, category="Psychiatrie", keywords=["  eigenes ", "Eigenes", "zweites"])
    assert doc["category"] == "Psychiatrie"
    assert doc["auto_classified"] is False
    assert doc["keywords"] == ["eigenes", "zweites"]  # trimmed and de-duplicated


def test_create_rejects_invalid_input(client):
    base = {"title": "Titel", "content": "Genug Inhalt für den Test.", "doc_type": "Symptom"}
    cases = [
        {**base, "title": "ab"},
        {**base, "content": "kurz"},
        {**base, "doc_type": "Unbekannt"},
        {**base, "category": "Astrologie"},
        {**base, "keywords": ["x" * 51]},
        {**base, "keywords": [f"k{i}" for i in range(21)]},
    ]
    for payload in cases:
        assert client.post("/api/documents", json=payload).status_code == 422, payload


# ----------------------------------------------------------------------- read / update


def test_get_and_404(client):
    doc = make_doc(client)
    assert client.get(f"/api/documents/{doc['id']}").json()["title"] == "Testeintrag"
    assert client.get("/api/documents/9999").status_code == 404


def test_update_partial_keeps_other_fields(client):
    doc = make_doc(client)
    response = client.patch(f"/api/documents/{doc['id']}", json={"title": "Neuer Titel"})
    updated = response.json()
    assert response.status_code == 200
    assert updated["title"] == "Neuer Titel"
    assert updated["content"] == doc["content"]
    assert updated["category"] == doc["category"]


def test_update_category_makes_it_manual(client):
    doc = make_doc(client)
    updated = client.patch(f"/api/documents/{doc['id']}", json={"category": "Kardiologie"}).json()
    assert updated["category"] == "Kardiologie"
    assert updated["auto_classified"] is False


def test_content_change_does_not_override_manual_category(client):
    doc = make_doc(client, category="Psychiatrie")
    updated = client.patch(
        f"/api/documents/{doc['id']}",
        json={"content": "Jetzt geht es um Ohrenschmerzen, Tinnitus und das Trommelfell."},
    ).json()
    assert updated["category"] == "Psychiatrie"


def test_reclassify_runs_classifier_again(client):
    doc = make_doc(client, category="Psychiatrie")
    updated = client.patch(
        f"/api/documents/{doc['id']}",
        json={
            "content": "Jetzt geht es um Ohrenschmerzen, Tinnitus und das Trommelfell.",
            "reclassify": True,
        },
    ).json()
    assert updated["category"] == "HNO"
    assert updated["auto_classified"] is True


def test_empty_keywords_on_update_regenerate(client):
    doc = make_doc(client, keywords=["eigenes"])
    updated = client.patch(f"/api/documents/{doc['id']}", json={"keywords": []}).json()
    assert "eigenes" not in updated["keywords"]
    assert "Migräne" in updated["keywords"]


def test_source_can_be_set_and_cleared(client):
    doc = make_doc(client)
    url = f"/api/documents/{doc['id']}"
    assert client.patch(url, json={"source": "Lehrbuch"}).json()["source"] == "Lehrbuch"
    assert client.patch(url, json={"source": None}).json()["source"] is None


def test_update_validation(client):
    doc = make_doc(client)
    url = f"/api/documents/{doc['id']}"
    assert client.patch(url, json={}).status_code == 422
    assert client.patch(url, json={"title": None}).status_code == 422
    assert client.patch(url, json={"category": "Astrologie"}).status_code == 422
    assert client.patch("/api/documents/9999", json={"title": "Irgendwas"}).status_code == 404


def test_delete(client):
    doc = make_doc(client)
    assert client.delete(f"/api/documents/{doc['id']}").status_code == 204
    assert client.get(f"/api/documents/{doc['id']}").status_code == 404
    assert client.delete(f"/api/documents/{doc['id']}").status_code == 404


# ----------------------------------------------------------------------------- search


def titles(client, **params):
    response = client.get("/api/documents", params=params)
    assert response.status_code == 200
    return [d["title"] for d in response.json()["items"]]


def test_search_in_title_content_and_keywords(client):
    make_doc(client, title="Alpha", content="Dieser Text handelt von Sodbrennen im Alltag.")
    make_doc(client, title="Bravo Zwerchfell", content="Ein ganz anderer Inhalt ohne Bezug.")
    make_doc(
        client, title="Charlie", content="Noch ein Inhalt ohne Bezug.", keywords=["Spezialwort"]
    )

    assert titles(client, q="sodbrennen") == ["Alpha"]
    assert titles(client, q="zwerchfell") == ["Bravo Zwerchfell"]
    assert titles(client, q="spezialwort") == ["Charlie"]
    assert titles(client, q="gibtesnicht") == []


def test_search_is_case_insensitive_including_umlauts(client):
    make_doc(client, title="Übelkeit", content="Ein Text über Übelkeit und Ärger beim Essen.")
    assert titles(client, q="übelkeit") == ["Übelkeit"]
    assert titles(client, q="ÜBELKEIT") == ["Übelkeit"]
    assert titles(client, q="ärger") == ["Übelkeit"]


def test_search_requires_all_terms(client):
    make_doc(client, title="Eins", content="Kopfschmerzen und Übelkeit kommen zusammen vor.")
    make_doc(client, title="Zwei", content="Nur Kopfschmerzen, sonst nichts Besonderes hier.")
    assert sorted(titles(client, q="kopfschmerzen")) == ["Eins", "Zwei"]
    assert titles(client, q="kopfschmerzen übelkeit") == ["Eins"]


def test_search_ranks_title_hits_first(client):
    make_doc(
        client, title="Allgemeiner Text", content="Hier kommt das Wort Zielwort nur im Inhalt vor."
    )
    make_doc(client, title="Zielwort im Titel", content="Der Inhalt enthält etwas völlig anderes.")
    assert titles(client, q="zielwort") == ["Zielwort im Titel", "Allgemeiner Text"]


def test_search_wildcards_are_escaped(client):
    make_doc(client, title="Prozent", content="Eine Zahl wie 100% ist nicht gleich 1000 oder 10.")
    make_doc(client, title="Unterstrich", content="Das ist ein_Beispiel mit Unterstrich und mehr.")
    assert titles(client, q="100%") == ["Prozent"]
    assert titles(client, q="%") == ["Prozent"]  # a literal percent sign, not "match everything"
    assert titles(client, q="ein_b") == ["Unterstrich"]
    assert titles(client, q="_") == ["Unterstrich"]


def test_filters_by_category_and_type(client):
    make_doc(client, title="Eins", category="HNO")
    make_doc(client, title="Zwei", category="Neurologie")
    client.post(
        "/api/documents",
        json={
            "title": "Drei",
            "content": "Ein Befund ohne Fachbegriffe im Text.",
            "doc_type": "Befund",
        },
    )
    assert titles(client, category="HNO") == ["Eins"]
    assert titles(client, doc_type="Befund") == ["Drei"]
    assert titles(client, category="HNO", doc_type="Befund") == []
    assert titles(client, q="eins", category="HNO") == ["Eins"]
    assert titles(client, q="eins", category="Neurologie") == []


def test_pagination(client):
    for i in range(5):
        make_doc(client, title=f"Eintrag {i}")
    first = client.get("/api/documents", params={"limit": 2}).json()
    assert first["total"] == 5 and len(first["items"]) == 2
    last = client.get("/api/documents", params={"limit": 2, "offset": 4}).json()
    assert len(last["items"]) == 1
    seen = [
        d["id"]
        for off in (0, 2, 4)
        for d in client.get("/api/documents", params={"limit": 2, "offset": off}).json()["items"]
    ]
    assert len(set(seen)) == 5  # no duplicates or gaps across pages
    assert client.get("/api/documents", params={"limit": 0}).status_code == 422
    assert client.get("/api/documents", params={"limit": 101}).status_code == 422


# ------------------------------------------------------------------- classify / stats


def test_classify_endpoint_does_not_save(client):
    response = client.post(
        "/api/classify",
        json={"title": "Windpocken", "content": "Windpocken treten häufig bei Kindern auf."},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["category"] == "Pädiatrie"
    assert body["fallback"] is False
    assert "Windpocken" in body["keywords"]
    assert client.get("/api/documents").json()["total"] == 0


def test_stats(client):
    make_doc(client, title="Eins", content="Ohrenschmerzen und Tinnitus und Trommelfell.")
    make_doc(client, title="Zwei", category="Kardiologie")
    stats = client.get("/api/stats").json()
    by_category = {c["name"]: c["count"] for c in stats["categories"]}
    assert stats["total"] == 2
    assert stats["auto_classified"] == 1
    assert by_category["HNO"] == 1 and by_category["Kardiologie"] == 1
    assert by_category["Dermatologie"] == 0  # categories without entries are listed too
    assert {t["name"] for t in stats["doc_types"]} >= {"Symptom", "Befund"}
    assert [r["title"] for r in stats["recent"]][0] == "Zwei"


@pytest.mark.parametrize("q", ['"', "[", "]", ",", '","'])
def test_search_ignores_json_syntax_of_the_keyword_column(client, q):
    # Keywords are stored as JSON text; its quotes, brackets and commas must not match everything.
    make_doc(client, title="Migräne", content="Kopfschmerz einseitig", keywords=["Kopf", "Schmerz"])
    assert titles(client, q=q) == []


def test_search_still_finds_punctuation_inside_title_or_content(client):
    make_doc(client, title='Das "Kopfweh"-Tagebuch', content="Notizen, Termine [optional]")
    assert titles(client, q='"Kopfweh"') == ['Das "Kopfweh"-Tagebuch']
    assert titles(client, q="[optional]") == ['Das "Kopfweh"-Tagebuch']


# ------------------------------------------------------- search over both languages


def _en_doc(client, title, title_en=None, content_en=None, **extra):
    payload = {
        "title": title,
        "content": "Deutscher Text ohne den gesuchten Begriff.",
        "doc_type": "Symptom",
        **extra,
    }
    if title_en:
        payload["title_en"] = title_en
    if content_en:
        payload["content_en"] = content_en
    response = client.post("/api/documents", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_english_term_finds_the_entry_through_its_english_version(client):
    doc = _en_doc(client, "Erkältung", title_en="Common cold")
    _en_doc(client, "Migräne", title_en="Migraine")
    found = client.get("/api/documents", params={"q": "cold"}).json()["items"]
    assert [d["id"] for d in found] == [doc["id"]]
    assert [
        d["id"] for d in client.get("/api/documents", params={"q": "Erkältung"}).json()["items"]
    ] == [doc["id"]]


def test_english_title_hit_outranks_english_content_hit(client):
    first = _en_doc(client, "Alpha", title_en="Cold sores")
    _en_doc(client, "Beta", content_en="A text about a cold in winter, in English.")
    ids = [d["id"] for d in client.get("/api/documents", params={"q": "cold"}).json()["items"]]
    assert ids[0] == first["id"] and len(ids) == 2


def test_english_keywords_are_searched_and_json_syntax_is_skipped(client):
    doc = _en_doc(client, "Gicht", keywords_en=["Uric acid"])
    assert [
        d["id"] for d in client.get("/api/documents", params={"q": "uric"}).json()["items"]
    ] == [doc["id"]]
    assert client.get("/api/documents", params={"q": 'uric"'}).status_code == 200
