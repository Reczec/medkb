"""Test setup.

By default the tests run against an in-memory SQLite database. Set TEST_DATABASE_URL to run the
same tests against another database, e.g. PostgreSQL:

    TEST_DATABASE_URL=postgresql+psycopg://medkb:medkb@localhost:5432/medkb_test pytest
"""

import os

# Must be set before the application modules are imported (the engine is created on import).
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "sqlite://")

import pytest  # noqa: E402
import respx  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from pwdlib import PasswordHash  # noqa: E402
from pwdlib.hashers.bcrypt import BcryptHasher  # noqa: E402

import app.auth as _auth  # noqa: E402
from app.config import Settings, get_settings  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.users import ensure_users  # noqa: E402

# Full-strength bcrypt costs ~0.25 s per hash; tests only need it to work, not to be slow.
_auth._hasher = PasswordHash((BcryptHasher(rounds=4),))

JWT_SECRET = "test-secret-that-is-at-least-32-bytes"
ADMIN_PASSWORD = "admin-test-password"


def make_settings(archive_dir, **overrides) -> Settings:
    values = {
        "database_url": "sqlite://",
        "archive_dir": archive_dir,
        "jwt_secret": JWT_SECRET,
        "demo_mode": True,
        "admin_password": ADMIN_PASSWORD,
        **overrides,
    }
    return Settings(_env_file=None, **values)


@pytest.fixture(autouse=True)
def clean_database(tmp_path):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        ensure_users(db, make_settings(tmp_path / "archives"))
    yield


@pytest.fixture(autouse=True)
def network():
    """No test reaches the internet. Unmatched requests get an empty 200 response, which the
    source clients treat as "unavailable"; tests add their own routes with ``network.get(...)``."""
    with respx.mock(assert_all_called=False, assert_all_mocked=False) as router:
        yield router


@pytest.fixture
def db_session():
    with SessionLocal() as session:
        yield session


@pytest.fixture
def archive_dir(tmp_path):
    return tmp_path / "archives"


def _client_for(role: str | None) -> TestClient:
    # No "with" block: the startup hook (table creation, seeding) is handled by the fixtures.
    test_client = TestClient(app)
    if role:
        response = test_client.post("/api/auth/demo", json={"role": role})
        assert response.status_code == 200, response.text
        test_client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    return test_client


@pytest.fixture
def test_settings(archive_dir):
    settings = make_settings(archive_dir)
    app.dependency_overrides[get_settings] = lambda: settings
    yield settings
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_settings):
    """Logged in as the demo admin."""
    return _client_for("admin")


@pytest.fixture
def doctor_client(test_settings):
    return _client_for("doctor")


@pytest.fixture
def patient_client(test_settings):
    return _client_for("patient")


@pytest.fixture
def anon_client(test_settings):
    return _client_for(None)


def make_doc(
    client, title="Testeintrag", content="Ein Text über Kopfschmerzen und Migräne.", **extra
):
    payload = {"title": title, "content": content, "doc_type": "Symptom", **extra}
    response = client.post("/api/documents", json=payload)
    assert response.status_code == 201, response.text
    return response.json()
