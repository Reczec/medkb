"""Explicit operator action: python -m app.rag.index_cli --pause 4."""

import argparse
import json
from dataclasses import asdict

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.rag.embeddings import get_embeddings
from app.rag.index import build_index


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pause", type=float, default=4)
    parser.add_argument("--limit-documents", type=int)
    parser.add_argument("--cleanup", action="store_true")
    args = parser.parse_args()
    settings = get_settings()
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        report = build_index(
            db, settings, get_embeddings(settings), args.pause, args.cleanup, args.limit_documents
        )
    print(json.dumps(asdict(report)))
    return 0 if report.total and report.ready == report.total and not report.failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
