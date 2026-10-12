from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Neurodermitis (atopisches Ekzem)": {
            "title_en": "Atopic dermatitis (eczema)",
            "sections_en": {
                "definition": (
                    "Atopic dermatitis is a chronic inflammatory skin disease that runs in "
                    "flares and often begins in childhood."
                ),
                "symptoms": (
                    "Typical are severe itching and dry, reddened, sometimes weeping skin "
                    "patches, in adults often in the elbow creases and behind the knees."
                ),
                "causes": (
                    "A disturbed skin barrier and an overreactive immune system act together. "
                    "Triggers for flares are, for example, stress, sweating, wool or "
                    "infections."
                ),
                "diagnostics": (
                    "The skin doctor makes the diagnosis from the skin appearance and the "
                    "history; allergy tests clarify possible triggers."
                ),
                "therapy": (
                    "The basis is consistent moisturising with rich skin care. During a "
                    "flare, anti-inflammatory creams help; severe forms are treated with "
                    "modern systemic therapies."
                ),
                "red_flags": (
                    "Painful blisters and fever appearing suddenly in atopic dermatitis can "
                    "be a dangerous herpes infection of the skin – see a doctor quickly."
                ),
            },
            "keywords_en": [
                "Eczema",
                "Atopic dermatitis",
                "Itching",
                "Dry skin",
                "Flare",
                "Skin care",
            ],
        },
        "Schuppenflechte (Psoriasis)": {
            "title_en": "Psoriasis",
            "sections_en": {
                "definition": (
                    "Psoriasis is a chronic inflammatory disease in which the skin renews "
                    "itself much faster than normal. It is not contagious."
                ),
                "symptoms": (
                    "Typical are sharply defined, reddened patches with silvery scales, often "
                    "on the elbows, knees and scalp. Nails and joints can also be involved."
                ),
                "causes": (
                    "A hereditary predisposition and the immune system play the main role; "
                    "stress, infections and skin injuries can trigger flares."
                ),
                "diagnostics": (
                    "The diagnosis is usually made from the typical skin appearance by the "
                    "skin doctor."
                ),
                "therapy": (
                    "Depending on severity, creams, light therapy or internal medicines and "
                    "biologics are used."
                ),
                "red_flags": (
                    "Widespread reddened skin over the whole body with fever or shivering is "
                    "an emergency and must be treated at once."
                ),
            },
            "keywords_en": [
                "Psoriasis",
                "Scales",
                "Skin",
                "Light therapy",
                "Joints",
                "Immune system",
            ],
        },
        "Gürtelrose (Herpes zoster)": {
            "title_en": "Shingles (herpes zoster)",
            "sections_en": {
                "definition": (
                    "Shingles is a reactivation of the chickenpox virus, which stays in the "
                    "nerve ganglia after a chickenpox infection."
                ),
                "symptoms": (
                    "After burning pain, a belt-shaped, one-sided rash with blisters appears, "
                    "usually on the trunk."
                ),
                "causes": (
                    "A declining immune system due to age, stress or illness lets the dormant "
                    "virus become active again."
                ),
                "diagnostics": (
                    "The typical one-sided skin picture is usually enough for the diagnosis "
                    "by the skin doctor or family doctor."
                ),
                "therapy": (
                    "Antiviral medicines work best in the first days. Good pain treatment "
                    "prevents lasting nerve pain; a vaccination is available for older "
                    "people."
                ),
                "red_flags": (
                    "A rash on the face, especially near the eye, must be treated by a doctor "
                    "the same day."
                ),
            },
            "keywords_en": [
                "Shingles",
                "Herpes zoster",
                "Blisters",
                "Nerve pain",
                "Antiviral",
                "Vaccination",
            ],
        },
    },
)
