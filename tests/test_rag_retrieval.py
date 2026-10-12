import pytest
from fastapi import HTTPException

from app.ai.provider import get_provider
from app.ai.schemas import AskRequest
from app.ai.store import usage_today
from app.main import app
from tests.conftest import make_doc
from tests.test_ai_api import FakeProvider
from tests.test_rag_index import FakeEmbeddings


def setup_index(client, db, settings):
    from app.rag.index import build_index

    doc = make_doc(client, title="Migräne")
    provider = FakeEmbeddings()
    build_index(db, settings, provider, pause=0)
    settings.rag_enabled = True
    return doc, provider


def test_hybrid_sources_are_exact_excerpts_and_query_is_not_stripped(
    client, db_session, test_settings
):
    from app.rag.retrieval import retrieve

    doc, provider = setup_index(client, db_session, test_settings)
    body = AskRequest(question="Could a pounding head happen without nausea?")
    result = retrieve(db_session, body, "en", test_settings, provider, "visitor")
    assert result.mode == "hybrid" and result.reason is None
    assert result.citations[0]["id"] == doc["id"]
    assert result.citations[0]["excerpt"] == result.entries[0]["content"]
    assert provider.calls[-1][0] == [body.question]
    assert usage_today(db_session) == 2


def test_followup_retains_question_and_previous_topic(client, db_session, test_settings):
    from app.rag.retrieval import retrieve

    _, provider = setup_index(client, db_session, test_settings)
    body = AskRequest(
        question="How is it treated?",
        history=[
            {"role": "user", "content": "What is migraine?"},
            {"role": "assistant", "content": "General information [1]."},
        ],
    )
    retrieve(db_session, body, "en", test_settings, provider, "visitor")
    assert "How is it treated?" in provider.calls[-1][0][0]
    assert "migraine" in provider.calls[-1][0][0]


def test_low_semantic_similarity_abstains_without_lexical_bypass(client, db_session, test_settings):
    from app.rag.retrieval import retrieve

    _, provider = setup_index(client, db_session, test_settings)
    provider.embed = lambda texts, task: [[0, 1] + [0] * 766]
    result = retrieve(
        db_session, AskRequest(question="Migräne"), "de", test_settings, provider, "visitor"
    )
    assert result.mode == "hybrid" and not result.entries


@pytest.mark.parametrize("reason", ["disabled", "index_incomplete", "embedding_unavailable"])
def test_fallback_reports_real_mode(client, db_session, test_settings, reason):
    from app.rag.retrieval import retrieve

    provider = FakeEmbeddings()
    if reason == "embedding_unavailable":
        setup_index(client, db_session, test_settings)
        provider.fail_at = 1
    else:
        make_doc(client, title="Migräne")
        test_settings.rag_enabled = reason != "disabled"
    result = retrieve(
        db_session, AskRequest(question="Migräne"), "de", test_settings, provider, "visitor"
    )
    assert result.mode == "lexical" and result.reason == reason and result.citations


def test_quota_exhaustion_never_falls_back(client, db_session, test_settings):
    from app.rag.retrieval import retrieve

    _, provider = setup_index(client, db_session, test_settings)
    test_settings.ai_daily_limit = 1
    with pytest.raises(HTTPException) as error:
        retrieve(
            db_session, AskRequest(question="Migräne"), "de", test_settings, provider, "visitor"
        )
    assert error.value.status_code == 429 and len(provider.calls) == 1


def test_empty_generic_questions_do_not_call_models(client, db_session, test_settings):
    from app.rag.retrieval import retrieve

    _, provider = setup_index(client, db_session, test_settings)
    result = retrieve(
        db_session, AskRequest(question="???"), "de", test_settings, provider, "visitor"
    )
    assert not result.entries and len(provider.calls) == 1


def test_api_json_and_sse_done_have_metadata_and_only_used_sources(
    client, db_session, test_settings, monkeypatch
):
    import app.rag.retrieval as rag

    _, embeddings = setup_index(client, db_session, test_settings)
    make_doc(client, title="Zweiter Migräne-Eintrag")
    from app.rag.index import build_index

    build_index(db_session, test_settings, embeddings, pause=0)
    monkeypatch.setattr(rag, "get_embeddings", lambda settings: embeddings)
    provider = FakeProvider()
    provider.answer = "General evidence [1]."
    app.dependency_overrides[get_provider] = lambda: provider
    result = client.post("/api/ai/ask", json={"question": "Migräne"}).json()
    assert result["retrieval"]["mode"] == "hybrid"
    assert len(result["citations"]) == 1
    assert "excerpt" in result["citations"][0]
    response = client.post("/api/ai/ask?stream=true", json={"question": "Migräne"})
    assert '"mode": "hybrid"' in response.text and "event: done" in response.text


def test_rank_context_is_bounded_and_sources_distinct(client, db_session, test_settings):
    from app.rag.index import build_index
    from app.rag.retrieval import retrieve

    for number in range(7):
        make_doc(client, title=f"Topic {number}", content="topic " * 450)
    provider = FakeEmbeddings()
    build_index(db_session, test_settings, provider, pause=0)
    test_settings.rag_enabled = True
    result = retrieve(
        db_session, AskRequest(question="Topic"), "en", test_settings, provider, "visitor"
    )
    assert len({ref["id"] for ref in result.citations}) <= 5
    assert all(
        sum(ref["id"] == other["id"] for other in result.citations) <= 2 for ref in result.citations
    )
    assert (
        sum(len(e["title"]) + len(e["section"]) + len(e["content"]) for e in result.entries) <= 6000
    )
    again = retrieve(
        db_session, AskRequest(question="Topic"), "en", test_settings, provider, "visitor"
    )
    assert result.citations == again.citations
