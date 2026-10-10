"""WHO ICD-11 lookup via OAuth2 client credentials (spec §6)."""

import httpx
import pytest

from tests.conftest import make_doc

TOKEN = "https://icdaccessmanagement.who.int/connect/token"
CODEINFO = "https://id.who.int/icd/release/11/2026-01/mms/codeinfo/{code}"
ENTITY = "https://id.who.int/icd/release/11/2026-01/mms/1260284546"

ENTITY_JSON = {
    "code": "8A80",
    "title": {"@language": "de", "@value": "Migräne"},
    "definition": {
        "@language": "de",
        "@value": "Migräne ist eine wiederkehrende Kopfschmerzerkrankung.",
    },
}


@pytest.fixture
def keys(test_settings):
    test_settings.icd_client_id = "client-id"
    test_settings.icd_client_secret = "client-secret"
    return test_settings


@pytest.fixture
def who(network):
    token = network.post(TOKEN).mock(
        return_value=httpx.Response(
            200, json={"access_token": "tok-1", "token_type": "Bearer", "expires_in": 3600}
        )
    )
    codeinfo = network.get(CODEINFO.format(code="8A80")).mock(
        return_value=httpx.Response(
            200,
            json={
                "code": "8A80",
                "stemId": "http://id.who.int/icd/release/11/2026-01/mms/1260284546",
            },
        )
    )
    entity = network.get(ENTITY).mock(return_value=httpx.Response(200, json=ENTITY_JSON))
    return token, codeinfo, entity


def icd_doc(client, code="8A80"):
    return make_doc(client, title="Migräne", icd11_code=code)


def test_not_configured_without_keys(doctor_client, client, who):
    doc = icd_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()
    assert body == {"status": "not_configured", "fetched_at": None, "data": None}
    assert not who[0].called


def test_document_without_code_is_empty(doctor_client, client, keys, who):
    doc = make_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()
    assert body["status"] == "empty"
    assert not who[0].called


def test_lookup_returns_title_definition_and_browser_link(doctor_client, client, keys, who):
    doc = icd_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()

    assert body["status"] == "ok"
    assert body["data"] == {
        "code": "8A80",
        "title": "Migräne",
        "definition": "Migräne ist eine wiederkehrende Kopfschmerzerkrankung.",
        "url": "https://icd.who.int/browse/2026-01/mms/de#1260284546",
        "release": "2026-01",
        "language": "de",
    }
    token_form = who[0].calls.last.request.content.decode()
    assert "grant_type=client_credentials" in token_form
    assert "scope=icdapi_access" in token_form
    for route in (who[1], who[2]):
        headers = route.calls.last.request.headers
        assert headers["Authorization"] == "Bearer tok-1"
        assert headers["API-Version"] == "v2"
        assert headers["Accept-Language"] == "de"
    assert who[2].calls.last.request.url.scheme == "https"  # stemId is http://


def test_english_fallback_reports_the_returned_language(doctor_client, client, keys, who):
    who[2].mock(
        return_value=httpx.Response(
            200, json={"code": "8A80", "title": {"@language": "en", "@value": "Migraine"}}
        )
    )
    doc = icd_doc(client)
    data = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()["data"]
    assert data["language"] == "en"
    assert data["url"] == "https://icd.who.int/browse/2026-01/mms/en#1260284546"


def test_token_is_reused_until_expiry(doctor_client, client, keys, who, network):
    network.get(CODEINFO.format(code="BA00")).mock(
        return_value=httpx.Response(
            200, json={"stemId": "http://id.who.int/icd/release/11/2026-01/mms/1260284546"}
        )
    )
    for code in ("8A80", "BA00"):
        doc = icd_doc(client, code)
        assert (
            doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()["status"] == "ok"
        )
    assert who[0].call_count == 1


def test_wrong_credentials_are_unavailable(doctor_client, client, keys, who):
    who[0].mock(return_value=httpx.Response(401, json={"error": "invalid_client"}))
    doc = icd_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()
    assert body["status"] == "unavailable"


def test_unknown_code_is_empty(doctor_client, client, keys, who, network):
    network.get(CODEINFO.format(code="ZZ99")).mock(return_value=httpx.Response(404))
    doc = icd_doc(client, "ZZ99")
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()
    assert body["status"] == "empty"


def test_entity_without_definition_is_ok_with_null_definition(doctor_client, client, keys, who):
    who[2].mock(
        return_value=httpx.Response(
            200, json={"code": "8A80", "title": {"@language": "de", "@value": "Migräne"}}
        )
    )
    doc = icd_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()
    assert body["status"] == "ok"
    assert body["data"]["definition"] is None


def test_entity_without_title_is_unavailable(doctor_client, client, keys, who):
    who[2].mock(return_value=httpx.Response(200, json={"code": "8A80"}))
    doc = icd_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/icd11").json()
    assert body["status"] == "unavailable"
