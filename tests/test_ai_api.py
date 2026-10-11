import json

import httpx
import pytest
from sqlalchemy import func, select, update

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
        assert "not medical advice" in response.json()["text"]


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
    response = client.post(
        "/api/ai/ask",
        json={"question": "KeinePassendenEinträge"},
        headers={"Accept-Language": "de"},
    )
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
    assert "individual diagnoses" in fake.calls[0][0]["content"]
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
    replacement_id = db_session.scalar(select(Document.id).order_by(Document.id))
    # Simulate PostgreSQL's continuing sequence even when this suite uses SQLite.
    new_id = replacement_id + 10_000
    db_session.execute(update(Document).where(Document.id == replacement_id).values(id=new_id))
    db_session.commit()
    assert client.post(f"/api/ai/documents/{new_id}/explain").json()["cached"] is True
    assert len(fake.calls) == 1


@pytest.mark.parametrize("question", ["Was ist Migräne?", "Was sind die Symptome von Migräne?"])
def test_natural_questions_retrieve_the_relevant_entry(client, fake, question):
    make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information [1]."
    response = client.post("/api/ai/ask", json={"question": question})
    assert response.status_code == 200
    assert len(response.json()["citations"]) == 1
    assert len(fake.calls) == 1


def test_followup_retrieves_the_previous_topic(client, fake):
    make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information [1]."
    response = client.post(
        "/api/ai/ask",
        json={
            "question": "Und wie wird das behandelt?",
            "history": [
                {"role": "user", "content": "Was ist Migräne?"},
                {"role": "assistant", "content": "Information [1]."},
            ],
        },
    )
    assert len(response.json()["citations"]) == 1
    assert len(fake.calls) == 1


def test_slow_abstract_does_not_block_unrelated_requests(client, fake, monkeypatch):
    import asyncio
    import threading
    import time

    import app.routers.ai as ai_router

    release = threading.Event()
    started = threading.Event()
    started_at = []

    def slow_fetch(*args):
        started_at.append(time.monotonic())
        started.set()
        release.wait(0.5)
        return "Abstract fixture."

    monkeypatch.setattr(ai_router, "fetch_abstract", slow_fetch)

    async def exercise():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test", headers=client.headers
        ) as concurrent:

            async def health():
                while not started.is_set():
                    await asyncio.sleep(0.001)
                response = await concurrent.get("/api/health")
                release.set()
                assert response.status_code == 200
                return time.monotonic() - started_at[0]

            results = await asyncio.gather(
                concurrent.post("/api/ai/studies/summarize", json={"pmid": "123456"}), health()
            )
            assert results[0].status_code == 200
            assert results[1] < 0.3

    asyncio.run(exercise())


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


def test_explain_is_plain_language_for_every_role(client, fake):
    # "Einfach erklärt" means plain language, also when a doctor or admin asks for it.
    doc = make_doc(client)
    client.post(f"/api/ai/documents/{doc['id']}/explain")
    assert "B1" in fake.calls[0][0]["content"]


def test_summary_stays_professional(doctor_client, client, fake):
    doc = make_doc(client)
    doctor_client.post(f"/api/ai/documents/{doc['id']}/summary")
    assert "professional language for medical staff" in fake.calls[0][0]["content"]


def test_red_flags_answer_only_with_warning_signs(patient_client, client, fake):
    doc = make_doc(client)
    patient_client.post(f"/api/ai/documents/{doc['id']}/red-flags")
    system = fake.calls[0][0]["content"]
    assert "Only warning signs" in system
    assert "### Call emergency number 144 now" in system


def test_prompts_ask_for_the_markdown_subset_the_ui_renders(patient_client, client, fake):
    doc = make_doc(client)
    patient_client.post(f"/api/ai/documents/{doc['id']}/explain")
    system = fake.calls[0][0]["content"]
    assert "### " in system and "- " in system and "**bold**" in system
    assert "Start directly with the content" in system


def _ask(client, ip=None):
    headers = {"True-Client-IP": ip} if ip else {}
    return client.post("/api/ai/ask", json={"question": "Migräne"}, headers=headers)


def test_spoofed_ip_header_is_ignored_without_configuration(client, fake, test_settings):
    make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information [1]."
    test_settings.ai_client_daily_limit = 1
    assert _ask(client, "203.0.113.1").status_code == 200
    assert _ask(client, "203.0.113.2").status_code == 429  # same real client, new fake header


