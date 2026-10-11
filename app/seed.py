"""Insert the bundled example documents.

Usage:  python -m app.seed          (only if the database is empty)
        python -m app.seed --force  (add them even if documents already exist)
"""

from __future__ import annotations

import argparse

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Document
from app.schemas import DocType, DocumentCreate
from app.seed_data import SEED_DOCUMENTS, SOURCE
from app.services import create_document


def seed_if_empty(db: Session, force: bool = False, commit: bool = True) -> int:
    """Create the example documents; categories and keywords come from the classifier."""
    if not force and (db.scalar(select(func.count(Document.id))) or 0) > 0:
        return 0
    for item in SEED_DOCUMENTS:
        create_document(
            db,
            DocumentCreate(
                title=item["title"],
                doc_type=DocType(item["doc_type"]),
                sections=item["sections"],
                term_en=item["term_en"],
                icd11_code=item.get("icd11_code"),
                medications=item.get("medications", []),
                further_reading=item["further_reading"],
                source=SOURCE,
            ),
            commit=commit,
        )
    return len(SEED_DOCUMENTS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Insert example documents.")
    parser.add_argument("--force", action="store_true", help="insert even if the DB is not empty")
    args = parser.parse_args()

    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        added = seed_if_empty(db, force=args.force)
    print(f"Inserted {added} example documents." if added else "Database not empty, nothing to do.")


if __name__ == "__main__":
    main()
