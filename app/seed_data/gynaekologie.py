from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Endometriose": {
            "title_en": "Endometriosis",
            "sections_en": {
                "definition": (
                    "In endometriosis, tissue similar to the lining of the womb grows outside "
                    "the womb, for example on the ovaries or the peritoneum."
                ),
                "symptoms": (
                    "The leading symptom is severe period pain. Lower abdominal pain, pain "
                    "during intercourse and sometimes an unfulfilled wish for a child are "
                    "added."
                ),
                "causes": (
                    "The exact cause is unclear. Backward flow of menstrual blood and "
                    "hormonal and immunological factors are discussed."
                ),
                "diagnostics": (
                    "A gynaecological examination and ultrasound give hints; the diagnosis is "
                    "often confirmed only by keyhole surgery of the abdomen."
                ),
                "therapy": (
                    "Pain relievers, hormonal treatment and surgical removal of the lesions "
                    "ease the symptoms. Treatment depends on symptoms and the wish for a "
                    "child."
                ),
                "red_flags": (
                    "Sudden, very severe lower abdominal pain with circulatory problems or "
                    "fever requires immediate assessment – call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Endometriosis",
                "Period pain",
                "Womb",
                "Lower abdominal pain",
                "Hormones",
                "Fertility",
            ],
        },
        "Wechseljahre (Klimakterium)": {
            "title_en": "Menopause (climacteric)",
            "sections_en": {
                "definition": (
                    "The menopause is the natural transition phase in which the ovaries stop "
                    "producing hormones. Menopause itself is the last menstrual period, "
                    "usually around the age of 50."
                ),
                "symptoms": (
                    "Common are hot flushes, sweating, sleep problems, mood swings and "
                    "vaginal dryness."
                ),
                "therapy": (
                    "Exercise, a balanced diet and relaxation help many women. For severe "
                    "symptoms, hormone treatment can make sense after consultation."
                ),
                "red_flags": (
                    "Bleeding after the menopause is not normal and should be investigated by "
                    "a gynaecologist."
                ),
            },
            "keywords_en": [
                "Menopause",
                "Hot flushes",
                "Hormones",
                "Sleep problems",
                "Mood swings",
                "Gynaecologist",
            ],
        },
        "Polyzystisches Ovarsyndrom (PCOS)": {
            "title_en": "Polycystic ovary syndrome (PCOS)",
            "sections_en": {
                "definition": (
                    "Polycystic ovary syndrome is a common hormonal disorder in women of "
                    "reproductive age in which more male hormones are produced."
                ),
                "symptoms": (
                    "Typical are an irregular cycle or missing periods, increased body hair, "
                    "acne and difficulty becoming pregnant."
                ),
                "causes": (
                    "A predisposition and reduced insulin action play a role; overweight "
                    "makes the symptoms worse."
                ),
                "diagnostics": (
                    "The diagnosis is based on cycle disorders, hormone levels in the blood "
                    "and an ultrasound of the ovaries."
                ),
                "therapy": (
                    "Weight loss and exercise often improve cycle and metabolism. Depending "
                    "on the goal, hormonal contraceptives or fertility treatment help."
                ),
                "red_flags": (
                    "Sudden severe lower abdominal pain can point to a burst or twisted cyst "
                    "and must be assessed at once."
                ),
            },
            "keywords_en": ["PCOS", "Ovaries", "Irregular cycle", "Acne", "Insulin", "Fertility"],
        },
    },
)
