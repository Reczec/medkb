"""Frozen-corpus operator benchmark; never called by automated tests with a live provider."""

import argparse
import asyncio
import csv
import hashlib
import json
import math
import statistics
import time
from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import select

from app.ai import retrieval as lexical
from app.ai import service
from app.ai.provider import AIUnavailable, OpenAIProvider
from app.ai.schemas import AskRequest
from app.config import get_settings
from app.database import SessionLocal
from app.models import Document
from app.rag.chunks import signature
from app.rag.embeddings import get_embeddings
from app.rag.index import corpus
from app.rag.retrieval import retrieve
from app.seed_data import SEED_DOCUMENTS


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def validate_cases(raw):
    known = {doc["title"]: doc for doc in SEED_DOCUMENTS}
    ids, questions = set(), set()
    for case in raw["cases"]:
        question = " ".join(case["question"].casefold().split())
        if case["id"] in ids or question in questions:
            raise ValueError("Duplicate case or question")
        ids.add(case["id"])
        questions.add(question)
        if case["lang"] not in ("de", "en") or case["split"] not in ("dev", "test"):
            raise ValueError("Unknown language or split")
        if case["kind"] not in ("answerable", "unrelated", "safety"):
            raise ValueError("Unknown control kind")
        AskRequest(question=case["question"], history=case.get("history", []))
        if case["kind"] == "answerable" and not case["expected"]:
            raise ValueError("Missing expected title")
        for title in case["expected"]:
            if title not in known or case["section"] not in known[title]["sections"]:
                raise ValueError("Unknown title or section")
    return raw["cases"]


def metrics(rows):
    answerable = [r for r in rows if r["kind"] == "answerable"]
    unrelated = [r for r in rows if r["kind"] == "unrelated"]
    ranks, recall = [], []
    for row in answerable:
        expected = set(row["expected"])
        found = row["retrieved"][:5]
        ranks.append(next((i for i, title in enumerate(found, 1) if title in expected), 0))
        recall.append(len(expected.intersection(found)) / len(expected))
    latency = sorted(r["latency"] for r in rows)
    denominator = len(answerable) or 1
    return {
        "answerable": len(answerable),
        "hit_at_1": sum(r == 1 for r in ranks) / denominator,
        "hit_at_5": sum(r > 0 for r in ranks) / denominator,
        "recall_at_5": sum(recall) / denominator,
        "mrr_at_5": sum(1 / r for r in ranks if r) / denominator,
        "provider_failures": sum(bool(r.get("error")) for r in rows),
        "unrelated": len(unrelated),
        "unrelated_acceptance": sum(bool(r["retrieved"]) for r in unrelated),
        "safety": sum(r["kind"] == "safety" for r in rows),
        "latency_median": statistics.median(latency) if latency else 0,
        "latency_p95": latency[math.ceil(len(latency) * 0.95) - 1] if latency else 0,
    }


def evaluate(db, settings, cases, provider, pause=4):
    settings = settings.model_copy(
        update={"rag_enabled": True, "ai_client_daily_limit": settings.ai_daily_limit}
    )
    titles = {doc.id: doc.title for doc in db.scalars(select(Document))}
    snapshot = sorted(chunk.key for chunk in corpus(db, settings))
    rows = []
    halted = False
    for case in cases:
        body = AskRequest(question=case["question"], history=case.get("history", []))
        start = time.perf_counter()
        baseline = [doc.title for doc in lexical.find(db, body)]
        base = {"retrieved": baseline, "latency": time.perf_counter() - start}
        start = time.perf_counter()
        hybrid = {"retrieved": []}
        if halted:
            hybrid["error"] = "quota_exhausted"
        else:
            try:
                found = retrieve(db, body, case["lang"], settings, provider, "rag-evaluation")
                if found.mode != "hybrid":
                    hybrid["error"] = found.reason or "lexical_fallback"
                else:
                    hybrid["retrieved"] = list(
                        dict.fromkeys(titles[c["id"]] for c in found.citations)
                    )
                    hybrid["citations"] = found.citations
            except HTTPException as error:
                hybrid["error"] = f"http_{error.status_code}"
                halted = error.status_code == 429
        hybrid["latency"] = time.perf_counter() - start
        rows.append({**case, "lexical": base, "hybrid": hybrid})
        if pause and not halted:
            time.sleep(pause)
    report = {
        "created_at": datetime.now(UTC).isoformat(),
        "corpus_sha": digest(snapshot),
        "dataset_sha": digest(cases),
        "signature": signature(settings),
        "threshold": settings.rag_min_similarity,
        "documents": len(titles),
        "chunks": len(snapshot),
        "rows": rows,
    }
    for method in ("lexical", "hybrid"):
        report[method] = metrics([{**r, **r[method]} for r in rows])
        report[method]["languages"] = {
            lang: metrics([{**r, **r[method]} for r in rows if r["lang"] == lang])
            for lang in ("de", "en")
        }
    return report


