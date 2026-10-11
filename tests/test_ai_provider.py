import asyncio
import json

import httpx
import pytest

from app.ai.provider import AIUnavailable, OpenAIProvider, get_provider
from app.config import Settings

MESSAGES = [{"role": "user", "content": "Explain migraine"}]
URL = "https://example.test/v1/chat/completions"


def settings(**extra):
    return Settings(
        _env_file=None, ai_api_key="test", ai_base_url="https://example.test/v1", **extra
    )


def test_complete_uses_configured_model_and_messages(network):
    route = network.post(URL).respond(
        200, json={"choices": [{"message": {"content": "Antwort"}, "finish_reason": "stop"}]}
    )
    assert OpenAIProvider(settings()).complete(MESSAGES) == "Antwort"
    body = json.loads(route.calls.last.request.content)
    assert body["messages"] == MESSAGES
    assert body["model"] == "gemini-3.5-flash-lite"
    assert body["max_tokens"] == 4096


def test_no_key_is_not_configured():
    with pytest.raises(AIUnavailable, match="ai_not_configured"):
        get_provider(Settings(_env_file=None))


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"choices": []},
        {"choices": [{"message": {"content": ""}}]},
        {"choices": [{"message": {"content": "x" * 20001}}]},
        {"choices": [{"message": {"content": "partial"}, "finish_reason": "length"}]},
    ],
)
def test_malformed_complete_is_unavailable(network, payload):
    network.post(URL).respond(200, json=payload)
    with pytest.raises(AIUnavailable):
        OpenAIProvider(settings()).complete(MESSAGES)


@pytest.mark.parametrize("status", [429, 500])
def test_http_failure_does_not_expose_secrets(network, status):
    network.post(URL).respond(status, text="secret-provider-error")
    with pytest.raises(AIUnavailable) as error:
        OpenAIProvider(settings()).complete(MESSAGES)
    assert "secret-provider-error" not in str(error.value)


def test_timeout_is_unavailable(network):
    network.post(URL).mock(side_effect=httpx.ReadTimeout("timeout"))
    with pytest.raises(AIUnavailable):
        OpenAIProvider(settings()).complete(MESSAGES)


def collect(provider):
    async def run():
        return [chunk async for chunk in provider.stream(MESSAGES)]

    return asyncio.run(run())


def test_stream_reads_deltas_and_terminal_event(network):
    text = 'data: {"choices":[{"delta":{"content":"Übel"},"finish_reason":null}]}\n\ndata: {"choices":[{"delta":{"content":"keit"},"finish_reason":"stop"}]}\n\ndata: [DONE]\n\n'
    network.post(URL).respond(200, text=text)
    assert collect(OpenAIProvider(settings())) == ["Übel", "keit"]


@pytest.mark.parametrize(
    "text",
    [
        "data: nope\n\n",
        'data: {"choices":[{"delta":{"content":"partial"}}]}\n\n',
        'data: {"choices":[{"delta":{},"finish_reason":"length"}]}\n\ndata: [DONE]\n\n',
    ],
)
def test_bad_or_interrupted_stream_is_unavailable(network, text):
    network.post(URL).respond(200, text=text)
    with pytest.raises(AIUnavailable):
        collect(OpenAIProvider(settings()))
