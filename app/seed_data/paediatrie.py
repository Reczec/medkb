from app.seed_data.english import with_english
from app.seed_data.links import medlineplus

ENTRIES = [
    {
        "title": "Windpocken (Varizellen)",
        "doc_type": "Diagnose",
        "expected_category": "Pädiatrie",
        "term_en": "Chickenpox",
        "icd11_code": "1E90",
        "sections": {
            "definition": (
                "Windpocken sind eine hochansteckende Kinderkrankheit, ausgelöst durch das "
                "Varizella-Zoster-Virus."
            ),
            "symptoms": (
                "Typisch ist ein juckender Ausschlag mit Bläschen in verschiedenen "
                "Entwicklungsstadien am ganzen Körper, dazu leichtes Fieber."
            ),
            "causes": (
                "Die Übertragung erfolgt über Tröpfchen und den Inhalt der Bläschen; "
                "ungeimpfte Kinder im Kindergartenalter erkranken am häufigsten."
            ),
            "diagnostics": ("Der Kinderarzt erkennt Windpocken meist am typischen Ausschlag."),
            "therapy": (
                "Behandelt werden die Beschwerden: juckreizstillende Lotionen, kurze "
                "Fingernägel und bei Bedarf fiebersenkende Mittel. Die Impfung wird für "
                "Kinder empfohlen."
            ),
            "red_flags": (
                "Atemnot, Benommenheit, Krampfanfälle oder stark gerötete, eitrige Bläschen "
                "erfordern sofort ärztliche Hilfe."
            ),
        },
        "further_reading": [medlineplus("chickenpox", "Chickenpox")],
    },
    {
        "title": "Scharlach",
        "doc_type": "Diagnose",
        "expected_category": "Pädiatrie",
        "term_en": "Scarlet fever",
        "icd11_code": "1B50",
        "medications": ["penicillin"],
        "sections": {
            "definition": (
                "Scharlach ist eine bakterielle Kinderkrankheit durch Streptokokken, die vor "
                "allem Kinder im Schul- und Kindergartenalter betrifft."
            ),
            "symptoms": (
                "Typisch sind Halsschmerzen, Fieber, eine himbeerrote Zunge und ein "
                "feinfleckiger, samtiger Ausschlag, der in den Leisten beginnt."
            ),
            "causes": (
                "Die Bakterien werden über Tröpfchen übertragen. Man kann mehrmals an "
                "Scharlach erkranken."
            ),
            "diagnostics": (
                "Ein Rachenabstrich mit Schnelltest weist die Streptokokken in der "
                "kinderärztlichen Praxis nach."
            ),
            "therapy": (
                "Antibiotika verkürzen die Krankheit und senken das Risiko für Komplikationen. "
                "Nach 24 Stunden Behandlung sind Kinder meist nicht mehr ansteckend."
            ),
            "red_flags": (
                "Atemnot, Schluckunfähigkeit, starke Schwellung am Hals oder Teilnahmslosigkeit "
                "erfordern sofort ärztliche Hilfe."
            ),
        },
        "further_reading": [medlineplus("streptococcalinfections", "Streptococcal Infections")],
    },
    {
        "title": "Fieber bei Säuglingen und Kleinkindern",
        "doc_type": "Symptom",
        "expected_category": "Pädiatrie",
        "term_en": "Fever in children",
        "icd11_code": "MG26",
        "medications": ["acetaminophen", "ibuprofen"],
        "sections": {
            "definition": (
                "Fieber ist bei Kindern eine häufige und meist sinnvolle Abwehrreaktion. Ab "
                "38,5 °C spricht man bei Säuglingen und Kleinkindern von Fieber."
            ),
            "symptoms": (
                "Das Kind ist warm, müde oder quengelig, trinkt weniger und hat oft einen "
                "schnelleren Puls."
            ),
            "causes": (
                "Meist stecken harmlose virale Infekte dahinter, seltener bakterielle "
                "Infektionen wie eine Mittelohr- oder Harnwegsentzündung."
            ),
            "diagnostics": (
                "Entscheidend ist der Allgemeinzustand des Kindes. Der Kinderarzt sucht die "
                "Ursache durch Untersuchung und bei Bedarf Urin- oder Bluttests."
            ),
            "therapy": (
                "Ausreichend trinken und Ruhe sind wichtig. Fiebersenkende Mittel dienen dem "
                "Wohlbefinden, nicht dem Senken um jeden Preis."
            ),
            "red_flags": (
                "Fieber bei Säuglingen unter drei Monaten, Teilnahmslosigkeit, "
                "Nackensteifigkeit, Atemnot, ein Ausschlag, der sich nicht wegdrücken lässt, "
                "oder ein Krampfanfall: sofort Kinderarzt oder Notruf 144."
            ),
        },
        "further_reading": [medlineplus("fever", "Fever")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Windpocken (Varizellen)": {
            "title_en": "Chickenpox (varicella)",
            "sections_en": {
                "definition": (
                    "Chickenpox is a highly contagious childhood illness caused by the "
                    "varicella-zoster virus."
                ),
                "symptoms": (
                    "Typical is an itchy rash with blisters in different stages across the "
                    "whole body, together with mild fever."
                ),
                "causes": (
                    "It spreads by droplets and the content of the blisters; unvaccinated "
                    "children of nursery age fall ill most often."
                ),
                "diagnostics": (
                    "The paediatrician usually recognises chickenpox from the typical rash."
                ),
                "therapy": (
                    "The symptoms are treated: itch-relieving lotions, short fingernails and, "
                    "if needed, fever-lowering medicines. Vaccination is recommended for "
                    "children."
                ),
                "red_flags": (
                    "Shortness of breath, drowsiness, seizures or strongly reddened, purulent "
                    "blisters need medical help at once."
                ),
            },
            "keywords_en": [
                "Chickenpox",
                "Varicella",
                "Rash",
                "Blisters",
                "Children",
                "Vaccination",
            ],
        },
        "Scharlach": {
            "title_en": "Scarlet fever",
            "sections_en": {
                "definition": (
                    "Scarlet fever is a bacterial childhood illness caused by streptococci "
                    "that mainly affects children of school and nursery age."
                ),
                "symptoms": (
                    "Typical are a sore throat, fever, a raspberry-red tongue and a fine, "
                    "sandpaper-like rash that starts in the groin."
                ),
                "causes": (
                    "The bacteria spread by droplets. One can get scarlet fever more than once."
                ),
                "diagnostics": (
                    "A throat swab with a rapid test detects the streptococci in the "
                    "paediatric practice."
                ),
                "therapy": (
                    "Antibiotics shorten the illness and lower the risk of complications. "
                    "After 24 hours of treatment children are usually no longer contagious."
                ),
                "red_flags": (
                    "Shortness of breath, being unable to swallow, marked swelling of the "
                    "neck or listlessness need medical help at once."
                ),
            },
            "keywords_en": [
                "Scarlet fever",
                "Streptococci",
                "Sore throat",
                "Rash",
                "Antibiotics",
                "Children",
            ],
        },
        "Fieber bei Säuglingen und Kleinkindern": {
            "title_en": "Fever in babies and young children",
            "sections_en": {
                "definition": (
                    "Fever is a common and usually useful defence reaction in children. In "
                    "babies and young children, fever starts at 38.5 °C."
                ),
                "symptoms": (
                    "The child feels warm, is tired or fretful, drinks less and often has a "
                    "faster pulse."
                ),
                "causes": (
                    "Usually harmless viral infections are behind it, less often bacterial "
                    "infections such as an ear or urinary tract infection."
                ),
                "diagnostics": (
                    "The child's general condition is decisive. The paediatrician looks for "
                    "the cause by examination and, if needed, urine or blood tests."
                ),
                "therapy": (
                    "Drinking enough and rest are important. Fever-lowering medicines serve "
                    "comfort, not lowering the temperature at any price."
                ),
                "red_flags": (
                    "Fever in babies under three months, listlessness, a stiff neck, "
                    "shortness of breath, a rash that does not fade under pressure or a "
                    "seizure: see a paediatrician at once or call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": ["Fever", "Baby", "Child", "Temperature", "Paediatrician", "Seizure"],
        },
    },
)
