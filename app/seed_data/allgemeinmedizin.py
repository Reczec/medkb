from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Erkältung (grippaler Infekt)": {
            "title_en": "Common cold",
            "sections_en": {
                "definition": (
                    "A cold is a harmless viral infection that usually clears up by itself "
                    "after seven to ten days."
                ),
                "symptoms": (
                    "Typical are a runny nose, a scratchy throat, cough, tiredness and mild fever."
                ),
                "therapy": (
                    "The symptoms are treated: drink enough, rest and, if needed, "
                    "fever-lowering medicines. Antibiotics do not help against cold viruses."
                ),
                "red_flags": (
                    "With high fever, shortness of breath, chest pain or a worsening after a "
                    "few days, seek advice from your family doctor."
                ),
            },
            "keywords_en": ["Cold", "Runny nose", "Cough", "Sore throat", "Fever", "Virus"],
        },
        "Impfungen und Vorsorgeuntersuchungen im Erwachsenenalter": {
            "title_en": "Vaccinations and check-ups for adults",
            "sections_en": {
                "definition": (
                    "Regular check-ups and vaccinations help to prevent illnesses or to "
                    "detect them early."
                ),
                "diagnostics": (
                    "In Austria, adults can use the free preventive check-up at the family "
                    "doctor, with questions about general well-being, an examination and "
                    "laboratory values."
                ),
                "therapy": (
                    "The Austrian vaccination schedule recommends boosters, for example "
                    "against tetanus and diphtheria, as well as further vaccinations such as "
                    "against flu depending on age and risk factors."
                ),
            },
            "keywords_en": [
                "Vaccination",
                "Check-up",
                "Prevention",
                "Tetanus",
                "Flu",
                "Family doctor",
            ],
        },
    },
)
