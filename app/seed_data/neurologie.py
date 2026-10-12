from app.seed_data.english import with_english
from app.seed_data.links import gesundheit_gv, medlineplus, who

ENTRIES = [
    {
        "title": "Migräne",
        "doc_type": "Diagnose",
        "expected_category": "Neurologie",
        "term_en": "Migraine",
        "icd11_code": "8A80",
        "medications": ["sumatriptan", "ibuprofen"],
        "sections": {
            "definition": (
                "Migräne ist eine anfallsartige Kopfschmerzerkrankung, bei der wiederholt "
                "starke, meist einseitige und pulsierende Kopfschmerzen auftreten."
            ),
            "symptoms": (
                "Begleitend treten oft Übelkeit sowie Licht- und Lärmempfindlichkeit auf. Bei "
                "manchen kündigt eine Aura mit Sehstörungen den Anfall an. Unbehandelt dauert "
                "ein Anfall mehrere Stunden bis drei Tage."
            ),
            "causes": (
                "Die Veranlagung ist häufig familiär. Auslöser sind individuell verschieden, "
                "etwa Stress, Schlafmangel, hormonelle Schwankungen oder ausgelassene "
                "Mahlzeiten."
            ),
            "diagnostics": (
                "Die Diagnose beruht auf der typischen Krankengeschichte und einer "
                "neurologischen Untersuchung. Ein Kopfschmerzkalender hilft, Muster und "
                "Auslöser zu erkennen."
            ),
            "therapy": (
                "Im Anfall helfen Schmerzmittel oder Triptane, Ruhe und ein abgedunkelter "
                "Raum. Bei häufigen Anfällen kommt eine vorbeugende Behandlung in Frage."
            ),
            "red_flags": (
                "Ein plötzlicher, nie zuvor erlebter heftigster Kopfschmerz, Lähmungen oder "
                "Sprachstörungen sind keine typische Migräne – sofort Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("migraine", "Migraine"),
            who("headache-disorders", "Headache disorders"),
        ],
    },
    {
        "title": "Schlaganfall – Warnzeichen",
        "doc_type": "Diagnose",
        "expected_category": "Neurologie",
        "term_en": "Stroke",
        "icd11_code": "8B20",
        "medications": ["aspirin"],
        "sections": {
            "definition": (
                "Ein Schlaganfall entsteht durch eine plötzliche Durchblutungsstörung oder "
                "eine Blutung im Gehirn, wodurch Nervenzellen geschädigt werden."
            ),
            "symptoms": (
                "Warnzeichen sind plötzliche Lähmungen oder Taubheitsgefühle einer "
                "Körperseite, ein hängender Mundwinkel, Sprachstörungen, Sehstörungen und "
                "starker Schwindel."
            ),
            "causes": (
                "Meist verschließt ein Blutgerinnsel ein Hirngefäß. Risikofaktoren sind "
                "Bluthochdruck, Vorhofflimmern, Diabetes, Rauchen und erhöhte Blutfette."
            ),
            "diagnostics": (
                "Im Krankenhaus klärt eine Bildgebung des Gehirns (CT oder MRT) rasch, ob ein "
                "Gefäßverschluss oder eine Blutung vorliegt."
            ),
            "therapy": (
                "Ein Gefäßverschluss kann in den ersten Stunden medikamentös aufgelöst oder "
                "mit einem Katheter entfernt werden. Danach folgen Rehabilitation und die "
                "Behandlung der Risikofaktoren."
            ),
            "red_flags": (
                "Jede Minute zählt: Bei Verdacht auf Schlaganfall sofort Notruf 144 wählen, "
                "auch wenn die Beschwerden wieder verschwinden."
            ),
        },
        "further_reading": [
            gesundheit_gv("gehirn-nerven/schlaganfall", "Schlaganfall"),
            medlineplus("stroke", "Stroke"),
            who("stroke", "Stroke"),
        ],
    },
    {
        "title": "Anamnese bei Kopfschmerzen",
        "doc_type": "Anamnese",
        "expected_category": "Neurologie",
        "term_en": "Headache",
        "sections": {
            "definition": (
                "Die Anamnese ist bei Kopfschmerzen das wichtigste diagnostische Werkzeug: Die "
                "meisten Kopfschmerzformen lassen sich anhand der Schilderung einordnen."
            ),
            "diagnostics": (
                "Erfragt werden Beginn, Dauer, Häufigkeit, Lokalisation und Charakter der "
                "Kopfschmerzen, Begleitsymptome wie Übelkeit oder Sehstörungen, auslösende "
                "Faktoren, Medikamenteneinnahme, frühere Erkrankungen und familiäre Häufung."
            ),
            "red_flags": (
                "Ein plötzlich einsetzender, nie zuvor erlebter Vernichtungskopfschmerz, "
                "Fieber mit Nackensteifigkeit oder neue neurologische Ausfälle erfordern eine "
                "sofortige Abklärung – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("headache", "Headache")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Migräne": {
            "title_en": "Migraine",
            "sections_en": {
                "definition": (
                    "Migraine is an attack-like headache disorder in which severe, usually "
                    "one-sided and throbbing headaches occur repeatedly."
                ),
                "symptoms": (
                    "Nausea and sensitivity to light and noise often accompany the headache. "
                    "Some people notice an aura with visual disturbances before the attack. "
                    "Untreated, an attack lasts several hours up to three days."
                ),
                "causes": (
                    "The tendency often runs in families. Triggers differ from person to "
                    "person, for example stress, lack of sleep, hormonal changes or skipped "
                    "meals."
                ),
                "diagnostics": (
                    "The diagnosis is based on the typical history and a neurological "
                    "examination. A headache diary helps to recognise patterns and triggers."
                ),
                "therapy": (
                    "During an attack, pain relievers or triptans, rest and a darkened room "
                    "help. For frequent attacks, preventive treatment can be considered."
                ),
                "red_flags": (
                    "A sudden, never-before-experienced worst headache, paralysis or speech "
                    "problems are not typical migraine – call the emergency number 144 "
                    "(Austria) at once."
                ),
            },
            "keywords_en": [
                "Migraine",
                "Headache",
                "Aura",
                "Nausea",
                "Triptans",
                "Light sensitivity",
            ],
        },
        "Schlaganfall – Warnzeichen": {
            "title_en": "Stroke – warning signs",
            "sections_en": {
                "definition": (
                    "A stroke is caused by a sudden disturbance of blood flow or a bleed in "
                    "the brain, which damages nerve cells."
                ),
                "symptoms": (
                    "Warning signs are sudden paralysis or numbness on one side of the body, "
                    "a drooping corner of the mouth, speech problems, vision problems and "
                    "severe dizziness."
                ),
                "causes": (
                    "Usually a blood clot blocks a vessel in the brain. Risk factors are high "
                    "blood pressure, atrial fibrillation, diabetes, smoking and high blood "
                    "fats."
                ),
                "diagnostics": (
                    "In hospital, brain imaging (CT or MRI) quickly clarifies whether a "
                    "vessel is blocked or there is a bleed."
                ),
                "therapy": (
                    "A vessel blockage can be dissolved with medicines or removed with a "
                    "catheter in the first hours. Rehabilitation and treatment of the risk "
                    "factors follow."
                ),
                "red_flags": (
                    "Every minute counts: if a stroke is suspected, call the emergency number "
                    "144 (Austria) at once, even if the symptoms go away again."
                ),
            },
            "keywords_en": [
                "Stroke",
                "Paralysis",
                "Speech problems",
                "Emergency",
                "Brain",
                "Blood clot",
            ],
        },
        "Anamnese bei Kopfschmerzen": {
            "title_en": "Medical history for headaches",
            "sections_en": {
                "definition": (
                    "For headaches, the medical history is the most important diagnostic "
                    "tool: most types of headache can be classified from the description."
                ),
                "diagnostics": (
                    "The questions cover onset, duration, frequency, location and character "
                    "of the headache, accompanying symptoms such as nausea or visual "
                    "disturbances, triggering factors, medication, past illnesses and family "
                    "history."
                ),
                "red_flags": (
                    "A sudden, never-before-experienced worst headache, fever with a stiff "
                    "neck or new neurological deficits require immediate assessment – call "
                    "the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Headache",
                "Medical history",
                "Duration",
                "Triggers",
                "Nausea",
                "Warning signs",
            ],
        },
    },
)
