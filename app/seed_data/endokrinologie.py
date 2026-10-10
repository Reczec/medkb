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
