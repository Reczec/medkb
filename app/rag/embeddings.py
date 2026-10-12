"""Native Gemini text retrieval embeddings, validated before persistence or search."""

import math
from typing import Literal, Protocol

import httpx

from app.ai.provider import AIUnavailable
from app.config import Settings
from app.rag.chunks import DIMENSIONS, MODEL

Task = Literal["document", "query"]
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:batchEmbedContents"


def normalize(values: list, dimensions: int = DIMENSIONS) -> list[float]:
    try:
        if not isinstance(values, list) or len(values) != dimensions:
            raise ValueError("dimensions")
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
            raise ValueError("numbers")
        norm = math.hypot(*values)
        if not math.isfinite(norm) or norm == 0:
            raise ValueError("norm")
        return [v / norm for v in values]
    except (ValueError, TypeError, OverflowError) as exc:
        raise AIUnavailable("embedding_unavailable") from exc


class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str], task: Task) -> list[list[float]]: ...


class GeminiEmbeddings:
    def __init__(self, settings: Settings):
        self.settings = settings

    def embed(self, texts: list[str], task: Task) -> list[list[float]]:
        if not 1 <= len(texts) <= 16 or task not in ("document", "query"):
            raise ValueError("Invalid embedding batch")
        if any(not text.strip() or len(text) > 1100 for text in texts):
            raise ValueError("Invalid embedding input")
        key = self.settings.embedding_api_key.strip()
        if not key and self.settings.ai_base_url.startswith(
            "https://generativelanguage.googleapis.com/"
        ):
            key = self.settings.ai_api_key.strip()
        if not key:
            raise AIUnavailable("embedding_not_configured")
        config = {
            "taskType": "RETRIEVAL_DOCUMENT" if task == "document" else "RETRIEVAL_QUERY",
            "outputDimensionality": DIMENSIONS,
        }
        try:
            with httpx.Client(timeout=self.settings.embedding_timeout) as client:
                response = client.post(
                    URL,
                    headers={"x-goog-api-key": key},
                    json={
                        "requests": [
                            {
                                "model": f"models/{MODEL}",
                                "content": {"parts": [{"text": text}]},
                                "config": config,
                            }
                            for text in texts
                        ]
                    },
                )
                response.raise_for_status()
                data = response.json()["embeddings"]
                if not isinstance(data, list) or len(data) != len(texts):
                    raise ValueError("count")
                return [normalize(row["values"]) for row in data]
        except (httpx.HTTPError, ValueError, KeyError, TypeError, AttributeError) as exc:
            raise AIUnavailable("embedding_unavailable") from exc


def get_embeddings(settings: Settings) -> EmbeddingProvider:
    return GeminiEmbeddings(settings)