def test_configured_proxy_header_separates_visitors(client, fake, test_settings):
    make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information [1]."
    test_settings.ai_client_daily_limit = 1
    test_settings.client_ip_header = "true-client-ip"
    assert _ask(client, "203.0.113.1").status_code == 200
    assert _ask(client, "203.0.113.2").status_code == 200
    assert _ask(client, "203.0.113.1").status_code == 429
    assert _ask(client).status_code == 200  # header missing: falls back to the connection


COLD = "Eine Erkältung wird durch Viren ausgelöst. Ruhe und ausreichend trinken lindern Schnupfen."


@pytest.mark.parametrize(
    "question",
    [
        "Was hilft bei Erkältung?",
        "Was kann man gegen eine Erkältung tun?",
        "Erkältung – was soll ich machen?",
    ],
)
def test_everyday_questions_find_the_entry(client, fake, question):
    make_doc(client, title="Erkältung (grippaler Infekt)", content=COLD)
    fake.answer = "Allgemeine Information [1]."
    response = client.post("/api/ai/ask", json={"question": question})
    assert response.status_code == 200, response.text
    assert [c["title"] for c in response.json()["citations"]] == ["Erkältung (grippaler Infekt)"]


def test_unknown_extra_words_fall_back_to_the_best_partial_matches(client, fake):
    make_doc(client, title="Erkältung (grippaler Infekt)", content=COLD)
    make_doc(client, title="Migräne", content="Anfallsartige Kopfschmerzen mit Übelkeit.")
    fake.answer = "Allgemeine Information [1]."
    response = client.post("/api/ai/ask", json={"question": "Erkältung Schnupfen Wadenkrampf"})
    assert response.status_code == 200, response.text
    context = fake.calls[0][1]["content"]
    assert "Erkältung" in context and "Migräne" not in context


def test_partial_matches_rank_entries_with_more_hits_first(client):
    from app.ai.retrieval import find
    from app.ai.schemas import AskRequest
    from app.database import SessionLocal

    make_doc(client, title="Nur Schnupfen", content="Ein Text über Schnupfen allein.")
    make_doc(client, title="Erkältung (grippaler Infekt)", content=COLD)
    with SessionLocal() as db:
        found = find(db, AskRequest(question="Erkältung Schnupfen Wadenkrampf"))
    assert [d.title for d in found][:2] == ["Erkältung (grippaler Infekt)", "Nur Schnupfen"]


def test_rare_words_outweigh_common_ones_in_partial_matches(client):
    from app.ai.retrieval import find
    from app.ai.schemas import AskRequest
    from app.database import SessionLocal

    for title in ("Eins", "Zwei", "Drei"):
        make_doc(client, title=title, content="Das kann gefährlich werden, sagt der Text.")
    make_doc(client, title="Sepsis (Blutvergiftung)", content="Eine lebensbedrohliche Reaktion.")
    with SessionLocal() as db:
        found = find(db, AskRequest(question="Wie gefährlich ist eine Blutvergiftung?"))
    assert found[0].title == "Sepsis (Blutvergiftung)"


def test_title_hits_break_ties_in_partial_matches(client):
    from app.ai.retrieval import find
    from app.ai.schemas import AskRequest
    from app.database import SessionLocal

    make_doc(client, title="Neurodermitis", content="Eine gefährliche Herpes-Infektion der Haut.")
    make_doc(client, title="Sepsis (Blutvergiftung)", content="Eine lebensbedrohliche Reaktion.")
    with SessionLocal() as db:
        found = find(db, AskRequest(question="Wie gefährlich ist eine Blutvergiftung?"))
    assert found[0].title == "Sepsis (Blutvergiftung)"


def test_proxy_header_uses_the_value_the_proxy_appended(client, fake, test_settings):
    # With a list-valued header the proxy appends the real client last; earlier values are
    # whatever the visitor sent.
    make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information [1]."
    test_settings.ai_client_daily_limit = 1
    test_settings.client_ip_header = "x-real-chain"
    send = lambda first: client.post(  # noqa: E731
        "/api/ai/ask",
        json={"question": "Migräne"},
        headers={"X-Real-Chain": f"{first}, 198.51.100.7"},
    )
    assert send("203.0.113.1").status_code == 200
    assert send("203.0.113.2").status_code == 429  # same real client behind a new fake prefix


def test_prewarm_can_pause_between_calls_for_provider_rate_limits(
    db_session, fake, test_settings, client, monkeypatch
):
    import asyncio

    import app.ai.prewarm as prewarm_module

    make_doc(client)
    pauses = []

    async def fake_sleep(seconds):
        pauses.append(seconds)

    monkeypatch.setattr(prewarm_module.asyncio, "sleep", fake_sleep)
    result = asyncio.run(prewarm_module.prewarm(db_session, test_settings, fake, limit=1, pause=4))
    assert result == {"completed": 8, "failed": 0}
    assert pauses == [4] * 7  # between the 8 calls, not after the last


