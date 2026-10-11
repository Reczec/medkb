from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Harnwegsinfekt und Blasenentzündung (Zystitis)": {
            "title_en": "Urinary tract infection and bladder infection (cystitis)",
            "sections_en": {
                "definition": (
                    "A bladder infection is an infection of the lower urinary tract, usually "
                    "caused by gut bacteria. Women are affected more often because of the "
                    "shorter urethra."
                ),
                "symptoms": (
                    "Typical are burning when passing urine, frequent urges with small "
                    "amounts and pain above the bladder."
                ),
                "causes": (
                    "Bacteria reach the bladder through the urethra. Sexual intercourse, "
                    "drinking too little and diabetes raise the risk."
                ),
                "diagnostics": (
                    "A urine dipstick test shows signs of inflammation; for recurrent "
                    "infections a urine culture is made."
                ),
                "therapy": (
                    "Uncomplicated infections are treated briefly with antibiotics or, for "
                    "mild symptoms, symptomatically. Drinking plenty supports healing."
                ),
                "red_flags": (
                    "Fever, flank pain or shivering suggest a kidney infection and should be "
                    "treated by a doctor the same day."
                ),
            },
            "keywords_en": [
                "Cystitis",
                "Urinary infection",
                "Bladder",
                "Burning",
                "Antibiotics",
                "Urine test",
            ],
        },
        "Nierensteine und Harnsteine": {
            "title_en": "Kidney stones and urinary stones",
            "sections_en": {
                "definition": (
                    "Urinary stones form from salts in the urine in the kidney and can move "
                    "into the ureter."
                ),
                "symptoms": (
                    "A moving stone causes renal colic: severe, wave-like flank pain that "
                    "radiates to the groin or genitals, often with nausea and blood in the "
                    "urine."
                ),
                "causes": (
                    "Drinking too little, a salty and protein-rich diet, overweight and "
                    "metabolic disorders promote stone formation."
                ),
                "diagnostics": (
                    "Ultrasound and a urine test, if needed a CT scan, show the size and "
                    "position of the stone."
                ),
                "therapy": (
                    "Small stones often pass by themselves with pain relievers and plenty of "
                    "fluid. Larger ones are removed with shock waves or endoscopically."
                ),
                "red_flags": (
                    "Colic with fever or shivering is an emergency because the blocked urine "
                    "can become infected – go to hospital at once or call the emergency "
                    "number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Kidney stones",
                "Renal colic",
                "Flank pain",
                "Urine",
                "Ultrasound",
                "Shock wave",
            ],
        },
        "Gutartige Prostatavergrößerung (BPH)": {
            "title_en": "Benign prostatic hyperplasia (BPH)",
            "sections_en": {
                "definition": (
                    "Benign prostatic hyperplasia is an age-related enlargement of the "
                    "prostate that occurs in many men from the age of 50."
                ),
                "symptoms": (
                    "Typical are a weak urine stream, hesitancy at the start of urination, "
                    "dribbling afterwards, nighttime urges and the feeling of not emptying "
                    "the bladder completely."
                ),
                "causes": (
                    "Hormonal changes with age make the prostate tissue grow and narrow the "
                    "urethra."
                ),
                "diagnostics": (
                    "The urologist palpates the prostate, measures the urine stream and "
                    "residual urine by ultrasound and determines the PSA value."
                ),
                "therapy": (
                    "For mild symptoms, watchful waiting is enough. Medicines relax or shrink "
                    "the prostate; for severe symptoms surgery helps."
                ),
                "red_flags": (
                    "If no urine can be passed at all (urinary retention), this is an "
                    "emergency – go to a urology department or emergency room at once."
                ),
            },
            "keywords_en": [
                "Prostate",
                "BPH",
                "Urine stream",
                "Nighttime urination",
                "PSA",
                "Urologist",
            ],
        },
    },
)
