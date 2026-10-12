"""Regressions from the fresh whole-branch review; all providers are synthetic."""

import asyncio
import json
import threading

import pytest
from sqlalchemy import text

from app.ai.provider import get_provider
from app.ai.schemas import AskRequest
from app.main import app
from app.models import Document
from app.rag import retrieval
from app.rag.evaluate import evaluate
from app.rag.index import build_index
from tests.conftest import make_doc
from tests.test_ai_api import FakeProvider
from tests.test_rag_index import FakeEmbeddings


@pytest.mark.parametrize(
    "lang,question,section,history",
    [
        ("en", "How is migraine treated?", "therapy", []),
        ("de", "Wie wird Migräne behandelt?", "therapy", []),
        ("en", "Which migraine warning signs are an emergency?", "red_flags", []),
        ("de", "Welche Warnzeichen bei Migräne sind gefährlich?", "red_flags", []),
        (
            "en",
            "How is it diagnosed?",
            "diagnostics",
            [{"role": "user", "content": "What is migraine?"}],
        ),
        (
            "de",
            "Wie wird es behandelt?",
            "therapy",
            [{"role": "user", "content": "Was ist Migräne?"}],
        ),
    ],
)
def test_keyword_fallback_preserves_original_section_intent(
    client, db_session, lang, question, section, history
):
    make_doc(
        client,
        title="Migräne",
        title_en="Migraine",
        sections={
            "definition": "Migräne bezeichnet wiederkehrende Kopfschmerzen.",
            "symptoms": "Migräne kann Lichtempfindlichkeit verursachen.",
            "causes": "Die Ursachen sind vielfältig.",
            "diagnostics": "Die Untersuchung erfolgt anhand der Anamnese.",
            "therapy": "Die Behandlung umfasst allgemeine Maßnahmen.",
            "red_flags": "Plötzliche neue neurologische Ausfälle sind Warnzeichen.",
        },
    )
    found = retrieval.fallback(
        db_session, AskRequest(question=question, history=history), lang, "disabled"
    )
    assert section in [entry["section"] for entry in found.entries]
    assert len(found.entries) <= 2
    provider = FakeProvider()
    provider.answer = "General information [1]."
    app.dependency_overrides[get_provider] = lambda: provider
    response = client.post(
        "/api/ai/ask",
        headers={"Accept-Language": lang},
        json={"question": question, "history": history},
    )
    assert response.status_code == 200
    inputs = json.loads(provider.calls[-1][-1]["content"])
    assert section in [entry["section"] for entry in inputs["entries"]]


@pytest.mark.parametrize("change", ["same_id", "new_id"])
def test_evaluation_invalidates_changed_corpus_instead_of_false_success(
    client, db_session, test_settings, change
):
    make_doc(client, title="Original")
    provider = FakeEmbeddings()
    build_index(db_session, test_settings, provider, pause=0)

    def replace():
        provider.on_call = None
        document = db_session.query(Document).one()
        if change == "same_id":
            document.title = "Replacement"
        else:
            document.id = 99
        db_session.commit()
        build_index(db_session, test_settings, FakeEmbeddings(), pause=0)

    provider.on_call = replace
    result = evaluate(
        db_session,
        test_settings,
        [
            {
                "id": "fixture",
                "lang": "de",
                "kind": "answerable",
                "question": "Original?",
                "expected": ["Original"],
                "section": "content",
                "synonym": False,
            }
        ],
        provider,
        pause=0,
    )
    assert result["valid"] is False
    assert result["invalid_reason"] == "corpus_changed"
    assert result["hybrid"]["hit_at_5"] is None
    assert result["lexical"]["hit_at_5"] is None


def test_cancellation_waits_for_database_worker_before_owner_closes(monkeypatch, db_session):
    started, release = threading.Event(), threading.Event()
    closed = False
    completion_started = False

    def worker(db):
        db.execute(text("SELECT 1"))
        started.set()
        assert release.wait(5)
        assert not closed
        db.execute(text("SELECT 1"))

    monkeypatch.setattr(retrieval, "retrieve", worker)

    async def run():
        nonlocal closed, completion_started

        async def owner():
            nonlocal closed, completion_started
            try:
                if hasattr(retrieval, "retrieve_async"):
                    await retrieval.retrieve_async(db_session)
                else:
                    await asyncio.to_thread(retrieval.retrieve, db_session)
                completion_started = True
            finally:
                db_session.close()
                closed = True

        task = asyncio.create_task(owner())
        assert await asyncio.to_thread(started.wait, 5)
        task.cancel()
        await asyncio.sleep(0.01)
        task.cancel()  # repeated cancellation must not abandon the session worker either
        await asyncio.sleep(0.01)
        try:
            assert not task.done() and not closed
        finally:
            release.set()
            with pytest.raises(asyncio.CancelledError):
                await task
        assert closed and not completion_started and not db_session.in_transaction()

    asyncio.run(run())
