from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Lyme-Borreliose": {
            "title_en": "Lyme disease",
            "sections_en": {
                "definition": "Lyme disease is a bacterial infection transmitted by a tick bite.",
                "symptoms": (
                    "The most common sign is the migrating erythema, a ring-shaped reddening "
                    "spreading around the bite. Later, nerves, joints or the heart can be "
                    "affected."
                ),
                "causes": (
                    "The causative agents are bacteria of the genus Borrelia, which infected "
                    "ticks usually transmit only after many hours of feeding."
                ),
                "diagnostics": (
                    "The migrating erythema is enough for the diagnosis. For later signs, "
                    "antibody tests in the blood help."
                ),
                "therapy": (
                    "Antibiotics reliably cure the infection in early stages. Ticks should be "
                    "removed quickly; a vaccination exists only against tick-borne "
                    "encephalitis."
                ),
                "red_flags": (
                    "Facial paralysis, severe headache with a stiff neck or an irregular "
                    "heartbeat after a tick bite should be assessed promptly."
                ),
            },
            "keywords_en": [
                "Lyme disease",
                "Tick bite",
                "Borrelia",
                "Erythema",
                "Antibiotics",
                "Nerves",
            ],
        },
        "Influenza (echte Grippe)": {
            "title_en": "Influenza (flu)",
            "sections_en": {
                "definition": (
                    "Influenza is an acute infection of the airways caused by influenza "
                    "viruses that cause waves mainly in the winter months."
                ),
                "symptoms": (
                    "Typical is a sudden onset with high fever, headache and aching limbs, "
                    "dry cough and a strong feeling of illness."
                ),
                "causes": (
                    "The viruses spread by droplets and hands and are highly contagious; they "
                    "change constantly."
                ),
                "diagnostics": (
                    "During a flu wave the diagnosis is often made clinically; a swab with a "
                    "rapid or PCR test detects the virus."
                ),
                "therapy": (
                    "Rest, fluids and fever-lowering medicines help. Antiviral medicines may "
                    "be considered early for people at risk. The yearly vaccination protects."
                ),
                "red_flags": (
                    "Shortness of breath, chest pain, confusion or a renewed rise in fever "
                    "after improvement can point to complications – seek medical help, in an "
                    "emergency call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": ["Influenza", "Flu", "Fever", "Cough", "Vaccination", "Virus"],
        },
        "Sepsis (Blutvergiftung)": {
            "title_en": "Sepsis (blood poisoning)",
            "sections_en": {
                "definition": (
                    "Sepsis is a life-threatening faulty reaction of the body to an infection "
                    "that damages organs."
                ),
                "symptoms": (
                    "Warning signs are fever or a low body temperature, a fast pulse and fast "
                    "breathing, confusion, cold and mottled skin and a severe feeling of "
                    "illness."
                ),
                "causes": (
                    "The starting point is usually an infection of the lungs, urinary tract "
                    "or abdomen. Older people, small children and people with a weakened "
                    "immune system are particularly at risk."
                ),
                "diagnostics": (
                    "In hospital, vital signs, blood values such as lactate and blood "
                    "cultures are determined to find the germ and the source."
                ),
                "therapy": (
                    "Decisive is the quick start of antibiotics and fluids, often in "
                    "intensive care; the source of infection is treated."
                ),
                "red_flags": (
                    "With suspected sepsis every hour counts – call the emergency number 144 "
                    "(Austria) at once."
                ),
            },
            "keywords_en": [
                "Sepsis",
                "Blood poisoning",
                "Infection",
                "Fever",
                "Emergency",
                "Antibiotics",
            ],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "COVID-19",
            "doc_type": "Diagnose",
            "expected_category": "Infektiologie",
            "term_en": "COVID-19",
            "icd11_code": "RA01",
            "medications": ["nirmatrelvir", "paracetamol"],
            "sections": {
                "definition": (
                    "COVID-19 ist eine durch das Coronavirus SARS-CoV-2 ausgelöste "
                    "Infektionskrankheit, die vor allem die Atemwege betrifft."
                ),
                "symptoms": (
                    "Husten, Halsschmerzen, Schnupfen, Fieber, Kopf- und Gliederschmerzen "
                    "sowie Müdigkeit. Der Geruchs- und Geschmackssinn kann vorübergehend "
                    "ausfallen. Die meisten Verläufe sind mild, schwere Verläufe treten "
                    "vor allem bei Risikogruppen auf."
                ),
                "causes": (
                    "Das Virus wird hauptsächlich über Tröpfchen und kleinste Partikel in "
                    "der Luft übertragen. Höheres Alter, Vorerkrankungen und eine "
                    "geschwächte Abwehr erhöhen das Risiko eines schweren Verlaufs."
                ),
                "diagnostics": (
                    "Ein Antigen-Schnelltest oder ein PCR-Test aus einem Abstrich aus "
                    "Nase oder Rachen weist das Virus nach."
                ),
                "therapy": (
                    "Bei milden Verläufen helfen Ruhe, Flüssigkeit sowie Schmerz- und "
                    "Fiebermittel. Bei Risikopatienten können frühzeitig antivirale "
                    "Medikamente eingesetzt werden. Impfungen verringern das Risiko eines "
                    "schweren Verlaufs."
                ),
                "red_flags": (
                    "Atemnot, anhaltender Druck oder Schmerz in der Brust, Verwirrtheit, "
                    "bläuliche Lippen oder ein sehr hohes Fieber sind Notfallzeichen – "
                    "sofort Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("covid19coronavirusdisease2019", "COVID-19"),
                who("coronavirus-disease-(covid-19)", "Coronavirus disease (COVID-19)"),
            ],
        },
        {
            "title": "Tuberkulose",
            "doc_type": "Diagnose",
            "expected_category": "Infektiologie",
            "term_en": "Tuberculosis",
            "icd11_code": "1B10",
            "medications": ["isoniazid", "rifampicin"],
            "sections": {
                "definition": (
                    "Die Tuberkulose ist eine bakterielle Infektionskrankheit, die meist die "
                    "Lunge befällt, aber auch andere Organe betreffen kann."
                ),
                "symptoms": (
                    "Länger als drei Wochen anhaltender Husten, teils mit Auswurf oder Blut, "
                    "Nachtschweiß, Fieber, Gewichtsverlust und Müdigkeit."
                ),
                "causes": (
                    "Verursacht wird sie durch Mycobacterium tuberculosis, das beim Husten "
                    "über winzige Tröpfchen übertragen wird. Nicht jede Ansteckung führt zur "
                    "Erkrankung; eine geschwächte Abwehr erhöht das Risiko."
                ),
                "diagnostics": (
                    "Eine Röntgenaufnahme des Brustkorbs, die Untersuchung von Auswurf auf "
                    "die Bakterien sowie Blut- oder Hauttests sichern die Diagnose. Die "
                    "Erkrankung ist meldepflichtig."
                ),
                "therapy": (
                    "Die Behandlung dauert mehrere Monate und kombiniert mehrere "
                    "Antibiotika. Wichtig ist die konsequente Einnahme, da sonst "
                    "resistente Keime entstehen. Ansteckende Patientinnen und Patienten "
                    "werden zunächst isoliert."
                ),
                "red_flags": (
                    "Bluthusten, Atemnot, hohes Fieber oder starke Brustschmerzen "
                    "erfordern sofortige ärztliche Abklärung – bei starker Atemnot oder "
                    "größeren Blutmengen Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("tuberculosis", "Tuberculosis"),
                who("tuberculosis", "Tuberculosis"),
            ],
        },
        {
            "title": "Hepatitis B",
            "doc_type": "Diagnose",
            "expected_category": "Infektiologie",
            "term_en": "Hepatitis B",
            "icd11_code": "1E51.0",
            "medications": ["tenofovir", "entecavir"],
            "sections": {
                "definition": (
                    "Hepatitis B ist eine durch das Hepatitis-B-Virus verursachte "
                    "Leberentzündung, die ausheilen oder chronisch werden kann."
                ),
                "symptoms": (
                    "Viele Infizierte haben keine Beschwerden. Möglich sind Müdigkeit, "
                    "Übelkeit, Bauchschmerzen, dunkler Urin und eine Gelbfärbung von Haut "
                    "und Augen."
                ),
                "causes": (
                    "Das Virus wird über Blut und Körperflüssigkeiten übertragen, etwa bei "
                    "ungeschütztem Geschlechtsverkehr, gemeinsam benutzten Nadeln oder von der "
                    "Mutter auf das Neugeborene."
                ),
                "diagnostics": (
                    "Blutuntersuchungen auf Virusbestandteile und Antikörper zeigen, ob eine "
                    "akute oder chronische Infektion oder ein Impfschutz vorliegt. Leberwerte "
                    "und Ultraschall beurteilen den Leberschaden."
                ),
                "therapy": (
                    "Akute Infektionen heilen meist von selbst aus. Chronische Verläufe "
                    "werden mit antiviralen Medikamenten behandelt und regelmäßig "
                    "kontrolliert. Eine Impfung schützt sehr zuverlässig."
                ),
                "red_flags": (
                    "Zunehmende Gelbsucht, Verwirrtheit, starke Schläfrigkeit, Blutungen "
                    "oder ein geschwollener Bauch können auf ein Leberversagen hinweisen – "
                    "sofort Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("hepatitisb", "Hepatitis B"),
                who("hepatitis-b", "Hepatitis B"),
            ],
        },
    ],
    {
        "COVID-19": {
            "title_en": "COVID-19",
            "sections_en": {
                "definition": (
                    "COVID-19 is an infectious disease caused by the coronavirus "
                    "SARS-CoV-2 that mainly affects the airways."
                ),
                "symptoms": (
                    "Cough, sore throat, a runny nose, fever, headache and aching limbs "
                    "and tiredness. The sense of smell and taste can be lost for a while. "
                    "Most courses are mild; severe courses occur mainly in risk groups."
                ),
                "causes": (
                    "The virus spreads mainly through droplets and tiny particles in the "
                    "air. Higher age, pre-existing conditions and weakened defences raise "
                    "the risk of a severe course."
                ),
                "diagnostics": (
                    "A rapid antigen test or a PCR test on a swab from the nose or throat "
                    "detects the virus."
                ),
                "therapy": (
                    "In mild courses rest, fluids and pain and fever relievers help. In "
                    "people at risk, antiviral medicines can be used early. Vaccinations "
                    "reduce the risk of a severe course."
                ),
                "red_flags": (
                    "Breathlessness, lasting pressure or pain in the chest, confusion, "
                    "bluish lips or a very high fever are emergency signs – call the "
                    "emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "COVID-19",
                "Coronavirus",
                "SARS-CoV-2",
                "Cough",
                "Fever",
                "Vaccination",
            ],
        },
        "Tuberkulose": {
            "title_en": "Tuberculosis",
            "sections_en": {
                "definition": (
                    "Tuberculosis is a bacterial infectious disease that mostly affects "
                    "the lungs but can also involve other organs."
                ),
                "symptoms": (
                    "A cough lasting longer than three weeks, sometimes with sputum or "
                    "blood, night sweats, fever, weight loss and tiredness."
                ),
                "causes": (
                    "It is caused by Mycobacterium tuberculosis, which spreads through "
                    "tiny droplets when coughing. Not every infection leads to disease; "
                    "weakened defences raise the risk."
                ),
                "diagnostics": (
                    "A chest X-ray, examination of sputum for the bacteria, and blood or "
                    "skin tests confirm the diagnosis. The disease has to be reported."
                ),
                "therapy": (
                    "Treatment lasts several months and combines several antibiotics. "
                    "Taking them consistently is important, since otherwise resistant "
                    "germs develop. Infectious patients are isolated at first."
                ),
                "red_flags": (
                    "Coughing up blood, breathlessness, high fever or severe chest pain "
                    "need immediate medical assessment – for severe breathlessness or "
                    "larger amounts of blood call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Tuberculosis",
                "TB",
                "Cough",
                "Night sweats",
                "Antibiotics",
                "Chest X-ray",
            ],
        },
        "Hepatitis B": {
            "title_en": "Hepatitis B",
            "sections_en": {
                "definition": (
                    "Hepatitis B is an inflammation of the liver caused by the hepatitis "
                    "B virus, which can heal or become chronic."
                ),
                "symptoms": (
                    "Many infected people have no symptoms. Possible are tiredness, "
                    "nausea, abdominal pain, dark urine and a yellow colour of the skin "
                    "and eyes."
                ),
                "causes": (
                    "The virus is spread through blood and body fluids, for example "
                    "through unprotected sex, shared needles or from mother to newborn."
                ),
                "diagnostics": (
                    "Blood tests for virus components and antibodies show whether there "
                    "is an acute or chronic infection or vaccine protection. Liver values "
                    "and ultrasound assess the liver damage."
                ),
                "therapy": (
                    "Acute infections usually heal on their own. Chronic courses are "
                    "treated with antiviral medicines and checked regularly. A "
                    "vaccination protects very reliably."
                ),
                "red_flags": (
                    "Increasing jaundice, confusion, marked drowsiness, bleeding or a "
                    "swollen abdomen can point to liver failure – call the emergency "
                    "number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Hepatitis B",
                "Liver",
                "Jaundice",
                "Vaccination",
                "Antiviral",
                "Blood test",
            ],
        },
    },
)
