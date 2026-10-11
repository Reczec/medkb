"""Bounded OpenAI-compatible chat completions. Secrets never enter public error text."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Annotated, Protocol

import httpx
from fastapi import Depends

from app.config import Settings, get_settings

MAX_OUTPUT = 20_000


class AIUnavailable(Exception):
    """Unconfigured, failed, interrupted or unusable provider response."""


class AIProvider(Protocol):
    def complete(self, messages: list[dict[str, str]]) -> str: ...

    def stream(self, messages: list[dict[str, str]]) -> AsyncIterator[str]: ...


class OpenAIProvider:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _request(self, messages: list[dict[str, str]], stream: bool = False) -> dict:
        return {
            "model": self.settings.ai_model,
            "messages": messages,
            "max_tokens": 4096,
            "stream": stream,
        }

    @property
    def url(self) -> str:
        return self.settings.ai_base_url.rstrip("/") + "/chat/completions"

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.settings.ai_api_key}"}

    def complete(self, messages: list[dict[str, str]]) -> str:
        try:
            with httpx.Client(timeout=self.settings.ai_timeout) as client:
                response = client.post(self.url, headers=self.headers, json=self._request(messages))
                response.raise_for_status()
                choice = response.json()["choices"][0]
                text = choice["message"]["content"]
                if choice.get("finish_reason") != "stop":
                    raise ValueError("incomplete")
                if not isinstance(text, str) or not text.strip() or len(text) > MAX_OUTPUT:
                    raise ValueError("unusable text")
                return text.strip()
        except (
            httpx.HTTPError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
            AttributeError,
        ) as exc:
            raise AIUnavailable("ai_unavailable") from exc

    async def stream(self, messages: list[dict[str, str]]) -> AsyncIterator[str]:
        size = 0
        finished = False
        try:
            async with httpx.AsyncClient(timeout=self.settings.ai_timeout) as client:
                async with client.stream(
                    "POST", self.url, headers=self.headers, json=self._request(messages, True)
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            if not finished or not size:
                                raise ValueError("incomplete stream")
                            return
                        payload = json.loads(data)
                        if payload.get("error"):
                            raise ValueError("provider error")
                        choices = payload["choices"]
                        if not choices:  # final usage-only event
                            continue
                        choice = choices[0]
                        reason = choice.get("finish_reason")
                        if reason and reason != "stop":
                            raise ValueError("incomplete stream")
                        finished = finished or reason == "stop"
                        text = choice["delta"].get("content")
                        if text is not None:
                            if not isinstance(text, str):
                                raise ValueError("invalid delta")
                            size += len(text)
                            if size > MAX_OUTPUT:
                                raise ValueError("oversized stream")
                            if text:
                                yield text
                    raise ValueError("missing terminal event")
        except (
            httpx.HTTPError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
            AttributeError,
        ) as exc:
            raise AIUnavailable("ai_unavailable") from exc


def get_provider(settings: Annotated[Settings, Depends(get_settings)]) -> AIProvider:
    if not settings.ai_api_key.strip():
        raise AIUnavailable("ai_not_configured")
    return OpenAIProvider(settings)
