from app.seed_data.links import medlineplus

ENTRIES = [
    {
        "title": "Sodbrennen und Reflux",
        "doc_type": "Symptom",
        "expected_category": "Gastroenterologie",
        "term_en": "Gastroesophageal reflux disease",
        "icd11_code": "DA22",
        "medications": ["omeprazole", "pantoprazole"],
        "sections": {
            "definition": (
                "Sodbrennen entsteht, wenn Magensäure in die Speiseröhre zurückfließt. Tritt es "
                "häufig auf, spricht man von einer Refluxkrankheit."
            ),
            "symptoms": (
                "Betroffene spüren ein Brennen hinter dem Brustbein, saures Aufstoßen und "
                "manchmal Reizhusten, oft nach üppigen Mahlzeiten oder im Liegen."
            ),
            "causes": (
                "Ein geschwächter Schließmuskel am Mageneingang, Übergewicht, fettes Essen, "
                "Alkohol, Rauchen und Stress begünstigen den Reflux."
            ),
            "diagnostics": (
                "Bei typischen Beschwerden genügt oft ein Therapieversuch. Eine "
                "Magenspiegelung klärt anhaltende Beschwerden und Warnzeichen ab."
            ),
            "therapy": (
                "Kleinere Mahlzeiten, kein spätes Essen und ein erhöhtes Kopfende helfen. "
                "Säurehemmer lindern die Beschwerden zuverlässig."
            ),
            "red_flags": (
                "Schluckbeschwerden, ungewollter Gewichtsverlust, Bluterbrechen oder schwarzer "
                "Stuhl müssen rasch abgeklärt werden. Brustschmerz kann auch vom Herzen "
                "kommen – im Zweifel Notruf 144."
            ),
        },
        "further_reading": [medlineplus("gerd", "GERD")],
    },
    {
        "title": "Reizdarmsyndrom",
        "doc_type": "Diagnose",
        "expected_category": "Gastroenterologie",
        "term_en": "Irritable bowel syndrome",
        "icd11_code": "DD91.0",
        "medications": ["loperamide"],
        "sections": {
            "definition": (
                "Das Reizdarmsyndrom ist eine häufige funktionelle Störung des Darms: Die "
                "Beschwerden sind real, ohne dass sich eine organische Ursache findet."
            ),
            "symptoms": (
                "Typisch sind wiederkehrende Bauchschmerzen, Blähungen und ein veränderter "
                "Stuhlgang mit Durchfall, Verstopfung oder beidem im Wechsel."
            ),
            "causes": (
                "Beteiligt sind eine empfindlichere Darmwahrnehmung, veränderte Darmbewegung, "
                "Stress und manchmal ein vorausgegangener Darminfekt."
            ),
            "diagnostics": (
                "Die Diagnose wird gestellt, wenn die typischen Beschwerden länger bestehen und "
                "andere Erkrankungen wie Zöliakie oder chronische Darmentzündungen "
                "ausgeschlossen sind."
            ),
            "therapy": (
                "Hilfreich sind eine angepasste Ernährung, Bewegung, Stressabbau und je nach "
                "Hauptbeschwerde gezielte Medikamente."
            ),
            "red_flags": (
                "Blut im Stuhl, Gewichtsverlust, nächtliche Beschwerden, Fieber oder ein "
                "Beginn nach dem 50. Lebensjahr passen nicht zum Reizdarm und gehören "
                "abgeklärt."
            ),
        },
        "further_reading": [medlineplus("irritablebowelsyndrome", "Irritable Bowel Syndrome")],
    },
    {
        "title": "Gallensteine (Cholelithiasis)",
        "doc_type": "Diagnose",
        "expected_category": "Gastroenterologie",
        "term_en": "Cholelithiasis",
        "icd11_code": "DC11",
        "medications": ["ursodiol"],
        "sections": {
            "definition": (
                "Gallensteine sind feste Ablagerungen in der Gallenblase oder den "
                "Gallenwegen. Viele Menschen tragen sie, ohne es zu bemerken."
            ),
            "symptoms": (
                "Wandert ein Stein, kommt es zu krampfartigen Schmerzen im rechten Oberbauch "
                "(Gallenkolik), oft nach fettem Essen, mit Übelkeit und Erbrechen."
            ),
            "causes": (
                "Risikofaktoren sind weibliches Geschlecht, Übergewicht, rascher "
                "Gewichtsverlust, höheres Alter und familiäre Veranlagung."
            ),
            "diagnostics": (
                "Ein Ultraschall des Bauchs zeigt die Steine zuverlässig. Blutwerte geben "
                "Hinweise auf eine Entzündung oder einen Gallenstau."
            ),
            "therapy": (
                "Steine ohne Beschwerden werden meist nicht behandelt. Nach Koliken wird die "
                "Gallenblase in der Regel minimal-invasiv entfernt."
            ),
            "red_flags": (
                "Fieber mit Oberbauchschmerzen, gelbe Haut oder Augen oder heftige "
                "anhaltende Schmerzen erfordern eine sofortige Abklärung."
            ),
        },
        "further_reading": [medlineplus("gallstones", "Gallstones")],
    },
]
