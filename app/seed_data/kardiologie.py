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
