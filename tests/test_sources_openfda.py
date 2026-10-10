"""openFDA drug labels per active ingredient (spec §6)."""

import httpx
import pytest

from app.sources.openfda import truncate
from tests.conftest import make_doc

LABEL = "https://api.fda.gov/drug/label.json"


def label(**fields):
    return {
        "results": [
            {
                "openfda": {
                    "brand_name": ["Glucophage", "Glucophage"],
                    "generic_name": ["METFORMIN"],
                },
                "indications_and_usage": ["Metformin is indicated as an adjunct to diet."],
                "warnings": ["General warning text."],
                "adverse_reactions": ["Diarrhea, nausea, vomiting."],
                **fields,
            }
        ]
    }


@pytest.fixture
def fda(network):
    return network.get(LABEL).mock(return_value=httpx.Response(200, json=label()))


def med_doc(client, medications=("metformin",)):
    return make_doc(client, title="Diabetes", medications=list(medications))


def test_label_fields_are_extracted(doctor_client, client, fda):
    doc = med_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()

    assert body["status"] == "ok"
    assert body["data"]["missing"] == []
    (found,) = body["data"]["found"]
    assert found == {
        "ingredient": "metformin",
        "brand_names": ["Glucophage"],
        "indications": "Metformin is indicated as an adjunct to diet.",
        "warnings": "General warning text.",
        "adverse_reactions": "Diarrhea, nausea, vomiting.",
        "url": "https://open.fda.gov/apis/drug/label/",
    }
    params = fda.calls.last.request.url.params
    assert params["search"] == 'openfda.generic_name:"metformin"'
    assert params["limit"] == "10"


def test_boxed_warning_is_preferred(doctor_client, client, fda):
    fda.mock(
        return_value=httpx.Response(
            200,
            json=label(
                boxed_warning=["WARNING: LACTIC ACIDOSIS"],
                warnings_and_cautions=["Second choice."],
            ),
        )
    )
    doc = med_doc(client)
    found = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()["data"]
    assert found["found"][0]["warnings"] == "WARNING: LACTIC ACIDOSIS"


def test_warnings_and_cautions_before_plain_warnings(doctor_client, client, fda):
    fda.mock(return_value=httpx.Response(200, json=label(warnings_and_cautions=["W&C text."])))
    doc = med_doc(client)
    found = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()["data"]
    assert found["found"][0]["warnings"] == "W&C text."


def test_long_texts_are_truncated_at_a_word_boundary():
    text = "wort " * 200
    short = truncate(text)
    assert len(short) <= 601
    assert short.endswith("…")
    assert not short[:-1].endswith(" ")
    assert truncate("  kurz  ") == "kurz"
    assert truncate(None) is None


def test_unknown_ingredient_goes_to_missing(doctor_client, client, fda):
    def answer(request):
        if "unknownium" in request.url.params["search"]:
            return httpx.Response(404, json={"error": {"code": "NOT_FOUND"}})
        return httpx.Response(200, json=label())

    fda.mock(side_effect=answer)
    doc = med_doc(client, ["unknownium", "metformin"])
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()
    assert body["status"] == "ok"
    assert body["data"]["missing"] == ["unknownium"]
    assert [m["ingredient"] for m in body["data"]["found"]] == ["metformin"]


def test_each_ingredient_is_cached_separately(doctor_client, client, fda):
    first = med_doc(client, ["metformin"])
    doctor_client.get(f"/api/sources/documents/{first['id']}/medications")
    second = med_doc(client, ["metformin", "insulin glargine"])
    doctor_client.get(f"/api/sources/documents/{second['id']}/medications")
    searches = [call.request.url.params["search"] for call in fda.calls]
    assert searches == [
        'openfda.generic_name:"metformin"',
        'openfda.generic_name:"insulin glargine"',
    ]


@pytest.mark.parametrize(
    "response",
    [httpx.Response(500), httpx.Response(200, json={"meta": {}}), httpx.ConnectError("down")],
    ids=["http-500", "no-results", "connect-error"],
)
def test_upstream_error_is_unavailable(doctor_client, client, fda, response):
    if isinstance(response, Exception):
        fda.mock(side_effect=response)
    else:
        fda.mock(return_value=response)
    doc = med_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()
    assert body == {"status": "unavailable", "fetched_at": None, "data": None}


def test_no_medications_is_empty_without_network(doctor_client, client, fda):
    doc = make_doc(client)
    body = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()
    assert body["status"] == "empty"
    assert not fda.called


def test_single_ingredient_prescription_label_is_preferred(doctor_client, client, fda):
    combo = {
        "openfda": {
            "brand_name": ["ZITUVIMET"],
            "generic_name": ["SITAGLIPTIN AND METFORMIN HYDROCHLORIDE"],
            "product_type": ["HUMAN PRESCRIPTION DRUG"],
        },
        "indications_and_usage": ["Combination product."],
    }
    homeopathic = {
        "openfda": {
            "brand_name": ["METFORMINUM"],
            "generic_name": ["METFORMIN"],
            "product_type": ["HUMAN OTC DRUG"],
        },
        "indications_and_usage": ["Homeopathic."],
    }
    single = {
        "openfda": {
            "brand_name": ["Glucophage"],
            "generic_name": ["METFORMIN HYDROCHLORIDE"],
            "product_type": ["HUMAN PRESCRIPTION DRUG"],
        },
        "indications_and_usage": ["Metformin alone."],
    }
    fda.mock(return_value=httpx.Response(200, json={"results": [combo, homeopathic, single]}))
    doc = med_doc(client)
    found = doctor_client.get(f"/api/sources/documents/{doc['id']}/medications").json()["data"]
    assert found["found"][0]["brand_names"] == ["Glucophage"]
    assert found["found"][0]["indications"] == "Metformin alone."
