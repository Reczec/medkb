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
