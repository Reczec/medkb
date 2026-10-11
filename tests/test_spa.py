import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.spa import install_security_headers, mount_frontend


@pytest.fixture
def dist(tmp_path):
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text('<!doctype html><div id="root"></div>', encoding="utf-8")
    (dist / "assets" / "app.js").write_text("console.log('medkb')", encoding="utf-8")
    (dist / "favicon.svg").write_text("<svg/>", encoding="utf-8")
    return dist


@pytest.fixture
def spa_client(dist):
    app = FastAPI()

    @app.get("/api/ping")
    def ping():
        return {"pong": True}

    install_security_headers(app)
    mount_frontend(app, dist)
    return TestClient(app)


def test_root_serves_index(spa_client):
    assert '<div id="root">' in spa_client.get("/").text


def test_deep_link_serves_index(spa_client):
    response = spa_client.get("/wissen/12")
    assert response.status_code == 200
    assert '<div id="root">' in response.text


def test_asset_is_served(spa_client):
    response = spa_client.get("/assets/app.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]


def test_top_level_static_file_is_served(spa_client):
    assert spa_client.get("/favicon.svg").text == "<svg/>"


def test_api_routes_still_work(spa_client):
    assert spa_client.get("/api/ping").json() == {"pong": True}


def test_unknown_api_path_is_json_404(spa_client):
    response = spa_client.get("/api/does-not-exist")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_missing_asset_is_404_not_index(spa_client):
    assert spa_client.get("/assets/missing.js").status_code == 404


def test_path_traversal_does_not_leak_files(spa_client, tmp_path):
    (tmp_path / "secret.txt").write_text("TOP-SECRET", encoding="utf-8")
    for path in ("/..%2Fsecret.txt", "/%2E%2E/secret.txt", "/assets/..%2F..%2Fsecret.txt"):
        assert "TOP-SECRET" not in spa_client.get(path).text


def test_missing_dist_shows_hint(tmp_path):
    app = FastAPI()
    mount_frontend(app, tmp_path / "nope")
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert "Frontend nicht gebaut" in response.text


def test_hashed_assets_are_cached_for_a_year(spa_client):
    response = spa_client.get("/assets/app.js")
    assert response.headers["cache-control"] == "public, max-age=31536000, immutable"


def test_the_shell_is_never_cached(spa_client):
    for path in ("/", "/wissen/12"):
        assert spa_client.get(path).headers["cache-control"] == "no-cache"


def test_missing_asset_is_404_not_the_shell(spa_client):
    # An old tab asking for a replaced bundle must not get HTML instead of JavaScript.
    response = spa_client.get("/assets/app-old123.js")
    assert response.status_code == 404
    assert "root" not in response.text


def test_head_on_the_shell(spa_client):
    assert spa_client.head("/").status_code == 200


@pytest.mark.parametrize("path", ["/", "/assets/app.js", "/api/ping"])
def test_security_headers_on_every_response(spa_client, path):
    headers = spa_client.get(path).headers
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert headers["x-frame-options"] == "DENY"


def test_the_real_app_sends_security_headers(client):
    assert client.get("/api/health").headers["x-content-type-options"] == "nosniff"


def test_explicit_index_html_is_never_cached(spa_client):
    assert spa_client.get("/index.html").headers["cache-control"] == "no-cache"
