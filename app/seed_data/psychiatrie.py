from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Depressive Episode",
        "doc_type": "Diagnose",
        "expected_category": "Psychiatrie",
        "term_en": "Depressive disorder",
        "icd11_code": "6A70",
        "medications": ["sertraline", "escitalopram"],
        "sections": {
            "definition": (
                "Eine depressive Episode ist eine psychische Erkrankung mit gedrückter Stimmung, "
                "Antriebslosigkeit und Verlust von Interesse oder Freude über mindestens zwei "
                "Wochen."
            ),
            "symptoms": (
                "Häufig kommen Schlafstörungen, Konzentrationsprobleme, Appetitveränderungen, "
                "Schuldgefühle und Hoffnungslosigkeit hinzu."
            ),
            "causes": (
                "Es wirken Veranlagung, belastende Lebensereignisse, chronischer Stress und "
                "körperliche Erkrankungen zusammen."
            ),
            "diagnostics": (
                "Die Diagnose stellen Ärztinnen, Psychiater oder Psychotherapeutinnen im "
                "Gespräch, oft unterstützt durch Fragebögen; körperliche Ursachen werden "
                "ausgeschlossen."
            ),
            "therapy": (
                "Depressionen sind gut behandelbar, etwa durch Psychotherapie und "
                "gegebenenfalls Antidepressiva. Bewegung und eine feste Tagesstruktur "
                "unterstützen."
            ),
            "red_flags": (
                "Bei Suizidgedanken ist sofortige Hilfe wichtig: in Österreich die "
                "Telefonseelsorge unter 142, im akuten Notfall Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("depression", "Depression"),
            who("depression", "Depression"),
        ],
    },
    {
        "title": "Generalisierte Angststörung",
        "doc_type": "Diagnose",
        "expected_category": "Psychiatrie",
        "term_en": "Generalized anxiety disorder",
        "icd11_code": "6B00",
        "medications": ["escitalopram"],
        "sections": {
            "definition": (
                "Bei der generalisierten Angststörung bestehen über Monate anhaltende, "
                "übermäßige Sorgen und Ängste, die sich kaum kontrollieren lassen."
            ),
            "symptoms": (
                "Typisch sind ständige Anspannung, Nervosität, Schlafstörungen, "
                "Muskelverspannungen, Konzentrationsprobleme und körperliche Beschwerden wie "
                "Herzklopfen."
            ),
            "causes": (
                "Veranlagung, belastende Erfahrungen und erlernte Denkmuster tragen zur "
                "Entstehung der Angststörung bei."
            ),
            "diagnostics": (
                "Die Diagnose erfolgt im psychiatrischen oder psychotherapeutischen Gespräch; "
                "körperliche Ursachen wie eine Schilddrüsenüberfunktion werden ausgeschlossen."
            ),
            "therapy": (
                "Am wirksamsten ist kognitive Verhaltenstherapie, bei Bedarf ergänzt durch "
                "Medikamente. Entspannungsverfahren und Bewegung helfen zusätzlich."
            ),
            "red_flags": (
                "Brustschmerz mit Atemnot sollte nicht vorschnell als Panik gedeutet werden – "
                "im Zweifel Notruf 144. Bei Suizidgedanken sofort Hilfe holen."
            ),
        },
        "further_reading": [
            medlineplus("anxiety", "Anxiety"),
            who("anxiety-disorders", "Anxiety disorders"),
        ],
    },
    {
        "title": "Burnout",
        "doc_type": "Beschreibung",
        "expected_category": "Psychiatrie",
        "term_en": "Burnout",
        "icd11_code": "QD85",
        "sections": {
            "definition": (
                "Burnout beschreibt einen Zustand der Erschöpfung infolge chronischer, nicht "
                "bewältigter Belastung am Arbeitsplatz. In der ICD-11 ist es keine "
                "psychische Erkrankung, sondern ein Faktor, der die Gesundheit beeinflusst."
            ),
            "symptoms": (
                "Typisch sind emotionale Erschöpfung, zunehmende Distanz zur Arbeit, "
                "Zynismus und das Gefühl verminderter Leistungsfähigkeit."
            ),
            "diagnostics": (
                "Wichtig ist die Abgrenzung zur Depression und zu körperlichen Ursachen der "
                "Erschöpfung durch ärztliche und psychiatrische Abklärung."
            ),
            "therapy": (
                "Hilfreich sind Entlastung, Veränderungen der Arbeitssituation, "
                "Stressbewältigung und bei Bedarf Psychotherapie."
            ),
            "red_flags": (
                "Hoffnungslosigkeit oder Suizidgedanken sind Zeichen einer ernsten Krise – "
                "Telefonseelsorge 142, im Notfall Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("stress", "Stress"),
            who("mental-health-at-work", "Mental health at work"),
        ],
    },
]
