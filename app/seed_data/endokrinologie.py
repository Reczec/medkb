from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Diabetes mellitus Typ 2",
        "doc_type": "Diagnose",
        "expected_category": "Endokrinologie",
        "term_en": "Type 2 diabetes mellitus",
        "icd11_code": "5A11",
        "medications": ["metformin", "empagliflozin"],
        "sections": {
            "definition": (
                "Beim Diabetes mellitus Typ 2 spricht der Körper schlechter auf Insulin an, "
                "wodurch der Blutzucker dauerhaft erhöht ist."
            ),
            "symptoms": (
                "Lange bestehen kaum Beschwerden. Später treten starker Durst, häufiges "
                "Wasserlassen, Müdigkeit und schlecht heilende Wunden auf."
            ),
            "causes": (
                "Veranlagung, Übergewicht und Bewegungsmangel führen zu einer "
                "Insulinresistenz, die die Bauchspeicheldrüse zunächst ausgleicht."
            ),
            "diagnostics": (
                "Nüchternblutzucker und der Langzeitzuckerwert HbA1c sichern die Diagnose. "
                "Regelmäßige Kontrollen von Augen, Nieren und Füßen erkennen Folgeschäden "
                "früh."
            ),
            "therapy": (
                "Basis sind Gewichtsreduktion, Bewegung und ausgewogene Ernährung; zusätzlich "
                "kommen blutzuckersenkende Medikamente und bei Bedarf Insulin zum Einsatz."
            ),
            "red_flags": (
                "Verwirrtheit, Schweißausbruch und Zittern bei Unterzuckerung oder starker "
                "Durst mit Benommenheit bei sehr hohem Blutzucker sind Notfälle – Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("diabetestype2", "Type 2 Diabetes"),
            who("diabetes", "Diabetes"),
        ],
    },
    {
        "title": "Schilddrüsenunterfunktion (Hypothyreose)",
        "doc_type": "Diagnose",
        "expected_category": "Endokrinologie",
        "term_en": "Hypothyroidism",
        "icd11_code": "5A00",
        "medications": ["levothyroxine"],
        "sections": {
            "definition": (
                "Bei einer Hypothyreose bildet die Schilddrüse zu wenig Hormone, wodurch der "
                "Stoffwechsel verlangsamt wird."
            ),
            "symptoms": (
                "Typisch sind Müdigkeit, Kälteempfindlichkeit, Gewichtszunahme, trockene Haut, "
                "Verstopfung und eine gedrückte Stimmung."
            ),
            "causes": (
                "Häufigste Ursache ist die Hashimoto-Thyreoiditis, eine Autoimmunentzündung "
                "der Schilddrüse; seltener Operation, Radiojodtherapie oder Jodmangel."
            ),
            "diagnostics": (
                "Ein erhöhter TSH-Wert mit erniedrigtem freiem Schilddrüsenhormon bestätigt "
                "die Diagnose; Antikörper und Ultraschall zeigen die Ursache."
            ),
            "therapy": (
                "Das fehlende Hormon wird als Tablette ersetzt und die Dosis anhand des "
                "TSH-Werts angepasst – meist lebenslang."
            ),
            "red_flags": (
                "Starke Benommenheit, Unterkühlung und verlangsamter Herzschlag bei bekannter "
                "Unterfunktion sind selten, aber ein Notfall – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("hypothyroidism", "Hypothyroidism")],
    },
    {
        "title": "Schilddrüsenüberfunktion (Hyperthyreose)",
        "doc_type": "Diagnose",
        "expected_category": "Endokrinologie",
        "term_en": "Hyperthyroidism",
        "icd11_code": "5A02",
        "medications": ["methimazole"],
        "sections": {
            "definition": (
                "Bei einer Hyperthyreose bildet die Schilddrüse zu viele Hormone, der "
                "Stoffwechsel läuft beschleunigt."
            ),
            "symptoms": (
                "Typisch sind Herzrasen, Nervosität, Zittern, Schwitzen, Gewichtsverlust trotz "
                "Appetit und Schlafstörungen."
            ),
            "causes": (
                "Häufige Ursachen sind Morbus Basedow, eine Autoimmunerkrankung, und "
                "Schilddrüsenknoten, die unkontrolliert Hormone bilden."
            ),
            "diagnostics": (
                "Ein erniedrigter TSH-Wert mit erhöhten Schilddrüsenhormonen, Antikörper, "
                "Ultraschall und Szintigrafie klären Art und Ursache."
            ),
            "therapy": (
                "Thyreostatika bremsen die Hormonbildung. Je nach Ursache folgen "
                "Radiojodtherapie oder Operation."
            ),
            "red_flags": (
                "Hohes Fieber, starkes Herzrasen, Unruhe oder Verwirrtheit können eine "
                "thyreotoxische Krise sein – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("hyperthyroidism", "Hyperthyroidism")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Diabetes mellitus Typ 2": {
            "title_en": "Type 2 diabetes mellitus",
            "sections_en": {
                "definition": (
                    "In type 2 diabetes mellitus, the body responds less well to insulin, so "
                    "the blood sugar is permanently raised."
                ),
                "symptoms": (
                    "For a long time there are hardly any symptoms. Later, strong thirst, "
                    "frequent urination, tiredness and poorly healing wounds appear."
                ),
                "causes": (
                    "A predisposition, overweight and lack of exercise lead to insulin "
                    "resistance, which the pancreas first compensates."
                ),
                "diagnostics": (
                    "Fasting blood sugar and the long-term sugar value HbA1c confirm the "
                    "diagnosis. Regular checks of the eyes, kidneys and feet detect "
                    "complications early."
                ),
                "therapy": (
                    "The basis is weight loss, exercise and a balanced diet; in addition, "
                    "blood-sugar-lowering medicines and, if needed, insulin are used."
                ),
                "red_flags": (
                    "Confusion, sweating and trembling with low blood sugar, or severe thirst "
                    "with drowsiness with very high blood sugar, are emergencies – call the "
                    "emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Diabetes",
                "Blood sugar",
                "Insulin",
                "HbA1c",
                "Overweight",
                "Metformin",
            ],
        },
        "Schilddrüsenunterfunktion (Hypothyreose)": {
            "title_en": "Underactive thyroid (hypothyroidism)",
            "sections_en": {
                "definition": (
                    "With hypothyroidism, the thyroid gland produces too few hormones, so the "
                    "metabolism slows down."
                ),
                "symptoms": (
                    "Typical are tiredness, sensitivity to cold, weight gain, dry skin, "
                    "constipation and a low mood."
                ),
                "causes": (
                    "The most common cause is Hashimoto's thyroiditis, an autoimmune "
                    "inflammation of the thyroid; less often surgery, radioiodine therapy or "
                    "iodine deficiency."
                ),
                "diagnostics": (
                    "A raised TSH with a lowered free thyroid hormone confirms the diagnosis; "
                    "antibodies and ultrasound show the cause."
                ),
                "therapy": (
                    "The missing hormone is replaced as a tablet and the dose is adjusted by "
                    "the TSH value – usually for life."
                ),
                "red_flags": (
                    "Severe drowsiness, low body temperature and a slow heartbeat in known "
                    "hypothyroidism are rare but an emergency – call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Hypothyroidism",
                "Thyroid",
                "TSH",
                "Hashimoto",
                "Tiredness",
                "Levothyroxine",
            ],
        },
        "Schilddrüsenüberfunktion (Hyperthyreose)": {
            "title_en": "Overactive thyroid (hyperthyroidism)",
            "sections_en": {
                "definition": (
                    "With hyperthyroidism, the thyroid gland produces too many hormones and "
                    "the metabolism runs faster."
                ),
                "symptoms": (
                    "Typical are a racing heart, nervousness, trembling, sweating, weight "
                    "loss despite a good appetite and sleep problems."
                ),
                "causes": (
                    "Common causes are Graves' disease, an autoimmune condition, and thyroid "
                    "nodules that produce hormones uncontrolled."
                ),
                "diagnostics": (
                    "A lowered TSH with raised thyroid hormones, antibodies, ultrasound and "
                    "scintigraphy clarify the type and cause."
                ),
                "therapy": (
                    "Antithyroid drugs slow down hormone production. Depending on the cause, "
                    "radioiodine therapy or surgery follow."
                ),
                "red_flags": (
                    "High fever, a very fast heartbeat, restlessness or confusion can be a "
                    "thyrotoxic crisis – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Hyperthyroidism",
                "Thyroid",
                "Graves' disease",
                "Racing heart",
                "Weight loss",
                "Scintigraphy",
            ],
        },
    },
)
