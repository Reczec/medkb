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


EXTRA = with_english(
    [
        {
            "title": "Harninkontinenz (Blasenschwäche)",
            "doc_type": "Diagnose",
            "expected_category": "Urologie",
            "term_en": "Urinary incontinence",
            "icd11_code": "MF50.2",
            "medications": ["solifenacin", "mirabegron"],
            "sections": {
                "definition": (
                    "Bei der Harninkontinenz geht unwillkürlich Urin ab, weil die Blase den "
                    "Harn nicht sicher halten kann."
                ),
                "symptoms": (
                    "Bei der Belastungsinkontinenz geht Urin beim Husten, Niesen oder Heben "
                    "ab. Bei der Dranginkontinenz tritt plötzlich starker Harndrang auf, den "
                    "man nicht mehr aufhalten kann."
                ),
                "causes": (
                    "Eine geschwächte Beckenbodenmuskulatur nach Geburten, im Alter oder "
                    "nach Operationen, eine überaktive Blase, eine vergrößerte Prostata, "
                    "Harnwegsinfekte, Medikamente und Nervenerkrankungen können dahinterstecken."
                ),
                "diagnostics": (
                    "Die Urologin erfragt Trinkmenge, Häufigkeit und Auslöser, oft mit einem "
                    "Blasentagebuch. Es folgen Urinuntersuchung, Ultraschall und bei Bedarf "
                    "eine Messung des Blasendrucks."
                ),
                "therapy": (
                    "Beckenbodentraining, Blasentraining, Gewichtsabnahme und angepasste "
                    "Trinkmengen helfen oft. Medikamente beruhigen eine überaktive Blase, "
                    "bei Belastungsinkontinenz kann eine Operation sinnvoll sein."
                ),
                "red_flags": (
                    "Plötzlich auftretende Blasenschwäche mit Taubheit im Intimbereich, "
                    "Beinschwäche oder Rückenschmerzen kann auf eine Nervenschädigung "
                    "hinweisen – umgehend ärztlich abklären, bei Lähmungen Notruf 144."
                ),
            },
            "further_reading": [medlineplus("urinaryincontinence", "Urinary incontinence")],
        },
        {
            "title": "Akute Nierenbeckenentzündung (Pyelonephritis)",
            "doc_type": "Diagnose",
            "expected_category": "Urologie",
            "term_en": "Pyelonephritis",
            "icd11_code": "GB51",
            "medications": ["ciprofloxacin", "ibuprofen"],
            "sections": {
                "definition": (
                    "Bei der Nierenbeckenentzündung sind das Nierenbecken und das "
                    "Nierengewebe durch Bakterien entzündet, meist als Folge eines "
                    "aufsteigenden Harnwegsinfekts."
                ),
                "symptoms": (
                    "Fieber mit Schüttelfrost, Flankenschmerzen, ein klopfempfindlicher "
                    "Rücken, Brennen beim Wasserlassen und ein allgemeines Krankheitsgefühl."
                ),
                "causes": (
                    "Meist steigen Darmbakterien, vor allem E. coli, über die Harnröhre und "
                    "die Blase zur Niere auf. Harnstau durch Nierensteine, Diabetes und "
                    "Schwangerschaft erhöhen das Risiko."
                ),
                "diagnostics": (
                    "Urinuntersuchung mit Urinkultur, Blutuntersuchung auf Entzündungswerte "
                    "und ein Ultraschall der Nieren, um einen Harnstau auszuschließen."
                ),
                "therapy": (
                    "Behandelt wird mit einem Antibiotikum, in schweren Fällen im "
                    "Krankenhaus über die Vene. Viel Trinken und Fiebersenkung "
                    "unterstützen. Ein Harnstau muss rasch beseitigt werden."
                ),
                "red_flags": (
                    "Hohes Fieber mit Schüttelfrost, Benommenheit, sehr schneller Puls oder "
                    "niedriger Blutdruck können auf eine Sepsis hinweisen – sofort Notruf "
                    "144."
                ),
            },
            "further_reading": [medlineplus("urinarytractinfections", "Urinary tract infections")],
        },
        {
            "title": "Prostatakrebs",
            "doc_type": "Diagnose",
            "expected_category": "Urologie",
            "term_en": "Prostate cancer",
            "icd11_code": "2C82",
            "medications": ["bicalutamide"],
            "sections": {
                "definition": (
                    "Prostatakrebs ist ein bösartiger Tumor der Vorsteherdrüse und die "
                    "häufigste Krebserkrankung bei Männern."
                ),
                "symptoms": (
                    "Im Frühstadium gibt es meist keine Beschwerden. Später können "
                    "Probleme beim Wasserlassen, Blut im Urin oder Samen, Rücken- und "
                    "Knochenschmerzen auftreten."
                ),
                "causes": (
                    "Das Risiko steigt mit dem Alter. Familiäre Häufung und erbliche "
                    "Veranlagung spielen eine Rolle; weitere Ursachen sind nicht sicher "
                    "bekannt."
                ),
                "diagnostics": (
                    "Der Urologe tastet die Prostata ab und bestimmt gegebenenfalls den PSA-"
                    "Wert im Blut. Bei Auffälligkeiten folgen Magnetresonanztomografie und "
                    "eine Gewebeprobe. Der PSA-Test hat Vor- und Nachteile und wird "
                    "individuell besprochen."
                ),
                "therapy": (
                    "Je nach Ausbreitung und Aggressivität kommen aktive Überwachung, "
                    "Operation, Bestrahlung oder eine Hormontherapie in Frage. Über das "
                    "Vorgehen entscheidet ein ärztliches Team gemeinsam mit dem Patienten."
                ),
                "red_flags": (
                    "Starke neue Rückenschmerzen mit Taubheit oder Schwäche der Beine, "
                    "Probleme mit Blase und Darm oder Harnverhalt sind dringend – sofort "
                    "ärztliche Hilfe, bei Lähmungen Notruf 144."
                ),
            },
            "further_reading": [medlineplus("prostatecancer", "Prostate cancer")],
        },
    ],
    {
        "Harninkontinenz (Blasenschwäche)": {
            "title_en": "Urinary incontinence (weak bladder)",
            "sections_en": {
                "definition": (
                    "In urinary incontinence urine leaks involuntarily, because the "
                    "bladder cannot hold the urine reliably."
                ),
                "symptoms": (
                    "In stress incontinence urine leaks when coughing, sneezing or "
                    "lifting. In urge incontinence a sudden strong urge to urinate occurs "
                    "that cannot be held back."
                ),
                "causes": (
                    "A weakened pelvic floor after childbirth, in old age or after "
                    "operations, an overactive bladder, an enlarged prostate, urinary "
                    "tract infections, medicines and nerve diseases can be behind it."
                ),
                "diagnostics": (
                    "The urologist asks about the amount drunk, frequency and triggers, "
                    "often with a bladder diary. Urine tests, an ultrasound and, if "
                    "needed, a measurement of the bladder pressure follow."
                ),
                "therapy": (
                    "Pelvic floor training, bladder training, weight loss and adjusted "
                    "drinking amounts often help. Medicines calm an overactive bladder; "
                    "in stress incontinence an operation can make sense."
                ),
                "red_flags": (
                    "Sudden bladder weakness with numbness in the genital area, leg "
                    "weakness or back pain can point to nerve damage – have it checked at "
                    "once, and call the emergency number 144 (Austria) for paralysis."
                ),
            },
            "keywords_en": [
                "Urinary incontinence",
                "Bladder",
                "Pelvic floor",
                "Urge",
                "Bladder diary",
                "Urologist",
            ],
        },
        "Akute Nierenbeckenentzündung (Pyelonephritis)": {
            "title_en": "Acute kidney infection (pyelonephritis)",
            "sections_en": {
                "definition": (
                    "In pyelonephritis the renal pelvis and kidney tissue are inflamed by "
                    "bacteria, usually as a result of an ascending urinary tract "
                    "infection."
                ),
                "symptoms": (
                    "Fever with shivering, pain in the flank, a back that is tender to "
                    "tapping, burning on urination and a general feeling of illness."
                ),
                "causes": (
                    "Usually gut bacteria, above all E. coli, ascend through the urethra "
                    "and the bladder to the kidney. A blocked urine flow from kidney "
                    "stones, diabetes and pregnancy raise the risk."
                ),
                "diagnostics": (
                    "A urine test with urine culture, a blood test for inflammation "
                    "markers and an ultrasound of the kidneys to rule out a blocked urine "
                    "flow."
                ),
                "therapy": (
                    "It is treated with an antibiotic, in severe cases in hospital "
                    "through a vein. Drinking plenty and lowering the fever support the "
                    "treatment. A blockage of the urine flow must be removed quickly."
                ),
                "red_flags": (
                    "High fever with shivering, drowsiness, a very fast pulse or low "
                    "blood pressure can point to sepsis – call the emergency number 144 "
                    "(Austria) at once."
                ),
            },
            "keywords_en": [
                "Kidney infection",
                "Pyelonephritis",
                "Flank pain",
                "Fever",
                "Antibiotic",
                "Urine culture",
            ],
        },
        "Prostatakrebs": {
            "title_en": "Prostate cancer",
            "sections_en": {
                "definition": (
                    "Prostate cancer is a malignant tumour of the prostate gland and the "
                    "most common cancer in men."
                ),
                "symptoms": (
                    "In the early stage there are usually no symptoms. Later, problems "
                    "passing urine, blood in the urine or semen, and back and bone pain "
                    "can occur."
                ),
                "causes": (
                    "The risk rises with age. Cases in the family and inherited tendency "
                    "play a role; other causes are not known for certain."
                ),
                "diagnostics": (
                    "The urologist feels the prostate and, where appropriate, measures "
                    "the PSA value in the blood. If there are abnormalities, magnetic "
                    "resonance imaging and a tissue sample follow. The PSA test has "
                    "advantages and disadvantages and is discussed individually."
                ),
                "therapy": (
                    "Depending on spread and aggressiveness, active surveillance, "
                    "surgery, radiotherapy or hormone therapy come into question. A "
                    "medical team decides on the approach together with the patient."
                ),
                "red_flags": (
                    "New severe back pain with numbness or weakness of the legs, problems "
                    "with bladder and bowel or being unable to pass urine are urgent – "
                    "seek medical help at once, and call the emergency number 144 "
                    "(Austria) for paralysis."
                ),
            },
            "keywords_en": [
                "Prostate cancer",
                "Prostate",
                "PSA",
                "Urologist",
                "Radiotherapy",
                "Active surveillance",
            ],
        },
    },
)
