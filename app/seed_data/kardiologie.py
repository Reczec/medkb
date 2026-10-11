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
