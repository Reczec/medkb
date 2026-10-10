"""The permission matrix from the spec, checked endpoint by endpoint for every role."""

import pytest

from tests.conftest import make_doc

ALL = {"admin", "doctor", "patient"}
STAFF = {"admin", "doctor"}
ADMIN_ONLY = {"admin"}

ARCHIVE = "archive_20260101_000000.json"

# (method, path, json body, roles that may call it)
ENDPOINTS = [
    ("get", "/api/documents", None, ALL),
    ("get", "/api/documents/{id}", None, ALL),
    ("get", "/api/meta", None, ALL),
    ("get", "/api/stats", None, ALL),
    ("post", "/api/classify", {"title": "Herz", "content": "Herzrasen"}, STAFF),
    (
        "post",
        "/api/documents",
        {"title": "Neu", "content": "Ein neuer Eintrag.", "doc_type": "Symptom"},
        ADMIN_ONLY,
    ),
    ("patch", "/api/documents/{id}", {"title": "Geändert"}, ADMIN_ONLY),
    ("delete", "/api/documents/{id}", None, ADMIN_ONLY),
    ("get", "/api/archives", None, ADMIN_ONLY),
    ("post", "/api/archives", None, ADMIN_ONLY),
    ("get", f"/api/archives/{ARCHIVE}", None, ADMIN_ONLY),
    ("post", f"/api/archives/{ARCHIVE}/restore", None, ADMIN_ONLY),
    ("get", "/api/audit", None, ADMIN_ONLY),
    ("get", "/api/users", None, ADMIN_ONLY),
    ("get", "/api/sources/documents/{id}/studies", None, STAFF),
    ("get", "/api/sources/latest-studies", None, STAFF),
    ("get", "/api/sources/documents/{id}/icd11", None, STAFF),
    ("get", "/api/sources/documents/{id}/medications", None, STAFF),
]


@pytest.fixture
def clients(client, doctor_client, patient_client, anon_client):
    return {
        "admin": client,
        "doctor": doctor_client,
        "patient": patient_client,
        None: anon_client,
    }


@pytest.mark.parametrize("method,path,body,allowed", ENDPOINTS, ids=lambda v: str(v))
@pytest.mark.parametrize("role", ["admin", "doctor", "patient", None])
def test_permission_matrix(clients, client, method, path, body, allowed, role):
    doc_id = make_doc(client)["id"]
    url = path.format(id=doc_id)
    kwargs = {"json": body} if body is not None else {}
    status = getattr(clients[role], method)(url, **kwargs).status_code

    if role is None:
        assert status == 401
    elif role in allowed:
        assert status not in (401, 403), f"{role} should be allowed on {method} {path}"
    else:
        assert status == 403


@pytest.mark.parametrize("path", ["/api/health", "/api/auth/options"])
def test_public_endpoints(anon_client, path):
    assert anon_client.get(path).status_code == 200


def test_audit_records_who_changed_what(client):
    make_doc(client, title="Mit Akteur")
    entry = client.get("/api/audit").json()[0]
    assert entry["action"] == "create"
    assert entry["actor"] == "demo-admin"


def test_users_list_has_no_password_hashes(client):
    users = client.get("/api/users").json()
    assert {u["username"] for u in users} >= {"demo-admin", "demo-doctor", "demo-patient"}
    assert all("password_hash" not in u for u in users)
