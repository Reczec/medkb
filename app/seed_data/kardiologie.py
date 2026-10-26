from app.seed_data.english import with_english
from app.seed_data.links import gesundheit_gv, medlineplus, who

ENTRIES = [
    {
        "title": "Bluthochdruck (arterielle Hypertonie)",
        "doc_type": "Diagnose",
        "expected_category": "Kardiologie",
        "term_en": "Hypertension",
        "icd11_code": "BA00",
        "medications": ["ramipril", "amlodipine", "hydrochlorothiazide"],
        "sections": {
            "definition": (
                "Bluthochdruck ist ein dauerhaft erhöhter Blutdruck in den Arterien, ab "
                "Werten von 140/90 mmHg in wiederholten Messungen."
            ),
            "symptoms": (
                "Bluthochdruck bleibt oft lange unbemerkt. Manche spüren Kopfschmerzen, "
                "Schwindel oder Herzklopfen."
            ),
            "causes": (
                "Meist wirken Veranlagung, Übergewicht, Bewegungsmangel, salzreiche Ernährung, "
                "Alkohol und Stress zusammen. Seltener steckt eine andere Erkrankung dahinter."
            ),
            "diagnostics": (
                "Die Diagnose erfolgt durch wiederholte Blutdruckmessungen, ergänzt durch "
                "Langzeitmessung, ein EKG und Laboruntersuchungen."
            ),
            "therapy": (
                "Lebensstiländerungen bilden die Basis; reichen sie nicht aus, senken "
                "Medikamente den Blutdruck. Unbehandelt steigt das Risiko für Herzinfarkt, "
                "Schlaganfall und Nierenschäden."
            ),
            "red_flags": (
                "Sehr hohe Werte mit Brustschmerz, Atemnot, Sehstörungen oder Lähmungen sind "
                "ein Notfall – Notruf 144."
            ),
        },
        "further_reading": [
            gesundheit_gv("herz-kreislauf/bluthochdruck", "Bluthochdruck"),
            medlineplus("highbloodpressure", "High Blood Pressure"),
            who("hypertension", "Hypertension"),
        ],
    },
    {
        "title": "Vorhofflimmern",
        "doc_type": "Symptom",
        "expected_category": "Kardiologie",
        "term_en": "Atrial fibrillation",
        "icd11_code": "BC81.3",
        "medications": ["apixaban", "bisoprolol"],
        "sections": {
            "definition": (
                "Vorhofflimmern ist die häufigste anhaltende Herzrhythmusstörung: Die Vorhöfe "
                "des Herzens schlagen ungeordnet, der Puls wird unregelmäßig."
            ),
            "symptoms": (
                "Betroffene spüren Herzrasen, Herzstolpern, Atemnot oder eine verminderte "
                "Belastbarkeit; manche bemerken keine Beschwerden."
            ),
            "causes": (
                "Häufige Ursachen sind Bluthochdruck, Herzschwäche, Herzklappenerkrankungen, "
                "eine Schilddrüsenüberfunktion und höheres Alter."
            ),
            "diagnostics": (
                "Ein EKG sichert die Diagnose; bei zeitweisem Vorhofflimmern hilft ein "
                "Langzeit-EKG. Ein Herzultraschall zeigt mögliche Ursachen."
            ),
            "therapy": (
                "Blutverdünnende Medikamente senken das Schlaganfallrisiko. Zusätzlich wird "
                "die Herzfrequenz kontrolliert oder der normale Rhythmus wiederhergestellt."
            ),
            "red_flags": (
                "Brustschmerzen, Ohnmacht, starke Atemnot oder Schlaganfall-Zeichen erfordern "
                "sofort den Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("atrialfibrillation", "Atrial Fibrillation"),
            who("cardiovascular-diseases-(cvds)", "Cardiovascular diseases"),
        ],
    },
    {
        "title": "Herzinsuffizienz (Herzschwäche)",
        "doc_type": "Diagnose",
        "expected_category": "Kardiologie",
        "term_en": "Heart failure",
        "icd11_code": "BD10",
        "medications": ["furosemide", "spironolactone"],
        "sections": {
            "definition": (
                "Bei einer Herzinsuffizienz pumpt das Herz nicht mehr genug Blut, um den "
                "Körper ausreichend zu versorgen."
            ),
            "symptoms": (
                "Typisch sind Atemnot bei Belastung oder im Liegen, rasche Ermüdung und "
                "Wassereinlagerungen in den Beinen."
            ),
            "causes": (
                "Häufigste Ursachen sind die koronare Herzkrankheit nach einem Herzinfarkt und "
                "langjähriger Bluthochdruck, seltener Herzklappenfehler oder "
                "Herzmuskelentzündungen."
            ),
            "diagnostics": (
                "Herzultraschall, EKG und ein Bluttest auf das Herzhormon BNP bestätigen die "
                "Diagnose und zeigen den Schweregrad."
            ),
            "therapy": (
                "Medikamente entlasten das Herz und verbessern die Prognose. Wichtig sind "
                "tägliches Wiegen, angepasste Trinkmenge und Bewegung nach ärztlicher "
                "Anleitung."
            ),
            "red_flags": (
                "Plötzliche schwere Atemnot, rasselnde Atmung oder Brustschmerzen sind ein "
                "Notfall – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("heartfailure", "Heart Failure")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Bluthochdruck (arterielle Hypertonie)": {
            "title_en": "High blood pressure (arterial hypertension)",
            "sections_en": {
                "definition": (
                    "High blood pressure is a persistently raised pressure in the arteries, "
                    "from values of 140/90 mmHg on repeated measurements."
                ),
                "symptoms": (
                    "High blood pressure often goes unnoticed for a long time. Some people "
                    "feel headaches, dizziness or palpitations."
                ),
                "causes": (
                    "Usually a predisposition, overweight, lack of exercise, a salty diet, "
                    "alcohol and stress act together. Less often another illness is behind "
                    "it."
                ),
                "diagnostics": (
                    "The diagnosis is made by repeated blood pressure measurements, "
                    "supplemented by long-term measurement, an ECG and laboratory tests."
                ),
                "therapy": (
                    "Lifestyle changes are the basis; if they are not enough, medicines lower "
                    "the blood pressure. Untreated, the risk of heart attack, stroke and "
                    "kidney damage rises."
                ),
                "red_flags": (
                    "Very high values with chest pain, shortness of breath, vision problems "
                    "or paralysis are an emergency – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Hypertension",
                "Blood pressure",
                "Heart attack",
                "Stroke",
                "ECG",
                "Lifestyle",
            ],
        },
        "Vorhofflimmern": {
            "title_en": "Atrial fibrillation",
            "sections_en": {
                "definition": (
                    "Atrial fibrillation is the most common persistent heart rhythm disorder: "
                    "the upper chambers of the heart beat in a disorganised way and the pulse "
                    "becomes irregular."
                ),
                "symptoms": (
                    "Affected people feel a racing heart, skipped beats, shortness of breath "
                    "or reduced exercise capacity; some notice no symptoms."
                ),
                "causes": (
                    "Common causes are high blood pressure, heart failure, heart valve "
                    "disease, an overactive thyroid and higher age."
                ),
                "diagnostics": (
                    "An ECG confirms the diagnosis; for intermittent atrial fibrillation a "
                    "long-term ECG helps. A heart ultrasound shows possible causes."
                ),
                "therapy": (
                    "Blood-thinning medicines lower the risk of stroke. In addition, the "
                    "heart rate is controlled or the normal rhythm is restored."
                ),
                "red_flags": (
                    "Chest pain, fainting, severe shortness of breath or signs of a stroke "
                    "require the emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Atrial fibrillation",
                "Heart rhythm",
                "Palpitations",
                "ECG",
                "Stroke risk",
                "Blood thinners",
            ],
        },
        "Herzinsuffizienz (Herzschwäche)": {
            "title_en": "Heart failure",
            "sections_en": {
                "definition": (
                    "With heart failure, the heart no longer pumps enough blood to supply the "
                    "body adequately."
                ),
                "symptoms": (
                    "Typical are shortness of breath on exertion or when lying down, quick "
                    "tiredness and fluid retention in the legs."
                ),
                "causes": (
                    "The most common causes are coronary heart disease after a heart attack "
                    "and long-standing high blood pressure, less often heart valve defects or "
                    "inflammation of the heart muscle."
                ),
                "diagnostics": (
                    "A heart ultrasound, an ECG and a blood test for the heart hormone BNP "
                    "confirm the diagnosis and show its severity."
                ),
                "therapy": (
                    "Medicines relieve the heart and improve the outlook. Daily weighing, an "
                    "adjusted fluid intake and exercise under medical guidance are important."
                ),
                "red_flags": (
                    "Sudden severe shortness of breath, rattling breathing or chest pain are "
                    "an emergency – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Heart failure",
                "Shortness of breath",
                "Fluid retention",
                "Heart ultrasound",
                "BNP",
                "Diuretics",
            ],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Koronare Herzkrankheit und Angina pectoris",
            "doc_type": "Diagnose",
            "expected_category": "Kardiologie",
            "term_en": "Coronary artery disease",
            "icd11_code": "BA40",
            "medications": ["aspirin", "atorvastatin", "nitroglycerin"],
            "sections": {
                "definition": (
                    "Bei der koronaren Herzkrankheit (KHK) sind die Herzkranzgefäße durch "
                    "Ablagerungen verengt, sodass der Herzmuskel zu wenig Blut und Sauerstoff "
                    "erhält. Die Angina pectoris ist das typische Beschwerdebild."
                ),
                "symptoms": (
                    "Bei Belastung treten Druck oder Enge in der Brust auf, die in Arm, Hals "
                    "oder Kiefer ausstrahlen können. In Ruhe klingen die Beschwerden meist "
                    "nach wenigen Minuten ab. Häufig kommen Atemnot und Leistungsschwäche dazu."
                ),
                "causes": (
                    "Ursache ist die Arteriosklerose. Risikofaktoren sind Rauchen, "
                    "Bluthochdruck, erhöhte Blutfette, Diabetes, Übergewicht, Bewegungsmangel "
                    "und familiäre Belastung."
                ),
                "diagnostics": (
                    "Die Kardiologin erhebt die Beschwerden, schreibt ein EKG, führt ein "
                    "Belastungs-EKG oder eine Herzultraschalluntersuchung durch. Eine "
                    "Herzkatheteruntersuchung zeigt die Engstellen direkt."
                ),
                "therapy": (
                    "Behandelt werden Risikofaktoren, außerdem helfen Medikamente wie "
                    "Cholesterinsenker, Gerinnungshemmer und Betablocker. Engstellen können "
                    "mit einem Stent geweitet oder durch eine Bypass-Operation umgangen "
                    "werden."
                ),
                "red_flags": (
                    "Brustschmerz, der länger als fünf Minuten dauert, in Ruhe auftritt oder "
                    "mit Atemnot, Schweißausbruch oder Übelkeit einhergeht, kann ein "
                    "Herzinfarkt sein – sofort Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("coronaryarterydisease", "Coronary artery disease"),
                who("cardiovascular-diseases-(cvds)", "Cardiovascular diseases"),
            ],
        },
        {
            "title": "Herzinfarkt",
            "doc_type": "Diagnose",
            "expected_category": "Kardiologie",
            "term_en": "Myocardial infarction",
            "icd11_code": "BA41",
            "medications": ["aspirin", "heparin"],
            "sections": {
                "definition": (
                    "Ein Herzinfarkt entsteht, wenn ein Herzkranzgefäß plötzlich verschlossen "
                    "wird und ein Teil des Herzmuskels nicht mehr durchblutet wird und "
                    "abzusterben beginnt."
                ),
                "symptoms": (
                    "Typisch sind starke, anhaltende Schmerzen oder ein Druckgefühl hinter "
                    "dem Brustbein, die in Arm, Schulter, Hals, Kiefer oder Oberbauch "
                    "ausstrahlen, begleitet von Angst, Kaltschweißigkeit und Übelkeit. Bei "
                    "Frauen sind Beschwerden oft weniger typisch."
                ),
                "causes": (
                    "Meist reißt eine Ablagerung in einem verengten Herzkranzgefäß auf, und "
                    "ein Blutgerinnsel verstopft das Gefäß. Risikofaktoren entsprechen denen "
                    "der koronaren Herzkrankheit."
                ),
                "diagnostics": (
                    "Im Rettungsdienst und im Krankenhaus werden EKG und Blutwerte (Troponin) "
                    "bestimmt. Eine Herzkatheteruntersuchung klärt, welches Gefäß betroffen "
                    "ist."
                ),
                "therapy": (
                    "Das verschlossene Gefäß wird so schnell wie möglich im Herzkatheterlabor "
                    "wieder eröffnet, meist mit einem Stent. Zusätzlich erhalten Betroffene "
                    "blutverdünnende Medikamente. Danach folgen Rehabilitation und eine "
                    "dauerhafte medikamentöse Behandlung."
                ),
                "red_flags": (
                    "Jede Minute zählt: Bei Verdacht auf Herzinfarkt sofort Notruf 144 "
                    "wählen, nicht selbst ins Krankenhaus fahren und bei Bewusstlosigkeit "
                    "ohne Atmung mit der Herzdruckmassage beginnen."
                ),
            },
            "further_reading": [medlineplus("heartattack", "Heart attack")],
        },
        {
            "title": "Tiefe Beinvenenthrombose",
            "doc_type": "Diagnose",
            "expected_category": "Kardiologie",
            "term_en": "Deep vein thrombosis",
            "icd11_code": "BD71",
            "medications": ["rivaroxaban", "heparin"],
            "sections": {
                "definition": (
                    "Bei einer tiefen Beinvenenthrombose bildet sich ein Blutgerinnsel in "
                    "einer tiefen Vene, meist im Unterschenkel oder Oberschenkel, und "
                    "behindert den Blutfluss."
                ),
                "symptoms": (
                    "Ein Bein ist plötzlich geschwollen, gespannt und schmerzt, oft mit "
                    "Wärme und bläulicher Verfärbung der Haut. Die Beschwerden betreffen "
                    "meist nur ein Bein."
                ),
                "causes": (
                    "Begünstigt wird sie durch lange Bettruhe oder lange Reisen, Operationen, "
                    "Verletzungen, Schwangerschaft, hormonelle Verhütung, Rauchen, "
                    "Übergewicht und eine erbliche Gerinnungsneigung."
                ),
                "diagnostics": (
                    "Die Ärztin schätzt anhand der Beschwerden das Risiko ein. Ein Bluttest "
                    "(D-Dimere) und eine Ultraschalluntersuchung der Venen sichern die "
                    "Diagnose."
                ),
                "therapy": (
                    "Gerinnungshemmende Medikamente verhindern, dass das Gerinnsel wächst "
                    "und sich ablöst. Sie werden meist mehrere Monate eingenommen. "
                    "Kompressionsstrümpfe und Bewegung unterstützen die Behandlung."
                ),
                "red_flags": (
                    "Plötzliche Atemnot, Brustschmerz beim Einatmen, Herzrasen oder Husten "
                    "mit Blut können auf eine Lungenembolie hinweisen – sofort Notruf 144."
                ),
            },
            "further_reading": [medlineplus("deepveinthrombosis", "Deep vein thrombosis")],
        },
    ],
    {
        "Koronare Herzkrankheit und Angina pectoris": {
            "title_en": "Coronary artery disease and angina pectoris",
            "sections_en": {
                "definition": (
                    "In coronary artery disease (CAD) the coronary arteries are narrowed "
                    "by deposits, so that the heart muscle gets too little blood and "
                    "oxygen. Angina pectoris is the typical symptom."
                ),
                "symptoms": (
                    "With exertion, pressure or tightness in the chest occurs and may "
                    "spread to the arm, neck or jaw. At rest the symptoms usually fade "
                    "after a few minutes. Breathlessness and reduced fitness are often "
                    "added."
                ),
                "causes": (
                    "The cause is arteriosclerosis. Risk factors are smoking, high blood "
                    "pressure, raised blood fats, diabetes, overweight, lack of exercise "
                    "and a family history."
                ),
                "diagnostics": (
                    "The cardiologist asks about the symptoms, records an ECG, and carries "
                    "out an exercise ECG or an ultrasound of the heart. A cardiac "
                    "catheter examination shows the narrowings directly."
                ),
                "therapy": (
                    "Risk factors are treated, and medicines such as cholesterol-lowering "
                    "drugs, blood thinners and beta blockers help. Narrowings can be "
                    "widened with a stent or bypassed with bypass surgery."
                ),
                "red_flags": (
                    "Chest pain that lasts longer than five minutes, occurs at rest or "
                    "comes with breathlessness, sweating or nausea can be a heart attack – "
                    "call the emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Coronary artery disease",
                "Angina pectoris",
                "Chest pain",
                "Arteriosclerosis",
                "Stent",
                "Cholesterol",
            ],
        },
        "Herzinfarkt": {
            "title_en": "Heart attack",
            "sections_en": {
                "definition": (
                    "A heart attack occurs when a coronary artery is suddenly blocked, so "
                    "that part of the heart muscle no longer gets blood and begins to be damaged."
                ),
                "symptoms": (
                    "Typical are severe, lasting pain or a feeling of pressure behind the "
                    "breastbone that spreads to the arm, shoulder, neck, jaw or upper "
                    "abdomen, with fear, cold sweat and nausea. In women the symptoms are "
                    "often less typical."
                ),
                "causes": (
                    "Usually a deposit in a narrowed coronary artery ruptures and a blood "
                    "clot blocks the vessel. The risk factors are the same as for coronary "
                    "artery disease."
                ),
                "diagnostics": (
                    "In the ambulance and in hospital an ECG and blood values (troponin) "
                    "are taken. A cardiac catheter examination shows which vessel is "
                    "affected."
                ),
                "therapy": (
                    "The blocked vessel is reopened as quickly as possible in the cardiac "
                    "catheter laboratory, usually with a stent. Blood-thinning medicines "
                    "are added. Rehabilitation and long-term treatment with medicines "
                    "follow."
                ),
                "red_flags": (
                    "Every minute counts: if a heart attack is suspected call the "
                    "emergency number 144 (Austria) at once, do not drive to hospital "
                    "yourself, and start chest compressions if the person is unconscious "
                    "and not breathing."
                ),
            },
            "keywords_en": [
                "Heart attack",
                "Myocardial infarction",
                "Chest pain",
                "Troponin",
                "Cardiac catheter",
                "Emergency",
            ],
        },
        "Tiefe Beinvenenthrombose": {
            "title_en": "Deep vein thrombosis",
            "sections_en": {
                "definition": (
                    "In deep vein thrombosis a blood clot forms in a deep vein, usually in "
                    "the lower or upper leg, and obstructs the blood flow."
                ),
                "symptoms": (
                    "One leg is suddenly swollen, tense and painful, often with warmth and "
                    "a bluish colour of the skin. The symptoms usually affect only one "
                    "leg."
                ),
                "causes": (
                    "It is favoured by long bed rest or long journeys, operations, "
                    "injuries, pregnancy, hormonal contraception, smoking, overweight and "
                    "an inherited tendency to clotting."
                ),
                "diagnostics": (
                    "The doctor estimates the risk from the symptoms. A blood test "
                    "(D-dimer) and an ultrasound examination of the veins confirm the "
                    "diagnosis."
                ),
                "therapy": (
                    "Anticoagulant medicines prevent the clot from growing and breaking "
                    "off. They are usually taken for several months. Compression "
                    "stockings and exercise support the treatment."
                ),
                "red_flags": (
                    "Sudden breathlessness, chest pain on breathing in, a racing heart or "
                    "coughing up blood can point to a pulmonary embolism – call the "
                    "emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Deep vein thrombosis",
                "Thrombosis",
                "Leg swelling",
                "Blood clot",
                "Anticoagulation",
                "Compression stockings",
            ],
        },
    },
)
