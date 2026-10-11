import asyncio

from sqlalchemy import func, select

import app.demo as demo
from app.models import AuditLog, Document
from app.seed_data import SEED_DOCUMENTS
from tests.conftest import ADMIN_PASSWORD, make_doc


def test_reset_restores_the_seed_entries_and_clears_the_log(client, db_session):
    make_doc(client, title="Wird beim Reset verworfen")

    count = demo.reset_demo(db_session)

    assert count == len(SEED_DOCUMENTS)
    assert db_session.scalar(select(func.count(Document.id))) == len(SEED_DOCUMENTS)
    titles = db_session.scalars(select(Document.title)).all()
    assert "Wird beim Reset verworfen" not in titles
    log = db_session.scalars(select(AuditLog)).all()
    assert [(e.action, e.actor) for e in log] == [("demo_reset", "system")]


def test_reset_keeps_the_logins(client, anon_client, db_session):
    demo.reset_demo(db_session)
    response = anon_client.post(
        "/api/auth/login", json={"username": "admin", "password": ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    assert anon_client.post("/api/auth/demo", json={"role": "patient"}).status_code == 200


def test_reset_loop_runs_the_reset_periodically(monkeypatch, archive_dir):
    calls = []
    monkeypatch.setattr(demo, "reset_demo", lambda db: calls.append(1) or 0)

    async def run():
        settings = type("S", (), {"demo_reset_hours": 0.01 / 3600})()  # every 10 ms
        task = asyncio.create_task(demo.demo_reset_loop(settings))
        await asyncio.sleep(0.1)
        task.cancel()

    asyncio.run(run())
    assert len(calls) >= 2


def test_reset_is_one_transaction(client, db_session, monkeypatch):
    make_doc(client, title="Bleibt bei einem Fehler erhalten")
    before = db_session.scalars(select(Document.title)).all()
    log_before = db_session.scalar(select(func.count(AuditLog.id)))

    import app.services as services

    real_create = services.create_document
    calls = []

    def failing_create(*args, **kwargs):
        calls.append(1)
        if len(calls) == 5:
            raise RuntimeError("Abbruch mitten im Reset")
        return real_create(*args, **kwargs)

    monkeypatch.setattr("app.seed.create_document", failing_create)
    try:
        demo.reset_demo(db_session)
    except RuntimeError:
        pass
    else:
        raise AssertionError("reset should have failed")

    db_session.expire_all()
    assert db_session.scalars(select(Document.title)).all() == before
    assert db_session.scalar(select(func.count(AuditLog.id))) == log_before


def test_reader_never_sees_an_empty_base_during_reset(client, db_session, monkeypatch):
    from app.database import SessionLocal

    make_doc(client, title="Alter Stand")
    seen = []
    real_commit = db_session.commit

    def look_then_commit():
        with SessionLocal() as reader:
            seen.append(reader.scalar(select(func.count(Document.id))))
        real_commit()

    monkeypatch.setattr(db_session, "commit", look_then_commit)
    demo.reset_demo(db_session)
    assert seen and min(seen) > 0
