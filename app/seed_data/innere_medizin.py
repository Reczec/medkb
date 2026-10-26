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


EXTRA = with_english(
    [
        {
            "title": "Vitamin-B12-Mangel",
            "doc_type": "Diagnose",
            "expected_category": "Innere Medizin",
            "term_en": "Vitamin B12 deficiency",
            "icd11_code": "5B5F",
            "medications": ["cyanocobalamin"],
            "sections": {
                "definition": (
                    "Beim Vitamin-B12-Mangel fehlt dem Körper das Vitamin Cobalamin, das für "
                    "die Blutbildung, die Nerven und den Stoffwechsel wichtig ist."
                ),
                "symptoms": (
                    "Müdigkeit, Blässe, Atemnot bei Belastung, Zungenbrennen sowie "
                    "Kribbeln und Taubheitsgefühle in Händen und Füßen. Später können "
                    "Gedächtnisprobleme und Gangunsicherheit auftreten."
                ),
                "causes": (
                    "Häufig ist eine eingeschränkte Aufnahme im Magen-Darm-Trakt die "
                    "Ursache, etwa bei Magenschleimhautentzündung, nach Magenoperationen oder "
                    "durch Medikamente wie Metformin. Eine rein pflanzliche Ernährung "
                    "ohne Ergänzung führt ebenfalls zu einem Mangel."
                ),
                "diagnostics": (
                    "Eine Blutuntersuchung misst Vitamin B12 und das Blutbild. Bei "
                    "Anämie zeigen sich vergrößerte rote Blutkörperchen. Ergänzende Werte "
                    "klären die Ursache."
                ),
                "therapy": (
                    "Vitamin B12 wird als Spritze oder hochdosiert als Tablette ersetzt. "
                    "Bei Aufnahmestörungen ist die Spritze oft zuverlässiger. Die Behandlung "
                    "ist langfristig nötig, wenn die Ursache bestehen bleibt."
                ),
                "red_flags": (
                    "Neu auftretende Lähmungen, Gangunsicherheit, Verwirrtheit oder "
                    "starke Atemnot und Herzklopfen bei Anämie sollten umgehend ärztlich "
                    "abgeklärt werden, bei Lähmungen oder Atemnot Notruf 144."
                ),
            },
            "further_reading": [medlineplus("anemia", "Anemia")],
        },
        {
            "title": "Systemischer Lupus erythematodes",
            "doc_type": "Diagnose",
            "expected_category": "Innere Medizin",
            "term_en": "Systemic lupus erythematosus",
            "icd11_code": "4A40",
            "medications": ["hydroxychloroquine", "prednisone"],
            "sections": {
                "definition": (
                    "Der systemische Lupus erythematodes ist eine Autoimmunerkrankung, bei "
                    "der das Immunsystem körpereigenes Gewebe angreift und Haut, Gelenke, "
                    "Nieren und weitere Organe entzünden kann."
                ),
                "symptoms": (
                    "Typisch sind ein schmetterlingsförmiger Ausschlag im Gesicht, "
                    "Gelenkschmerzen, Fieber, Müdigkeit und Lichtempfindlichkeit der Haut. Bei "
                    "Nierenbeteiligung treten Eiweiß im Urin und Wassereinlagerungen auf."
                ),
                "causes": (
                    "Die Ursache ist nicht vollständig geklärt. Erbliche Veranlagung, "
                    "Hormone, UV-Licht und Infekte spielen eine Rolle. Frauen im "
                    "gebärfähigen Alter sind am häufigsten betroffen."
                ),
                "diagnostics": (
                    "Die Diagnose stützt sich auf Beschwerden, körperliche Untersuchung, "
                    "Blutwerte mit Autoantikörpern, Nierenwerte und Urinuntersuchung. Bei "
                    "Bedarf folgt eine Gewebeprobe."
                ),
                "therapy": (
                    "Sonnenschutz und Hydroxychloroquin bilden die Basis. Bei starker "
                    "Krankheitsaktivität werden Kortison und das Immunsystem dämpfende "
                    "Medikamente eingesetzt. Regelmäßige Kontrollen der Nieren sind wichtig."
                ),
                "red_flags": (
                    "Starke Atemnot, Brustschmerz, Krampfanfälle, Verwirrtheit oder "
                    "ausgeprägte Wassereinlagerungen mit wenig Urin können auf schwere "
                    "Organbeteiligung hinweisen – sofort Notruf 144."
                ),
            },
            "further_reading": [medlineplus("lupus", "Lupus")],
        },
        {
            "title": "Flüssigkeitsmangel (Exsikkose)",
            "doc_type": "Diagnose",
            "expected_category": "Innere Medizin",
            "term_en": "Dehydration",
            "icd11_code": "5C70.0",
            "medications": [],
            "sections": {
                "definition": (
                    "Bei einer Exsikkose (Austrocknung) hat der Körper zu wenig Wasser und "
                    "Elektrolyte, weil mehr verloren geht als aufgenommen wird."
                ),
                "symptoms": (
                    "Starker Durst, trockene Mundschleimhaut, dunkler und seltener Urin, "
                    "Kopfschmerzen, Schwindel, Müdigkeit und stehende Hautfalten. Bei "
                    "älteren Menschen zeigen sich oft Verwirrtheit und Stürze."
                ),
                "causes": (
                    "Durchfall, Erbrechen, Fieber, starkes Schwitzen und zu geringe "
                    "Trinkmenge, besonders bei älteren Menschen, Kleinkindern und im Sommer. "
                    "Entwässernde Medikamente und Diabetes erhöhen das Risiko."
                ),
                "diagnostics": (
                    "Die Ärztin beurteilt Hautspannung, Puls und Blutdruck. Blutwerte wie "
                    "Elektrolyte, Kreatinin und Harnstoff zeigen das Ausmaß und mögliche "
                    "Nierenfolgen."
                ),
                "therapy": (
                    "Leichte Formen werden durch Trinken, bei Durchfall mit "
                    "Elektrolytlösungen, behandelt. Bei schwerer Austrocknung erhalten "
                    "Patienten Infusionen im Krankenhaus. Die Ursache wird behandelt."
                ),
                "red_flags": (
                    "Verwirrtheit, sehr schneller Puls, niedriger Blutdruck, kaum Urin oder "
                    "Bewusstseinstrübung sind Notfallzeichen – sofort Notruf 144. Bei "
                    "Säuglingen mit Durchfall und trockenen Windeln umgehend zum Kinderarzt."
                ),
            },
            "further_reading": [medlineplus("dehydration", "Dehydration")],
        },
    ],
    {
        "Vitamin-B12-Mangel": {
            "title_en": "Vitamin B12 deficiency",
            "sections_en": {
                "definition": (
                    "In vitamin B12 deficiency the body lacks the vitamin cobalamin, "
                    "which is important for blood formation, the nerves and metabolism."
                ),
                "symptoms": (
                    "Tiredness, pallor, breathlessness on exertion, a burning tongue and "
                    "tingling and numbness in the hands and feet. Later memory problems "
                    "and unsteady walking can occur."
                ),
                "causes": (
                    "Reduced absorption in the digestive tract is a common cause, for "
                    "example in inflammation of the stomach lining, after stomach "
                    "operations or because of medicines such as metformin. A purely plant "
                    "based diet without supplements also leads to a deficiency."
                ),
                "diagnostics": (
                    "A blood test measures vitamin B12 and the blood count. In anaemia, "
                    "enlarged red blood cells are seen. Additional values clarify the "
                    "cause."
                ),
                "therapy": (
                    "Vitamin B12 is replaced as an injection or as a high-dose tablet. "
                    "With absorption disorders the injection is often more reliable. "
                    "Treatment is needed long term if the cause remains."
                ),
                "red_flags": (
                    "Newly occurring paralysis, unsteady walking, confusion or severe "
                    "breathlessness and palpitations in anaemia should be checked "
                    "promptly; for paralysis or breathlessness call the emergency number "
                    "144 (Austria)."
                ),
            },
            "keywords_en": [
                "Vitamin B12",
                "Deficiency",
                "Anaemia",
                "Tingling",
                "Blood count",
                "Injection",
            ],
        },
        "Systemischer Lupus erythematodes": {
            "title_en": "Systemic lupus erythematosus",
            "sections_en": {
                "definition": (
                    "Systemic lupus erythematosus is an autoimmune disease in which the "
                    "immune system attacks the body's own tissue and can inflame the "
                    "skin, joints, kidneys and other organs."
                ),
                "symptoms": (
                    "Typical are a butterfly-shaped rash on the face, joint pain, fever, "
                    "tiredness and sensitivity of the skin to light. With kidney "
                    "involvement, protein in the urine and fluid retention occur."
                ),
                "causes": (
                    "The cause is not fully understood. Inherited tendency, hormones, UV "
                    "light and infections play a role. Women of childbearing age are "
                    "affected most often."
                ),
                "diagnostics": (
                    "The diagnosis rests on the symptoms, a physical examination, blood "
                    "values with autoantibodies, kidney values and a urine test. If "
                    "needed, a tissue sample follows."
                ),
                "therapy": (
                    "Sun protection and hydroxychloroquine form the basis. With high "
                    "disease activity, cortisone and medicines that dampen the immune "
                    "system are used. Regular checks of the kidneys are important."
                ),
                "red_flags": (
                    "Severe breathlessness, chest pain, seizures, confusion or marked "
                    "fluid retention with little urine can point to serious organ "
                    "involvement – call the emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Lupus",
                "Autoimmune disease",
                "Butterfly rash",
                "Joint pain",
                "Kidneys",
                "Sun protection",
            ],
        },
        "Flüssigkeitsmangel (Exsikkose)": {
            "title_en": "Fluid deficiency (dehydration)",
            "sections_en": {
                "definition": (
                    "In dehydration the body has too little water and electrolytes, "
                    "because more is lost than is taken in."
                ),
                "symptoms": (
                    "Strong thirst, a dry mouth, dark urine passed less often, headache, "
                    "dizziness, tiredness and skin folds that stay up. In older people, "
                    "confusion and falls often appear."
                ),
                "causes": (
                    "Diarrhoea, vomiting, fever, heavy sweating and drinking too little, "
                    "especially in older people, small children and in summer. "
                    "Diuretics and diabetes raise the risk."
                ),
                "diagnostics": (
                    "The doctor assesses skin tension, pulse and blood pressure. Blood "
                    "values such as electrolytes, creatinine and urea show the extent and "
                    "possible effects on the kidneys."
                ),
                "therapy": (
                    "Mild forms are treated by drinking, with diarrhoea using electrolyte "
                    "solutions. In severe dehydration patients receive infusions in "
                    "hospital. The cause is treated."
                ),
                "red_flags": (
                    "Confusion, a very fast pulse, low blood pressure, hardly any urine "
                    "or clouding of consciousness are emergency signs – call the "
                    "emergency number 144 (Austria) at once. For babies with diarrhoea "
                    "and dry nappies go to the paediatrician immediately."
                ),
            },
            "keywords_en": [
                "Dehydration",
                "Fluid deficiency",
                "Thirst",
                "Electrolytes",
                "Diarrhoea",
                "Infusion",
            ],
        },
    },
)
