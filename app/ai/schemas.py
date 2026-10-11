"""Bounded requests and validated structured model opinions."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.classifier import CATEGORIES
from app.schemas import Title


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=200)
    history: list[HistoryMessage] = Field(default_factory=list, max_length=6)


class DraftRequest(BaseModel):
    title: Title


class StudyRequest(BaseModel):
    pmid: str = Field(pattern=r"^[1-9]\d{0,11}$")


class Classification(BaseModel):
    category: str
    confidence: float = Field(ge=0, le=1, allow_inf_nan=False)
    reasoning: str = Field(min_length=1, max_length=2000)

    @field_validator("category")
    @classmethod
    def known_category(cls, value: str) -> str:
        if value not in CATEGORIES:
            raise ValueError("Unknown category")
        return value