@pytest.mark.parametrize(
    ("header", "limit_text", "notice"),
    [
        (
            "de",
            "KI-Tageslimit erreicht. Bitte morgen erneut versuchen.",
            "Prototyp mit Beispieldaten",
        ),
        ("en", "Daily AI limit reached. Please try again tomorrow.", "Prototype with example data"),
        (None, "Daily AI limit reached. Please try again tomorrow.", "Prototype with example data"),
    ],
)
def test_ai_messages_follow_the_request_language(
    client, fake, test_settings, header, limit_text, notice
):
    make_doc(client, title="Migräne")
    fake.answer = "Allgemeine Information [1]."
    test_settings.ai_client_daily_limit = 1
    headers = {"Accept-Language": header} if header else {}
    first = client.post("/api/ai/ask", json={"question": "Migräne"}, headers=headers)
    assert first.status_code == 200
    assert notice in first.json()["text"]
    second = client.post("/api/ai/ask", json={"question": "Migräne"}, headers=headers)
    assert second.status_code == 429
    assert second.json()["detail"] == limit_text


def test_no_matching_entries_is_english_without_a_header(client, fake):
    response = client.post("/api/ai/ask", json={"question": "KeinePassendenEinträge"})
    assert "no matching entries" in response.json()["text"].lower()
    assert "Prototype with example data" in response.json()["text"]


def test_stream_error_message_follows_the_request_language(client, fake):
    doc = make_doc(client)
    fake.stream_fail = True
    de = client.post(
        f"/api/ai/documents/{doc['id']}/explain?stream=true", headers={"Accept-Language": "de"}
    )
    en = client.post(f"/api/ai/documents/{doc['id']}/explain?stream=true")
    assert "nicht vollständig erstellt" in de.text
    assert "could not be completed" in en.text


# --------------------------------------------------------- language of AI requests

ENGLISH_DOC = {
    "title": "Erkältung",
    "content": "Eine Erkältung wird durch Viren ausgelöst. Ruhe und Trinken helfen.",
    "doc_type": "Beschreibung",
    "title_en": "Common cold",
    "sections_en": {"definition": "A cold is caused by viruses.", "therapy": "Rest and fluids."},
}


def _system(fake, index=0):
    return fake.calls[index][0]["content"]


def _user(fake, index=0):
    return fake.calls[index][1]["content"]


