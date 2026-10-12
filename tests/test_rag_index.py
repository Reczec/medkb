import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.ai.provider import AIUnavailable
from app.ai.store import usage_today
from app.models import Document
from tests.conftest import make_doc


class FakeEmbeddings:
    def __init__(self):
        self.calls = []
        self.fail_at = 0
        self.on_call = None

    def embed(self, texts, task):
        self.calls.append((texts, task))
        if self.on_call:
            self.on_call()
        if len(self.calls) == self.fail_at:
            raise AIUnavailable("embedding_unavailable")
        return [[1.0] + [0.0] * 767 for _ in texts]


def test_index_resumes_and_reserves_only_missing_batches(client, db_session, test_settings):
    from app.rag.index import build_index, load_current

    make_doc(client)
    provider = FakeEmbeddings()
    report = build_index(db_session, test_settings, provider, pause=0)
    assert report.failed == 0 and report.ready == report.total == 2
    assert len(provider.calls) == 1 and usage_today(db_session) == 1
    assert len(load_current(db_session, test_settings, "de")) == 1
    assert build_index(db_session, test_settings, provider, pause=0).ready == 2
    assert len(provider.calls) == 1


def test_changed_deleted_or_reset_ids_cannot_reuse_stale_evidence(
    client, db_session, test_settings
):
    from app.rag.index import build_index, load_current

    make_doc(client)
    build_index(db_session, test_settings, FakeEmbeddings(), pause=0)
    doc = db_session.scalar(select(Document))
    doc.id += 1000
    db_session.commit()
    assert load_current(db_session, test_settings, "de")[0][0].document_id == doc.id
    doc.content = "Different content after restoring an archive"
    db_session.commit()
    assert load_current(db_session, test_settings, "de") is None
    db_session.delete(doc)
    db_session.commit()
    assert load_current(db_session, test_settings, "de") == []


def test_partial_failure_preserves_successful_batches(client, db_session, test_settings):
    from app.rag.index import build_index

    for number in range(9):
        make_doc(client, title=f"Entry {number}")
    provider = FakeEmbeddings()
    provider.fail_at = 2
    report = build_index(db_session, test_settings, provider, pause=0)
    assert report.ready == 16 and report.total == 18 and report.failed == 2
    assert usage_today(db_session) == 2
    report = build_index(db_session, test_settings, provider, pause=0)
    assert report.ready == 18 and report.failed == 0
    assert len(provider.calls) == 3


def test_concurrent_content_change_does_not_publish_stale_ready_state(
    client, db_session, test_settings
):
    from app.rag.index import build_index, load_current

    make_doc(client)
    provider = FakeEmbeddings()

    def edit():
        doc = db_session.scalar(select(Document))
        doc.content = "Edited while the embedding request was running"
        db_session.commit()

    provider.on_call = edit
    report = build_index(db_session, test_settings, provider, pause=0)
    assert report.ready == 0
    assert load_current(db_session, test_settings, "de") is None


def test_corrupt_vector_is_rebuilt_and_never_loaded(client, db_session, test_settings):
    from app.models import Embedding
    from app.rag.index import build_index, load_current

    make_doc(client)
    provider = FakeEmbeddings()
    build_index(db_session, test_settings, provider, pause=0)
    for row in db_session.scalars(select(Embedding)):
        row.vector = [0.0] * 768
    db_session.commit()
    assert load_current(db_session, test_settings, "de") is None
    assert build_index(db_session, test_settings, provider, pause=0).ready == 2


def test_bound_and_global_quota_prevent_unbounded_index_calls(client, db_session, test_settings):
    from app.rag.index import build_index

    make_doc(client)
    provider = FakeEmbeddings()
    test_settings.rag_max_chunks = 1
    with pytest.raises(ValueError):
        build_index(db_session, test_settings, provider, pause=0)
    assert not provider.calls
    test_settings.rag_max_chunks = 5000
    test_settings.ai_daily_limit = 1
    test_settings.ai_client_daily_limit = 1
    assert build_index(db_session, test_settings, provider, pause=0).ready == 2
    doc = db_session.scalar(select(Document))
    doc.content = "Changed content requiring another provider call"
    db_session.commit()
    with pytest.raises(HTTPException) as error:
        build_index(db_session, test_settings, provider, pause=0)
    assert error.value.status_code == 429 and len(provider.calls) == 1


def test_cleanup_is_explicit_and_preserves_live_vectors(client, db_session, test_settings):
    from app.models import Embedding
    from app.rag.index import build_index

    make_doc(client)
    provider = FakeEmbeddings()
    build_index(db_session, test_settings, provider, pause=0)
    db_session.add(Embedding(key="f" * 64, signature="unused", vector=[1] + [0] * 767))
    db_session.commit()
    build_index(db_session, test_settings, provider, pause=0)
    assert db_session.get(Embedding, "f" * 64) is not None
    report = build_index(db_session, test_settings, provider, pause=0, cleanup=True)
    assert report.ready == 2 and db_session.get(Embedding, "f" * 64) is None
