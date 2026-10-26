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


EXTRA = with_english(
    [
        {
            "title": "Schwangerschaftsdiabetes (Gestationsdiabetes)",
            "doc_type": "Diagnose",
            "expected_category": "Endokrinologie",
            "term_en": "Gestational diabetes",
            "icd11_code": "JA63.2",
            "medications": ["insulin", "metformin"],
            "sections": {
                "definition": (
                    "Beim Schwangerschaftsdiabetes tritt erstmals in der Schwangerschaft "
                    "eine Störung des Zuckerstoffwechsels auf, die sich meist nach der Geburt "
                    "wieder normalisiert."
                ),
                "symptoms": (
                    "Meist gibt es keine Beschwerden. Gelegentlich kommen verstärkter Durst, "
                    "häufiges Wasserlassen oder Müdigkeit vor. Deshalb wird in der "
                    "Schwangerschaft gezielt untersucht."
                ),
                "causes": (
                    "Hormone der Plazenta machen den Körper weniger empfindlich für Insulin. "
                    "Übergewicht, höheres Alter, Diabetes in der Familie und ein früherer "
                    "Schwangerschaftsdiabetes erhöhen das Risiko."
                ),
                "diagnostics": (
                    "Zwischen der 24. und 28. Schwangerschaftswoche wird ein oraler "
                    "Zuckerbelastungstest (Glukosetoleranztest) durchgeführt."
                ),
                "therapy": (
                    "Ernährungsumstellung, Bewegung und regelmäßige Blutzuckermessung "
                    "reichen oft aus. Gelingt die Einstellung damit nicht, wird Insulin "
                    "gespritzt. Die Betreuung erfolgt gemeinsam durch Frauenärztin und "
                    "Diabetesteam."
                ),
                "red_flags": (
                    "Starker Durst mit häufigem Erbrechen, Bauchschmerzen, Verwirrtheit oder "
                    "verminderte Kindsbewegungen sind Warnzeichen – sofort ärztliche Hilfe, "
                    "im Zweifel Notruf 144."
                ),
            },
            "further_reading": [medlineplus("diabetesandpregnancy", "Diabetes and pregnancy")],
        },
        {
            "title": "Gebärmuttermyome",
            "doc_type": "Diagnose",
            "expected_category": "Gynäkologie",
            "term_en": "Uterine fibroids",
            "icd11_code": "2E86.0",
            "medications": ["tranexamic acid", "ibuprofen"],
            "sections": {
                "definition": (
                    "Myome sind gutartige Knoten aus Muskelgewebe in der Gebärmutterwand. Sie "
                    "gehören zu den häufigsten gutartigen Veränderungen bei Frauen im "
                    "gebärfähigen Alter."
                ),
                "symptoms": (
                    "Viele Frauen haben keine Beschwerden. Möglich sind starke und lange "
                    "Regelblutungen, Unterbauchschmerzen, Druckgefühl, häufiger Harndrang "
                    "und Verstopfung. Selten erschweren Myome das Schwangerwerden."
                ),
                "causes": (
                    "Das Wachstum hängt von weiblichen Hormonen ab. Familiäre Häufung, "
                    "Übergewicht und eine frühe erste Regelblutung begünstigen Myome."
                ),
                "diagnostics": (
                    "Die Frauenärztin tastet den Unterleib ab und erkennt Myome im "
                    "Ultraschall. Bei Bedarf folgt eine Magnetresonanztomografie."
                ),
                "therapy": (
                    "Ohne Beschwerden genügt Beobachten. Bei starken Blutungen helfen "
                    "Medikamente, bei großen Myomen kann eine Operation oder eine "
                    "Embolisation der Gefäße nötig sein. Die Gebärmutter kann oft erhalten "
                    "bleiben."
                ),
                "red_flags": (
                    "Sehr starke Blutungen mit Schwindel, Kreislaufproblemen oder "
                    "Blässe, plötzliche heftige Unterbauchschmerzen oder Fieber sollten "
                    "umgehend untersucht werden, bei Kreislaufkollaps Notruf 144."
                ),
            },
            "further_reading": [medlineplus("uterinefibroids", "Uterine fibroids")],
        },
        {
            "title": "Regelschmerzen (Dysmenorrhö)",
            "doc_type": "Diagnose",
            "expected_category": "Gynäkologie",
            "term_en": "Dysmenorrhea",
            "icd11_code": "GA34.3",
            "medications": ["ibuprofen", "naproxen"],
            "sections": {
                "definition": (
                    "Regelschmerzen sind krampfartige Schmerzen im Unterbauch vor oder "
                    "während der Menstruation. Man unterscheidet primäre Beschwerden ohne "
                    "Organerkrankung und sekundäre Beschwerden mit einer Ursache."
                ),
                "symptoms": (
                    "Ziehende oder krampfartige Unterbauchschmerzen, oft mit Rückenschmerzen, "
                    "Übelkeit, Durchfall oder Kopfschmerzen. Die Beschwerden halten meist "
                    "ein bis drei Tage an."
                ),
                "causes": (
                    "Bei der primären Form zieht sich die Gebärmutter durch Botenstoffe "
                    "(Prostaglandine) stark zusammen. Sekundär können Endometriose, Myome "
                    "oder Entzündungen die Ursache sein."
                ),
                "diagnostics": (
                    "Die Frauenärztin erfragt den Zyklus und untersucht den Unterleib mit "
                    "Ultraschall. Treten die Schmerzen neu oder zunehmend auf, wird nach "
                    "Ursachen gesucht."
                ),
                "therapy": (
                    "Wärme, Bewegung und entzündungshemmende Schmerzmittel lindern die "
                    "Beschwerden. Hormonelle Verhütungsmittel können helfen. Bei einer "
                    "Ursache wie Endometriose wird diese behandelt."
                ),
                "red_flags": (
                    "Sehr starke, neu aufgetretene Unterleibsschmerzen, Fieber oder "
                    "Schmerzen mit Ohnmacht und verspäteter Regel (Verdacht auf "
                    "Eileiterschwangerschaft) sind ein Notfall – Notruf 144."
                ),
            },
            "further_reading": [medlineplus("menstruation", "Menstruation")],
        },
    ],
    {
        "Schwangerschaftsdiabetes (Gestationsdiabetes)": {
            "title_en": "Diabetes in pregnancy (gestational diabetes)",
            "sections_en": {
                "definition": (
                    "In gestational diabetes a disorder of sugar metabolism occurs for "
                    "the first time during pregnancy, and it usually returns to normal "
                    "after the birth."
                ),
                "symptoms": (
                    "There are usually no symptoms. Occasionally increased thirst, "
                    "frequent urination or tiredness occur. That is why targeted testing "
                    "is done in pregnancy."
                ),
                "causes": (
                    "Hormones from the placenta make the body less sensitive to insulin. "
                    "Overweight, higher age, diabetes in the family and gestational "
                    "diabetes in an earlier pregnancy raise the risk."
                ),
                "diagnostics": (
                    "Between the 24th and 28th week of pregnancy an oral sugar load test "
                    "(glucose tolerance test) is carried out."
                ),
                "therapy": (
                    "Changes to diet, exercise and regular blood sugar measurement are "
                    "often enough. If this does not achieve control, insulin is injected. "
                    "Care is shared between the gynaecologist and the diabetes team."
                ),
                "red_flags": (
                    "Severe thirst with frequent vomiting, abdominal pain, confusion or "
                    "reduced movements of the baby are warning signs – seek medical help "
                    "at once, and if in doubt call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Gestational diabetes",
                "Pregnancy",
                "Blood sugar",
                "Glucose tolerance test",
                "Insulin",
                "Gynaecologist",
            ],
        },
        "Gebärmuttermyome": {
            "title_en": "Uterine fibroids",
            "sections_en": {
                "definition": (
                    "Fibroids are benign nodules of muscle tissue in the wall of the "
                    "uterus. They are among the most common benign changes in women of "
                    "childbearing age."
                ),
                "symptoms": (
                    "Many women have no symptoms. Possible are heavy and long periods, "
                    "lower abdominal pain, a feeling of pressure, frequent urge to "
                    "urinate and constipation. Rarely, fibroids make it harder to become "
                    "pregnant."
                ),
                "causes": (
                    "Growth depends on female hormones. Cases in the family, overweight "
                    "and an early first period favour fibroids."
                ),
                "diagnostics": (
                    "The gynaecologist feels the abdomen and sees fibroids on an "
                    "ultrasound. If needed, magnetic resonance imaging follows."
                ),
                "therapy": (
                    "Without symptoms, watching is enough. Medicines help with heavy "
                    "bleeding; with large fibroids an operation or an embolisation of the "
                    "vessels can be necessary. The uterus can often be preserved."
                ),
                "red_flags": (
                    "Very heavy bleeding with dizziness, circulation problems or pallor, "
                    "sudden severe lower abdominal pain or fever should be examined "
                    "promptly; for a circulatory collapse call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Uterine fibroids",
                "Myoma",
                "Heavy periods",
                "Uterus",
                "Ultrasound",
                "Gynaecologist",
            ],
        },
        "Regelschmerzen (Dysmenorrhö)": {
            "title_en": "Period pain (dysmenorrhoea)",
            "sections_en": {
                "definition": (
                    "Period pain is cramping pain in the lower abdomen before or during "
                    "menstruation. A distinction is made between primary pain without an "
                    "organ disease and secondary pain with a cause."
                ),
                "symptoms": (
                    "Pulling or cramping pain in the lower abdomen, often with back "
                    "pain, nausea, diarrhoea or headache. The symptoms usually last one "
                    "to three days."
                ),
                "causes": (
                    "In the primary form the uterus contracts strongly because of "
                    "messenger substances (prostaglandins). In the secondary form "
                    "endometriosis, fibroids or inflammation can be the cause."
                ),
                "diagnostics": (
                    "The gynaecologist asks about the cycle and examines the abdomen with "
                    "an ultrasound. If the pain is new or getting worse, causes are "
                    "looked for."
                ),
                "therapy": (
                    "Heat, exercise and anti-inflammatory pain relievers ease the "
                    "symptoms. Hormonal contraceptives can help. If there is a cause such "
                    "as endometriosis, it is treated."
                ),
                "red_flags": (
                    "Very severe, newly occurring pain in the lower abdomen, fever, or "
                    "pain with fainting and a late period (suspected ectopic pregnancy) "
                    "is an emergency – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Period pain",
                "Dysmenorrhoea",
                "Menstruation",
                "Cramps",
                "Pain relievers",
                "Endometriosis",
            ],
        },
    },
)
