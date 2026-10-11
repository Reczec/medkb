from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Eisenmangelanämie",
        "doc_type": "Diagnose",
        "expected_category": "Innere Medizin",
        "term_en": "Iron deficiency anemia",
        "icd11_code": "3A00",
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Eisenmangelanämie": {
            "title_en": "Iron deficiency anaemia",
            "sections_en": {
                "definition": (
                    "In iron deficiency anaemia the body lacks iron to form enough red blood "
                    "pigment (haemoglobin). It is the most common form of anaemia."
                ),
                "symptoms": (
                    "Typical are tiredness, reduced performance, paleness, headaches, brittle "
                    "nails and shortness of breath on exertion."
                ),
                "causes": (
                    "Causes are blood loss, for example through heavy periods or in the gut, "
                    "an increased need in pregnancy and a diet low in iron."
                ),
                "diagnostics": (
                    "A blood count, haemoglobin and ferritin confirm the diagnosis. Finding "
                    "the cause is important; in adults this often involves gastroscopy and "
                    "colonoscopy."
                ),
                "therapy": (
                    "Iron is replaced as tablets or an infusion; at the same time the cause "
                    "is treated."
                ),
                "red_flags": (
                    "Black or bloody stools, chest pain or fainting with anaemia require "
                    "immediate medical assessment."
                ),
            },
            "keywords_en": [
                "Anaemia",
                "Iron deficiency",
                "Haemoglobin",
                "Ferritin",
                "Tiredness",
                "Blood count",
            ],
        },
        "Gicht": {
            "title_en": "Gout",
            "sections_en": {
                "definition": (
                    "Gout is a metabolic disease in which uric acid crystals are deposited in "
                    "joints and trigger inflammation."
                ),
                "symptoms": (
                    "A gout attack often starts at night with severe pain, redness and "
                    "swelling of a joint, typically the base of the big toe."
                ),
                "causes": (
                    "A raised uric acid level arises from predisposition, reduced excretion "
                    "by the kidney, alcohol and a purine-rich diet."
                ),
                "diagnostics": (
                    "The clinical picture and uric acid in the blood give hints; crystals in "
                    "the joint fluid are conclusive."
                ),
                "therapy": (
                    "During an attack, anti-inflammatory medicines and cooling help. In the "
                    "long term, medicines and a change of diet lower the uric acid."
                ),
                "red_flags": (
                    "Fever with a hot, swollen joint can also be a joint infection and must "
                    "be assessed at once."
                ),
            },
            "keywords_en": ["Gout", "Uric acid", "Joint", "Big toe", "Attack", "Purines"],
        },
        "Chronische Nierenkrankheit": {
            "title_en": "Chronic kidney disease",
            "sections_en": {
                "definition": (
                    "In chronic kidney disease, kidney function declines for at least three "
                    "months, often progressing slowly."
                ),
                "symptoms": (
                    "For a long time there are no symptoms. Later, tiredness, fluid retention "
                    "(oedema), itching and high blood pressure appear."
                ),
                "causes": (
                    "The most common causes are diabetes and high blood pressure, also kidney "
                    "inflammation and hereditary diseases."
                ),
                "diagnostics": (
                    "The kidney values in the blood (creatinine, estimated filtration rate) "
                    "and protein in the urine determine the stage."
                ),
                "therapy": (
                    "Good control of blood pressure and blood sugar slows progression. In the "
                    "final stage dialysis or a kidney transplant is needed."
                ),
                "red_flags": (
                    "A strongly reduced amount of urine, shortness of breath from fluid "
                    "retention or confusion are emergencies – call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Kidney",
                "Kidney failure",
                "Creatinine",
                "Dialysis",
                "Oedema",
                "Blood pressure",
            ],
        },
    },
)