async def answer_review(db, settings, report, output):
    """Mechanical validation only. Human factual-support labels intentionally stay blank."""
    provider = OpenAIProvider(settings)
    trusted = settings.model_copy(update={"ai_client_daily_limit": settings.ai_daily_limit})
    halted = False
    for row in report["rows"]:
        citations = row["hybrid"].get("citations", [])
        if row["hybrid"].get("error") or not citations or halted:
            row["answer"] = {"status": "not_generated"}
            continue
        entries = [{**c, "content": c["excerpt"]} for c in citations]
        try:
            result = await service.execute(
                db,
                trusted,
                provider,
                "rag-evaluation",
                "ask",
                {
                    "question": row["question"],
                    "history": row.get("history", []),
                    "entries": entries,
                },
                "patient",
                citations=citations,
                lang=row["lang"],
            )
            row["answer"] = {"status": "validated", **result}
        except AIUnavailable:
            row["answer"] = {"status": "provider_or_validation_failure"}
        except HTTPException as error:
            row["answer"] = {"status": f"http_{error.status_code}"}
            halted = error.status_code == 429
        await asyncio.sleep(4)
    with output.with_suffix(".review.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["id", "supported_claims", "total_claims", "appropriate_abstention", "notes"]
        )
        writer.writerows([row["id"], "", "", "", ""] for row in report["rows"])


class MemoizedDevEmbeddings:
    """Dev-only sweep reuses actual query vectors in memory; reservations stay conservative."""

    def __init__(self, provider, pause):
        self.provider, self.pause, self.cache = provider, pause, {}

    def embed(self, texts, task):
        key = (task, tuple(texts))
        if key not in self.cache:
            if self.cache and self.pause:
                time.sleep(self.pause)
            self.cache[key] = self.provider.embed(texts, task)
        return self.cache[key]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pause", type=float, default=4)
    parser.add_argument("--threshold", type=float)
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--answers", action="store_true")
    args = parser.parse_args()
    if args.pause < 0 or args.threshold is not None and not 0 <= args.threshold <= 1:
        parser.error("Invalid pause or threshold")
    if args.sweep and (args.split != "dev" or args.answers or args.threshold is not None):
        parser.error("Sweep is dev-only and incompatible with answers/threshold")
    raw = json.loads(Path("evaluation/rag/questions.json").read_text(encoding="utf-8"))
    cases = [c for c in validate_cases(raw) if c["split"] == args.split]
    settings = get_settings()
    if args.threshold is not None:
        settings = settings.model_copy(update={"rag_min_similarity": args.threshold})
    with SessionLocal() as db:
        if args.sweep:
            provider = MemoizedDevEmbeddings(get_embeddings(settings), args.pause)
            runs = [
                evaluate(
                    db,
                    settings.model_copy(update={"rag_min_similarity": threshold}),
                    cases,
                    provider,
                    0,
                )
                for threshold in (0.35, 0.4, 0.45, 0.5, 0.55, 0.6)
            ]
            result = {
                "runs": runs,
                "grid": [0.35, 0.4, 0.45, 0.5, 0.55, 0.6],
                "split": "dev",
                "query_vectors": "live, reused in memory across thresholds",
            }
        else:
            result = evaluate(db, settings, cases, get_embeddings(settings), args.pause)
            if args.answers:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                asyncio.run(answer_review(db, settings, result, args.output))
    result["frozen_dataset_sha"] = digest(raw)
    result["provider"] = "live-gemini-embedding-001"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if args.sweep:
        print(
            json.dumps(
                [{"threshold": r["threshold"], "hybrid": r["hybrid"]} for r in result["runs"]]
            )
        )
        return int(any(r["hybrid"]["provider_failures"] for r in result["runs"]))
    print(json.dumps({m: result[m] for m in ("lexical", "hybrid")}))
    return int(bool(result["hybrid"]["provider_failures"]))


if __name__ == "__main__":
    raise SystemExit(main())
