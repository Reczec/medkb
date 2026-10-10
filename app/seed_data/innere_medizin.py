from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Eisenmangelanämie",
        "doc_type": "Diagnose",
        "expected_category": "Innere Medizin",
        "term_en": "Iron deficiency anemia",
        "icd11_code": "3A00",
        "medications": ["ferrous sulfate"],
        "sections": {
            "definition": (
                "Bei der Eisenmangelanämie fehlt dem Körper Eisen, um ausreichend roten "
                "Blutfarbstoff (Hämoglobin) zu bilden. Sie ist die häufigste Form der "
                "Blutarmut."
            ),
            "symptoms": (
                "Typisch sind Müdigkeit, Leistungsknick, Blässe, Kopfschmerzen, brüchige "
                "Nägel und Atemnot bei Belastung."
            ),
            "causes": (
                "Ursachen sind Blutverluste etwa durch starke Regelblutungen oder im "
                "Magen-Darm-Trakt, ein erhöhter Bedarf in der Schwangerschaft und eisenarme "
                "Ernährung."
            ),
            "diagnostics": (
                "Blutbild, Hämoglobin und Ferritin sichern die Diagnose. Wichtig ist die "
                "Suche nach der Ursache, bei Erwachsenen oft mit Magen- und Darmspiegelung."
            ),
            "therapy": (
                "Eisen wird als Tablette oder Infusion ersetzt; gleichzeitig wird die Ursache "
                "behandelt."
            ),
            "red_flags": (
                "Schwarzer oder blutiger Stuhl, Brustschmerzen oder Ohnmacht bei Blutarmut "
                "erfordern eine sofortige ärztliche Abklärung."
            ),
        },
        "further_reading": [medlineplus("anemia", "Anemia"), who("anaemia", "Anaemia")],
    },
    {
        "title": "Gicht",
        "doc_type": "Diagnose",
        "expected_category": "Innere Medizin",
        "term_en": "Gout",
        "icd11_code": "FA25",
        "medications": ["allopurinol", "colchicine"],
        "sections": {
            "definition": (
                "Gicht ist eine Stoffwechselerkrankung, bei der sich Harnsäurekristalle in "
                "Gelenken ablagern und Entzündungen auslösen."
            ),
            "symptoms": (
                "Ein Gichtanfall beginnt oft nachts mit heftigen Schmerzen, Rötung und "
                "Schwellung eines Gelenks, typischerweise am Großzehengrundgelenk."
            ),
            "causes": (
                "Ein erhöhter Harnsäurespiegel entsteht durch Veranlagung, eine eingeschränkte "
                "Ausscheidung über die Niere, Alkohol und purinreiche Ernährung."
            ),
            "diagnostics": (
                "Klinisches Bild und Harnsäure im Blut geben Hinweise; beweisend ist der "
                "Nachweis von Kristallen in der Gelenkflüssigkeit."
            ),
            "therapy": (
                "Im Anfall helfen entzündungshemmende Medikamente und Kühlen. Langfristig "
                "senken Medikamente und Ernährungsumstellung die Harnsäure."
            ),
            "red_flags": (
                "Fieber mit einem heißen, geschwollenen Gelenk kann auch eine Gelenkinfektion "
                "sein und muss sofort abgeklärt werden."
            ),
        },
        "further_reading": [medlineplus("gout", "Gout")],
    },
    {
        "title": "Chronische Nierenkrankheit",
        "doc_type": "Diagnose",
        "expected_category": "Innere Medizin",
        "term_en": "Chronic kidney disease",
        "icd11_code": "GB61",
        "sections": {
            "definition": (
                "Bei der chronischen Nierenkrankheit lässt die Nierenfunktion über mindestens "
                "drei Monate nach, oft langsam fortschreitend."
            ),
            "symptoms": (
                "Lange gibt es keine Beschwerden. Später treten Müdigkeit, Wassereinlagerungen "
                "(Ödeme), Juckreiz und Bluthochdruck auf."
            ),
            "causes": (
                "Häufigste Ursachen sind Diabetes und Bluthochdruck, außerdem Entzündungen der "
                "Nieren und erbliche Erkrankungen."
            ),
            "diagnostics": (
                "Die Nierenwerte im Blut (Kreatinin, geschätzte Filtrationsrate) und Eiweiß im "
                "Urin bestimmen das Stadium."
            ),
            "therapy": (
                "Gute Einstellung von Blutdruck und Blutzucker bremst das Fortschreiten. Im "
                "Endstadium sind Dialyse oder Nierentransplantation nötig."
            ),
            "red_flags": (
                "Stark verminderte Urinmenge, Atemnot durch Wassereinlagerungen oder "
                "Verwirrtheit sind Notfälle – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("chronickidneydisease", "Chronic Kidney Disease")],
    },
]
