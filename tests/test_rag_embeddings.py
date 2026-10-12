import math

import httpx
import pytest

from app.ai.provider import AIUnavailable


@pytest.mark.parametrize(
    "values",
    [[0.0] * 768, [True] * 768, [math.nan] * 768, [math.inf] * 768, [1.0] * 767, ["1"] * 768],
)
def test_invalid_vectors_rejected(values):
    from app.rag.embeddings import normalize

    with pytest.raises(AIUnavailable, match="embedding_unavailable"):
        normalize(values)


def test_vector_normalization():
    from app.rag.embeddings import normalize

    vector = normalize([3.0, 4.0] + [0.0] * 766)
    assert vector[:2] == [0.6, 0.8]


@pytest.mark.parametrize(
    "task,expected", [("document", "RETRIEVAL_DOCUMENT"), ("query", "RETRIEVAL_QUERY")]
)
def test_native_embedding_batch_contract(network, test_settings, task, expected):
    from app.rag.embeddings import URL, GeminiEmbeddings

    test_settings.embedding_api_key = "synthetic-secret"
    route = network.post(URL).mock(
        return_value=httpx.Response(200, json={"embeddings": [{"values": [3, 4] + [0] * 766}]})
    )
    assert GeminiEmbeddings(test_settings).embed(["safe example"], task)[0][:2] == [0.6, 0.8]
    import json

    payload = json.loads(route.calls[0].request.content)
    request = payload["requests"][0]
    assert request["config"] == {"taskType": expected, "outputDimensionality": 768}
    assert request["content"]["parts"][0]["text"] == "safe example"
    assert route.call_count == 1


@pytest.mark.parametrize(
    "status,payload", [(429, {"error": "secret"}), (200, {}), (200, {"embeddings": []})]
)
def test_provider_errors_are_bounded_and_private(network, test_settings, status, payload):
    from app.rag.embeddings import URL, GeminiEmbeddings

    test_settings.embedding_api_key = "synthetic-secret"
    network.post(URL).mock(return_value=httpx.Response(status, json=payload))
    with pytest.raises(AIUnavailable) as error:
        GeminiEmbeddings(test_settings).embed(["example"], "query")
    assert str(error.value) == "embedding_unavailable"


def test_missing_key_and_batch_bound_do_not_call_provider(test_settings, network):
    from app.rag.embeddings import GeminiEmbeddings

    test_settings.ai_api_key = ""
    with pytest.raises(AIUnavailable):
        GeminiEmbeddings(test_settings).embed(["example"], "query")
    test_settings.embedding_api_key = "synthetic-secret"
    with pytest.raises(ValueError):
        GeminiEmbeddings(test_settings).embed(["x"] * 17, "document")
    assert not network.calls
