import json

import pytest
from sqlalchemy import func, select

from app.ai.provider import AIUnavailable, get_provider
from app.ai.store import usage_today
from app.main import app
from app.models import AICache, Document
from tests.conftest import make_doc


class FakeProvider:
    def __init__(self):
        self.answer = "Eine allgemeine Erklärung."
        self.calls = []
        self.fail = False
        self.stream_fail = False

    def complete(self, messages):
        self.calls.append(messages)
        if self.fail:
            raise AIUnavailable("ai_unavailable")
        return self.answer

    async def stream(self, messages):
        text = self.complete(messages)
        yield text[:5]
        if self.stream_fail:
            raise AIUnavailable("ai_unavailable")
        yield text[5:]


@pytest.fixture
def fake(test_settings):
    provider = FakeProvider()
    app.dependency_overrides[get_provider] = lambda: provider
    return provider


def test_missing_configuration_is_503(client):
    doc = make_doc(client)
    response = client.post(f"/api/ai/documents/{doc['id']}/explain")
    assert response.status_code == 503
    assert response.json()["detail"] == "ai_not_configured"


@pytest.mark.parametrize("role", ["admin", "doctor", "patient", None])
@pytest.mark.parametrize("feature", ["explain", "red-flags", "summary"])
def test_document_roles(client, doctor_client, patient_client, anon_client, fake, role, feature):
    doc = make_doc(client)
    clients = {
        "admin": client,
        "doctor": doctor_client,
        "patient": patient_client,
        None: anon_client,
    }
    response = clients[role].post(f"/api/ai/documents/{doc['id']}/{feature}")
    expected = 401 if role is None else 403 if role == "patient" and feature == "summary" else 200
    assert response.status_code == expected
    if expected == 200:
        assert "keine medizinische Beratung" in response.json()["text"]


def test_cache_hit_costs_no_quota_and_edit_or_role_changes_cache(
    client, doctor_client, fake, db_session
):
    doc = make_doc(client)
    path = f"/api/ai/documents/{doc['id']}/explain"
    assert client.post(path).json()["cached"] is False
    assert client.post(path).json()["cached"] is True
    assert usage_today(db_session) == 1
    client.patch(
        f"/api/documents/{doc['id']}", json={"content": "Eine neue Beschreibung der Migräne."}
    )
    assert client.post(path).json()["cached"] is False
    assert doctor_client.post(path).json()["cached"] is False
    assert len(fake.calls) == 3


def test_failed_provider_is_not_cached_and_retry_consumes_another_call(client, fake, db_session):
    doc = make_doc(client)
    path = f"/api/ai/documents/{doc['id']}/explain"
    fake.fail = True
    assert client.post(path).status_code == 503
    assert db_session.scalar(select(func.count()).select_from(AICache)) == 0
    fake.fail = False
    assert client.post(path).status_code == 200
    assert usage_today(db_session) == 2


def test_stream_has_tokens_and_validated_done(client, fake):
    doc = make_doc(client)
    response = client.post(f"/api/ai/documents/{doc['id']}/summary?stream=true")
    assert response.headers["content-type"].startswith("text/event-stream")
    assert "event: token" in response.text and "event: done" in response.text
    assert "event: error" not in response.text


def test_interrupted_stream_is_not_cached(client, fake, db_session):
    doc = make_doc(client)
    fake.stream_fail = True
    response = client.post(f"/api/ai/documents/{doc['id']}/explain?stream=true")
    assert "event: error" in response.text and "event: done" not in response.text
    assert db_session.scalar(select(func.count()).select_from(AICache)) == 0


def test_ask_no_context_is_honest_and_uses_no_provider(client, fake, db_session):
    response = client.post("/api/ai/ask", json={"question": "KeinePassendenEinträge"})
    assert response.status_code == 200
    assert response.json()["citations"] == []
    assert "keine passenden" in response.json()["text"].lower()
    assert fake.calls == [] and usage_today(db_session) == 0


def test_grounded_ask_cites_actual_entries_and_role_prompt(patient_client, client, fake):
    doc = make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information zur Migräne [1]."
    response = patient_client.post(
        "/api/ai/ask",
        json={"question": "Migräne", "history": [{"role": "user", "content": "Hallo"}]},
    )
    assert response.status_code == 200
    assert response.json()["citations"] == [{"index": 1, "id": doc["id"], "title": "Migräne"}]
    assert "B1" in fake.calls[0][0]["content"]
    assert "keine individuellen Diagnosen" in fake.calls[0][0]["content"]
    assert "144" in fake.calls[0][0]["content"]
    assert client.post("/api/ai/ask", json={"question": "Migräne"}).status_code == 200
    assert len(fake.calls) == 2  # ask is never cached


@pytest.mark.parametrize("answer", ["Unbelegt.", "Falsche Quelle [9]."])
def test_ask_rejects_unverifiable_citations(client, fake, answer):
    make_doc(client, title="Migräne")
    fake.answer = answer
    assert client.post("/api/ai/ask", json={"question": "Migräne"}).status_code == 503


def test_history_and_question_are_bounded(client, fake):
    assert (
        client.post(
            "/api/ai/ask",
            json={"question": "Migräne", "history": [{"role": "user", "content": "x"}] * 7},
        ).status_code
        == 422
    )
    assert client.post("/api/ai/ask", json={"question": "x" * 201}).status_code == 422


