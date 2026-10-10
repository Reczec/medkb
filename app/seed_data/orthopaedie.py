from app.seed_data.links import medlineplus

ENTRIES = [
    {
        "title": "Rückenschmerzen",
        "doc_type": "Symptom",
        "expected_category": "Orthopädie",
        "term_en": "Low back pain",
        "icd11_code": "ME84.2",
        "medications": ["ibuprofen"],
        "sections": {
            "definition": (
                "Rückenschmerzen gehören zu den häufigsten Beschwerden. Meist sind sie "
                "unspezifisch, also ohne klar erkennbare strukturelle Ursache."
            ),
            "symptoms": (
                "Schmerzen im unteren Rücken, Verspannungen der Muskulatur und "
                "eingeschränkte Beweglichkeit, teils mit Ausstrahlung ins Gesäß."
            ),
            "causes": (
                "Bewegungsmangel, schwache Rumpfmuskulatur, einseitige Belastung und Stress "
                "tragen bei; selten stecken ein Bandscheibenvorfall oder andere "
                "Erkrankungen der Wirbelsäule dahinter."
            ),
            "diagnostics": (
                "Anamnese und körperliche Untersuchung genügen meist. Bildgebung ist nur bei "
                "Warnzeichen oder anhaltenden Beschwerden nötig."
            ),
            "therapy": (
                "Bewegung und das Beibehalten alltäglicher Aktivitäten fördern die Heilung; "
                "Bettruhe schadet eher. Wärme und kurzfristig Schmerzmittel helfen."
            ),
            "red_flags": (
                "Lähmungen, Taubheit im Genitalbereich, Probleme beim Wasserlassen oder Fieber "
                "erfordern eine sofortige ärztliche Abklärung."
            ),
        },
        "further_reading": [medlineplus("backpain", "Back Pain")],
    },
    {
        "title": "Kniearthrose (Gonarthrose)",
        "doc_type": "Diagnose",
        "expected_category": "Orthopädie",
        "term_en": "Knee osteoarthritis",
        "icd11_code": "FA01",
        "medications": ["ibuprofen", "diclofenac"],
        "sections": {
            "definition": (
                "Bei der Kniearthrose nutzt sich der Gelenkknorpel im Kniegelenk fortschreitend ab."
            ),
            "symptoms": (
                "Typisch sind Anlaufschmerzen, Steifigkeit am Morgen, Schmerzen bei Belastung "
                "und später Schwellungen des Gelenks."
            ),
            "causes": (
                "Alter, Übergewicht, frühere Verletzungen wie Meniskus- oder "
                "Kreuzbandschäden und Fehlstellungen begünstigen die Arthrose."
            ),
            "diagnostics": (
                "Die orthopädische Untersuchung und ein Röntgenbild zeigen den verschmälerten "
                "Gelenkspalt."
            ),
            "therapy": (
                "Gewichtsreduktion, gezielte Bewegungstherapie und Kräftigung der "
                "Oberschenkelmuskulatur lindern die Beschwerden. Bei fortgeschrittenem Verlauf "
                "kommt ein Gelenkersatz in Betracht."
            ),
            "red_flags": (
                "Ein plötzlich heißes, stark geschwollenes Knie mit Fieber kann eine "
                "Gelenkinfektion sein und muss sofort behandelt werden."
            ),
        },
        "further_reading": [medlineplus("osteoarthritis", "Osteoarthritis")],
    },
    {
        "title": "Karpaltunnelsyndrom",
        "doc_type": "Diagnose",
        "expected_category": "Orthopädie",
        "term_en": "Carpal tunnel syndrome",
        "icd11_code": "8C10.0",
        "sections": {
            "definition": (
                "Beim Karpaltunnelsyndrom wird der Mittelnerv im Karpaltunnel am Handgelenk "
                "eingeengt."
            ),
            "symptoms": (
                "Typisch sind Kribbeln und Taubheit in Daumen, Zeige- und Mittelfinger, "
                "besonders nachts, später Schwäche beim Greifen."
            ),
            "causes": (
                "Häufige Ursachen sind Überlastung des Handgelenks, Schwangerschaft, "
                "Diabetes und rheumatische Erkrankungen."
            ),
            "diagnostics": (
                "Neben der klinischen Untersuchung bestätigt die Messung der "
                "Nervenleitgeschwindigkeit die Diagnose."
            ),
            "therapy": (
                "Eine nächtliche Handgelenkschiene hilft bei leichten Formen. Bei "
                "anhaltenden Beschwerden wird das Band über dem Karpaltunnel operativ "
                "durchtrennt."
            ),
            "red_flags": (
                "Zunehmende Schwäche oder Muskelschwund am Daumenballen sollten rasch "
                "behandelt werden, um bleibende Schäden zu vermeiden."
            ),
        },
        "further_reading": [medlineplus("carpaltunnelsyndrome", "Carpal Tunnel Syndrome")],
    },
]
