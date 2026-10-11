from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Lyme-Borreliose",
        "doc_type": "Diagnose",
        "expected_category": "Infektiologie",
        "term_en": "Lyme disease",
        "icd11_code": "1C1G",
        "medications": ["doxycycline", "amoxicillin"],
        "sections": {
            "definition": (
                "Die Lyme-Borreliose ist eine bakterielle Infektion, die durch einen "
                "Zeckenstich übertragen wird."
            ),
            "symptoms": (
                "Häufigstes Zeichen ist die Wanderröte, eine sich ringförmig ausbreitende "
                "Rötung um die Stichstelle. Später können Nerven, Gelenke oder das Herz "
                "betroffen sein."
            ),
            "causes": (
                "Erreger sind Bakterien der Gattung Borrelia, die von infizierten Zecken "
                "meist erst nach vielen Stunden Saugzeit übertragen werden."
            ),
            "diagnostics": (
                "Die Wanderröte genügt für die Diagnose. Bei späteren Krankheitszeichen "
                "helfen Antikörpertests im Blut."
            ),
            "therapy": (
                "Antibiotika heilen die Infektion in frühen Stadien zuverlässig. Zecken "
                "sollten rasch entfernt werden; eine Impfung gibt es nur gegen FSME."
            ),
            "red_flags": (
                "Gesichtslähmung, starke Kopfschmerzen mit Nackensteifigkeit oder "
                "Herzstolpern nach einem Zeckenstich gehören rasch ärztlich abgeklärt."
            ),
        },
        "further_reading": [
            medlineplus("lymedisease", "Lyme Disease"),
            who("lyme-disease", "Lyme disease"),
        ],
    },
    {
        "title": "Influenza (echte Grippe)",
        "doc_type": "Diagnose",
        "expected_category": "Infektiologie",
        "term_en": "Influenza",
        "icd11_code": "1E32",
        "medications": ["oseltamivir"],
        "sections": {
            "definition": (
                "Die Influenza ist eine akute Infektion der Atemwege durch Influenzaviren, die "
                "vor allem in den Wintermonaten Wellen auslöst."
            ),
            "symptoms": (
                "Typisch ist ein plötzlicher Beginn mit hohem Fieber, Kopf- und "
                "Gliederschmerzen, trockenem Husten und starkem Krankheitsgefühl."
            ),
            "causes": (
                "Die Viren werden über Tröpfchen und Hände übertragen und sind stark "
                "ansteckend; sie verändern sich ständig."
            ),
            "diagnostics": (
                "Während einer Grippewelle wird die Diagnose oft klinisch gestellt; ein "
                "Abstrich mit Schnell- oder PCR-Test weist die Erreger nach."
            ),
            "therapy": (
                "Ruhe, Flüssigkeit und fiebersenkende Mittel helfen. Antivirale Medikamente "
                "kommen bei Risikopatienten früh im Verlauf in Frage. Die jährliche Impfung "
                "schützt."
            ),
            "red_flags": (
                "Atemnot, Brustschmerzen, Verwirrtheit oder erneuter Fieberanstieg nach "
                "Besserung können auf Komplikationen hinweisen – ärztliche Hilfe, im Notfall "
                "Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("flu", "Flu"),
            who("influenza-(seasonal)", "Influenza (seasonal)"),
        ],
    },
    {
        "title": "Sepsis (Blutvergiftung)",
        "doc_type": "Diagnose",
        "expected_category": "Infektiologie",
        "term_en": "Sepsis",
        "icd11_code": "1G40",
        "sections": {
            "definition": (
                "Eine Sepsis ist eine lebensbedrohliche Fehlreaktion des Körpers auf eine "
                "Infektion, die Organe schädigt."
            ),
            "symptoms": (
                "Warnzeichen sind Fieber oder Untertemperatur, schneller Puls und schnelle "
                "Atmung, Verwirrtheit, kalte und fleckige Haut sowie ein schweres "
                "Krankheitsgefühl."
            ),
            "causes": (
                "Ausgangspunkt sind meist Infektionen der Lunge, der Harnwege oder des Bauchs. "
                "Ältere, Kleinkinder und Menschen mit geschwächtem Immunsystem sind "
                "besonders gefährdet."
            ),
            "diagnostics": (
                "Im Krankenhaus werden Vitalzeichen, Blutwerte wie Laktat und Blutkulturen "
                "bestimmt, um Erreger und Ausgangspunkt zu finden."
            ),
            "therapy": (
                "Entscheidend ist der rasche Beginn von Antibiotika und Flüssigkeit, oft auf "
                "der Intensivstation; der Infektionsherd wird saniert."
            ),
            "red_flags": ("Bei Verdacht auf Sepsis zählt jede Stunde – sofort Notruf 144."),
        },
        "further_reading": [medlineplus("sepsis", "Sepsis"), who("sepsis", "Sepsis")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Lyme-Borreliose": {
            "title_en": "Lyme disease",
            "sections_en": {
                "definition": "Lyme disease is a bacterial infection transmitted by a tick bite.",
                "symptoms": (
                    "The most common sign is the migrating erythema, a ring-shaped reddening "
                    "spreading around the bite. Later, nerves, joints or the heart can be "
                    "affected."
                ),
                "causes": (
                    "The causative agents are bacteria of the genus Borrelia, which infected "
                    "ticks usually transmit only after many hours of feeding."
                ),
                "diagnostics": (
                    "The migrating erythema is enough for the diagnosis. For later signs, "
                    "antibody tests in the blood help."
                ),
                "therapy": (
                    "Antibiotics reliably cure the infection in early stages. Ticks should be "
                    "removed quickly; a vaccination exists only against tick-borne "
                    "encephalitis."
                ),
                "red_flags": (
                    "Facial paralysis, severe headache with a stiff neck or an irregular "
                    "heartbeat after a tick bite should be assessed promptly."
                ),
            },
            "keywords_en": [
                "Lyme disease",
                "Tick bite",
                "Borrelia",
                "Erythema",
                "Antibiotics",
                "Nerves",
            ],
        },
        "Influenza (echte Grippe)": {
            "title_en": "Influenza (flu)",
            "sections_en": {
                "definition": (
                    "Influenza is an acute infection of the airways caused by influenza "
                    "viruses that cause waves mainly in the winter months."
                ),
                "symptoms": (
                    "Typical is a sudden onset with high fever, headache and aching limbs, "
                    "dry cough and a strong feeling of illness."
                ),
                "causes": (
                    "The viruses spread by droplets and hands and are highly contagious; they "
                    "change constantly."
                ),
                "diagnostics": (
                    "During a flu wave the diagnosis is often made clinically; a swab with a "
                    "rapid or PCR test detects the virus."
                ),
                "therapy": (
                    "Rest, fluids and fever-lowering medicines help. Antiviral medicines may "
                    "be considered early for people at risk. The yearly vaccination protects."
                ),
                "red_flags": (
                    "Shortness of breath, chest pain, confusion or a renewed rise in fever "
                    "after improvement can point to complications – seek medical help, in an "
                    "emergency call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": ["Influenza", "Flu", "Fever", "Cough", "Vaccination", "Virus"],
        },
        "Sepsis (Blutvergiftung)": {
            "title_en": "Sepsis (blood poisoning)",
            "sections_en": {
                "definition": (
                    "Sepsis is a life-threatening faulty reaction of the body to an infection "
                    "that damages organs."
                ),
                "symptoms": (
                    "Warning signs are fever or a low body temperature, a fast pulse and fast "
                    "breathing, confusion, cold and mottled skin and a severe feeling of "
                    "illness."
                ),
                "causes": (
                    "The starting point is usually an infection of the lungs, urinary tract "
                    "or abdomen. Older people, small children and people with a weakened "
                    "immune system are particularly at risk."
                ),
                "diagnostics": (
                    "In hospital, vital signs, blood values such as lactate and blood "
                    "cultures are determined to find the germ and the source."
                ),
                "therapy": (
                    "Decisive is the quick start of antibiotics and fluids, often in "
                    "intensive care; the source of infection is treated."
                ),
                "red_flags": (
                    "With suspected sepsis every hour counts – call the emergency number 144 "
                    "(Austria) at once."
                ),
            },
            "keywords_en": [
                "Sepsis",
                "Blood poisoning",
                "Infection",
                "Fever",
                "Emergency",
                "Antibiotics",
            ],
        },
    },
)
