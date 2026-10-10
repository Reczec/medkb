from app.seed_data.links import medlineplus

ENTRIES = [
    {
        "title": "Endometriose",
        "doc_type": "Diagnose",
        "expected_category": "Gynäkologie",
        "term_en": "Endometriosis",
        "icd11_code": "GA10",
        "medications": ["ibuprofen"],
        "sections": {
            "definition": (
                "Bei der Endometriose wächst Gewebe, das der Gebärmutterschleimhaut ähnelt, "
                "außerhalb der Gebärmutter, etwa an Eierstöcken oder Bauchfell."
            ),
            "symptoms": (
                "Leitsymptom sind starke Regelschmerzen. Hinzu kommen Unterbauchschmerzen, "
                "Schmerzen beim Geschlechtsverkehr und mitunter unerfüllter Kinderwunsch."
            ),
            "causes": (
                "Die genaue Ursache ist unklar. Diskutiert werden rückfließendes "
                "Menstruationsblut, hormonelle und immunologische Faktoren."
            ),
            "diagnostics": (
                "Gynäkologische Untersuchung und Ultraschall geben Hinweise; gesichert wird "
                "die Diagnose oft erst durch eine Bauchspiegelung."
            ),
            "therapy": (
                "Schmerzmittel, hormonelle Behandlung und die operative Entfernung der Herde "
                "lindern die Beschwerden. Die Behandlung richtet sich nach Beschwerden und "
                "Kinderwunsch."
            ),
            "red_flags": (
                "Plötzliche, sehr starke Unterbauchschmerzen mit Kreislaufproblemen oder "
                "Fieber erfordern eine sofortige Abklärung – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("endometriosis", "Endometriosis")],
    },
    {
        "title": "Wechseljahre (Klimakterium)",
        "doc_type": "Beschreibung",
        "expected_category": "Gynäkologie",
        "term_en": "Menopause",
        "sections": {
            "definition": (
                "Die Wechseljahre sind die natürliche Übergangsphase, in der die Eierstöcke "
                "ihre Hormonbildung einstellen. Die Menopause ist die letzte Regelblutung, "
                "meist um das 50. Lebensjahr."
            ),
            "symptoms": (
                "Häufig sind Hitzewallungen, Schweißausbrüche, Schlafstörungen, "
                "Stimmungsschwankungen und Scheidentrockenheit."
            ),
            "therapy": (
                "Bewegung, ausgewogene Ernährung und Entspannung helfen vielen Frauen. Bei "
                "starken Beschwerden kann nach Beratung eine Hormonbehandlung sinnvoll sein."
            ),
            "red_flags": (
                "Blutungen nach der Menopause sind nicht normal und sollten frauenärztlich "
                "abgeklärt werden."
            ),
        },
        "further_reading": [medlineplus("menopause", "Menopause")],
    },
    {
        "title": "Polyzystisches Ovarsyndrom (PCOS)",
        "doc_type": "Diagnose",
        "expected_category": "Gynäkologie",
        "term_en": "Polycystic ovary syndrome",
        "icd11_code": "5A80.1",
        "medications": ["metformin"],
        "sections": {
            "definition": (
                "Das polyzystische Ovarsyndrom ist eine häufige hormonelle Störung bei "
                "Frauen im gebärfähigen Alter, bei der vermehrt männliche Hormone gebildet "
                "werden."
            ),
            "symptoms": (
                "Typisch sind ein unregelmäßiger Zyklus oder ausbleibende Regelblutung, "
                "vermehrte Körperbehaarung, Akne und Schwierigkeiten, schwanger zu werden."
            ),
            "causes": (
                "Veranlagung und eine verminderte Insulinwirkung spielen eine Rolle; "
                "Übergewicht verstärkt die Beschwerden."
            ),
            "diagnostics": (
                "Die Diagnose stützt sich auf Zyklusstörungen, Hormonwerte im Blut und den "
                "Ultraschall der Eierstöcke."
            ),
            "therapy": (
                "Gewichtsreduktion und Bewegung verbessern oft Zyklus und Stoffwechsel. Je "
                "nach Ziel helfen hormonelle Verhütungsmittel oder eine "
                "Kinderwunschbehandlung."
            ),
            "red_flags": (
                "Plötzliche starke Unterbauchschmerzen können auf eine geplatzte oder "
                "gedrehte Zyste hinweisen und müssen sofort abgeklärt werden."
            ),
        },
        "further_reading": [medlineplus("polycysticovarysyndrome", "Polycystic Ovary Syndrome")],
    },
]
