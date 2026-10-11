from sqlalchemy import create_engine, inspect, text

from app.database import Base, upgrade_schema


def test_adds_the_actor_column_to_an_old_audit_log(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE audit_log (id INTEGER PRIMARY KEY, timestamp DATETIME, "
                "action VARCHAR(30), document_id INTEGER, detail VARCHAR(255))"
            )
        )
        conn.execute(text("INSERT INTO audit_log (action, detail) VALUES ('create', 'alt')"))

    Base.metadata.create_all(engine)
    upgrade_schema(engine)
    upgrade_schema(engine)  # idempotent

    columns = {c["name"] for c in inspect(engine).get_columns("audit_log")}
    assert "actor" in columns
    with engine.connect() as conn:
        assert conn.execute(text("SELECT detail, actor FROM audit_log")).one() == ("alt", None)


def test_adds_document_columns_to_an_old_database(tmp_path):
    from sqlalchemy.orm import Session

    from app.models import Document
    from app.schemas import DocumentOut

    engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE documents (id INTEGER PRIMARY KEY, title VARCHAR(200), "
                "content TEXT, category VARCHAR(50), doc_type VARCHAR(30), keywords JSON, "
                "source VARCHAR(200), auto_classified BOOLEAN, created_at DATETIME, "
                "updated_at DATETIME)"
            )
        )
        conn.execute(
            text(
                "INSERT INTO documents (title, content, category, doc_type, keywords, "
                "auto_classified, created_at, updated_at) VALUES ('Alt', 'Alter Inhalt', "
                "'HNO', 'Symptom', '[]', 1, '2026-01-01 00:00:00', '2026-01-01 00:00:00')"
            )
        )

    Base.metadata.create_all(engine)
    upgrade_schema(engine)
    upgrade_schema(engine)  # idempotent

    columns = {c["name"] for c in inspect(engine).get_columns("documents")}
    assert {
        "term_en",
        "icd11_code",
        "medications",
        "sections",
        "further_reading",
        "ai_generated",
    } <= columns
    with Session(engine) as db:
        out = DocumentOut.model_validate(db.get(Document, 1))
    assert out.medications == [] and out.further_reading == []
    assert out.sections is None and out.ai_generated is False


def test_server_databases_check_pooled_connections_before_use():
    # Neon suspends after 5 idle minutes and drops pooled connections; without a ping the next
    # request after a reading pause fails once with OperationalError.
    from app.database import make_engine

    assert make_engine("postgresql://user:pw@example.neon.tech/medkb").pool._pre_ping is True
    assert make_engine("sqlite://").pool._pre_ping is False
