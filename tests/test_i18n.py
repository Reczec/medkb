"""Request language and localized server messages (spec: Mehrsprachigkeit §4)."""

import re

import pytest

from app.i18n import MESSAGES, message, parse_language


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        (None, "en"),
        ("", "en"),
        ("de", "de"),
        ("de-AT,de;q=0.9", "de"),
        ("EN-gb", "en"),
        ("fr", "en"),
        ("fr, de", "en"),  # only the first entry counts
        ("*", "en"),
        (";;q=", "en"),
    ],
)
def test_parse_language(header, expected):
    assert parse_language(header) == expected


def test_every_message_exists_in_both_languages_with_the_same_placeholders():
    placeholders = lambda text: sorted(re.findall(r"\{(\w+)\}", text))  # noqa: E731
    for code, texts in MESSAGES.items():
        assert set(texts) == {"en", "de"}, code
        assert texts["en"].strip() and texts["de"].strip(), code
        assert placeholders(texts["en"]) == placeholders(texts["de"]), code


def test_unknown_message_code_is_an_error():
    with pytest.raises(KeyError):
        message("no_such_code", "en")


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("de", "Benutzername oder Passwort falsch"),
        ("en", "Wrong username or password"),
        (None, "Wrong username or password"),
    ],
)
def test_login_error_follows_the_header(anon_client, header, expected):
    headers = {"Accept-Language": header} if header else {}
    response = anon_client.post(
        "/api/auth/login", json={"username": "admin", "password": "falsch"}, headers=headers
    )
    assert response.status_code == 401
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("de", "Nicht angemeldet oder Sitzung abgelaufen."),
        ("en", "Not signed in or the session has expired."),
        (None, "Not signed in or the session has expired."),
    ],
)
def test_missing_login_follows_the_header(anon_client, header, expected):
    headers = {"Accept-Language": header} if header else {}
    response = anon_client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("header", "expected"),
    [("de", "Demo-Zugang ist deaktiviert."), ("en", "Demo access is switched off.")],
)
def test_disabled_demo_follows_the_header(archive_dir, header, expected):
    from fastapi.testclient import TestClient

    from app.config import get_settings
    from app.main import app
    from tests.conftest import make_settings

    settings = make_settings(archive_dir, demo_mode=False)
    app.dependency_overrides[get_settings] = lambda: settings
    try:
        response = TestClient(app).post(
            "/api/auth/demo", json={"role": "admin"}, headers={"Accept-Language": header}
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 404
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("header", "expected"),
    [("de", "Keine Berechtigung für diese Aktion."), ("en", "You are not allowed to do this.")],
)
def test_forbidden_follows_the_header(patient_client, header, expected):
    response = patient_client.get("/api/audit", headers={"Accept-Language": header})
    assert response.status_code == 403
    assert response.json()["detail"] == expected
