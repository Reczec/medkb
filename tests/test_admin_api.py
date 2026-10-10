import json

import pytest

from tests.conftest import make_doc

ADMIN_ENDPOINTS = [
    ("post", "/api/archives"),
    ("get", "/api/archives"),
    ("get", "/api/archives/archive_20260101_000000.json"),
    ("post", "/api/archives/archive_20260101_000000.json/restore"),
    ("get", "/api/audit"),
]


@pytest.mark.parametrize(("method", "url"), ADMIN_ENDPOINTS)
def test_admin_endpoints_need_the_admin_role(anon_client, doctor_client, method, url):
    assert getattr(anon_client, method)(url).status_code == 401
    assert getattr(doctor_client, method)(url).status_code == 403


def test_create_list_and_download_archive(client, archive_dir):
    make_doc(client, title="Eins", keywords=["Übung"])
    make_doc(client, title="Zwei", category="Kardiologie")

    created = client.post("/api/archives")
    assert created.status_code == 201
    info = created.json()
    assert info["document_count"] == 2
    assert info["name"].startswith("archive_") and info["name"].endswith(".json")
    assert (archive_dir / info["name"]).is_file()

    listing = client.get("/api/archives").json()
    assert [a["name"] for a in listing] == [info["name"]]

    download = client.get(f"/api/archives/{info['name']}")
    assert download.status_code == 200
    payload = json.loads(download.content)
    assert payload["document_count"] == 2
    assert {d["title"] for d in payload["documents"]} == {"Eins", "Zwei"}
    assert "Übung" in json.dumps(payload, ensure_ascii=False)  # umlauts stay readable
    assert all("id" not in d for d in payload["documents"])


def test_two_archives_in_the_same_second_do_not_collide(client):
    make_doc(client)
    names = {client.post("/api/archives").json()["name"] for _ in range(3)}
    assert len(names) == 3
    assert len(client.get("/api/archives").json()) == 3


def test_restore_replaces_documents_and_creates_backup(client):
    make_doc(client, title="Original", keywords=["Alt"], category="HNO")
    archive = client.post("/api/archives").json()

    client.delete("/api/documents/1")
    make_doc(client, title="Neuer Eintrag nach dem Archiv")
    make_doc(client, title="Noch einer")

    result = client.post(f"/api/archives/{archive['name']}/restore")
    assert result.status_code == 200
    body = result.json()
    assert body["restored"] == 1
    assert body["backup"]["name"].endswith("_pre-restore.json")
    assert body["backup"]["document_count"] == 2  # state right before the restore

    items = client.get("/api/documents").json()["items"]
    assert [d["title"] for d in items] == ["Original"]
    assert items[0]["keywords"] == ["Alt"] and items[0]["category"] == "HNO"

    # The backup can itself be restored (undo).
    undo = client.post(f"/api/archives/{body['backup']['name']}/restore")
    assert undo.json()["restored"] == 2
    assert {d["title"] for d in client.get("/api/documents").json()["items"]} == {
        "Neuer Eintrag nach dem Archiv",
        "Noch einer",
    }


def test_new_documents_can_be_created_after_restore(client):
    make_doc(client)
    archive = client.post("/api/archives").json()
    client.post(f"/api/archives/{archive['name']}/restore")
    make_doc(client, title="Nach dem Restore")
    assert client.get("/api/documents").json()["total"] == 2


@pytest.mark.parametrize(
    "name", ["evil.json", "archive_1.json", "archive_20260101_000000.txt", "..%2Fsecret.json"]
)
def test_invalid_archive_names_are_rejected(client, name):
    # 405 can occur when an encoded slash makes the path fall through to the frontend catch-all.
    assert client.get(f"/api/archives/{name}").status_code in (400, 404)
    assert client.post(f"/api/archives/{name}/restore").status_code in (
        400,
        404,
        405,
    )


def test_unknown_archive_is_404(client):
    assert client.get("/api/archives/archive_20260101_000000.json").status_code == 404


def test_path_traversal_cannot_read_other_files(client, archive_dir, tmp_path):
    (tmp_path / "secret.json").write_text('{"secret": true}')
    archive_dir.mkdir()
    response = client.get("/api/archives/..%2Fsecret.json")
    assert response.status_code in (400, 404)
    assert b"secret" not in response.content


@pytest.mark.parametrize(
    "content",
    [
        "this is not json",
        '{"format_version": 99, "documents": []}',
        '{"format_version": 1, "documents": "nope"}',
        '{"format_version": 1, "documents": [{"title": "x"}]}',
    ],
)
def test_corrupt_archive_is_rejected_and_database_is_untouched(client, archive_dir, content):
    make_doc(client, title="Muss erhalten bleiben")
    archive_dir.mkdir()
    (archive_dir / "archive_20260101_000000.json").write_text(content, encoding="utf-8")

    response = client.post("/api/archives/archive_20260101_000000.json/restore")
    assert response.status_code == 400
    assert [d["title"] for d in client.get("/api/documents").json()["items"]] == [
        "Muss erhalten bleiben"
    ]
    # no backup is created for a failed restore
    assert [a["name"] for a in client.get("/api/archives").json()] == [
        "archive_20260101_000000.json"
    ]


def test_audit_log_records_changes(client):
    doc = make_doc(client, title="Protokoll")
    client.patch(f"/api/documents/{doc['id']}", json={"title": "Protokoll neu"})
    client.delete(f"/api/documents/{doc['id']}")
    client.post("/api/archives")

    entries = client.get("/api/audit").json()
    assert [e["action"] for e in entries] == ["archive_create", "delete", "update", "create"]
    assert entries[1]["document_id"] == doc["id"]
    assert "Protokoll neu" in entries[1]["detail"]  # entries survive deletion of the document
    assert client.get("/api/audit", params={"limit": 2}).json().__len__() == 2
