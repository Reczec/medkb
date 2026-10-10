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