def test_draft_is_validated_marked_and_not_saved(client, fake, db_session):
    fake.answer = json.dumps(
        {
            "title": "Migräne",
            "content": "Allgemeines Beispiel für Migräne.",
            "doc_type": "Diagnose",
            "term_en": "Migraine",
            "icd11_code": "8A80",
            "medications": ["sumatriptan"],
        }
    )
    response = client.post("/api/ai/draft", json={"title": "Migräne"})
    assert response.status_code == 200
    assert response.json()["draft"]["ai_generated"] is True
    assert response.json()["draft"]["term_en"] == "Migraine"
    assert db_session.scalar(select(func.count()).select_from(Document)) == 0


def test_invalid_draft_is_not_cached_or_saved(client, fake, db_session):
    fake.answer = json.dumps(
        {
            "title": "Migräne",
            "content": "Ein Beispieltext.",
            "doc_type": "Diagnose",
            "icd11_code": "8A80.123",
        }
    )
    assert client.post("/api/ai/draft", json={"title": "Migräne"}).status_code == 503
    assert db_session.scalar(select(func.count()).select_from(Document)) == 0


def test_classification_is_a_validated_separate_opinion(client, fake):
    fake.answer = json.dumps(
        {"category": "Neurologie", "confidence": 0.8, "reasoning": "Kopfschmerzen."}
    )
    response = client.post(
        "/api/ai/classify", json={"title": "Migräne", "content": "Kopfschmerzen mit Übelkeit."}
    )
    assert response.json()["classification"]["category"] == "Neurologie"
    fake.answer = json.dumps({"category": "Invented", "confidence": 0.8, "reasoning": "Wrong"})
    assert (
        client.post(
            "/api/ai/classify", json={"title": "Migräne", "content": "Kopfschmerzen mit Übelkeit."}
        ).status_code
        == 503
    )


@pytest.mark.parametrize(
    "path,payload",
    [
        ("draft", {"title": "Migräne"}),
        ("classify", {"title": "Migräne", "content": "Kopfschmerzen"}),
        ("studies/summarize", {"pmid": "123456"}),
    ],
)
def test_patient_cannot_use_admin_or_staff_features(patient_client, path, payload, fake):
    assert patient_client.post(f"/api/ai/{path}", json=payload).status_code == 403


def test_study_summary_fetches_real_abstract_with_safe_pmid(client, fake, network):
    route = network.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi").respond(
        200,
        text="<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>123456</PMID><Article><Abstract><AbstractText>Real abstract for this fixture.</AbstractText></Abstract></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>",
    )
    assert client.post("/api/ai/studies/summarize", json={"pmid": "123456"}).status_code == 200
    assert "Real abstract" in fake.calls[0][-1]["content"]
    assert route.calls.last.request.url.params["id"] == "123456"
    assert (
        client.post("/api/ai/studies/summarize", json={"pmid": "https://internal"}).status_code
        == 422
    )


def test_usage_staff_only(client, patient_client, fake):
    make_doc(client)
    assert client.get("/api/ai/usage").json()["today"] == 0
    assert patient_client.get("/api/ai/usage").status_code == 403


def test_quota_error_has_retry_after(client, fake, test_settings):
    test_settings.ai_daily_limit = 1
    doc = make_doc(client)
    client.post(f"/api/ai/documents/{doc['id']}/explain")
    response = client.post(f"/api/ai/documents/{doc['id']}/red-flags")
    assert response.status_code == 429 and int(response.headers["Retry-After"]) > 0


@pytest.mark.parametrize(
    "xml",
    [
        "broken",
        "<PubmedArticleSet><PMID>999</PMID></PubmedArticleSet>",
        '<!DOCTYPE x [<!ENTITY x "bad">]><x/>',
    ],
)
def test_unusable_abstract_never_reaches_provider(client, fake, network, xml):
    network.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi").respond(200, text=xml)
    assert client.post("/api/ai/studies/summarize", json={"pmid": "123456"}).status_code == 503
    assert fake.calls == []


def test_cached_stream_sends_done_without_provider_or_quota(client, fake, db_session):
    doc = make_doc(client)
    path = f"/api/ai/documents/{doc['id']}/explain"
    client.post(path)
    response = client.post(path + "?stream=true")
    assert "event: done" in response.text and '"cached": true' in response.text
    assert len(fake.calls) == 1 and usage_today(db_session) == 1


def test_unchanged_seed_reuses_cache_after_reset(client, fake, db_session):
    from app.demo import reset_demo

    reset_demo(db_session)
    document_id = db_session.scalar(select(Document.id).order_by(Document.id))
    path = f"/api/ai/documents/{document_id}/explain"
    assert client.post(path).json()["cached"] is False
    reset_demo(db_session)
    assert client.post(path).json()["cached"] is True
    assert len(fake.calls) == 1


@pytest.mark.parametrize("role", ["doctor", "patient", None])
def test_admin_endpoints_reject_other_roles_before_provider(
    doctor_client, patient_client, anon_client, role
):
    target = {"doctor": doctor_client, "patient": patient_client, None: anon_client}[role]
    response = target.post("/api/ai/draft", json={"title": "Migräne"})
    assert response.status_code == (401 if role is None else 403)


def test_prewarm_reuses_cache_and_keeps_global_limit(db_session, fake, test_settings, client):
    import asyncio

    from app.ai.prewarm import prewarm

    make_doc(client)
    test_settings.ai_client_daily_limit = 1
    assert asyncio.run(prewarm(db_session, test_settings, fake, limit=1)) == {
        "completed": 8,
        "failed": 0,
    }
    assert asyncio.run(prewarm(db_session, test_settings, fake, limit=1)) == {
        "completed": 8,
        "failed": 0,
    }
    assert len(fake.calls) == 8 and usage_today(db_session) == 8
