from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Asthma bronchiale",
        "doc_type": "Diagnose",
        "expected_category": "Pneumologie",
        "term_en": "Asthma",
        "icd11_code": "CA23",
        "medications": ["albuterol", "budesonide"],
        "sections": {
            "definition": (
                "Asthma bronchiale ist eine chronische Entzündung der Atemwege, bei der sich "
                "die Bronchien anfallsartig verengen."
            ),
            "symptoms": (
                "Typisch sind anfallsartige Atemnot, pfeifende Atmung (Giemen), "
                "Engegefühl in der Brust und Husten, besonders nachts oder bei Belastung."
            ),
            "causes": (
                "Allergien gegen Pollen, Hausstaubmilben oder Tierhaare, Atemwegsinfekte, "
                "kalte Luft, Rauch und körperliche Anstrengung können Anfälle auslösen."
            ),
            "diagnostics": (
                "Eine Lungenfunktionsprüfung (Spirometrie) zeigt die Verengung der "
                "Atemwege und ihre Besserung nach einem bronchienerweiternden Spray."
            ),
            "therapy": (
                "Inhalierbares Kortison wirkt der Entzündung entgegen, kurz wirksame "
                "Bronchienerweiterer helfen im Anfall. Auslöser sollten gemieden werden."
            ),
            "red_flags": (
                "Schwere Atemnot, Sprechen nur in kurzen Sätzen, bläuliche Lippen oder fehlende "
                "Besserung durch das Notfallspray: sofort Notruf 144."
            ),
        },
        "further_reading": [medlineplus("asthma", "Asthma"), who("asthma", "Asthma")],
    },
    {
        "title": "Chronisch obstruktive Lungenerkrankung (COPD)",
        "doc_type": "Diagnose",
        "expected_category": "Pneumologie",
        "term_en": "Chronic obstructive pulmonary disease",
        "icd11_code": "CA22",
        "medications": ["tiotropium"],
        "sections": {
            "definition": (
                "Die COPD ist eine fortschreitende Lungenerkrankung mit dauerhaft verengten "
                "Atemwegen und geschädigtem Lungengewebe."
            ),
            "symptoms": (
                "Leitsymptome sind Husten mit Auswurf und Atemnot, zunächst bei Belastung, "
                "später auch in Ruhe."
            ),
            "causes": (
                "Hauptursache ist langjähriges Rauchen; auch Feinstaub und Schadstoffe am "
                "Arbeitsplatz tragen bei."
            ),
            "diagnostics": (
                "Die Lungenfunktionsprüfung bestätigt die Verengung der Atemwege, die sich "
                "anders als beim Asthma nicht vollständig zurückbildet."
            ),
            "therapy": (
                "Am wichtigsten ist der Rauchstopp. Inhalierte Bronchienerweiterer, "
                "Lungensport und Impfungen gegen Grippe und Pneumokokken verbessern den "
                "Verlauf."
            ),
            "red_flags": (
                "Zunehmende Atemnot, Verwirrtheit oder bläuliche Lippen bei einer "
                "Verschlechterung erfordern sofort ärztliche Hilfe, bei Atemnot in Ruhe "
                "Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("copd", "COPD"),
            who(
                "chronic-obstructive-pulmonary-disease-(copd)",
                "Chronic obstructive pulmonary disease",
            ),
        ],
    },
    {
        "title": "Lungenentzündung (Pneumonie)",
        "doc_type": "Diagnose",
        "expected_category": "Pneumologie",
        "term_en": "Pneumonia",
        "icd11_code": "CA40",
        "medications": ["amoxicillin"],
        "sections": {
            "definition": (
                "Eine Lungenentzündung ist eine Entzündung des Lungengewebes, meist durch "
                "Bakterien oder Viren."
            ),
            "symptoms": (
                "Typisch sind Fieber, Husten mit Auswurf, Atemnot und Schmerzen beim Atmen. "
                "Ältere Menschen zeigen oft nur Schwäche oder Verwirrtheit."
            ),
            "causes": (
                "Häufigster bakterieller Erreger sind Pneumokokken. Ein höheres Alter, "
                "chronische Lungenerkrankungen und ein geschwächtes Immunsystem erhöhen das "
                "Risiko."
            ),
            "diagnostics": (
                "Abhören der Lunge, Röntgenbild und Blutwerte sichern die Diagnose. Die "
                "Sauerstoffsättigung zeigt den Schweregrad."
            ),
            "therapy": (
                "Bakterielle Lungenentzündungen werden mit Antibiotika behandelt. Schwere "
                "Verläufe brauchen eine Behandlung im Krankenhaus."
            ),
            "red_flags": (
                "Atemnot in Ruhe, Verwirrtheit, bläuliche Lippen oder sehr schneller Puls "
                "sind Alarmzeichen – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("pneumonia", "Pneumonia"), who("pneumonia", "Pneumonia")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Asthma bronchiale": {
            "title_en": "Bronchial asthma",
            "sections_en": {
                "definition": (
                    "Bronchial asthma is a chronic inflammation of the airways in which the "
                    "bronchial tubes narrow in attacks."
                ),
                "symptoms": (
                    "Typical are attack-like shortness of breath, wheezing, tightness in the "
                    "chest and cough, especially at night or on exertion."
                ),
                "causes": (
                    "Allergies to pollen, house dust mites or animal hair, respiratory "
                    "infections, cold air, smoke and physical exertion can trigger attacks."
                ),
                "diagnostics": (
                    "A lung function test (spirometry) shows the narrowing of the airways and "
                    "its improvement after a bronchodilator spray."
                ),
                "therapy": (
                    "Inhaled cortisone counteracts the inflammation, short-acting "
                    "bronchodilators help during an attack. Triggers should be avoided."
                ),
                "red_flags": (
                    "Severe shortness of breath, speaking only in short sentences, bluish "
                    "lips or no improvement from the rescue spray: call the emergency number "
                    "144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Asthma",
                "Wheezing",
                "Shortness of breath",
                "Inhaler",
                "Allergy",
                "Lung function",
            ],
        },
        "Chronisch obstruktive Lungenerkrankung (COPD)": {
            "title_en": "Chronic obstructive pulmonary disease (COPD)",
            "sections_en": {
                "definition": (
                    "COPD is a progressive lung disease with permanently narrowed airways and "
                    "damaged lung tissue."
                ),
                "symptoms": (
                    "The main symptoms are cough with sputum and shortness of breath, at "
                    "first on exertion and later also at rest."
                ),
                "causes": (
                    "The main cause is long-term smoking; fine dust and pollutants at work "
                    "also contribute."
                ),
                "diagnostics": (
                    "The lung function test confirms the narrowing of the airways, which, "
                    "unlike in asthma, does not recede completely."
                ),
                "therapy": (
                    "Stopping smoking is most important. Inhaled bronchodilators, lung sport "
                    "and vaccinations against flu and pneumococci improve the course."
                ),
                "red_flags": (
                    "Increasing shortness of breath, confusion or bluish lips during a "
                    "worsening require immediate medical help; with shortness of breath at "
                    "rest call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "COPD",
                "Smoking",
                "Cough",
                "Sputum",
                "Shortness of breath",
                "Lung function",
            ],
        },
        "Lungenentzündung (Pneumonie)": {
            "title_en": "Pneumonia",
            "sections_en": {
                "definition": (
                    "Pneumonia is an inflammation of the lung tissue, usually caused by "
                    "bacteria or viruses."
                ),
                "symptoms": (
                    "Typical are fever, cough with sputum, shortness of breath and pain when "
                    "breathing. Older people often show only weakness or confusion."
                ),
                "causes": (
                    "The most common bacterial germ is the pneumococcus. Higher age, chronic "
                    "lung disease and a weakened immune system raise the risk."
                ),
                "diagnostics": (
                    "Listening to the lungs, a chest X-ray and blood tests confirm the "
                    "diagnosis. The oxygen saturation shows the severity."
                ),
                "therapy": (
                    "Bacterial pneumonia is treated with antibiotics. Severe courses need "
                    "treatment in hospital."
                ),
                "red_flags": (
                    "Shortness of breath at rest, confusion, bluish lips or a very fast pulse "
                    "are alarm signs – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": ["Pneumonia", "Fever", "Cough", "Antibiotics", "Chest X-ray", "Oxygen"],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Lungenembolie",
            "doc_type": "Diagnose",
            "expected_category": "Pneumologie",
            "term_en": "Pulmonary embolism",
            "icd11_code": "BB00",
            "medications": ["heparin", "rivaroxaban"],
            "sections": {
                "definition": (
                    "Bei einer Lungenembolie verschließt ein Blutgerinnsel, das meist aus "
                    "den Beinvenen stammt, eine Schlagader in der Lunge."
                ),
                "symptoms": (
                    "Typisch sind plötzliche Atemnot, stechende Schmerzen beim Einatmen, "
                    "Herzrasen und Husten, manchmal mit Blut. Bei großen Embolien kommen "
                    "Schwindel und Ohnmacht hinzu."
                ),
                "causes": (
                    "Das Gerinnsel entsteht meist durch eine Thrombose der tiefen Beinvenen. "
                    "Risikofaktoren sind lange Bettruhe, Operationen, Krebserkrankungen, "
                    "Schwangerschaft und hormonelle Verhütung in Kombination mit Rauchen."
                ),
                "diagnostics": (
                    "Im Krankenhaus werden Blutwerte (D-Dimere), die Sauerstoffsättigung und "
                    "eine Computertomografie der Lungengefäße eingesetzt. Ein Herzultraschall "
                    "zeigt die Belastung des rechten Herzens."
                ),
                "therapy": (
                    "Gerinnungshemmende Medikamente verhindern, dass das Gerinnsel wächst. "
                    "Bei lebensbedrohlichen Verläufen wird es medikamentös aufgelöst oder "
                    "mit einem Katheter entfernt. Danach folgt eine mehrmonatige "
                    "Blutverdünnung."
                ),
                "red_flags": (
                    "Plötzliche Atemnot, Brustschmerz beim Atmen oder Ohnmacht sind ein "
                    "Notfall – sofort Notruf 144. Besonders nach einer Operation, einer "
                    "langen Reise oder bei einem geschwollenen Bein."
                ),
            },
            "further_reading": [medlineplus("pulmonaryembolism", "Pulmonary embolism")],
        },
        {
            "title": "Schlafapnoe",
            "doc_type": "Diagnose",
            "expected_category": "Pneumologie",
            "term_en": "Obstructive sleep apnea",
            "icd11_code": "7A41",
            "medications": [],
            "sections": {
                "definition": (
                    "Bei der obstruktiven Schlafapnoe erschlafft im Schlaf die Muskulatur der "
                    "oberen Atemwege, sodass die Atmung wiederholt für Sekunden aussetzt."
                ),
                "symptoms": (
                    "Laute Schnarchgeräusche mit beobachteten Atempausen, unruhiger Schlaf, "
                    "Kopfschmerzen am Morgen und ausgeprägte Tagesmüdigkeit bis hin zu "
                    "Sekundenschlaf."
                ),
                "causes": (
                    "Übergewicht, ein kurzer Hals, vergrößerte Mandeln, Alkohol oder "
                    "Beruhigungsmittel am Abend sowie das männliche Geschlecht und höheres Alter "
                    "erhöhen das Risiko."
                ),
                "diagnostics": (
                    "Ein tragbares Messgerät zu Hause und bei Bedarf eine Untersuchung im "
                    "Schlaflabor erfassen Atmung, Sauerstoffsättigung und Schlaf."
                ),
                "therapy": (
                    "Gewichtsabnahme, Verzicht auf Alkohol am Abend und Schlafen in "
                    "Seitenlage helfen. Bei ausgeprägter Schlafapnoe hält eine nächtliche "
                    "Atemmaske (CPAP) die Atemwege offen. Eine Unterkieferschiene oder "
                    "Operation kommen in ausgewählten Fällen in Frage."
                ),
                "red_flags": (
                    "Einschlafen am Steuer oder bei der Arbeit ist gefährlich: Betroffene "
                    "sollten bei starker Tagesmüdigkeit nicht Auto fahren und rasch ärztlichen "
                    "Rat suchen. Nächtliche Atemnot mit Brustschmerz verlangt Notruf 144."
                ),
            },
            "further_reading": [medlineplus("sleepapnea", "Sleep apnea")],
        },
        {
            "title": "Akute Bronchitis",
            "doc_type": "Diagnose",
            "expected_category": "Pneumologie",
            "term_en": "Acute bronchitis",
            "icd11_code": "CA42",
            "medications": ["ambroxol", "paracetamol"],
            "sections": {
                "definition": (
                    "Die akute Bronchitis ist eine Entzündung der Schleimhaut der Bronchien, "
                    "die meist im Rahmen eines Atemwegsinfekts auftritt."
                ),
                "symptoms": (
                    "Husten, anfangs trocken, später mit Schleim, dazu Brennen hinter dem "
                    "Brustbein, Abgeschlagenheit und leichtes Fieber. Der Husten kann "
                    "mehrere Wochen anhalten."
                ),
                "causes": (
                    "In den meisten Fällen lösen Viren die Entzündung aus. Rauchen und "
                    "Schadstoffe in der Luft reizen die Bronchien zusätzlich."
                ),
                "diagnostics": (
                    "Die Ärztin hört die Lunge ab und erfragt den Verlauf. Eine "
                    "Röntgenaufnahme der Lunge ist nur bei Verdacht auf eine Lungenentzündung "
                    "nötig."
                ),
                "therapy": (
                    "Ruhe, viel Trinken und Inhalieren mit Kochsalzlösung lindern die "
                    "Beschwerden. Antibiotika helfen bei Virusinfekten nicht und sind nur "
                    "bei bakteriellen Komplikationen sinnvoll."
                ),
                "red_flags": (
                    "Hohes Fieber über mehrere Tage, Atemnot, blutiger Auswurf, "
                    "Brustschmerz oder ein Husten, der länger als drei Wochen dauert, sollten "
                    "ärztlich abgeklärt werden. Bei starker Atemnot Notruf 144."
                ),
            },
            "further_reading": [medlineplus("bronchitis", "Bronchitis")],
        },
        {
            "title": "Husten",
            "doc_type": "Symptom",
            "expected_category": "Pneumologie",
            "term_en": "Cough",
            "icd11_code": "MD12",
            "medications": ["acetylcysteine", "dextromethorphan"],
            "sections": {
                "definition": (
                    "Husten ist ein Schutzreflex, der Fremdkörper und Schleim aus den "
                    "Atemwegen entfernt. Er ist ein häufiger Grund für den Besuch bei der "
                    "Hausärztin oder dem Hausarzt."
                ),
                "symptoms": (
                    "Man unterscheidet trockenen Reizhusten und Husten mit Auswurf. Je "
                    "nach Dauer spricht man von akutem Husten (bis drei Wochen), "
                    "anhaltendem und chronischem Husten (über acht Wochen)."
                ),
                "causes": (
                    "Meist stecken Erkältungen und Virusinfekte dahinter. Weitere Ursachen "
                    "sind Rauchen, Asthma, Reflux, Allergien, Medikamente (etwa "
                    "ACE-Hemmer) und seltener Lungenerkrankungen."
                ),
                "diagnostics": (
                    "Die Ärztin erfragt Dauer, Auswurf und Begleitbeschwerden, hört die "
                    "Lunge ab und veranlasst bei anhaltendem Husten eine Röntgenaufnahme "
                    "oder Lungenfunktionsprüfung."
                ),
                "therapy": (
                    "Viel trinken, Raumluft befeuchten und Inhalation lindern die "
                    "Beschwerden. Hustenstiller sind nur bei quälendem trockenem Husten "
                    "sinnvoll. Wer raucht, sollte aufhören. Die Ursache wird gezielt "
                    "behandelt."
                ),
                "red_flags": (
                    "Husten mit Blut, Atemnot, Brustschmerz, hohem Fieber, ungewolltem "
                    "Gewichtsverlust oder länger als acht Wochen gehört ärztlich "
                    "abgeklärt. Bei starker Atemnot Notruf 144."
                ),
            },
            "further_reading": [medlineplus("cough", "Cough")],
        },
    ],
    {
        "Lungenembolie": {
            "title_en": "Pulmonary embolism",
            "sections_en": {
                "definition": (
                    "In a pulmonary embolism a blood clot, usually coming from the leg "
                    "veins, blocks an artery in the lung."
                ),
                "symptoms": (
                    "Typical are sudden breathlessness, stabbing pain on breathing in, a "
                    "racing heart and coughing, sometimes with blood. In large embolisms "
                    "dizziness and fainting are added."
                ),
                "causes": (
                    "The clot usually arises from a thrombosis of the deep leg veins. Risk "
                    "factors are long bed rest, operations, cancer, pregnancy and hormonal "
                    "contraception combined with smoking."
                ),
                "diagnostics": (
                    "In hospital, blood values (D-dimer), oxygen saturation and a "
                    "computed tomography of the lung vessels are used. An ultrasound of "
                    "the heart shows the strain on the right side of the heart."
                ),
                "therapy": (
                    "Anticoagulant medicines prevent the clot from growing. In "
                    "life-threatening cases it is dissolved with medicines or removed with "
                    "a catheter. Blood-thinning for several months follows."
                ),
                "red_flags": (
                    "Sudden breathlessness, chest pain on breathing or fainting is an "
                    "emergency – call the emergency number 144 (Austria) at once. This is "
                    "especially true after an operation, a long journey or with a swollen "
                    "leg."
                ),
            },
            "keywords_en": [
                "Pulmonary embolism",
                "Breathlessness",
                "Blood clot",
                "Thrombosis",
                "Anticoagulation",
                "Emergency",
            ],
        },
        "Schlafapnoe": {
            "title_en": "Sleep apnoea",
            "sections_en": {
                "definition": (
                    "In obstructive sleep apnoea the muscles of the upper airway relax "
                    "during sleep, so that breathing stops repeatedly for seconds."
                ),
                "symptoms": (
                    "Loud snoring with observed pauses in breathing, restless sleep, "
                    "headaches in the morning and marked daytime sleepiness up to falling "
                    "asleep for seconds."
                ),
                "causes": (
                    "Overweight, a short neck, enlarged tonsils, alcohol or sedatives in "
                    "the evening, as well as male sex and higher age raise the risk."
                ),
                "diagnostics": (
                    "A portable measuring device at home and, if needed, an examination in "
                    "a sleep laboratory record breathing, oxygen saturation and sleep."
                ),
                "therapy": (
                    "Weight loss, no alcohol in the evening and sleeping on the side help. "
                    "In marked sleep apnoea a night-time breathing mask (CPAP) keeps the "
                    "airway open. A lower jaw splint or an operation come into question "
                    "in selected cases."
                ),
                "red_flags": (
                    "Falling asleep at the wheel or at work is dangerous: with marked "
                    "daytime sleepiness people should not drive and should seek medical "
                    "advice promptly. Breathlessness at night with chest pain needs the "
                    "emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Sleep apnoea",
                "Snoring",
                "Daytime sleepiness",
                "CPAP",
                "Sleep laboratory",
                "Overweight",
            ],
        },
        "Akute Bronchitis": {
            "title_en": "Acute bronchitis",
            "sections_en": {
                "definition": (
                    "Acute bronchitis is an inflammation of the lining of the bronchial "
                    "tubes, which usually occurs as part of a respiratory infection."
                ),
                "symptoms": (
                    "Cough, dry at first and later with mucus, plus burning behind the "
                    "breastbone, tiredness and a slight fever. The cough can last several "
                    "weeks."
                ),
                "causes": (
                    "In most cases viruses trigger the inflammation. Smoking and "
                    "pollutants in the air irritate the bronchial tubes further."
                ),
                "diagnostics": (
                    "The doctor listens to the lungs and asks about the course. A chest "
                    "X-ray is only needed if pneumonia is suspected."
                ),
                "therapy": (
                    "Rest, plenty of fluids and inhaling saline solution relieve the "
                    "symptoms. Antibiotics do not help against viral infections and make "
                    "sense only for bacterial complications."
                ),
                "red_flags": (
                    "High fever lasting several days, breathlessness, bloody sputum, chest "
                    "pain or a cough lasting longer than three weeks should be checked by "
                    "a doctor. For severe breathlessness call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Bronchitis",
                "Cough",
                "Mucus",
                "Bronchial tubes",
                "Respiratory infection",
                "Inhalation",
            ],
        },
        "Husten": {
            "title_en": "Cough",
            "sections_en": {
                "definition": (
                    "Coughing is a protective reflex that removes foreign bodies and "
                    "mucus from the airways. It is a common reason for visiting the "
                    "family doctor."
                ),
                "symptoms": (
                    "A distinction is made between a dry irritating cough and a cough "
                    "with sputum. Depending on duration one speaks of acute cough (up to "
                    "three weeks), and persistent and chronic cough (over eight weeks)."
                ),
                "causes": (
                    "Colds and viral infections are usually behind it. Other causes are "
                    "smoking, asthma, reflux, allergies, medicines (such as ACE "
                    "inhibitors) and, less often, lung diseases."
                ),
                "diagnostics": (
                    "The doctor asks about duration, sputum and accompanying symptoms, "
                    "listens to the lungs and, for a persistent cough, arranges an X-ray "
                    "or a lung function test."
                ),
                "therapy": (
                    "Drinking plenty, humidifying the room air and inhaling ease the "
                    "symptoms. Cough suppressants make sense only for a tormenting dry "
                    "cough. Smokers should stop. The cause is treated specifically."
                ),
                "red_flags": (
                    "A cough with blood, breathlessness, chest pain, high fever, "
                    "unintended weight loss or lasting longer than eight weeks should be "
                    "checked by a doctor. For severe breathlessness call the emergency "
                    "number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Cough",
                "Sputum",
                "Respiratory tract",
                "Cold",
                "Smoking",
                "Inhalation",
            ],
        },
    },
)
