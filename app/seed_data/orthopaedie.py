from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Rückenschmerzen": {
            "title_en": "Back pain",
            "sections_en": {
                "definition": (
                    "Back pain is one of the most common complaints. It is usually "
                    "non-specific, meaning without a clearly recognisable structural cause."
                ),
                "symptoms": (
                    "Pain in the lower back, tense muscles and restricted movement, sometimes "
                    "radiating into the buttocks."
                ),
                "causes": (
                    "Lack of exercise, weak trunk muscles, one-sided strain and stress "
                    "contribute; a slipped disc or other spinal disease is rarely behind it."
                ),
                "diagnostics": (
                    "The medical history and a physical examination are usually enough. "
                    "Imaging is needed only for warning signs or persistent symptoms."
                ),
                "therapy": (
                    "Staying active and keeping up everyday activities promote healing; bed "
                    "rest does more harm than good. Heat and, for a short time, pain "
                    "relievers help."
                ),
                "red_flags": (
                    "Paralysis, numbness in the genital area, problems passing urine or fever "
                    "require immediate medical assessment."
                ),
            },
            "keywords_en": [
                "Back pain",
                "Spine",
                "Muscle tension",
                "Slipped disc",
                "Exercise",
                "Pain relievers",
            ],
        },
        "Kniearthrose (Gonarthrose)": {
            "title_en": "Knee osteoarthritis",
            "sections_en": {
                "definition": (
                    "In knee osteoarthritis, the joint cartilage in the knee wears away "
                    "progressively."
                ),
                "symptoms": (
                    "Typical are start-up pain, morning stiffness, pain on loading and, "
                    "later, swelling of the joint."
                ),
                "causes": (
                    "Age, overweight, earlier injuries such as meniscus or cruciate ligament "
                    "damage and malalignment promote osteoarthritis."
                ),
                "diagnostics": (
                    "The orthopaedic examination and an X-ray show the narrowed joint space."
                ),
                "therapy": (
                    "Weight loss, targeted exercise therapy and strengthening of the thigh "
                    "muscles ease the symptoms. In advanced cases a joint replacement comes "
                    "into consideration."
                ),
                "red_flags": (
                    "A suddenly hot, strongly swollen knee with fever can be a joint "
                    "infection and must be treated at once."
                ),
            },
            "keywords_en": [
                "Knee",
                "Osteoarthritis",
                "Cartilage",
                "Joint",
                "Exercise therapy",
                "Joint replacement",
            ],
        },
        "Karpaltunnelsyndrom": {
            "title_en": "Carpal tunnel syndrome",
            "sections_en": {
                "definition": (
                    "In carpal tunnel syndrome, the median nerve is squeezed in the carpal "
                    "tunnel at the wrist."
                ),
                "symptoms": (
                    "Typical are tingling and numbness in the thumb, index and middle finger, "
                    "especially at night, and later weakness when gripping."
                ),
                "causes": (
                    "Common causes are overuse of the wrist, pregnancy, diabetes and "
                    "rheumatic diseases."
                ),
                "diagnostics": (
                    "Besides the clinical examination, measuring the nerve conduction "
                    "velocity confirms the diagnosis."
                ),
                "therapy": (
                    "A night splint for the wrist helps in mild forms. For persistent "
                    "symptoms the ligament over the carpal tunnel is cut by surgery."
                ),
                "red_flags": (
                    "Increasing weakness or wasting of the ball of the thumb should be "
                    "treated promptly to avoid permanent damage."
                ),
            },
            "keywords_en": ["Carpal tunnel", "Median nerve", "Numbness", "Wrist", "Hand", "Splint"],
        },
    },
)
