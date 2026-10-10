from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Erkältung (grippaler Infekt)",
        "doc_type": "Beschreibung",
        "expected_category": "Allgemeinmedizin",
        "term_en": "Common cold",
        "icd11_code": "CA00",
        "medications": ["acetaminophen"],
        "sections": {
            "definition": (
                "Eine Erkältung ist ein harmloser, durch Viren ausgelöster grippaler Infekt, "
                "der in der Regel nach sieben bis zehn Tagen von selbst abklingt."
            ),
            "symptoms": (
                "Typisch sind Schnupfen, Halskratzen, Husten, Abgeschlagenheit und leichtes Fieber."
            ),
            "therapy": (
                "Behandelt werden die Symptome: ausreichend trinken, sich schonen, bei Bedarf "
                "fiebersenkende Mittel. Antibiotika helfen gegen Erkältungsviren nicht."
            ),
            "red_flags": (
                "Bei hohem Fieber, Atemnot, Brustschmerzen oder einer Verschlechterung nach "
                "einigen Tagen sollte ärztlicher Rat beim Hausarzt eingeholt werden."
            ),
        },
        "further_reading": [medlineplus("commoncold", "Common Cold")],
    },
    {
        "title": "Impfungen und Vorsorgeuntersuchungen im Erwachsenenalter",
        "doc_type": "Leitlinie",
        "expected_category": "Allgemeinmedizin",
        "term_en": "Adult vaccination",
        "sections": {
            "definition": (
                "Regelmäßige Vorsorgeuntersuchungen und Impfungen helfen, Erkrankungen zu "
                "verhindern oder früh zu erkennen."
            ),
            "diagnostics": (
                "In Österreich steht Erwachsenen die kostenlose Vorsorgeuntersuchung beim "
                "Hausarzt zur Verfügung, mit Fragen zum Allgemeinbefinden, Untersuchung und "
                "Laborwerten."
            ),
            "therapy": (
                "Der österreichische Impfplan empfiehlt Auffrischungen, zum Beispiel gegen "
                "Tetanus und Diphtherie, sowie weitere Impfungen wie gegen Grippe je nach "
                "Alter und Risikofaktoren."
            ),
        },
        "further_reading": [
            medlineplus("vaccines", "Vaccines"),
            who("immunization-coverage", "Immunization coverage"),
        ],
    },
]