def test_german_cache_key_is_unchanged(test_settings):
    # Pinned from the code before the language feature: the warmed German answers must keep
    # hitting. Inputs have the shape document_inputs produced then.
    from app.ai import store
    from app.config import Settings

    settings = Settings(
        _env_file=None,
        jwt_secret="x",
        ai_model="gemini-3.5-flash-lite",
        ai_base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    inputs = {
        "title": "Migräne",
        "content": "Definition\nText.",
        "category": "Neurologie",
        "doc_type": "Diagnose",
        "keywords": ["Migräne"],
        "source": "Redaktionelle Demo-Inhalte auf Lehrbuchniveau – keine medizinische Beratung",
        "auto_classified": True,
        "term_en": "Migraine",
        "icd11_code": "8A80",
        "medications": ["sumatriptan"],
        "sections": {
            "definition": "Text.",
            "symptoms": None,
            "causes": None,
            "diagnostics": None,
            "therapy": None,
            "red_flags": None,
        },
        "further_reading": [{"label": "Portal", "url": "https://www.who.int/x"}],
        "ai_generated": False,
    }
    key = store.cache_key("explain", "seed:Migräne", inputs, "patient", settings)
    assert key == "5ce74d3f3f392e5aea408281fc60ad83fd8656137180920fc54ec85270836860"
    assert store.cache_key("explain", "seed:Migräne", inputs, "patient", settings, "de") == key
    assert store.cache_key("explain", "seed:Migräne", inputs, "patient", settings, "en") != key


def test_german_document_inputs_keep_their_old_shape(client):
    from app.ai.service import document_inputs
    from app.database import SessionLocal
    from app.models import Document

    doc = make_doc(
        client,
        title="Migräne",
        title_en="Migraine",
        further_reading=[
            {"label": "Portal", "label_en": "Portal EN", "url": "https://www.who.int/x"}
        ],
    )
    with SessionLocal() as db:
        inputs = document_inputs(db.get(Document, doc["id"]))
    assert set(inputs) == {
        "title",
        "content",
        "category",
        "doc_type",
        "keywords",
        "source",
        "auto_classified",
        "term_en",
        "icd11_code",
        "medications",
        "sections",
        "further_reading",
        "ai_generated",
    }
    assert inputs["further_reading"] == [{"label": "Portal", "url": "https://www.who.int/x"}]
    assert inputs["title"] == "Migräne"


def test_english_inputs_use_the_english_version_with_german_fallback(client):
    from app.ai.service import document_inputs
    from app.database import SessionLocal
    from app.models import Document

    doc = client.post("/api/documents", json=ENGLISH_DOC).json()
    with SessionLocal() as db:
        english = document_inputs(db.get(Document, doc["id"]), "en")
        german = document_inputs(db.get(Document, doc["id"]), "de")
    assert english["title"] == "Common cold"
    assert english["content"].startswith("Definition\nA cold is caused by viruses.")
    assert english["sections"]["therapy"] == "Rest and fluids."
    assert german["title"] == "Erkältung"
    # Without any English version the German text is used.
    plain = make_doc(client, title="Nur Deutsch")
    with SessionLocal() as db:
        assert document_inputs(db.get(Document, plain["id"]), "en")["title"] == "Nur Deutsch"


def test_prompt_names_the_answer_language(client, fake):
    doc = client.post("/api/documents", json=ENGLISH_DOC).json()
    client.post(f"/api/ai/documents/{doc['id']}/explain", headers={"Accept-Language": "en"})
    client.post(f"/api/ai/documents/{doc['id']}/explain", headers={"Accept-Language": "de"})
    assert "Answer in English." in _system(fake, 0) and "Common cold" in _user(fake, 0)
    assert "Answer in German." in _system(fake, 1) and "Erkältung" in _user(fake, 1)


def test_red_flag_headings_follow_the_language(client, fake):
    doc = make_doc(client)
    client.post(f"/api/ai/documents/{doc['id']}/red-flags", headers={"Accept-Language": "de"})
    assert "### Sofort Notruf 144" in _system(fake)
    assert "### Zeitnah ärztlich abklären" in _system(fake)


def test_cache_is_separate_per_language(client, fake):
    doc = client.post("/api/documents", json=ENGLISH_DOC).json()
    path = f"/api/ai/documents/{doc['id']}/explain"
    en = {"Accept-Language": "en"}
    de = {"Accept-Language": "de"}
    assert client.post(path, headers=en).json()["cached"] is False
    assert client.post(path, headers=de).json()["cached"] is False  # not the English answer
    assert client.post(path, headers=en).json()["cached"] is True
    assert client.post(path, headers=de).json()["cached"] is True
    assert len(fake.calls) == 2


def test_draft_is_always_written_in_german(client, fake):
    fake.answer = json.dumps(
        {"content": "Ein deutscher Entwurf mit genug Zeichen.", "doc_type": "Diagnose"}
    )
    response = client.post(
        "/api/ai/draft", json={"title": "Shingles"}, headers={"Accept-Language": "en"}
    )
    assert response.status_code == 200
    assert "Answer in German." in _system(fake) and "Answer in English." not in _system(fake)
    assert "Prototype with example data" in response.json()["text"]  # notice in the UI language


def test_english_question_finds_the_entry_through_its_english_version(client, fake):
    client.post("/api/documents", json=ENGLISH_DOC)
    fake.answer = "A cold is caused by viruses [1]."
    response = client.post(
        "/api/ai/ask",
        json={"question": "What helps with a cold?"},
        headers={"Accept-Language": "en"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["citations"][0]["title"] == "Common cold"
    assert "Rest and fluids." in _user(fake)
    de = client.post(
        "/api/ai/ask", json={"question": "Erkältung"}, headers={"Accept-Language": "de"}
    )
    assert de.json()["citations"][0]["title"] == "Erkältung"


def test_prewarm_writes_separate_english_and_german_entries(
    db_session, fake, test_settings, client
):
    import asyncio

    from app.ai.prewarm import prewarm

    client.post("/api/documents", json=ENGLISH_DOC)
    english = asyncio.run(prewarm(db_session, test_settings, fake, limit=1, lang="en"))
    assert english == {"completed": 8, "failed": 0}
    assert db_session.scalar(select(func.count()).select_from(AICache)) == 8
    asyncio.run(prewarm(db_session, test_settings, fake, limit=1, lang="de"))
    assert db_session.scalar(select(func.count()).select_from(AICache)) == 16
    again = asyncio.run(prewarm(db_session, test_settings, fake, limit=1, lang="en"))
    assert again == {"completed": 8, "failed": 0}
    assert len(fake.calls) == 16  # the repeat came from the cache
