"""Azure semantic retrieval is enabled only for a complete current bilingual index."""

import pytest

from scripts.azure.preflight import validate_rag_readiness


@pytest.mark.parametrize(
    "coverage",
    [
        {"de": (271, 271), "en": (271, 270)},
        {"de": (271, 271)},
        {"de": (270, 270), "en": (271, 271)},
        {},
    ],
)
def test_partial_missing_or_changed_corpus_is_rejected(coverage):
    with pytest.raises(ValueError, match="index"):
        validate_rag_readiness(coverage)


def test_complete_bilingual_index_is_allowed():
    validate_rag_readiness({"de": (271, 271), "en": (271, 271)})


def test_current_coverage_excludes_stale_signatures(db_session, test_settings):
    from app.models import Embedding
    from app.rag.chunks import signature
    from app.rag.index import corpus
    from app.seed import seed_if_empty
    from scripts.azure.preflight import rag_coverage

    seed_if_empty(db_session)
    current = corpus(db_session, test_settings)
    db_session.add_all(
        [
            Embedding(key=chunk.key, signature=signature(), vector=[1.0] + [0.0] * 767)
            for chunk in current
        ]
    )
    db_session.commit()
    per_language = len(current) // 2
    assert rag_coverage(db_session, test_settings) == {
        "de": (per_language, per_language),
        "en": (per_language, per_language),
    }
    db_session.get(Embedding, current[0].key).signature = "obsolete"
    db_session.commit()
    with pytest.raises(ValueError, match="index"):
        validate_rag_readiness(rag_coverage(db_session, test_settings))
