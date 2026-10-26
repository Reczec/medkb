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


EXTRA = with_english(
    [
        {
            "title": "Diabetes mellitus Typ 1",
            "doc_type": "Diagnose",
            "expected_category": "Endokrinologie",
            "term_en": "Type 1 diabetes mellitus",
            "icd11_code": "5A10",
            "medications": ["insulin"],
            "sections": {
                "definition": (
                    "Beim Typ-1-Diabetes zerstört das eigene Immunsystem die "
                    "insulinproduzierenden Zellen der Bauchspeicheldrüse, sodass Insulin "
                    "fehlt und der Blutzucker ansteigt."
                ),
                "symptoms": (
                    "Starker Durst, häufiges Wasserlassen, Gewichtsverlust, Müdigkeit und "
                    "Leistungsschwäche. Die Beschwerden entwickeln sich meist innerhalb "
                    "weniger Wochen, oft bei Kindern, Jugendlichen und jungen Erwachsenen."
                ),
                "causes": (
                    "Es handelt sich um eine Autoimmunerkrankung. Erbliche Veranlagung und "
                    "wahrscheinlich Auslöser wie Virusinfekte spielen eine Rolle. Lebensstil "
                    "ist nicht die Ursache."
                ),
                "diagnostics": (
                    "Der Blutzucker ist erhöht, der Langzeitwert HbA1c ist erhöht. Der "
                    "Nachweis bestimmter Antikörper sichert die Diagnose."
                ),
                "therapy": (
                    "Lebenslang ist eine Insulinbehandlung nötig, per Spritze, Pen oder Pumpe. "
                    "Der Blutzucker wird selbst oder mit einem Sensor gemessen. Schulung zu "
                    "Ernährung und Insulindosierung ist ein fester Teil der Behandlung."
                ),
                "red_flags": (
                    "Starke Übelkeit, Erbrechen, Bauchschmerzen, tiefe Atmung und "
                    "Benommenheit mit hohem Blutzucker deuten auf eine Ketoazidose hin; ein "
                    "zu niedriger Blutzucker mit Verwirrtheit, Zittern oder Bewusstlosigkeit "
                    "ist ebenso ein Notfall – Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("diabetestype1", "Type 1 diabetes"),
                who("diabetes", "Diabetes"),
            ],
        },
        {
            "title": "Adipositas (starkes Übergewicht)",
            "doc_type": "Diagnose",
            "expected_category": "Endokrinologie",
            "term_en": "Obesity",
            "icd11_code": "5B81",
            "medications": [],
            "sections": {
                "definition": (
                    "Adipositas ist eine chronische Erkrankung mit einem übermäßig hohen "
                    "Körperfettanteil. Ein Body-Mass-Index ab 30 gilt als Adipositas."
                ),
                "symptoms": (
                    "Betroffene bemerken Atemnot bei Belastung, Gelenkschmerzen, "
                    "Schnarchen und schnelle Ermüdung. Das Übergewicht erhöht das Risiko für "
                    "viele Folgeerkrankungen."
                ),
                "causes": (
                    "Mehr Energie wird aufgenommen als verbraucht. Dabei wirken Veranlagung, "
                    "Ernährung, Bewegungsmangel, Schlafmangel, Stress, Medikamente und "
                    "hormonelle Erkrankungen zusammen."
                ),
                "diagnostics": (
                    "Gewicht, Größe und Taillenumfang werden gemessen. Blutuntersuchungen "
                    "prüfen Blutzucker, Blutfette und Schilddrüse, um Folgeerkrankungen und "
                    "Ursachen zu erkennen."
                ),
                "therapy": (
                    "Grundlage sind eine dauerhafte Ernährungsumstellung, mehr Bewegung und "
                    "Verhaltenstherapie. Bei hohem Risiko kommen Medikamente oder eine "
                    "Operation am Magen in Frage. Kleine, aber dauerhafte Gewichtsabnahmen "
                    "verbessern bereits viele Werte."
                ),
                "red_flags": (
                    "Atemnot in Ruhe, Brustschmerzen oder ein stark geschwollenes Bein sind "
                    "ein Warnzeichen für Herz- oder Gefäßprobleme – Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("obesity", "Obesity"),
                who("obesity-and-overweight", "Obesity and overweight"),
            ],
        },
        {
            "title": "Erhöhte Blutfette (Fettstoffwechselstörung)",
            "doc_type": "Diagnose",
            "expected_category": "Endokrinologie",
            "term_en": "Hyperlipidemia",
            "icd11_code": "5C80",
            "medications": ["atorvastatin", "ezetimibe"],
            "sections": {
                "definition": (
                    "Bei einer Fettstoffwechselstörung sind Cholesterin oder Triglyzeride im "
                    "Blut dauerhaft erhöht, insbesondere das LDL-Cholesterin."
                ),
                "symptoms": (
                    "Erhöhte Blutfette verursachen meist keine Beschwerden. Bei sehr hohen "
                    "Werten oder erblichen Formen können Fettablagerungen an Sehnen oder "
                    "Augenlidern auftreten."
                ),
                "causes": (
                    "Ernährung mit viel gesättigten Fetten, Übergewicht, Bewegungsmangel, "
                    "Diabetes, Schilddrüsenunterfunktion und erbliche Veranlagung "
                    "(familiäre Hypercholesterinämie) erhöhen die Werte."
                ),
                "diagnostics": (
                    "Eine Blutabnahme bestimmt Gesamtcholesterin, LDL, HDL und Triglyzeride, "
                    "am besten nüchtern. Die Ärztin schätzt zusätzlich das Herz-Kreislauf-"
                    "Risiko ein."
                ),
                "therapy": (
                    "Ausgewogene Ernährung, Bewegung und Gewichtsabnahme sind die Basis. "
                    "Reicht das nicht aus, senken Medikamente wie Statine das LDL-"
                    "Cholesterin und das Risiko für Herzinfarkt und Schlaganfall."
                ),
                "red_flags": (
                    "Druck oder Schmerz in der Brust, plötzliche Lähmungen oder "
                    "Sprachstörungen können Folgen von Gefäßverengungen sein – sofort "
                    "Notruf 144. Sehr hohe Triglyzeride können eine Bauchspeicheldrüsen-"
                    "entzündung auslösen."
                ),
            },
            "further_reading": [medlineplus("cholesterol", "Cholesterol")],
        },
    ],
    {
        "Diabetes mellitus Typ 1": {
            "title_en": "Type 1 diabetes mellitus",
            "sections_en": {
                "definition": (
                    "In type 1 diabetes the body's own immune system destroys the "
                    "insulin-producing cells of the pancreas, so that insulin is missing "
                    "and the blood sugar rises."
                ),
                "symptoms": (
                    "Strong thirst, frequent urination, weight loss, tiredness and "
                    "reduced performance. The symptoms usually develop within a few weeks, "
                    "often in children, adolescents and young adults."
                ),
                "causes": (
                    "It is an autoimmune disease. Inherited tendency and probably "
                    "triggers such as viral infections play a role. Lifestyle is not the "
                    "cause."
                ),
                "diagnostics": (
                    "The blood sugar is raised, and so is the long-term value HbA1c. "
                    "Detecting certain antibodies confirms the diagnosis."
                ),
                "therapy": (
                    "Lifelong insulin treatment is needed, by syringe, pen or pump. Blood "
                    "sugar is measured by the person or with a sensor. Training in diet "
                    "and insulin dosing is a fixed part of the treatment."
                ),
                "red_flags": (
                    "Severe nausea, vomiting, abdominal pain, deep breathing and "
                    "drowsiness with high blood sugar point to ketoacidosis; blood sugar "
                    "that is too low, with confusion, trembling or loss of consciousness, "
                    "is an emergency as well – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Type 1 diabetes",
                "Insulin",
                "Blood sugar",
                "HbA1c",
                "Autoimmune disease",
                "Ketoacidosis",
            ],
        },
        "Adipositas (starkes Übergewicht)": {
            "title_en": "Obesity (severe overweight)",
            "sections_en": {
                "definition": (
                    "Obesity is a chronic disease with an excessive amount of body fat. A "
                    "body mass index of 30 or more counts as obesity."
                ),
                "symptoms": (
                    "People notice breathlessness on exertion, joint pain, snoring and "
                    "quick tiredness. The excess weight raises the risk of many "
                    "secondary diseases."
                ),
                "causes": (
                    "More energy is taken in than used. Inherited tendency, diet, lack of "
                    "exercise, lack of sleep, stress, medicines and hormonal diseases all "
                    "work together."
                ),
                "diagnostics": (
                    "Weight, height and waist circumference are measured. Blood tests "
                    "check blood sugar, blood fats and the thyroid, to recognise secondary "
                    "diseases and causes."
                ),
                "therapy": (
                    "The basis is a lasting change of diet, more exercise and behavioural "
                    "therapy. In high-risk cases medicines or an operation on the stomach "
                    "come into question. Small but lasting weight loss already improves "
                    "many values."
                ),
                "red_flags": (
                    "Breathlessness at rest, chest pain or a markedly swollen leg are "
                    "warning signs of heart or vessel problems – call the emergency "
                    "number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Obesity",
                "Overweight",
                "Body mass index",
                "Diet",
                "Exercise",
                "Weight loss",
            ],
        },
        "Erhöhte Blutfette (Fettstoffwechselstörung)": {
            "title_en": "Raised blood fats (lipid disorder)",
            "sections_en": {
                "definition": (
                    "In a lipid disorder, cholesterol or triglycerides in the blood are "
                    "permanently raised, especially LDL cholesterol."
                ),
                "symptoms": (
                    "Raised blood fats usually cause no symptoms. With very high values "
                    "or inherited forms, fat deposits can appear on tendons or eyelids."
                ),
                "causes": (
                    "A diet rich in saturated fats, overweight, lack of exercise, "
                    "diabetes, an underactive thyroid and inherited tendency (familial "
                    "hypercholesterolaemia) raise the values."
                ),
                "diagnostics": (
                    "A blood sample measures total cholesterol, LDL, HDL and "
                    "triglycerides, ideally on an empty stomach. The doctor also estimates "
                    "the cardiovascular risk."
                ),
                "therapy": (
                    "A balanced diet, exercise and weight loss are the basis. If that is "
                    "not enough, medicines such as statins lower LDL cholesterol and the "
                    "risk of heart attack and stroke."
                ),
                "red_flags": (
                    "Pressure or pain in the chest, sudden paralysis or speech problems "
                    "can be consequences of narrowed vessels – call the emergency number "
                    "144 (Austria) at once. Very high triglycerides can trigger "
                    "inflammation of the pancreas."
                ),
            },
            "keywords_en": [
                "Cholesterol",
                "Blood fats",
                "LDL",
                "Triglycerides",
                "Statins",
                "Cardiovascular risk",
            ],
        },
    },
)
