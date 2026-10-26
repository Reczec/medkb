from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

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


EXTRA = with_english(
    [
        {
            "title": "Osteoporose",
            "doc_type": "Diagnose",
            "expected_category": "Orthopädie",
            "term_en": "Osteoporosis",
            "icd11_code": "FB83.1",
            "medications": ["alendronate", "calcium", "vitamin D"],
            "sections": {
                "definition": (
                    "Bei der Osteoporose (Knochenschwund) nimmt die Knochenmasse ab und die "
                    "Knochenstruktur wird brüchig, sodass das Risiko für Knochenbrüche steigt."
                ),
                "symptoms": (
                    "Lange bleibt sie unbemerkt. Später treten Rückenschmerzen, eine "
                    "abnehmende Körpergröße, ein Rundrücken und Knochenbrüche nach geringer "
                    "Belastung auf, etwa an Wirbelsäule, Handgelenk oder Hüfte."
                ),
                "causes": (
                    "Häufig sind Frauen nach den Wechseljahren betroffen. Weitere "
                    "Faktoren sind höheres Alter, Bewegungsmangel, Rauchen, Alkohol, "
                    "Kortisontherapie, Vitamin-D-Mangel und familiäre Veranlagung."
                ),
                "diagnostics": (
                    "Eine Knochendichtemessung (DXA) sichert die Diagnose. Blutuntersuchungen "
                    "suchen nach Ursachen, etwa Mangel an Vitamin D oder Kalzium."
                ),
                "therapy": (
                    "Wichtig sind Bewegung und Krafttraining, kalziumreiche Ernährung, "
                    "Vitamin D und der Verzicht auf Rauchen. Medikamente wie Bisphosphonate "
                    "verlangsamen den Knochenabbau. Stürze sollten vermieden werden."
                ),
                "red_flags": (
                    "Plötzliche starke Rückenschmerzen nach einer kleinen Bewegung können "
                    "einen Wirbelbruch bedeuten. Nach einem Sturz mit starken Schmerzen in "
                    "der Hüfte, die kein Aufstehen erlauben, Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("osteoporosis", "Osteoporosis"),
                who("osteoporosis", "Osteoporosis"),
            ],
        },
        {
            "title": "Tennisellenbogen",
            "doc_type": "Diagnose",
            "expected_category": "Orthopädie",
            "term_en": "Lateral epicondylitis",
            "icd11_code": "FB55.1",
            "medications": ["ibuprofen", "diclofenac"],
            "sections": {
                "definition": (
                    "Der Tennisellenbogen ist eine schmerzhafte Reizung der Sehnenansätze "
                    "der Streckmuskeln der Unterarme an der Außenseite des Ellenbogens."
                ),
                "symptoms": (
                    "Druck- und Belastungsschmerz an der Außenseite des Ellenbogens, der "
                    "beim Greifen, Heben und Händeschütteln bis in den Unterarm ausstrahlt. "
                    "Die Kraft in der Hand lässt nach."
                ),
                "causes": (
                    "Wiederholte einseitige Belastung, etwa durch Sport, Computerarbeit oder "
                    "handwerkliche Tätigkeit, überfordert die Sehnenansätze."
                ),
                "diagnostics": (
                    "Die Orthopädin tastet den Ellenbogen ab und prüft gezielte "
                    "Bewegungen gegen Widerstand. Ein Ultraschall oder Röntgenbild schließt "
                    "andere Ursachen aus."
                ),
                "therapy": (
                    "Schonung der überlasteten Bewegung, Kühlen, eine Bandage und "
                    "Physiotherapie mit Dehnung und Kräftigung. Schmerzmittel helfen "
                    "kurzzeitig. Die Beschwerden klingen oft nach Monaten ab."
                ),
                "red_flags": (
                    "Taubheit, Kribbeln oder Lähmungserscheinungen in der Hand, ein stark "
                    "geschwollener, überwärmter Ellenbogen mit Fieber oder Beschwerden "
                    "nach einem Unfall sollten rasch ärztlich abgeklärt werden."
                ),
            },
            "further_reading": [
                medlineplus("elbowinjuriesanddisorders", "Elbow injuries and disorders")
            ],
        },
        {
            "title": "Rheumatoide Arthritis",
            "doc_type": "Diagnose",
            "expected_category": "Orthopädie",
            "term_en": "Rheumatoid arthritis",
            "icd11_code": "FA20",
            "medications": ["methotrexate", "prednisone"],
            "sections": {
                "definition": (
                    "Die rheumatoide Arthritis ist eine chronisch-entzündliche "
                    "Gelenkerkrankung, bei der das Immunsystem die Gelenkinnenhaut angreift."
                ),
                "symptoms": (
                    "Schmerzhafte, geschwollene und überwärmte Gelenke, vor allem an Händen "
                    "und Füßen, meist beidseitig. Typisch ist eine Morgensteifigkeit von mehr "
                    "als 30 Minuten sowie Müdigkeit."
                ),
                "causes": (
                    "Die Ursache ist nicht vollständig geklärt. Erbliche Veranlagung, "
                    "Rauchen und weitere Umweltfaktoren fördern die Entzündung. Frauen sind "
                    "häufiger betroffen."
                ),
                "diagnostics": (
                    "Die Rheumatologin untersucht die Gelenke, bestimmt Entzündungswerte und "
                    "Antikörper im Blut und verwendet Ultraschall und Röntgenbilder."
                ),
                "therapy": (
                    "Früh begonnene Basismedikamente bremsen die Erkrankung und schützen die "
                    "Gelenke. Dazu kommen Schmerzmittel, Kortison im Schub, Bewegungs- und "
                    "Physiotherapie."
                ),
                "red_flags": (
                    "Ein plötzlich stark geschwollenes, rotes, sehr schmerzhaftes Gelenk "
                    "mit Fieber kann auf eine Gelenkinfektion hinweisen – dringend ärztliche "
                    "Hilfe, bei hohem Fieber mit Verwirrtheit Notruf 144."
                ),
            },
            "further_reading": [medlineplus("rheumatoidarthritis", "Rheumatoid arthritis")],
        },
    ],
    {
        "Osteoporose": {
            "title_en": "Osteoporosis",
            "sections_en": {
                "definition": (
                    "In osteoporosis (bone loss) the bone mass decreases and the bone "
                    "structure becomes brittle, so that the risk of fractures rises."
                ),
                "symptoms": (
                    "For a long time it goes unnoticed. Later, back pain, decreasing "
                    "height, a rounded back and fractures after slight strain occur, for "
                    "example at the spine, wrist or hip."
                ),
                "causes": (
                    "Women after the menopause are often affected. Other factors are "
                    "higher age, lack of exercise, smoking, alcohol, cortisone treatment, "
                    "vitamin D deficiency and inherited tendency."
                ),
                "diagnostics": (
                    "A bone density measurement (DXA) confirms the diagnosis. Blood tests "
                    "look for causes, for example a lack of vitamin D or calcium."
                ),
                "therapy": (
                    "Exercise and strength training, a calcium-rich diet, vitamin D and "
                    "giving up smoking are important. Medicines such as bisphosphonates "
                    "slow down bone loss. Falls should be avoided."
                ),
                "red_flags": (
                    "Sudden severe back pain after a small movement can mean a vertebral "
                    "fracture. After a fall with severe pain in the hip that does not "
                    "allow standing up, call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Osteoporosis",
                "Bone density",
                "Fracture",
                "Calcium",
                "Vitamin D",
                "Menopause",
            ],
        },
        "Tennisellenbogen": {
            "title_en": "Tennis elbow",
            "sections_en": {
                "definition": (
                    "Tennis elbow is a painful irritation of the tendon attachments of "
                    "the forearm extensor muscles on the outer side of the elbow."
                ),
                "symptoms": (
                    "Pain on pressure and on exertion on the outer side of the elbow, "
                    "which spreads into the forearm when gripping, lifting and shaking "
                    "hands. Strength in the hand decreases."
                ),
                "causes": (
                    "Repeated one-sided strain, for example from sport, computer work or "
                    "manual work, overloads the tendon attachments."
                ),
                "diagnostics": (
                    "The orthopaedic doctor feels the elbow and tests specific movements "
                    "against resistance. An ultrasound or X-ray rules out other causes."
                ),
                "therapy": (
                    "Resting the overloaded movement, cooling, a brace and physiotherapy "
                    "with stretching and strengthening. Pain relievers help for a short "
                    "time. The symptoms often fade after months."
                ),
                "red_flags": (
                    "Numbness, tingling or signs of paralysis in the hand, a markedly "
                    "swollen, warm elbow with fever or symptoms after an accident should "
                    "be checked by a doctor promptly."
                ),
            },
            "keywords_en": [
                "Tennis elbow",
                "Elbow",
                "Tendon",
                "Overuse",
                "Physiotherapy",
                "Brace",
            ],
        },
        "Rheumatoide Arthritis": {
            "title_en": "Rheumatoid arthritis",
            "sections_en": {
                "definition": (
                    "Rheumatoid arthritis is a chronic inflammatory joint disease in "
                    "which the immune system attacks the lining of the joints."
                ),
                "symptoms": (
                    "Painful, swollen and warm joints, above all in the hands and feet, "
                    "usually on both sides. Typical are morning stiffness lasting more "
                    "than 30 minutes and tiredness."
                ),
                "causes": (
                    "The cause is not fully understood. Inherited tendency, smoking and "
                    "other environmental factors promote the inflammation. Women are "
                    "affected more often."
                ),
                "diagnostics": (
                    "The rheumatologist examines the joints, determines inflammation "
                    "markers and antibodies in the blood and uses ultrasound and X-rays."
                ),
                "therapy": (
                    "Disease-modifying medicines started early slow down the disease and "
                    "protect the joints. In addition there are pain relievers, cortisone "
                    "in flare-ups, and exercise and physiotherapy."
                ),
                "red_flags": (
                    "A suddenly markedly swollen, red, very painful joint with fever can "
                    "point to a joint infection – urgent medical help, and for high fever "
                    "with confusion call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Rheumatoid arthritis",
                "Joints",
                "Morning stiffness",
                "Inflammation",
                "Rheumatologist",
                "Immune system",
            ],
        },
    },
)
