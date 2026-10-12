import copy
import json
from pathlib import Path

import pytest


def test_frozen_dataset_is_bilingual_and_has_separate_controls():
    from app.rag.evaluate import validate_cases

    raw = json.loads(Path("evaluation/rag/questions.json").read_text(encoding="utf-8"))
    cases = validate_cases(raw)
    held = [c for c in cases if c["split"] == "test" and c["kind"] == "answerable"]
    assert len(held) == 20 and sum(c["lang"] == "en" for c in held) == 10
    assert sum(c["kind"] == "safety" for c in cases) == 2
    for bad in ("duplicate", "title", "section", "overlap"):
        invalid = copy.deepcopy(raw)
        if bad == "duplicate":
            invalid["cases"][1]["id"] = invalid["cases"][0]["id"]
        elif bad == "title":
            invalid["cases"][0]["expected"] = ["Nonexistent"]
        elif bad == "section":
            invalid["cases"][0]["section"] = "nonexistent"
        else:
            invalid["cases"][-1]["question"] = invalid["cases"][0]["question"]
        with pytest.raises(ValueError):
            validate_cases(invalid)


def test_metrics_count_failures_and_keep_control_denominators_separate():
    from app.rag.evaluate import metrics

    rows = [
        {"kind": "answerable", "expected": ["A", "B"], "retrieved": ["X", "A"], "latency": 0.1},
        {
            "kind": "answerable",
            "expected": ["A"],
            "retrieved": [],
            "error": "unavailable",
            "latency": 0.3,
        },
        {"kind": "unrelated", "expected": [], "retrieved": ["X"], "latency": 0.2},
        {"kind": "safety", "expected": [], "retrieved": ["A"], "latency": 0.4},
    ]
    result = metrics(rows)
    assert result["answerable"] == 2 and result["hit_at_1"] == 0
    assert result["hit_at_5"] == 0.5 and result["recall_at_5"] == 0.25
    assert result["mrr_at_5"] == 0.25 and result["provider_failures"] == 1
    assert result["unrelated"] == 1 and result["unrelated_acceptance"] == 1
    assert result["safety"] == 1 and result["latency_median"] == pytest.approx(0.25)
    assert result["latency_p95"] == 0.4


def test_evaluation_uses_real_retrieval_and_rejects_silent_fallback(
    client, db_session, test_settings
):
    from app.rag.evaluate import evaluate
    from app.rag.index import build_index
    from tests.conftest import make_doc
    from tests.test_rag_index import FakeEmbeddings

    make_doc(client, title="Migräne")
    provider = FakeEmbeddings()
    cases = [
        {
            "id": "fixture",
            "lang": "de",
            "kind": "answerable",
            "question": "Pochen im Kopf?",
            "expected": ["Migräne"],
            "section": "content",
            "synonym": True,
        }
    ]
    missing = evaluate(db_session, test_settings, cases, provider, pause=0)
    assert missing["hybrid"]["provider_failures"] == 1
    build_index(db_session, test_settings, provider, pause=0)
    result = evaluate(db_session, test_settings, cases, provider, pause=0)
    assert result["hybrid"]["hit_at_5"] == 1
    assert result["corpus_sha"] and result["signature"] and result["dataset_sha"]
    assert result["rows"][0]["hybrid"]["retrieved"] == ["Migräne"]
