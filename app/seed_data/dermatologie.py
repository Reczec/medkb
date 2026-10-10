from app.seed_data.links import gesundheit_gv, medlineplus

ENTRIES = [
    {
        "title": "Neurodermitis (atopisches Ekzem)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "term_en": "Atopic dermatitis",
        "icd11_code": "EA80",
        "medications": ["hydrocortisone", "tacrolimus"],
        "sections": {
            "definition": (
                "Die Neurodermitis ist eine chronisch-entzündliche Hauterkrankung, die in "
                "Schüben verläuft und häufig im Kindesalter beginnt."
            ),
            "symptoms": (
                "Typisch sind starker Juckreiz und trockene, gerötete, teils nässende "
                "Hautstellen, bei Erwachsenen oft in Ellenbeugen und Kniekehlen."
            ),
            "causes": (
                "Eine gestörte Hautbarriere und ein überempfindliches Immunsystem wirken "
                "zusammen. Auslöser für Schübe sind etwa Stress, Schwitzen, Wolle oder "
                "Infekte."
            ),
            "diagnostics": (
                "Der Hautarzt stellt die Diagnose anhand des Hautbilds und der "
                "Krankengeschichte; Allergietests klären mögliche Auslöser."
            ),
            "therapy": (
                "Basis ist konsequentes Eincremen mit rückfettender Pflege. Im Schub helfen "
                "entzündungshemmende Cremes, bei schweren Formen moderne Systemtherapien."
            ),
            "red_flags": (
                "Plötzlich auftretende schmerzhafte Bläschen und Fieber bei Neurodermitis "
                "können eine gefährliche Herpes-Infektion der Haut sein – rasch zum Arzt."
            ),
        },
        "further_reading": [
            gesundheit_gv("haut-haare-naegel/neurodermitis", "Neurodermitis"),
            medlineplus("eczema", "Eczema"),
        ],
    },
    {
        "title": "Schuppenflechte (Psoriasis)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "term_en": "Psoriasis",
        "icd11_code": "EA90",
        "medications": ["calcipotriene", "methotrexate"],
        "sections": {
            "definition": (
                "Die Psoriasis ist eine chronisch-entzündliche Erkrankung, bei der sich die "
                "Haut stark beschleunigt erneuert. Sie ist nicht ansteckend."
            ),
            "symptoms": (
                "Typisch sind scharf begrenzte, gerötete Herde mit silbrigen Schuppen, oft an "
                "Ellenbogen, Knien und Kopfhaut. Auch Nägel und Gelenke können beteiligt sein."
            ),
            "causes": (
                "Eine erbliche Veranlagung und das Immunsystem spielen die Hauptrolle; Stress, "
                "Infekte und Verletzungen der Haut können Schübe auslösen."
            ),
            "diagnostics": (
                "Die Diagnose erfolgt meist anhand des typischen Hautbilds durch den Hautarzt."
            ),
            "therapy": (
                "Je nach Schwere kommen Cremes, Lichttherapie oder innerliche Medikamente und "
                "Biologika zum Einsatz."
            ),
            "red_flags": (
                "Großflächig gerötete Haut am ganzen Körper mit Fieber oder Schüttelfrost ist "
                "ein Notfall und muss sofort behandelt werden."
            ),
        },
        "further_reading": [medlineplus("psoriasis", "Psoriasis")],
    },
    {
        "title": "Gürtelrose (Herpes zoster)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "term_en": "Herpes zoster",
        "icd11_code": "1E91",
        "medications": ["valacyclovir", "acyclovir"],
        "sections": {
            "definition": (
                "Die Gürtelrose ist eine Reaktivierung des Windpockenvirus, das nach einer "
                "Windpockenerkrankung in den Nervenknoten verbleibt."
            ),
            "symptoms": (
                "Nach brennenden Schmerzen tritt ein gürtelförmiger, einseitiger "
                "Hautausschlag mit Bläschen auf, meist am Rumpf."
            ),
            "causes": (
                "Ein nachlassendes Immunsystem durch Alter, Stress oder Erkrankungen lässt das "
                "ruhende Virus wieder aktiv werden."
            ),
            "diagnostics": (
                "Das typische einseitige Hautbild genügt meist für die Diagnose beim Hautarzt "
                "oder Hausarzt."
            ),
            "therapy": (
                "Virushemmende Medikamente wirken am besten in den ersten Tagen. Eine gute "
                "Schmerzbehandlung beugt anhaltenden Nervenschmerzen vor; für Ältere gibt es "
                "eine Impfung."
            ),
            "red_flags": (
                "Ein Ausschlag im Gesicht, besonders nahe dem Auge, muss am selben Tag "
                "ärztlich behandelt werden."
            ),
        },
        "further_reading": [medlineplus("shingles", "Shingles")],
    },
]
