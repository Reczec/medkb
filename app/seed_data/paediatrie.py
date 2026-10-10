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
