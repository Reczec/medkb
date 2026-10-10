"""PubMed studies via NCBI E-utilities, with the 24 h source cache (spec §6)."""

from datetime import timedelta

import httpx
import pytest
from sqlalchemy import func, select

from app.models import SourceCache, utcnow
from app.sources.cache import SourceUnavailable, cached, store
from tests.conftest import make_doc

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

SEARCH = {"esearchresult": {"count": "2", "idlist": ["41000002", "41000001"]}}
SUMMARY = {
    "result": {
        "uids": ["41000002", "41000001"],
        "41000002": {
            "uid": "41000002",
            "title": "Triptans in <i>acute</i> migraine: a review.",
            "fulljournalname": "The Journal of Headache and Pain",
            "source": "J Headache Pain",
            "pubdate": "2026 Sep 3",
            "authors": [
                {"name": "Müller A", "authtype": "Author"},
                {"name": "Smith B", "authtype": "Author"},
                {"name": "Rossi C", "authtype": "Author"},
                {"name": "Kim D", "authtype": "Author"},
            ],
        },
        "41000001": {
            "uid": "41000001",
            "title": "Migraine prevention trial",
            "source": "Cephalalgia",
            "pubdate": "2026",
            "authors": [{"name": "Lee E", "authtype": "Author"}],
        },
    }
}


@pytest.fixture
def pubmed(network):
    search = network.get(ESEARCH).mock(return_value=httpx.Response(200, json=SEARCH))
    summary = network.get(ESUMMARY).mock(return_value=httpx.Response(200, json=SUMMARY))
    return search, summary


def migraine_doc(client, **fields):
    return make_doc(client, title="Migräne", term_en="Migraine", **fields)


def test_studies_are_parsed_newest_first(doctor_client, client, pubmed):
    doc = migraine_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()

    assert body["status"] == "ok"
    assert body["fetched_at"]
    first, second = body["data"]
    assert first["pmid"] == "41000002"
    assert first["title"] == "Triptans in acute migraine: a review."
    assert first["journal"] == "The Journal of Headache and Pain"
    assert first["year"] == 2026
    assert first["authors"] == ["Müller A", "Smith B", "Rossi C"]
    assert first["more_authors"] is True
    assert first["url"] == "https://pubmed.ncbi.nlm.nih.gov/41000002/"
    assert second["journal"] == "Cephalalgia"  # falls back to the short source name
    assert second["more_authors"] is False

    search_params = pubmed[0].calls.last.request.url.params
    assert search_params["term"] == '"Migraine" AND hasabstract'
    assert "sort" not in search_params  # PubMed default: most recently added first
    assert search_params["retmax"] == "5"
    assert search_params["tool"] == "medkb"
    assert "api_key" not in search_params


def test_document_without_term_is_empty_without_network(doctor_client, client, pubmed):
    doc = make_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
    assert body == {"status": "empty", "fetched_at": None, "data": None}
    assert not pubmed[0].called


def test_no_hits_is_empty_and_cached(doctor_client, client, network):
    search = network.get(ESEARCH).mock(
        return_value=httpx.Response(200, json={"esearchresult": {"idlist": []}})
    )
    doc = migraine_doc(client)
    for _ in range(2):
        body = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
        assert body["status"] == "empty"
    assert search.call_count == 1


def test_second_call_is_served_from_cache(doctor_client, client, pubmed):
    doc = migraine_doc(client)
    first = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
    second = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
    assert second == first
    assert pubmed[0].call_count == 1


def test_stale_cache_is_refetched(doctor_client, client, pubmed, db_session):
    doc = migraine_doc(client)
    doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    for row in db_session.scalars(select(SourceCache)):
        row.fetched_at = utcnow() - timedelta(hours=25)
    db_session.commit()

    doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    assert pubmed[0].call_count == 2


def test_changed_term_uses_a_new_cache_entry(doctor_client, client, pubmed):
    doc = migraine_doc(client)
    doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    client.patch(f"/api/documents/{doc['id']}", json={"term_en": "Cluster headache"})
    doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    assert pubmed[0].call_count == 2
    assert pubmed[0].calls.last.request.url.params["term"] == '"Cluster headache" AND hasabstract'


@pytest.mark.parametrize(
    "response",
    [
        httpx.TimeoutException("slow"),
        httpx.Response(500),
        httpx.Response(200, text="<html>maintenance</html>"),
        httpx.Response(200, json={"error": "API rate limit exceeded"}),
    ],
    ids=["timeout", "http-500", "not-json", "missing-esearchresult"],
)
def test_upstream_failure_is_unavailable_and_not_cached(
    doctor_client, client, network, db_session, response
):
    route = network.get(ESEARCH)
    if isinstance(response, Exception):
        route.mock(side_effect=response)
    else:
        route.mock(return_value=response)
    doc = migraine_doc(client)

    result = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    assert result.status_code == 200
    assert result.json() == {"status": "unavailable", "fetched_at": None, "data": None}
    assert db_session.scalar(select(func.count()).select_from(SourceCache)) == 0


