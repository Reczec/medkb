import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.auth import create_token, decode_token, hash_password, verify_password
from app.config import Settings, get_settings
from app.main import app
from app.models import User
from app.users import ensure_users
from tests.conftest import ADMIN_PASSWORD, make_settings


def settings(**overrides) -> Settings:
    return Settings(_env_file=None, jwt_secret="unit-test-secret-with-32-bytes-ok!", **overrides)


def make_user() -> User:
    return User(id=7, username="dr", password_hash="x", role="doctor", display_name="Dr. Demo")


# ------------------------------------------------------------------------ helpers


def test_password_roundtrip():
    hashed = hash_password("geheim123")
    assert hashed != "geheim123"
    assert verify_password("geheim123", hashed)
    assert not verify_password("falsch", hashed)


def test_token_roundtrip_carries_id_and_role():
    claims = decode_token(create_token(make_user(), settings()), settings())
    assert claims["sub"] == "7"
    assert claims["role"] == "doctor"


def test_expired_token_is_rejected():
    token = create_token(make_user(), settings(jwt_hours=-1))
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token, settings())


def test_token_signed_with_other_secret_is_rejected():
    token = create_token(
        make_user(), Settings(_env_file=None, jwt_secret="another-secret-that-is-32-bytes-long")
    )
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token, settings())


# ---------------------------------------------------------------------------- API


@pytest.mark.parametrize("role", ["admin", "doctor", "patient"])
def test_demo_login_gives_a_token_for_the_role(anon_client, role):
    response = anon_client.post("/api/auth/demo", json={"role": role})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["role"] == role
    me = anon_client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"}
    )
    assert me.json()["role"] == role
    assert "password_hash" not in me.json()


def test_unknown_demo_role_is_rejected(anon_client):
    assert anon_client.post("/api/auth/demo", json={"role": "chef"}).status_code == 422


def test_password_login(anon_client):
    response = anon_client.post(
        "/api/auth/login", json={"username": "admin", "password": ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    assert response.json()["user"] == {
        "id": response.json()["user"]["id"],
        "username": "admin",
        "display_name": "Admin",
        "role": "admin",
    }


@pytest.mark.parametrize("username,password", [("admin", "falsch"), ("niemand", ADMIN_PASSWORD)])
def test_wrong_credentials_give_the_same_401(anon_client, username, password):
    response = anon_client.post(
        "/api/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Benutzername oder Passwort falsch"


def test_demo_accounts_cannot_log_in_with_a_guessed_password(anon_client):
    response = anon_client.post("/api/auth/login", json={"username": "demo-admin", "password": ""})
    assert response.status_code in (401, 422)


def test_me_requires_a_valid_token(anon_client):
    assert anon_client.get("/api/auth/me").status_code == 401
    bad = {"Authorization": "Bearer not-a-token"}
    assert anon_client.get("/api/auth/me", headers=bad).status_code == 401


def test_options_report_demo_mode(anon_client):
    assert anon_client.get("/api/auth/options").json() == {"demo_mode": True}


def test_demo_login_is_off_without_demo_mode(archive_dir):
    settings = make_settings(archive_dir, demo_mode=False)
    app.dependency_overrides[get_settings] = lambda: settings
    try:
        anon = TestClient(app)
        assert anon.post("/api/auth/demo", json={"role": "admin"}).status_code == 404
        assert anon.get("/api/auth/options").json() == {"demo_mode": False}
    finally:
        app.dependency_overrides.clear()


def test_ensure_users_is_idempotent_and_updates_the_admin_password(db_session, archive_dir):
    ensure_users(db_session, make_settings(archive_dir, admin_password="neues-passwort-123"))
    ensure_users(db_session, make_settings(archive_dir, admin_password="neues-passwort-123"))
    users = db_session.scalars(select(User)).all()
    assert sorted(u.username for u in users) == [
        "admin",
        "demo-admin",
        "demo-doctor",
        "demo-patient",
    ]
    admin = next(u for u in users if u.username == "admin")
    assert verify_password("neues-passwort-123", admin.password_hash)


def test_unknown_users_cost_as_much_as_wrong_passwords(anon_client, monkeypatch):
    # Otherwise the response time tells which usernames exist.
    import app.routers.auth as auth_router

    calls = []
    real = auth_router.verify_password
    monkeypatch.setattr(
        auth_router, "verify_password", lambda pw, hashed: calls.append(hashed) or real(pw, hashed)
    )
    anon_client.post("/api/auth/login", json={"username": "niemand", "password": "x"})
    assert len(calls) == 1


def test_admin_password_longer_than_bcrypt_limit_works(anon_client, db_session, archive_dir):
    long_password = "ä" * 60  # 120 bytes
    ensure_users(db_session, make_settings(archive_dir, admin_password=long_password))
    response = anon_client.post(
        "/api/auth/login", json={"username": "admin", "password": long_password}
    )
    assert response.status_code == 200
    wrong = anon_client.post(
        "/api/auth/login", json={"username": "admin", "password": "ä" * 59 + "a"}
    )
    assert wrong.status_code == 401


def test_token_without_exp_is_rejected(anon_client, test_settings, db_session):
    user = db_session.scalar(select(User).where(User.username == "demo-admin"))
    forever = jwt.encode({"sub": str(user.id), "role": "admin"}, test_settings.jwt_secret, "HS256")
    response = anon_client.get("/api/auth/me", headers={"Authorization": f"Bearer {forever}"})
    assert response.status_code == 401
