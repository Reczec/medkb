from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Asthma bronchiale",
        "doc_type": "Diagnose",
        "expected_category": "Pneumologie",
        "term_en": "Asthma",
        "icd11_code": "CA23",
        "medications": ["albuterol", "budesonide"],
        "sections": {
            "definition": (
                "Asthma bronchiale ist eine chronische Entzündung der Atemwege, bei der sich "
                "die Bronchien anfallsartig verengen."
            ),
            "symptoms": (
                "Typisch sind anfallsartige Atemnot, pfeifende Atmung (Giemen), "
                "Engegefühl in der Brust und Husten, besonders nachts oder bei Belastung."
            ),
            "causes": (
                "Allergien gegen Pollen, Hausstaubmilben oder Tierhaare, Atemwegsinfekte, "
                "kalte Luft, Rauch und körperliche Anstrengung können Anfälle auslösen."
            ),
            "diagnostics": (
                "Eine Lungenfunktionsprüfung (Spirometrie) zeigt die Verengung der "
                "Atemwege und ihre Besserung nach einem bronchienerweiternden Spray."
            ),
            "therapy": (
                "Inhalierbares Kortison wirkt der Entzündung entgegen, kurz wirksame "
                "Bronchienerweiterer helfen im Anfall. Auslöser sollten gemieden werden."
            ),
            "red_flags": (
                "Schwere Atemnot, Sprechen nur in kurzen Sätzen, bläuliche Lippen oder fehlende "
                "Besserung durch das Notfallspray: sofort Notruf 144."
            ),
        },
        "further_reading": [medlineplus("asthma", "Asthma"), who("asthma", "Asthma")],
    },
    {
        "title": "Chronisch obstruktive Lungenerkrankung (COPD)",
        "doc_type": "Diagnose",
        "expected_category": "Pneumologie",
        "term_en": "Chronic obstructive pulmonary disease",
        "icd11_code": "CA22",
        "medications": ["tiotropium"],
        "sections": {
            "definition": (
                "Die COPD ist eine fortschreitende Lungenerkrankung mit dauerhaft verengten "
                "Atemwegen und geschädigtem Lungengewebe."
            ),
            "symptoms": (
                "Leitsymptome sind Husten mit Auswurf und Atemnot, zunächst bei Belastung, "
                "später auch in Ruhe."
            ),
            "causes": (
                "Hauptursache ist langjähriges Rauchen; auch Feinstaub und Schadstoffe am "
                "Arbeitsplatz tragen bei."
            ),
            "diagnostics": (
                "Die Lungenfunktionsprüfung bestätigt die Verengung der Atemwege, die sich "
                "anders als beim Asthma nicht vollständig zurückbildet."
            ),
            "therapy": (
                "Am wichtigsten ist der Rauchstopp. Inhalierte Bronchienerweiterer, "
                "Lungensport und Impfungen gegen Grippe und Pneumokokken verbessern den "
                "Verlauf."
            ),
            "red_flags": (
                "Zunehmende Atemnot, Verwirrtheit oder bläuliche Lippen bei einer "
                "Verschlechterung erfordern sofort ärztliche Hilfe, bei Atemnot in Ruhe "
                "Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("copd", "COPD"),
            who(
                "chronic-obstructive-pulmonary-disease-(copd)",
                "Chronic obstructive pulmonary disease",
            ),
        ],
    },
    {
        "title": "Lungenentzündung (Pneumonie)",
        "doc_type": "Diagnose",
        "expected_category": "Pneumologie",
        "term_en": "Pneumonia",
        "icd11_code": "CA40",
        "medications": ["amoxicillin"],
        "sections": {
            "definition": (
                "Eine Lungenentzündung ist eine Entzündung des Lungengewebes, meist durch "
                "Bakterien oder Viren."
            ),
            "symptoms": (
                "Typisch sind Fieber, Husten mit Auswurf, Atemnot und Schmerzen beim Atmen. "
                "Ältere Menschen zeigen oft nur Schwäche oder Verwirrtheit."
            ),
            "causes": (
                "Häufigster bakterieller Erreger sind Pneumokokken. Ein höheres Alter, "
                "chronische Lungenerkrankungen und ein geschwächtes Immunsystem erhöhen das "
                "Risiko."
            ),
            "diagnostics": (
                "Abhören der Lunge, Röntgenbild und Blutwerte sichern die Diagnose. Die "
                "Sauerstoffsättigung zeigt den Schweregrad."
            ),
            "therapy": (
                "Bakterielle Lungenentzündungen werden mit Antibiotika behandelt. Schwere "
                "Verläufe brauchen eine Behandlung im Krankenhaus."
            ),
            "red_flags": (
                "Atemnot in Ruhe, Verwirrtheit, bläuliche Lippen oder sehr schneller Puls "
                "sind Alarmzeichen – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("pneumonia", "Pneumonia"), who("pneumonia", "Pneumonia")],
    },
]