def test_summary_entry_with_missing_fields_still_parses(doctor_client, client, network):
    network.get(ESEARCH).mock(
        return_value=httpx.Response(200, json={"esearchresult": {"idlist": ["1"]}})
    )
    network.get(ESUMMARY).mock(
        return_value=httpx.Response(200, json={"result": {"1": {"uid": "1", "title": "Nur Titel"}}})
    )
    doc = migraine_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
    assert body["status"] == "ok"
    assert body["data"][0] == {
        "pmid": "1",
        "title": "Nur Titel",
        "journal": None,
        "year": None,
        "authors": [],
        "more_authors": False,
        "url": "https://pubmed.ncbi.nlm.nih.gov/1/",
    }


def test_api_key_is_sent_when_configured(doctor_client, client, pubmed, test_settings):
    test_settings.ncbi_api_key = "ncbi-test-key"
    doc = migraine_doc(client)
    doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    assert pubmed[0].calls.last.request.url.params["api_key"] == "ncbi-test-key"
    assert pubmed[1].calls.last.request.url.params["api_key"] == "ncbi-test-key"


def test_latest_studies_uses_the_two_largest_specialties(doctor_client, client, pubmed):
    for _ in range(3):
        make_doc(client, title="Herz", content="Herzinfarkt und Vorhofflimmern im EKG.")
    for _ in range(2):
        make_doc(client, title="Ohr", content="Tinnitus und Trommelfell, Otitis media.")
    make_doc(client, title="Haut", content="Neurodermitis mit Juckreiz und Ekzem.")

    body = doctor_client.get("/api/sources/latest-studies").json()
    assert body["status"] == "ok"
    assert [group["category"] for group in body["data"]] == ["Kardiologie", "HNO"]
    terms = [call.request.url.params["term"] for call in pubmed[0].calls]
    assert terms == [
        '"Cardiovascular Diseases"[MeSH Major Topic] AND hasabstract',
        '"Otorhinolaryngologic Diseases"[MeSH Major Topic] AND hasabstract',
    ]
    assert all(call.request.url.params["retmax"] == "3" for call in pubmed[0].calls)


def test_latest_studies_unavailable_when_one_part_fails(doctor_client, client, network):
    network.get(ESEARCH).mock(side_effect=httpx.ConnectError("down"))
    make_doc(client, title="Herz", content="Herzinfarkt und Vorhofflimmern im EKG.")
    body = doctor_client.get("/api/sources/latest-studies").json()
    assert body["status"] == "unavailable"


def test_latest_studies_without_documents_is_empty(doctor_client, pubmed):
    assert doctor_client.get("/api/sources/latest-studies").json()["status"] == "empty"
    assert not pubmed[0].called


def test_cache_survives_demo_reset(doctor_client, client, pubmed, db_session):
    from app.demo import reset_demo

    doc = migraine_doc(client)
    doctor_client.get(f"/api/sources/documents/{doc['id']}/studies")
    reset_demo(db_session)
    assert db_session.scalar(select(func.count()).select_from(SourceCache)) == 1


def test_concurrent_store_of_same_key_does_not_fail(db_session, test_settings):
    from app.database import SessionLocal

    with SessionLocal() as other:
        store(other, "pubmed:x", ["erste Antwort"])
    # This session never saw the row: its insert collides and must fall back to an update.
    store(db_session, "pubmed:x", ["zweite Antwort"])
    assert db_session.get(SourceCache, "pubmed:x").payload == ["zweite Antwort"]


def test_cached_reports_unavailable_without_storing(db_session, test_settings):
    def fail():
        raise SourceUnavailable("down")

    result = cached(db_session, "pubmed:y", test_settings, fail)
    assert result.status == "unavailable"
    assert db_session.get(SourceCache, "pubmed:y") is None


class FakeClock:
    def __init__(self):
        self.now = 100.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


@pytest.mark.parametrize(("api_key", "interval"), [("", 0.4), ("key", 0.12)])
def test_requests_are_spaced_for_the_ncbi_rate_limit(monkeypatch, test_settings, api_key, interval):
    from app.sources import pubmed

    clock = FakeClock()
    monkeypatch.setattr(pubmed, "time", clock)
    monkeypatch.setattr(pubmed, "_last_request", 0.0)
    monkeypatch.setattr(pubmed, "MIN_INTERVAL", 0.4)
    monkeypatch.setattr(pubmed, "MIN_INTERVAL_WITH_KEY", 0.12)
    test_settings.ncbi_api_key = api_key

    pubmed.throttle(test_settings)  # first request: long after the last one, no wait
    pubmed.throttle(test_settings)  # immediately after: waits one interval
    assert clock.sleeps == [pytest.approx(interval)]


def test_rate_limited_request_is_retried_once(doctor_client, client, network, monkeypatch):
    from app.sources import pubmed

    monkeypatch.setattr(pubmed, "RETRY_AFTER_429", 0.0)
    network.get(ESEARCH).mock(side_effect=[httpx.Response(429), httpx.Response(200, json=SEARCH)])
    network.get(ESUMMARY).mock(return_value=httpx.Response(200, json=SUMMARY))
    doc = migraine_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
    assert body["status"] == "ok"


def test_second_429_gives_up(doctor_client, client, network, monkeypatch):
    from app.sources import pubmed

    monkeypatch.setattr(pubmed, "RETRY_AFTER_429", 0.0)
    network.get(ESEARCH).mock(return_value=httpx.Response(429))
    doc = migraine_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/studies").json()
    assert body["status"] == "unavailable"
