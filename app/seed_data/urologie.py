from app.seed_data.links import medlineplus

ENTRIES = [
    {
        "title": "Harnwegsinfekt und Blasenentzündung (Zystitis)",
        "doc_type": "Diagnose",
        "expected_category": "Urologie",
        "term_en": "Cystitis",
        "icd11_code": "GC00",
        "medications": ["nitrofurantoin", "fosfomycin"],
        "sections": {
            "definition": (
                "Eine Blasenentzündung ist ein Infekt der unteren Harnwege, meist durch "
                "Darmbakterien. Frauen sind wegen der kürzeren Harnröhre häufiger betroffen."
            ),
            "symptoms": (
                "Typisch sind Brennen beim Wasserlassen, häufiger Harndrang mit kleinen "
                "Mengen und Schmerzen über der Blase."
            ),
            "causes": (
                "Bakterien gelangen über die Harnröhre in die Harnblase. Geschlechtsverkehr, "
                "zu wenig Trinken und Diabetes erhöhen das Risiko."
            ),
            "diagnostics": (
                "Eine Urinuntersuchung mit Teststreifen zeigt Entzündungszeichen; bei "
                "wiederkehrenden Infekten wird eine Urinkultur angelegt."
            ),
            "therapy": (
                "Unkomplizierte Infekte werden kurz mit Antibiotika oder bei leichten "
                "Beschwerden symptomatisch behandelt. Viel Trinken unterstützt die Heilung."
            ),
            "red_flags": (
                "Fieber, Flankenschmerzen oder Schüttelfrost sprechen für eine "
                "Nierenbeckenentzündung und gehören am selben Tag ärztlich behandelt."
            ),
        },
        "further_reading": [
            medlineplus("urinarytractinfections", "Urinary Tract Infections"),
            medlineplus("bladderdiseases", "Bladder Diseases"),
        ],
    },
    {
        "title": "Nierensteine und Harnsteine",
        "doc_type": "Diagnose",
        "expected_category": "Urologie",
        "term_en": "Kidney stones",
        "icd11_code": "GB70",
        "medications": ["tamsulosin"],
        "sections": {
            "definition": (
                "Harnsteine bilden sich aus Salzen im Urin in der Niere und können in den "
                "Harnleiter wandern."
            ),
            "symptoms": (
                "Ein wandernder Stein verursacht eine Nierenkolik: heftige, wellenartige "
                "Flankenschmerzen, die in Leiste oder Genitalbereich ausstrahlen, oft mit "
                "Übelkeit und Blut im Urin."
            ),
            "causes": (
                "Zu wenig Trinken, salz- und eiweißreiche Ernährung, Übergewicht und "
                "Stoffwechselstörungen begünstigen die Steinbildung."
            ),
            "diagnostics": (
                "Ultraschall und Urinuntersuchung, bei Bedarf eine Computertomografie, zeigen "
                "Größe und Lage des Steins."
            ),
            "therapy": (
                "Kleine Steine gehen mit Schmerzmitteln und viel Flüssigkeit oft von selbst "
                "ab. Größere werden mit Stoßwellen oder endoskopisch entfernt."
            ),
            "red_flags": (
                "Kolik mit Fieber oder Schüttelfrost ist ein Notfall, weil sich der gestaute "
                "Urin infizieren kann – sofort ins Krankenhaus oder Notruf 144."
            ),
        },
        "further_reading": [medlineplus("kidneystones", "Kidney Stones")],
    },
    {
        "title": "Gutartige Prostatavergrößerung (BPH)",
        "doc_type": "Diagnose",
        "expected_category": "Urologie",
        "term_en": "Benign prostatic hyperplasia",
        "icd11_code": "GA90",
        "medications": ["tamsulosin", "finasteride"],
        "sections": {
            "definition": (
                "Die gutartige Prostatavergrößerung ist eine altersbedingte Vergrößerung der "
                "Prostata, die bei vielen Männern ab 50 auftritt."
            ),
            "symptoms": (
                "Typisch sind ein schwacher Harnstrahl, verzögerter Beginn beim "
                "Wasserlassen, Nachträufeln, nächtlicher Harndrang und das Gefühl, die Blase "
                "nicht ganz zu leeren."
            ),
            "causes": (
                "Hormonelle Veränderungen im Alter lassen das Prostatagewebe wachsen, das die "
                "Harnröhre einengt."
            ),
            "diagnostics": (
                "Die Urologin tastet die Prostata, misst Harnstrahl und Restharn per "
                "Ultraschall und bestimmt den PSA-Wert."
            ),
            "therapy": (
                "Bei leichten Beschwerden genügt Beobachten. Medikamente entspannen die "
                "Prostata oder verkleinern sie; bei starken Beschwerden hilft eine Operation."
            ),
            "red_flags": (
                "Kann kein Urin mehr gelassen werden (Harnverhalt), ist das ein Notfall – "
                "sofort Urologie oder Notaufnahme."
            ),
        },
        "further_reading": [medlineplus("enlargedprostatebph", "Enlarged Prostate (BPH)")],
    },
]
