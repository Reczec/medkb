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
