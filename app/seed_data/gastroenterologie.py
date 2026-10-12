from app.seed_data.english import with_english
from app.seed_data.links import medlineplus

ENTRIES = [
    {
        "title": "Sodbrennen und Reflux",
        "doc_type": "Symptom",
        "expected_category": "Gastroenterologie",
        "term_en": "Gastroesophageal reflux disease",
        "icd11_code": "DA22",
        "medications": ["omeprazole", "pantoprazole"],
        "sections": {
            "definition": (
                "Sodbrennen entsteht, wenn Magensäure in die Speiseröhre zurückfließt. Tritt es "
                "häufig auf, spricht man von einer Refluxkrankheit."
            ),
            "symptoms": (
                "Betroffene spüren ein Brennen hinter dem Brustbein, saures Aufstoßen und "
                "manchmal Reizhusten, oft nach üppigen Mahlzeiten oder im Liegen."
            ),
            "causes": (
                "Ein geschwächter Schließmuskel am Mageneingang, Übergewicht, fettes Essen, "
                "Alkohol, Rauchen und Stress begünstigen den Reflux."
            ),
            "diagnostics": (
                "Bei typischen Beschwerden genügt oft ein Therapieversuch. Eine "
                "Magenspiegelung klärt anhaltende Beschwerden und Warnzeichen ab."
            ),
            "therapy": (
                "Kleinere Mahlzeiten, kein spätes Essen und ein erhöhtes Kopfende helfen. "
                "Säurehemmer lindern die Beschwerden zuverlässig."
            ),
            "red_flags": (
                "Schluckbeschwerden, ungewollter Gewichtsverlust, Bluterbrechen oder schwarzer "
                "Stuhl müssen rasch abgeklärt werden. Brustschmerz kann auch vom Herzen "
                "kommen – im Zweifel Notruf 144."
            ),
        },
        "further_reading": [medlineplus("gerd", "GERD")],
    },
    {
        "title": "Reizdarmsyndrom",
        "doc_type": "Diagnose",
        "expected_category": "Gastroenterologie",
        "term_en": "Irritable bowel syndrome",
        "icd11_code": "DD91.0",
        "medications": ["loperamide"],
        "sections": {
            "definition": (
                "Das Reizdarmsyndrom ist eine häufige funktionelle Störung des Darms: Die "
                "Beschwerden sind real, ohne dass sich eine organische Ursache findet."
            ),
            "symptoms": (
                "Typisch sind wiederkehrende Bauchschmerzen, Blähungen und ein veränderter "
                "Stuhlgang mit Durchfall, Verstopfung oder beidem im Wechsel."
            ),
            "causes": (
                "Beteiligt sind eine empfindlichere Darmwahrnehmung, veränderte Darmbewegung, "
                "Stress und manchmal ein vorausgegangener Darminfekt."
            ),
            "diagnostics": (
                "Die Diagnose wird gestellt, wenn die typischen Beschwerden länger bestehen und "
                "andere Erkrankungen wie Zöliakie oder chronische Darmentzündungen "
                "ausgeschlossen sind."
            ),
            "therapy": (
                "Hilfreich sind eine angepasste Ernährung, Bewegung, Stressabbau und je nach "
                "Hauptbeschwerde gezielte Medikamente."
            ),
            "red_flags": (
                "Blut im Stuhl, Gewichtsverlust, nächtliche Beschwerden, Fieber oder ein "
                "Beginn nach dem 50. Lebensjahr passen nicht zum Reizdarm und gehören "
                "abgeklärt."
            ),
        },
        "further_reading": [medlineplus("irritablebowelsyndrome", "Irritable Bowel Syndrome")],
    },
    {
        "title": "Gallensteine (Cholelithiasis)",
        "doc_type": "Diagnose",
        "expected_category": "Gastroenterologie",
        "term_en": "Cholelithiasis",
        "icd11_code": "DC11",
        "medications": ["ursodiol"],
        "sections": {
            "definition": (
                "Gallensteine sind feste Ablagerungen in der Gallenblase oder den "
                "Gallenwegen. Viele Menschen tragen sie, ohne es zu bemerken."
            ),
            "symptoms": (
                "Wandert ein Stein, kommt es zu krampfartigen Schmerzen im rechten Oberbauch "
                "(Gallenkolik), oft nach fettem Essen, mit Übelkeit und Erbrechen."
            ),
            "causes": (
                "Risikofaktoren sind weibliches Geschlecht, Übergewicht, rascher "
                "Gewichtsverlust, höheres Alter und familiäre Veranlagung."
            ),
            "diagnostics": (
                "Ein Ultraschall des Bauchs zeigt die Steine zuverlässig. Blutwerte geben "
                "Hinweise auf eine Entzündung oder einen Gallenstau."
            ),
            "therapy": (
                "Steine ohne Beschwerden werden meist nicht behandelt. Nach Koliken wird die "
                "Gallenblase in der Regel minimal-invasiv entfernt."
            ),
            "red_flags": (
                "Fieber mit Oberbauchschmerzen, gelbe Haut oder Augen oder heftige "
                "anhaltende Schmerzen erfordern eine sofortige Abklärung."
            ),
        },
        "further_reading": [medlineplus("gallstones", "Gallstones")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Sodbrennen und Reflux": {
            "title_en": "Heartburn and acid reflux",
            "sections_en": {
                "definition": (
                    "Heartburn occurs when stomach acid flows back into the oesophagus. If it "
                    "happens often, it is called reflux disease."
                ),
                "symptoms": (
                    "Affected people feel a burning behind the breastbone, sour regurgitation "
                    "and sometimes an irritating cough, often after large meals or when lying "
                    "down."
                ),
                "causes": (
                    "A weakened sphincter at the entrance of the stomach, overweight, fatty "
                    "food, alcohol, smoking and stress promote reflux."
                ),
                "diagnostics": (
                    "With typical symptoms a trial of treatment is often enough. A "
                    "gastroscopy clarifies persistent symptoms and warning signs."
                ),
                "therapy": (
                    "Smaller meals, no late eating and a raised head of the bed help. Acid "
                    "blockers relieve the symptoms reliably."
                ),
                "red_flags": (
                    "Difficulty swallowing, unintended weight loss, vomiting blood or black "
                    "stools must be assessed promptly. Chest pain can also come from the "
                    "heart – if in doubt call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Heartburn",
                "Reflux",
                "Oesophagus",
                "Stomach acid",
                "Gastroscopy",
                "Acid blockers",
            ],
        },
        "Reizdarmsyndrom": {
            "title_en": "Irritable bowel syndrome",
            "sections_en": {
                "definition": (
                    "Irritable bowel syndrome is a common functional disorder of the gut: the "
                    "symptoms are real, although no organic cause is found."
                ),
                "symptoms": (
                    "Typical are recurring abdominal pain, bloating and changed bowel habits "
                    "with diarrhoea, constipation or both alternating."
                ),
                "causes": (
                    "A more sensitive perception of the gut, altered gut movement, stress and "
                    "sometimes a previous intestinal infection play a part."
                ),
                "diagnostics": (
                    "The diagnosis is made when the typical symptoms have lasted for some "
                    "time and other diseases such as coeliac disease or chronic bowel "
                    "inflammation have been ruled out."
                ),
                "therapy": (
                    "An adjusted diet, exercise, stress reduction and, depending on the main "
                    "complaint, targeted medicines help."
                ),
                "red_flags": (
                    "Blood in the stool, weight loss, symptoms at night, fever or onset after "
                    "the age of 50 do not fit irritable bowel syndrome and should be "
                    "investigated."
                ),
            },
            "keywords_en": [
                "Irritable bowel",
                "Bloating",
                "Diarrhoea",
                "Constipation",
                "Abdominal pain",
                "Stress",
            ],
        },
        "Gallensteine (Cholelithiasis)": {
            "title_en": "Gallstones (cholelithiasis)",
            "sections_en": {
                "definition": (
                    "Gallstones are solid deposits in the gallbladder or bile ducts. Many "
                    "people carry them without noticing."
                ),
                "symptoms": (
                    "When a stone moves, cramping pain in the right upper abdomen (biliary "
                    "colic) occurs, often after fatty food, with nausea and vomiting."
                ),
                "causes": (
                    "Risk factors are female sex, overweight, rapid weight loss, higher age "
                    "and family predisposition."
                ),
                "diagnostics": (
                    "An abdominal ultrasound shows the stones reliably. Blood tests give "
                    "hints of inflammation or a blocked bile duct."
                ),
                "therapy": (
                    "Stones without symptoms are usually not treated. After colic, the "
                    "gallbladder is usually removed by keyhole surgery."
                ),
                "red_flags": (
                    "Fever with upper abdominal pain, yellow skin or eyes or severe lasting "
                    "pain require immediate assessment."
                ),
            },
            "keywords_en": [
                "Gallstones",
                "Gallbladder",
                "Colic",
                "Upper abdomen",
                "Ultrasound",
                "Bile duct",
            ],
        },
    },
)
