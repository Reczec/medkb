import pytest

from app.classifier import CATEGORIES, DEFAULT_CATEGORY, MAX_KEYWORDS, classify
from app.seed_data import SEED_DOCUMENTS


@pytest.mark.parametrize("doc", SEED_DOCUMENTS, ids=[d["title"][:30] for d in SEED_DOCUMENTS])
def test_example_documents_get_expected_category(doc):
    # Note: these examples were written together with the vocabulary, so this is a regression
    # test for the rules, not an accuracy measurement on unseen text.
    assert classify(doc["title"], doc["content"]).category == doc["expected_category"]


def test_unspecific_text_falls_back_to_default():
    result = classify("Lorem ipsum", "Dies ist ein völlig unspezifischer Text ohne Fachbegriffe.")
    assert result.category == DEFAULT_CATEGORY
    assert result.fallback is True
    assert result.confidence == 0.0
    assert result.scores == {}


def test_single_weak_hit_is_not_enough():
    # One general term (weight 1) in the content stays below the minimum score.
    result = classify("Notiz", "Der Patient klagte kurz über Schnupfen.")
    assert result.fallback is True
    assert result.category == DEFAULT_CATEGORY


def test_title_counts_more_than_content():
    in_title = classify("Tinnitus", "Ein kurzer Text ohne weitere Hinweise auf irgendein Fach.")
    in_content = classify("Notiz", "Ein kurzer Text über Tinnitus ohne weitere Hinweise.")
    assert in_title.scores["HNO"] > in_content.scores["HNO"]


def test_repetition_is_capped():
    once = classify("Notiz", "Migräne " + "x " * 5)
    many = classify("Notiz", "Migräne " * 50)
    assert once.scores["Neurologie"] == 2  # weight 2, one hit
    assert many.scores["Neurologie"] == 6  # weight 2, capped at three hits


def test_compound_words_are_matched():
    # "kopfschmerz" sits in the middle of the compound word.
    result = classify(
        "Vernichtungskopfschmerz", "Der Vernichtungskopfschmerz kam plötzlich, dazu Schwindel."
    )
    assert result.category == "Neurologie"
    assert "Vernichtungskopfschmerz" in result.keywords


def test_word_start_rule_avoids_false_positive():
    # "Drachen" contains "rachen" but is not a throat term.
    result = classify("Drachen", "Der Drachen und die Drachen flogen über die Drachenburg.")
    assert "HNO" not in result.scores


def test_multiword_term_becomes_keyword():
    result = classify(
        "Notiz",
        "Bei Angina pectoris tritt Brustschmerz bei Belastung auf. Angina pectoris ist ernst.",
    )
    assert result.category == "Kardiologie"
    assert "Angina Pectoris" in result.keywords


def test_keywords_are_real_words_from_the_text_and_capped():
    doc = next(d for d in SEED_DOCUMENTS if d["title"] == "Schlaganfall – Warnzeichen")
    result = classify(doc["title"], doc["content"])
    assert "Schlaganfall" in result.keywords
    assert len(result.keywords) <= MAX_KEYWORDS
    assert len({k.lower() for k in result.keywords}) == len(result.keywords)
    haystack = (doc["title"] + " " + doc["content"]).lower()
    assert all(k.lower() in haystack for k in result.keywords)


def test_ties_prefer_specific_category():
    # HNO: Hörsturz (2) + Tinnitus (2) = 4. Allgemeinmedizin: four general terms = 4.
    result = classify("Notiz", "Hörsturz Tinnitus. Erkältung Fieber Husten Infekt.")
    assert result.scores["HNO"] == result.scores[DEFAULT_CATEGORY] == 4
    assert result.category == "HNO"


def test_all_categories_have_vocabulary():
    assert DEFAULT_CATEGORY in CATEGORIES
    assert CATEGORIES[-1] == DEFAULT_CATEGORY
