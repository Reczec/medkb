from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Erkältung (grippaler Infekt)",
        "doc_type": "Beschreibung",
        "expected_category": "Allgemeinmedizin",
        "term_en": "Common cold",
        "icd11_code": "CA00",
        "medications": ["acetaminophen"],
        "sections": {
            "definition": (
                "Eine Erkältung ist ein harmloser, durch Viren ausgelöster grippaler Infekt, "
                "der in der Regel nach sieben bis zehn Tagen von selbst abklingt."
            ),
            "symptoms": (
                "Typisch sind Schnupfen, Halskratzen, Husten, Abgeschlagenheit und leichtes Fieber."
            ),
            "therapy": (
                "Behandelt werden die Symptome: ausreichend trinken, sich schonen, bei Bedarf "
                "fiebersenkende Mittel. Antibiotika helfen gegen Erkältungsviren nicht."
            ),
            "red_flags": (
                "Bei hohem Fieber, Atemnot, Brustschmerzen oder einer Verschlechterung nach "
                "einigen Tagen sollte ärztlicher Rat beim Hausarzt eingeholt werden."
            ),
        },
        "further_reading": [medlineplus("commoncold", "Common Cold")],
    },
    {
        "title": "Impfungen und Vorsorgeuntersuchungen im Erwachsenenalter",
        "doc_type": "Leitlinie",
        "expected_category": "Allgemeinmedizin",
        "term_en": "Adult vaccination",
        "sections": {
            "definition": (
                "Regelmäßige Vorsorgeuntersuchungen und Impfungen helfen, Erkrankungen zu "
                "verhindern oder früh zu erkennen."
            ),
            "diagnostics": (
                "In Österreich steht Erwachsenen die kostenlose Vorsorgeuntersuchung beim "
                "Hausarzt zur Verfügung, mit Fragen zum Allgemeinbefinden, Untersuchung und "
                "Laborwerten."
            ),
            "therapy": (
                "Der österreichische Impfplan empfiehlt Auffrischungen, zum Beispiel gegen "
                "Tetanus und Diphtherie, sowie weitere Impfungen wie gegen Grippe je nach "
                "Alter und Risikofaktoren."
            ),
        },
        "further_reading": [
            medlineplus("vaccines", "Vaccines"),
            who("immunization-coverage", "Immunization coverage"),
        ],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Erkältung (grippaler Infekt)": {
            "title_en": "Common cold",
            "sections_en": {
                "definition": (
                    "A cold is a harmless viral infection that usually clears up by itself "
                    "after seven to ten days."
                ),
                "symptoms": (
                    "Typical are a runny nose, a scratchy throat, cough, tiredness and mild fever."
                ),
                "therapy": (
                    "The symptoms are treated: drink enough, rest and, if needed, "
                    "fever-lowering medicines. Antibiotics do not help against cold viruses."
                ),
                "red_flags": (
                    "With high fever, shortness of breath, chest pain or a worsening after a "
                    "few days, seek advice from your family doctor."
                ),
            },
            "keywords_en": ["Cold", "Runny nose", "Cough", "Sore throat", "Fever", "Virus"],
        },
        "Impfungen und Vorsorgeuntersuchungen im Erwachsenenalter": {
            "title_en": "Vaccinations and check-ups for adults",
            "sections_en": {
                "definition": (
                    "Regular check-ups and vaccinations help to prevent illnesses or to "
                    "detect them early."
                ),
                "diagnostics": (
                    "In Austria, adults can use the free preventive check-up at the family "
                    "doctor, with questions about general well-being, an examination and "
                    "laboratory values."
                ),
                "therapy": (
                    "The Austrian vaccination schedule recommends boosters, for example "
                    "against tetanus and diphtheria, as well as further vaccinations such as "
                    "against flu depending on age and risk factors."
                ),
            },
            "keywords_en": [
                "Vaccination",
                "Check-up",
                "Prevention",
                "Tetanus",
                "Flu",
                "Family doctor",
            ],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Müdigkeit und Erschöpfung",
            "doc_type": "Symptom",
            "expected_category": "Allgemeinmedizin",
            "term_en": "Fatigue",
            "icd11_code": "MG22",
            "medications": [],
            "sections": {
                "definition": (
                    "Anhaltende Müdigkeit und Erschöpfung bedeuten eine Mattigkeit, die sich "
                    "durch Schlaf und Ruhe nicht ausreichend bessert und den Alltag "
                    "beeinträchtigt."
                ),
                "symptoms": (
                    "Betroffene fühlen sich antriebslos, schwach und ausgelaugt, können sich "
                    "schlecht konzentrieren und sind gereizt. Oft kommen Schlafprobleme "
                    "und Kopf- oder Muskelschmerzen dazu."
                ),
                "causes": (
                    "Mögliche Ursachen sind Schlafmangel, Stress, Infekte, Nährstoffmangel, "
                    "hormonelle und Stoffwechselerkrankungen, Depression, Medikamente und "
                    "Schlafapnoe. Häufig wirken mehrere Faktoren zusammen."
                ),
                "diagnostics": (
                    "Die Hausärztin fragt nach Schlaf, Belastungen und Vorerkrankungen. Eine "
                    "Blutuntersuchung prüft unter anderem Blutbild, Entzündungswerte und "
                    "weitere Laborwerte."
                ),
                "therapy": (
                    "Regelmäßiger Schlaf, Bewegung, Entspannung, ausgewogene Ernährung und "
                    "weniger Alkohol helfen. Gefundene Ursachen wie ein Mangelzustand werden "
                    "gezielt behandelt."
                ),
                "red_flags": (
                    "Ungewollter Gewichtsverlust, Nachtschweiß, Fieber, Atemnot, "
                    "Brustschmerz oder Gedanken, sich das Leben zu nehmen verlangen rasche "
                    "Abklärung; Telefonseelsorge 142, in akuter Gefahr Notruf 144."
                ),
            },
            "further_reading": [medlineplus("fatigue", "Fatigue")],
        },
        {
            "title": "Fieber bei Erwachsenen",
            "doc_type": "Symptom",
            "expected_category": "Allgemeinmedizin",
            "term_en": "Fever",
            "icd11_code": "MG26",
            "medications": ["paracetamol", "ibuprofen"],
            "sections": {
                "definition": (
                    "Fieber ist eine Erhöhung der Körpertemperatur auf über 38 Grad Celsius "
                    "und meist ein Zeichen dafür, dass sich der Körper gegen einen Infekt "
                    "wehrt."
                ),
                "symptoms": (
                    "Hitzegefühl, Schüttelfrost, Schwitzen, Kopf- und Gliederschmerzen, "
                    "Abgeschlagenheit und Appetitlosigkeit. Die Herzfrequenz und die "
                    "Atmung sind meist beschleunigt."
                ),
                "causes": (
                    "Meist stecken Virusinfekte wie Erkältung oder Grippe dahinter, "
                    "seltener bakterielle Infektionen, Entzündungen, Medikamente oder "
                    "andere Erkrankungen."
                ),
                "diagnostics": (
                    "Die Hausärztin misst die Temperatur, untersucht Rachen, Lunge und "
                    "Bauch und veranlasst bei Bedarf eine Blut- oder Urinuntersuchung."
                ),
                "therapy": (
                    "Bettruhe, viel Trinken, leichte Kost und Wadenwickel helfen. "
                    "Fiebersenkende Mittel wie Paracetamol können Beschwerden lindern; "
                    "Fieber selbst muss nicht immer gesenkt werden."
                ),
                "red_flags": (
                    "Fieber über 40 Grad, Nackensteifigkeit, Verwirrtheit, Atemnot, ein "
                    "neuer Hautausschlag, anhaltendes Fieber über drei Tage oder Fieber "
                    "nach einer Reise erfordern ärztliche Abklärung; bei Bewusstseins- "
                    "trübung Notruf 144."
                ),
            },
            "further_reading": [medlineplus("fever", "Fever")],
        },
        {
            "title": "Vorsorgeuntersuchung (Gesundheitscheck)",
            "doc_type": "Leitlinie",
            "expected_category": "Allgemeinmedizin",
            "term_en": "Preventive health check",
            "sections": {
                "definition": (
                    "Die Vorsorgeuntersuchung ist ein kostenloser Gesundheitscheck bei der "
                    "Hausärztin oder dem Hausarzt, mit dem Risikofaktoren und "
                    "Erkrankungen früh erkannt werden sollen."
                ),
                "diagnostics": (
                    "Enthalten sind ein Gespräch zur Vorgeschichte, die Messung von "
                    "Blutdruck, Größe und Gewicht, eine Blutuntersuchung (Blutzucker, "
                    "Blutfette) sowie die Überprüfung des Impfstatus. Je nach Alter kommen "
                    "weitere Untersuchungen dazu, etwa Darmkrebs- und Hautkrebsvorsorge."
                ),
                "therapy": (
                    "Auffällige Werte werden besprochen und behandelt. Beratung zu "
                    "Ernährung, Bewegung, Rauchverzicht und Alkohol gehört dazu. Die "
                    "Untersuchung wird in der Regel einmal jährlich angeboten."
                ),
            },
            "further_reading": [medlineplus("healthcheckup", "Health checkup")],
        },
        {
            "title": "Reiseimpfungen und Reiseapotheke",
            "doc_type": "Leitlinie",
            "expected_category": "Allgemeinmedizin",
            "term_en": "Travel vaccination",
            "sections": {
                "definition": (
                    "Vor Reisen in Länder mit anderem Infektionsrisiko schützen Impfungen und "
                    "eine gut gepackte Reiseapotheke vor vermeidbaren Erkrankungen."
                ),
                "diagnostics": (
                    "Idealerweise vier bis sechs Wochen vor der Abreise bespricht die "
                    "Hausärztin oder eine reisemedizinische Beratungsstelle Reiseziel, "
                    "Reisedauer und Vorerkrankungen und prüft den Impfplan. Je nach Land "
                    "kommen Hepatitis A und B, Typhus, Tollwut, Gelbfieber oder "
                    "Malariaprophylaxe in Frage."
                ),
                "therapy": (
                    "In die Reiseapotheke gehören Schmerz- und Fiebermittel, Mittel gegen "
                    "Durchfall und Übelkeit, Elektrolytpulver, Wundversorgung, "
                    "Insektenschutz, Sonnenschutz und persönliche Dauermedikamente. Auf "
                    "sauberes Trinkwasser und Lebensmittelhygiene achten."
                ),
                "red_flags": (
                    "Fieber nach der Rückkehr aus den Tropen, anhaltender Durchfall oder "
                    "Atemnot sollten umgehend ärztlich abgeklärt werden; bei "
                    "Bewusstseinsstörung Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("travelershealth", "Traveler's health"),
                who("malaria", "Malaria"),
            ],
        },
    ],
    {
        "Müdigkeit und Erschöpfung": {
            "title_en": "Tiredness and exhaustion",
            "sections_en": {
                "definition": (
                    "Persistent tiredness and exhaustion mean a weariness that sleep and "
                    "rest do not improve enough and that affects everyday life."
                ),
                "symptoms": (
                    "People feel listless, weak and drained, have trouble concentrating "
                    "and are irritable. Sleep problems and headaches or muscle pain are "
                    "often added."
                ),
                "causes": (
                    "Possible causes are lack of sleep, stress, infections, nutrient "
                    "deficiency, hormonal and metabolic diseases, depression, medicines and "
                    "sleep apnoea. Often several factors act together."
                ),
                "diagnostics": (
                    "The family doctor asks about sleep, strains and previous illnesses. "
                    "A blood test checks, among other things, the blood count, "
                    "inflammation markers and further laboratory values."
                ),
                "therapy": (
                    "Regular sleep, exercise, relaxation, a balanced diet and less "
                    "alcohol help. Causes that are found, such as a deficiency state, are "
                    "treated specifically."
                ),
                "red_flags": (
                    "Unintended weight loss, night sweats, fever, breathlessness, chest "
                    "pain or thoughts of taking one's own life need prompt assessment; "
                    "telephone counselling 142 (Austria), and in acute danger the "
                    "emergency number 144."
                ),
            },
            "keywords_en": [
                "Tiredness",
                "Exhaustion",
                "Fatigue",
                "Iron deficiency",
                "Sleep",
                "Stress",
            ],
        },
        "Fieber bei Erwachsenen": {
            "title_en": "Fever in adults",
            "sections_en": {
                "definition": (
                    "Fever is a rise in body temperature above 38 degrees Celsius and "
                    "usually a sign that the body is fighting an infection."
                ),
                "symptoms": (
                    "A feeling of heat, shivering, sweating, headache and aching limbs, "
                    "tiredness and loss of appetite. Heart rate and breathing are usually "
                    "faster."
                ),
                "causes": (
                    "Viral infections such as a cold or flu are usually behind it, less "
                    "often bacterial infections, inflammation, medicines or other "
                    "diseases."
                ),
                "diagnostics": (
                    "The family doctor measures the temperature, examines the throat, "
                    "lungs and abdomen and, if needed, arranges a blood or urine test."
                ),
                "therapy": (
                    "Bed rest, plenty of fluids, light food and calf compresses help. "
                    "Fever-lowering medicines such as paracetamol can ease the symptoms; "
                    "the fever itself does not always have to be lowered."
                ),
                "red_flags": (
                    "Fever above 40 degrees, a stiff neck, confusion, breathlessness, a "
                    "new skin rash, fever lasting more than three days or fever after a "
                    "journey need medical assessment; for clouding of consciousness call "
                    "the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Fever",
                "Temperature",
                "Infection",
                "Paracetamol",
                "Family doctor",
                "Shivering",
            ],
        },
        "Vorsorgeuntersuchung (Gesundheitscheck)": {
            "title_en": "Preventive examination (health check)",
            "sections_en": {
                "definition": (
                    "The preventive examination is a free health check with the family "
                    "doctor that aims to find risk factors and diseases early."
                ),
                "diagnostics": (
                    "It includes a conversation about the history, measurement of blood "
                    "pressure, height and weight, a blood test (blood sugar, blood fats) "
                    "and a check of vaccination status. Depending on age, further "
                    "examinations are added, such as bowel cancer and skin cancer "
                    "screening."
                ),
                "therapy": (
                    "Abnormal values are discussed and treated. Advice on diet, exercise, "
                    "giving up smoking and alcohol is part of it. The examination is "
                    "usually offered once a year."
                ),
            },
            "keywords_en": [
                "Check-up",
                "Prevention",
                "Screening",
                "Family doctor",
                "Blood pressure",
                "Vaccination status",
            ],
        },
        "Reiseimpfungen und Reiseapotheke": {
            "title_en": "Travel vaccinations and travel first-aid kit",
            "sections_en": {
                "definition": (
                    "Before travelling to countries with a different risk of infection, "
                    "vaccinations and a well-packed first-aid kit protect against "
                    "avoidable illnesses."
                ),
                "diagnostics": (
                    "Ideally four to six weeks before departure, the family doctor or a "
                    "travel medicine clinic discusses destination, length of stay and "
                    "pre-existing conditions and checks the vaccination schedule. "
                    "Depending on the country, hepatitis A and B, typhoid, rabies, yellow "
                    "fever or malaria prevention come into question."
                ),
                "therapy": (
                    "The first-aid kit should contain pain and fever relievers, "
                    "medicines for diarrhoea and nausea, electrolyte powder, wound care, "
                    "insect protection, sun protection and personal regular medicines. "
                    "Pay attention to clean drinking water and food hygiene."
                ),
                "red_flags": (
                    "Fever after returning from the tropics, persistent diarrhoea or "
                    "breathlessness should be checked by a doctor promptly; for "
                    "disturbance of consciousness call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Travel vaccination",
                "Travel medicine",
                "Malaria prevention",
                "First-aid kit",
                "Vaccination schedule",
                "Hepatitis A",
            ],
        },
    },
)
