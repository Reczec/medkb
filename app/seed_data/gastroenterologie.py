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


EXTRA = with_english(
    [
        {
            "title": "Magenschleimhautentzündung (Gastritis)",
            "doc_type": "Diagnose",
            "expected_category": "Gastroenterologie",
            "term_en": "Gastritis",
            "icd11_code": "DA42",
            "medications": ["pantoprazole", "omeprazole"],
            "sections": {
                "definition": (
                    "Bei einer Gastritis ist die Schleimhaut des Magens entzündet, entweder "
                    "plötzlich (akut) oder über längere Zeit (chronisch)."
                ),
                "symptoms": (
                    "Oberbauchschmerzen, Völlegefühl, Übelkeit, Appetitlosigkeit und "
                    "Aufstoßen. Manchmal kommt es zu Erbrechen."
                ),
                "causes": (
                    "Häufigste Ursachen sind eine Infektion mit dem Bakterium Helicobacter "
                    "pylori, Schmerzmittel wie Ibuprofen oder Acetylsalicylsäure, Alkohol und "
                    "Stress."
                ),
                "diagnostics": (
                    "Ein Atemtest oder Stuhltest weist Helicobacter nach. Bei anhaltenden "
                    "Beschwerden wird eine Magenspiegelung mit Gewebeprobe durchgeführt."
                ),
                "therapy": (
                    "Auslöser wie Alkohol und Schmerzmittel meiden. Säurehemmer (Protonen- "
                    "pumpenhemmer) lindern die Beschwerden. Bei Helicobacter wird die "
                    "Infektion mit einer Kombination aus zwei Antibiotika und einem "
                    "Säurehemmer behandelt."
                ),
                "red_flags": (
                    "Erbrechen von Blut oder kaffeesatzartigem Material, schwarzer, teerartiger "
                    "Stuhl oder starke, plötzliche Bauchschmerzen sind ein Notfall – sofort "
                    "Notruf 144."
                ),
            },
            "further_reading": [medlineplus("stomachdisorders", "Stomach disorders")],
        },
        {
            "title": "Zöliakie",
            "doc_type": "Diagnose",
            "expected_category": "Gastroenterologie",
            "term_en": "Celiac disease",
            "icd11_code": "DA95",
            "medications": [],
            "sections": {
                "definition": (
                    "Die Zöliakie ist eine chronische Erkrankung des Dünndarms, bei der das "
                    "Immunsystem auf das Klebereiweiß Gluten reagiert und die Darmschleimhaut "
                    "schädigt."
                ),
                "symptoms": (
                    "Durchfälle, Blähungen, Bauchschmerzen, Gewichtsverlust und "
                    "Müdigkeit. Es gibt auch Verläufe mit wenigen Darmbeschwerden, etwa mit "
                    "Eisenmangel, Knochenschwund oder Hautausschlag."
                ),
                "causes": (
                    "Eine erbliche Veranlagung und der Kontakt mit Gluten aus Weizen, "
                    "Roggen und Gerste lösen die Erkrankung aus."
                ),
                "diagnostics": (
                    "Ein Bluttest auf bestimmte Antikörper gibt den ersten Hinweis, die "
                    "Diagnose wird mit einer Dünndarmbiopsie bei der Magen-Darm-Spiegelung "
                    "gesichert. Wichtig: Vorher nicht glutenfrei essen."
                ),
                "therapy": (
                    "Die einzige Behandlung ist eine lebenslange, strikt glutenfreie "
                    "Ernährung. Sie lässt die Schleimhaut abheilen. Eine Ernährungsberatung "
                    "erleichtert die Umstellung."
                ),
                "red_flags": (
                    "Starker Gewichtsverlust, anhaltende Durchfälle, Blut im Stuhl oder "
                    "Zeichen von Austrocknung bei Kindern sollten zeitnah ärztlich abgeklärt "
                    "werden."
                ),
            },
            "further_reading": [medlineplus("celiacdisease", "Celiac disease")],
        },
        {
            "title": "Colitis ulcerosa",
            "doc_type": "Diagnose",
            "expected_category": "Gastroenterologie",
            "term_en": "Ulcerative colitis",
            "icd11_code": "DD71",
            "medications": ["mesalamine", "prednisone"],
            "sections": {
                "definition": (
                    "Die Colitis ulcerosa ist eine chronisch-entzündliche Darmerkrankung, "
                    "die die Schleimhaut des Dickdarms und Mastdarms betrifft und in Schüben "
                    "verläuft."
                ),
                "symptoms": (
                    "Blutig-schleimige Durchfälle, Bauchkrämpfe, Stuhldrang, Gewichtsverlust "
                    "und Müdigkeit. In schubfreien Zeiten sind die Beschwerden gering."
                ),
                "causes": (
                    "Die Ursache ist nicht vollständig geklärt: Eine überschießende "
                    "Reaktion des Immunsystems, erbliche Veranlagung und die Darmflora "
                    "spielen zusammen."
                ),
                "diagnostics": (
                    "Blut- und Stuhluntersuchungen (Entzündungswerte, Calprotectin) und "
                    "eine Darmspiegelung mit Gewebeproben sichern die Diagnose."
                ),
                "therapy": (
                    "Entzündungshemmende Medikamente wie Mesalazin, im Schub Kortison, bei "
                    "schweren Verläufen Medikamente, die das Immunsystem dämpfen. In "
                    "seltenen Fällen ist eine Operation nötig. Regelmäßige Kontrollspiegelungen "
                    "dienen der Krebsvorsorge."
                ),
                "red_flags": (
                    "Starke blutige Durchfälle mit Fieber, Herzrasen und heftigen "
                    "Bauchschmerzen können einen gefährlichen Verlauf anzeigen – sofort "
                    "ärztliche Hilfe oder Notruf 144."
                ),
            },
            "further_reading": [medlineplus("ulcerativecolitis", "Ulcerative colitis")],
        },
        {
            "title": "Leberzirrhose",
            "doc_type": "Diagnose",
            "expected_category": "Gastroenterologie",
            "term_en": "Liver cirrhosis",
            "icd11_code": "DB93",
            "medications": ["spironolactone", "propranolol"],
            "sections": {
                "definition": (
                    "Bei der Leberzirrhose wird das Lebergewebe durch Narbengewebe ersetzt, "
                    "sodass die Leber ihre Aufgaben nur noch eingeschränkt erfüllen kann."
                ),
                "symptoms": (
                    "Anfangs treten Müdigkeit, Appetitlosigkeit und Leistungsabfall auf. "
                    "Später kommen Gelbsucht, Wasser im Bauch (Aszites), geschwollene Beine, "
                    "Juckreiz und eine Neigung zu Blutergüssen hinzu."
                ),
                "causes": (
                    "Häufige Ursachen sind langjähriger Alkoholkonsum, chronische Virushepatitis "
                    "(B und C) und eine Fettlebererkrankung. Seltenere Ursachen sind "
                    "Autoimmunerkrankungen und erbliche Stoffwechselstörungen."
                ),
                "diagnostics": (
                    "Blutwerte, Ultraschall und eine Messung der Lebersteifigkeit "
                    "(Elastografie) weisen die Zirrhose nach. Bei Bedarf wird eine "
                    "Gewebeprobe entnommen. Eine Magenspiegelung sucht nach Krampfadern der "
                    "Speiseröhre."
                ),
                "therapy": (
                    "Die Ursache wird behandelt, etwa durch Alkoholverzicht oder antivirale "
                    "Medikamente. Entwässernde Medikamente, eiweißbewusste Ernährung und "
                    "regelmäßige Kontrollen verhindern Komplikationen. Im Endstadium kommt "
                    "eine Lebertransplantation in Frage."
                ),
                "red_flags": (
                    "Erbrechen von Blut, schwarzer Stuhl, Verwirrtheit, starke Schläfrigkeit "
                    "oder Fieber mit Bauchschmerzen sind lebensbedrohlich – sofort "
                    "Notruf 144."
                ),
            },
            "further_reading": [medlineplus("cirrhosis", "Cirrhosis")],
        },
        {
            "title": "Fettleber (Steatotische Lebererkrankung)",
            "doc_type": "Diagnose",
            "expected_category": "Gastroenterologie",
            "term_en": "Fatty liver disease",
            "icd11_code": "DB92",
            "medications": [],
            "sections": {
                "definition": (
                    "Bei der Fettleber lagert die Leber übermäßig viel Fett ein. Man "
                    "unterscheidet die alkoholbedingte Form von der Form ohne "
                    "Alkoholmissbrauch, die mit Übergewicht und Diabetes zusammenhängt."
                ),
                "symptoms": (
                    "Meist gibt es keine Beschwerden. Manche Betroffenen verspüren "
                    "Müdigkeit oder ein Druckgefühl im rechten Oberbauch. Die Erkrankung wird "
                    "oft zufällig bei einer Blutuntersuchung oder einem Ultraschall entdeckt."
                ),
                "causes": (
                    "Übergewicht, Bewegungsmangel, Diabetes mellitus Typ 2, erhöhte "
                    "Blutfette und Alkohol fördern die Verfettung. Auch schnelle "
                    "Gewichtsabnahme und manche Medikamente können beteiligt sein."
                ),
                "diagnostics": (
                    "Ein Ultraschall zeigt die vermehrte Fetteinlagerung, Leberwerte im Blut "
                    "geben Hinweise. Eine Messung der Lebersteifigkeit schätzt die "
                    "Vernarbung ab."
                ),
                "therapy": (
                    "Gewichtsabnahme von fünf bis zehn Prozent, mediterrane Ernährung, "
                    "Bewegung und Verzicht auf Alkohol können die Leber deutlich "
                    "entlasten. Begleiterkrankungen wie Diabetes und Bluthochdruck werden "
                    "mitbehandelt."
                ),
                "red_flags": (
                    "Gelbfärbung von Haut oder Augen, ein zunehmend dicker Bauch, "
                    "Bluterbrechen oder Verwirrtheit weisen auf eine fortgeschrittene "
                    "Lebererkrankung hin – rasch ärztlich abklären, bei Bluterbrechen "
                    "Notruf 144."
                ),
            },
            "further_reading": [medlineplus("fattyliverdisease", "Fatty liver disease")],
        },
        {
            "title": "Akute Bauchspeicheldrüsenentzündung (Pankreatitis)",
            "doc_type": "Diagnose",
            "expected_category": "Gastroenterologie",
            "term_en": "Acute pancreatitis",
            "icd11_code": "DC31",
            "medications": ["paracetamol"],
            "sections": {
                "definition": (
                    "Bei der akuten Pankreatitis entzündet sich die Bauchspeicheldrüse "
                    "plötzlich, weil Verdauungsenzyme schon im Organ aktiv werden und es "
                    "selbst angreifen."
                ),
                "symptoms": (
                    "Heftige, gürtelförmige Schmerzen im Oberbauch, die in den Rücken "
                    "ausstrahlen, dazu Übelkeit, Erbrechen, Fieber und ein aufgetriebener "
                    "Bauch."
                ),
                "causes": (
                    "Die häufigsten Ursachen sind Gallensteine und Alkohol. Weitere sind "
                    "stark erhöhte Blutfette, bestimmte Medikamente und Eingriffe an den "
                    "Gallenwegen."
                ),
                "diagnostics": (
                    "Blutwerte (Lipase), Ultraschall des Bauches und bei Bedarf "
                    "Computertomografie sichern die Diagnose und zeigen das Ausmaß."
                ),
                "therapy": (
                    "Die Behandlung erfolgt im Krankenhaus: Flüssigkeit über die Vene, "
                    "Schmerzmittel, frühe, angepasste Ernährung und die Behandlung der "
                    "Ursache. Gallensteine werden gegebenenfalls entfernt."
                ),
                "red_flags": (
                    "Anhaltende heftige Bauchschmerzen mit Erbrechen, Fieber, Kreislauf- "
                    "problemen oder Atemnot können einen schweren Verlauf bedeuten – "
                    "sofort Notruf 144."
                ),
            },
            "further_reading": [medlineplus("pancreatitis", "Pancreatitis")],
        },
    ],
    {
        "Magenschleimhautentzündung (Gastritis)": {
            "title_en": "Stomach lining inflammation (gastritis)",
            "sections_en": {
                "definition": (
                    "In gastritis the lining of the stomach is inflamed, either suddenly "
                    "(acute) or over a longer time (chronic)."
                ),
                "symptoms": (
                    "Pain in the upper abdomen, a feeling of fullness, nausea, loss of "
                    "appetite and belching. Sometimes vomiting occurs."
                ),
                "causes": (
                    "The most common causes are infection with the bacterium Helicobacter "
                    "pylori, painkillers such as ibuprofen or acetylsalicylic acid, "
                    "alcohol and stress."
                ),
                "diagnostics": (
                    "A breath test or stool test detects Helicobacter. If the symptoms "
                    "persist, a gastroscopy with a tissue sample is carried out."
                ),
                "therapy": (
                    "Avoid triggers such as alcohol and painkillers. Acid blockers (proton "
                    "pump inhibitors) relieve the symptoms. With Helicobacter the "
                    "infection is treated with a combination of two antibiotics and an "
                    "acid blocker."
                ),
                "red_flags": (
                    "Vomiting blood or coffee-ground material, black, tarry stool or "
                    "severe, sudden abdominal pain are an emergency – call the emergency "
                    "number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Gastritis",
                "Stomach",
                "Helicobacter pylori",
                "Upper abdominal pain",
                "Acid blockers",
                "Gastroscopy",
            ],
        },
        "Zöliakie": {
            "title_en": "Coeliac disease",
            "sections_en": {
                "definition": (
                    "Coeliac disease is a chronic disease of the small intestine in which "
                    "the immune system reacts to the protein gluten and damages the lining "
                    "of the gut."
                ),
                "symptoms": (
                    "Diarrhoea, bloating, abdominal pain, weight loss and tiredness. There "
                    "are also courses with few gut symptoms, for example with iron "
                    "deficiency, bone loss or a skin rash."
                ),
                "causes": (
                    "An inherited tendency and contact with gluten from wheat, rye and "
                    "barley trigger the disease."
                ),
                "diagnostics": (
                    "A blood test for certain antibodies gives the first hint; the "
                    "diagnosis is confirmed by a biopsy of the small intestine during an "
                    "endoscopy. Important: do not eat gluten-free beforehand."
                ),
                "therapy": (
                    "The only treatment is a lifelong, strictly gluten-free diet. It lets "
                    "the lining heal. Dietary counselling makes the change easier."
                ),
                "red_flags": (
                    "Marked weight loss, persistent diarrhoea, blood in the stool or "
                    "signs of dehydration in children should be checked by a doctor "
                    "promptly."
                ),
            },
            "keywords_en": [
                "Coeliac disease",
                "Gluten",
                "Small intestine",
                "Diarrhoea",
                "Gluten-free diet",
                "Antibodies",
            ],
        },
        "Colitis ulcerosa": {
            "title_en": "Ulcerative colitis",
            "sections_en": {
                "definition": (
                    "Ulcerative colitis is a chronic inflammatory bowel disease that "
                    "affects the lining of the large intestine and rectum and runs in "
                    "flare-ups."
                ),
                "symptoms": (
                    "Bloody, mucous diarrhoea, abdominal cramps, urgency, weight loss and "
                    "tiredness. In periods without a flare-up the symptoms are slight."
                ),
                "causes": (
                    "The cause is not fully understood: an overshooting reaction of the "
                    "immune system, an inherited tendency and the gut flora work "
                    "together."
                ),
                "diagnostics": (
                    "Blood and stool tests (inflammation markers, calprotectin) and a "
                    "colonoscopy with tissue samples confirm the diagnosis."
                ),
                "therapy": (
                    "Anti-inflammatory medicines such as mesalazine, cortisone during a "
                    "flare-up, and in severe courses medicines that dampen the immune "
                    "system. Rarely an operation is needed. Regular follow-up "
                    "colonoscopies serve cancer prevention."
                ),
                "red_flags": (
                    "Severe bloody diarrhoea with fever, a racing heart and intense "
                    "abdominal pain can indicate a dangerous course – seek medical help "
                    "at once or call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Ulcerative colitis",
                "Inflammatory bowel disease",
                "Bloody diarrhoea",
                "Colonoscopy",
                "Mesalazine",
                "Flare-up",
            ],
        },
        "Leberzirrhose": {
            "title_en": "Liver cirrhosis",
            "sections_en": {
                "definition": (
                    "In liver cirrhosis, liver tissue is replaced by scar tissue, so that "
                    "the liver can only carry out its tasks to a limited extent."
                ),
                "symptoms": (
                    "At first tiredness, loss of appetite and reduced performance occur. "
                    "Later jaundice, fluid in the abdomen (ascites), swollen legs, itching "
                    "and a tendency to bruise are added."
                ),
                "causes": (
                    "Common causes are long-term alcohol use, chronic viral hepatitis (B "
                    "and C) and fatty liver disease. Rarer causes are autoimmune diseases "
                    "and inherited metabolic disorders."
                ),
                "diagnostics": (
                    "Blood values, ultrasound and a measurement of liver stiffness "
                    "(elastography) show the cirrhosis. If needed, a tissue sample is "
                    "taken. A gastroscopy looks for varicose veins of the oesophagus."
                ),
                "therapy": (
                    "The cause is treated, for example by stopping alcohol or with "
                    "antiviral medicines. Diuretics, a protein-aware diet and regular "
                    "check-ups prevent complications. In the end stage a liver "
                    "transplant comes into question."
                ),
                "red_flags": (
                    "Vomiting blood, black stool, confusion, marked drowsiness or fever "
                    "with abdominal pain are life-threatening – call the emergency "
                    "number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Liver cirrhosis",
                "Liver",
                "Ascites",
                "Jaundice",
                "Elastography",
                "Liver transplant",
            ],
        },
        "Fettleber (Steatotische Lebererkrankung)": {
            "title_en": "Fatty liver (steatotic liver disease)",
            "sections_en": {
                "definition": (
                    "In fatty liver the liver stores too much fat. A distinction is made "
                    "between the alcohol-related form and the form without alcohol "
                    "misuse, which is linked to overweight and diabetes."
                ),
                "symptoms": (
                    "There are usually no symptoms. Some people feel tired or have a "
                    "feeling of pressure in the right upper abdomen. The disease is often "
                    "found by chance during a blood test or an ultrasound."
                ),
                "causes": (
                    "Overweight, lack of exercise, type 2 diabetes mellitus, raised blood "
                    "fats and alcohol promote fat build-up. Rapid weight loss and some "
                    "medicines can also be involved."
                ),
                "diagnostics": (
                    "An ultrasound shows the increased fat storage, and liver values in "
                    "the blood give hints. A measurement of liver stiffness estimates the "
                    "scarring."
                ),
                "therapy": (
                    "Weight loss of five to ten percent, a Mediterranean diet, exercise "
                    "and giving up alcohol can relieve the liver markedly. Accompanying "
                    "diseases such as diabetes and high blood pressure are treated too."
                ),
                "red_flags": (
                    "A yellow colour of the skin or eyes, an increasingly large abdomen, "
                    "vomiting of blood or confusion point to advanced liver disease – "
                    "have it checked promptly, and for vomiting blood call the emergency "
                    "number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Fatty liver",
                "Liver",
                "Overweight",
                "Diabetes",
                "Liver values",
                "Mediterranean diet",
            ],
        },
        "Akute Bauchspeicheldrüsenentzündung (Pankreatitis)": {
            "title_en": "Acute inflammation of the pancreas (pancreatitis)",
            "sections_en": {
                "definition": (
                    "In acute pancreatitis the pancreas suddenly becomes inflamed, "
                    "because digestive enzymes become active within the organ and attack "
                    "it."
                ),
                "symptoms": (
                    "Severe, belt-like pain in the upper abdomen that spreads to the "
                    "back, plus nausea, vomiting, fever and a swollen abdomen."
                ),
                "causes": (
                    "The most common causes are gallstones and alcohol. Others are "
                    "markedly raised blood fats, certain medicines and procedures on the "
                    "bile ducts."
                ),
                "diagnostics": (
                    "Blood values (lipase), an ultrasound of the abdomen and, if needed, "
                    "computed tomography confirm the diagnosis and show its extent."
                ),
                "therapy": (
                    "Treatment takes place in hospital: fluids through a vein, pain "
                    "relief, early adapted nutrition and treatment of the cause. "
                    "Gallstones are removed where appropriate."
                ),
                "red_flags": (
                    "Lasting severe abdominal pain with vomiting, fever, circulation "
                    "problems or breathlessness can mean a severe course – call the "
                    "emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Pancreatitis",
                "Pancreas",
                "Upper abdominal pain",
                "Gallstones",
                "Lipase",
                "Alcohol",
            ],
        },
    },
)
