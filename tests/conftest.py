"""Test setup.

By default the tests run against an in-memory SQLite database. Set TEST_DATABASE_URL to run the
same tests against another database, e.g. PostgreSQL:

    TEST_DATABASE_URL=postgresql+psycopg://medkb:medkb@localhost:5432/medkb_test pytest
"""

import os

# Must be set before the application modules are imported (the engine is created on import).
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "sqlite://")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.config import Settings, get_settings  # noqa: E402
from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402

ADMIN_TOKEN = "test-admin-token"
ADMIN = {"X-Admin-Token": ADMIN_TOKEN}


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def archive_dir(tmp_path):
    return tmp_path / "archives"


@pytest.fixture
def client(archive_dir):
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None, database_url="sqlite://", admin_token=ADMIN_TOKEN, archive_dir=archive_dir
    )
    # No "with" block: the startup hook (table creation, seeding) is handled by the fixture above.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def admin_disabled_client(archive_dir):
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None, database_url="sqlite://", admin_token="", archive_dir=archive_dir
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_doc(
    client, title="Testeintrag", content="Ein Text über Kopfschmerzen und Migräne.", **extra
):
    payload = {"title": title, "content": content, "doc_type": "Symptom", **extra}
    response = client.post("/api/documents", json=payload)
    assert response.status_code == 201, response.text
    return response.json()
