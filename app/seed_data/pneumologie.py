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
