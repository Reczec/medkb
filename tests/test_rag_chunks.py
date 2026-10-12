from app.models import Document


def test_chunking_preserves_tail_overlap_and_sections():
    from app.rag.chunks import chunks

    text = "start " + "word " * 400 + "end"
    doc = Document(id=1, title="Test", content="not duplicated", sections={"symptoms": text})
    result = chunks(doc, "de")
    assert result[0].text.startswith("start") and result[-1].text.endswith("end")
    assert all(len(c.text) <= 800 and c.section == "symptoms" for c in result)
    assert result[0].text[-100:] == result[1].text[:100]
    assert "not duplicated" not in " ".join(c.text for c in result)


def test_chunk_keys_survive_reset_but_bind_text_and_language():
    from app.rag.chunks import chunks

    doc = Document(id=1, title="Example", content="German information")
    before = chunks(doc, "de")
    doc.id = 500
    assert before[0].key == chunks(doc, "de")[0].key
    assert before[0].key != chunks(doc, "en")[0].key
    doc.content = "changed information"
    assert before[0].key != chunks(doc, "de")[0].key


def test_partial_english_keeps_german_warning_signs():
    from app.rag.chunks import chunks

    doc = Document(
        id=1,
        title="Beispiel",
        title_en="Example",
        content="German information",
        sections={"definition": "Deutsch", "red_flags": "Notruf 144"},
        sections_en={"definition": "English"},
    )
    result = chunks(doc, "en")
    assert [(c.section, c.text) for c in result] == [
        ("definition", "English"),
        ("red_flags", "Notruf 144"),
    ]
    assert all(c.title == "Example" for c in result)
