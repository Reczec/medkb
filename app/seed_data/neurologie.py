from app.seed_data.english import with_english
from app.seed_data.links import gesundheit_gv, medlineplus, who

ENTRIES = [
    {
        "title": "Migräne",
        "doc_type": "Diagnose",
        "expected_category": "Neurologie",
        "term_en": "Migraine",
        "icd11_code": "8A80",
        "medications": ["sumatriptan", "ibuprofen"],
        "sections": {
            "definition": (
                "Migräne ist eine anfallsartige Kopfschmerzerkrankung, bei der wiederholt "
                "starke, meist einseitige und pulsierende Kopfschmerzen auftreten."
            ),
            "symptoms": (
                "Begleitend treten oft Übelkeit sowie Licht- und Lärmempfindlichkeit auf. Bei "
                "manchen kündigt eine Aura mit Sehstörungen den Anfall an. Unbehandelt dauert "
                "ein Anfall mehrere Stunden bis drei Tage."
            ),
            "causes": (
                "Die Veranlagung ist häufig familiär. Auslöser sind individuell verschieden, "
                "etwa Stress, Schlafmangel, hormonelle Schwankungen oder ausgelassene "
                "Mahlzeiten."
            ),
            "diagnostics": (
                "Die Diagnose beruht auf der typischen Krankengeschichte und einer "
                "neurologischen Untersuchung. Ein Kopfschmerzkalender hilft, Muster und "
                "Auslöser zu erkennen."
            ),
            "therapy": (
                "Im Anfall helfen Schmerzmittel oder Triptane, Ruhe und ein abgedunkelter "
                "Raum. Bei häufigen Anfällen kommt eine vorbeugende Behandlung in Frage."
            ),
            "red_flags": (
                "Ein plötzlicher, nie zuvor erlebter heftigster Kopfschmerz, Lähmungen oder "
                "Sprachstörungen sind keine typische Migräne – sofort Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("migraine", "Migraine"),
            who("headache-disorders", "Headache disorders"),
        ],
    },
    {
        "title": "Schlaganfall – Warnzeichen",
        "doc_type": "Diagnose",
        "expected_category": "Neurologie",
        "term_en": "Stroke",
        "icd11_code": "8B20",
        "medications": ["aspirin"],
        "sections": {
            "definition": (
                "Ein Schlaganfall entsteht durch eine plötzliche Durchblutungsstörung oder "
                "eine Blutung im Gehirn, wodurch Nervenzellen geschädigt werden."
            ),
            "symptoms": (
                "Warnzeichen sind plötzliche Lähmungen oder Taubheitsgefühle einer "
                "Körperseite, ein hängender Mundwinkel, Sprachstörungen, Sehstörungen und "
                "starker Schwindel."
            ),
            "causes": (
                "Meist verschließt ein Blutgerinnsel ein Hirngefäß. Risikofaktoren sind "
                "Bluthochdruck, Vorhofflimmern, Diabetes, Rauchen und erhöhte Blutfette."
            ),
            "diagnostics": (
                "Im Krankenhaus klärt eine Bildgebung des Gehirns (CT oder MRT) rasch, ob ein "
                "Gefäßverschluss oder eine Blutung vorliegt."
            ),
            "therapy": (
                "Ein Gefäßverschluss kann in den ersten Stunden medikamentös aufgelöst oder "
                "mit einem Katheter entfernt werden. Danach folgen Rehabilitation und die "
                "Behandlung der Risikofaktoren."
            ),
            "red_flags": (
                "Jede Minute zählt: Bei Verdacht auf Schlaganfall sofort Notruf 144 wählen, "
                "auch wenn die Beschwerden wieder verschwinden."
            ),
        },
        "further_reading": [
            gesundheit_gv("gehirn-nerven/schlaganfall", "Schlaganfall"),
            medlineplus("stroke", "Stroke"),
            who("stroke", "Stroke"),
        ],
    },
    {
        "title": "Anamnese bei Kopfschmerzen",
        "doc_type": "Anamnese",
        "expected_category": "Neurologie",
        "term_en": "Headache",
        "sections": {
            "definition": (
                "Die Anamnese ist bei Kopfschmerzen das wichtigste diagnostische Werkzeug: Die "
                "meisten Kopfschmerzformen lassen sich anhand der Schilderung einordnen."
            ),
            "diagnostics": (
                "Erfragt werden Beginn, Dauer, Häufigkeit, Lokalisation und Charakter der "
                "Kopfschmerzen, Begleitsymptome wie Übelkeit oder Sehstörungen, auslösende "
                "Faktoren, Medikamenteneinnahme, frühere Erkrankungen und familiäre Häufung."
            ),
            "red_flags": (
                "Ein plötzlich einsetzender, nie zuvor erlebter Vernichtungskopfschmerz, "
                "Fieber mit Nackensteifigkeit oder neue neurologische Ausfälle erfordern eine "
                "sofortige Abklärung – Notruf 144."
            ),
        },
        "further_reading": [medlineplus("headache", "Headache")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Migräne": {
            "title_en": "Migraine",
            "sections_en": {
                "definition": (
                    "Migraine is an attack-like headache disorder in which severe, usually "
                    "one-sided and throbbing headaches occur repeatedly."
                ),
                "symptoms": (
                    "Nausea and sensitivity to light and noise often accompany the headache. "
                    "Some people notice an aura with visual disturbances before the attack. "
                    "Untreated, an attack lasts several hours up to three days."
                ),
                "causes": (
                    "The tendency often runs in families. Triggers differ from person to "
                    "person, for example stress, lack of sleep, hormonal changes or skipped "
                    "meals."
                ),
                "diagnostics": (
                    "The diagnosis is based on the typical history and a neurological "
                    "examination. A headache diary helps to recognise patterns and triggers."
                ),
                "therapy": (
                    "During an attack, pain relievers or triptans, rest and a darkened room "
                    "help. For frequent attacks, preventive treatment can be considered."
                ),
                "red_flags": (
                    "A sudden, never-before-experienced worst headache, paralysis or speech "
                    "problems are not typical migraine – call the emergency number 144 "
                    "(Austria) at once."
                ),
            },
            "keywords_en": [
                "Migraine",
                "Headache",
                "Aura",
                "Nausea",
                "Triptans",
                "Light sensitivity",
            ],
        },
        "Schlaganfall – Warnzeichen": {
            "title_en": "Stroke – warning signs",
            "sections_en": {
                "definition": (
                    "A stroke is caused by a sudden disturbance of blood flow or a bleed in "
                    "the brain, which damages nerve cells."
                ),
                "symptoms": (
                    "Warning signs are sudden paralysis or numbness on one side of the body, "
                    "a drooping corner of the mouth, speech problems, vision problems and "
                    "severe dizziness."
                ),
                "causes": (
                    "Usually a blood clot blocks a vessel in the brain. Risk factors are high "
                    "blood pressure, atrial fibrillation, diabetes, smoking and high blood "
                    "fats."
                ),
                "diagnostics": (
                    "In hospital, brain imaging (CT or MRI) quickly clarifies whether a "
                    "vessel is blocked or there is a bleed."
                ),
                "therapy": (
                    "A vessel blockage can be dissolved with medicines or removed with a "
                    "catheter in the first hours. Rehabilitation and treatment of the risk "
                    "factors follow."
                ),
                "red_flags": (
                    "Every minute counts: if a stroke is suspected, call the emergency number "
                    "144 (Austria) at once, even if the symptoms go away again."
                ),
            },
            "keywords_en": [
                "Stroke",
                "Paralysis",
                "Speech problems",
                "Emergency",
                "Brain",
                "Blood clot",
            ],
        },
        "Anamnese bei Kopfschmerzen": {
            "title_en": "Medical history for headaches",
            "sections_en": {
                "definition": (
                    "For headaches, the medical history is the most important diagnostic "
                    "tool: most types of headache can be classified from the description."
                ),
                "diagnostics": (
                    "The questions cover onset, duration, frequency, location and character "
                    "of the headache, accompanying symptoms such as nausea or visual "
                    "disturbances, triggering factors, medication, past illnesses and family "
                    "history."
                ),
                "red_flags": (
                    "A sudden, never-before-experienced worst headache, fever with a stiff "
                    "neck or new neurological deficits require immediate assessment – call "
                    "the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Headache",
                "Medical history",
                "Duration",
                "Triggers",
                "Nausea",
                "Warning signs",
            ],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Epilepsie",
            "doc_type": "Diagnose",
            "expected_category": "Neurologie",
            "term_en": "Epilepsy",
            "icd11_code": "8A6Z",
            "medications": ["levetiracetam", "lamotrigine"],
            "sections": {
                "definition": (
                    "Epilepsie ist eine Erkrankung des Gehirns, bei der es wiederholt zu "
                    "epileptischen Anfällen kommt, weil Nervenzellen kurzzeitig übermäßig "
                    "gleichzeitig aktiv sind."
                ),
                "symptoms": (
                    "Die Anfälle sind sehr verschieden: Beim großen Anfall stürzt die Person "
                    "bewusstlos zu Boden und krampft am ganzen Körper. Andere Anfälle zeigen "
                    "sich nur als kurzes Starren, Zuckungen eines Arms oder seltsame "
                    "Empfindungen."
                ),
                "causes": (
                    "Ursachen sind Narben oder Fehlbildungen im Gehirn, Folgen eines "
                    "Schlaganfalls, einer Verletzung oder Entzündung, aber auch erbliche "
                    "Faktoren. Bei vielen Menschen bleibt die Ursache unbekannt."
                ),
                "diagnostics": (
                    "Die Neurologin oder der Neurologe erhebt die Krankengeschichte und "
                    "schreibt die Hirnströme (EEG). Eine Magnetresonanztomografie sucht nach "
                    "Veränderungen im Gehirn."
                ),
                "therapy": (
                    "Mit Antiepileptika sind viele Betroffene anfallsfrei. Wichtig sind "
                    "regelmäßige Einnahme, ausreichend Schlaf und der Verzicht auf bekannte "
                    "Auslöser. In ausgewählten Fällen helfen eine Operation oder ein "
                    "Nervenstimulator."
                ),
                "red_flags": (
                    "Ein Krampfanfall, der länger als fünf Minuten dauert, mehrere Anfälle "
                    "hintereinander, ein erster Anfall oder Verletzungen beim Sturz – sofort "
                    "Notruf 144. Während des Anfalls nichts in den Mund stecken."
                ),
            },
            "further_reading": [
                medlineplus("epilepsy", "Epilepsy"),
                who("epilepsy", "Epilepsy"),
            ],
        },
        {
            "title": "Parkinson-Krankheit",
            "doc_type": "Diagnose",
            "expected_category": "Neurologie",
            "term_en": "Parkinson disease",
            "icd11_code": "8A00.0",
            "medications": ["levodopa", "pramipexole"],
            "sections": {
                "definition": (
                    "Die Parkinson-Krankheit ist eine langsam fortschreitende Erkrankung des "
                    "Gehirns, bei der Nervenzellen absterben, die den Botenstoff Dopamin "
                    "herstellen."
                ),
                "symptoms": (
                    "Leitsymptome sind verlangsamte Bewegungen, Muskelsteifheit, ein Zittern "
                    "in Ruhe und eine Haltungsinstabilität. Früh können ein vermindertes "
                    "Riechen, Schlafstörungen und Verstopfung auftreten."
                ),
                "causes": (
                    "Warum die Zellen absterben, ist nicht vollständig geklärt. Alter, "
                    "genetische Faktoren und Umwelteinflüsse spielen eine Rolle."
                ),
                "diagnostics": (
                    "Die Diagnose stellt die Neurologin anhand der Beschwerden und der "
                    "körperlichen Untersuchung. Bildgebung dient vor allem dazu, andere "
                    "Ursachen auszuschließen."
                ),
                "therapy": (
                    "Medikamente, die Dopamin ersetzen oder nachahmen, lindern die Symptome "
                    "gut. Bewegung, Physio- und Sprachtherapie ergänzen sie. In ausgewählten "
                    "Fällen kann eine tiefe Hirnstimulation helfen."
                ),
                "red_flags": (
                    "Neue Stürze, Halluzinationen oder Verwirrtheit, plötzliche starke "
                    "Verschlechterung der Beweglichkeit oder Schluckstörungen mit Verschlucken "
                    "sollten rasch ärztlich abgeklärt werden."
                ),
            },
            "further_reading": [
                medlineplus("parkinsonsdisease", "Parkinson's disease"),
                who("parkinson-disease", "Parkinson disease"),
            ],
        },
        {
            "title": "Multiple Sklerose",
            "doc_type": "Diagnose",
            "expected_category": "Neurologie",
            "term_en": "Multiple sclerosis",
            "icd11_code": "8A40",
            "medications": ["interferon beta", "methylprednisolone"],
            "sections": {
                "definition": (
                    "Die Multiple Sklerose (MS) ist eine chronisch-entzündliche Erkrankung "
                    "des Nervensystems, bei der das Immunsystem die Schutzhülle der "
                    "Nervenfasern in Gehirn und Rückenmark angreift."
                ),
                "symptoms": (
                    "Häufig sind Sehstörungen, Missempfindungen und Taubheitsgefühle, "
                    "Lähmungen, Gleichgewichtsstörungen und eine ausgeprägte Müdigkeit. Die "
                    "Beschwerden treten oft in Schüben auf und bilden sich teilweise zurück."
                ),
                "causes": (
                    "Die Ursache ist nicht abschließend geklärt. Vermutet wird ein Zusammenspiel "
                    "aus erblicher Veranlagung und Umweltfaktoren. Frauen sind häufiger "
                    "betroffen, die Erkrankung beginnt meist zwischen 20 und 40 Jahren."
                ),
                "diagnostics": (
                    "Die Neurologin stützt sich auf Krankengeschichte, neurologische "
                    "Untersuchung, Magnetresonanztomografie von Gehirn und Rückenmark und "
                    "die Untersuchung des Nervenwassers."
                ),
                "therapy": (
                    "Im akuten Schub wird meist hochdosiertes Kortison gegeben. Langfristig "
                    "verringern Medikamente, die das Immunsystem beeinflussen, die Zahl der "
                    "Schübe. Physiotherapie und Rehabilitation ergänzen die Behandlung."
                ),
                "red_flags": (
                    "Neu auftretende Lähmungen, ein plötzlicher Sehverlust oder starke "
                    "Gleichgewichtsstörungen sind ein Grund für eine rasche neurologische "
                    "Abklärung; bei Schluck- oder Atemproblemen Notruf 144."
                ),
            },
            "further_reading": [medlineplus("multiplesclerosis", "Multiple sclerosis")],
        },
        {
            "title": "Spannungskopfschmerz",
            "doc_type": "Diagnose",
            "expected_category": "Neurologie",
            "term_en": "Tension-type headache",
            "icd11_code": "8A81",
            "medications": ["ibuprofen", "paracetamol"],
            "sections": {
                "definition": (
                    "Der Spannungskopfschmerz ist die häufigste Kopfschmerzform. Er fühlt sich "
                    "dumpf und drückend an, wie ein Band um den Kopf."
                ),
                "symptoms": (
                    "Der Schmerz betrifft beide Kopfseiten, ist leicht bis mittelstark und "
                    "verstärkt sich nicht durch körperliche Aktivität. Übelkeit fehlt meist, "
                    "Licht- oder Lärmempfindlichkeit sind nur schwach ausgeprägt."
                ),
                "causes": (
                    "Verspannte Nacken- und Schultermuskeln, Stress, Schlafmangel, langes "
                    "Sitzen am Bildschirm und zu wenig Trinken spielen eine Rolle."
                ),
                "diagnostics": (
                    "Die Diagnose ergibt sich aus der Beschreibung der Beschwerden. Ein "
                    "Kopfschmerzkalender hilft. Weitere Untersuchungen sind nur bei "
                    "auffälligen Zeichen nötig."
                ),
                "therapy": (
                    "Wärme, Bewegung, Entspannungsverfahren und Pausen helfen. Schmerzmittel "
                    "sollten an höchstens zehn Tagen im Monat eingenommen werden, um einen "
                    "Dauerkopfschmerz durch Medikamente zu vermeiden."
                ),
                "red_flags": (
                    "Ein plötzlich einsetzender heftigster Kopfschmerz, Fieber mit "
                    "Nackensteifigkeit, Lähmungen, Sprach- oder Sehstörungen oder Kopfschmerz "
                    "nach einem Unfall erfordern sofortige Abklärung – Notruf 144."
                ),
            },
            "further_reading": [medlineplus("headache", "Headache")],
        },
    ],
    {
        "Epilepsie": {
            "title_en": "Epilepsy",
            "sections_en": {
                "definition": (
                    "Epilepsy is a disease of the brain in which epileptic seizures occur "
                    "repeatedly because nerve cells are briefly overactive at the same time."
                ),
                "symptoms": (
                    "Seizures differ greatly: in a major seizure the person falls "
                    "unconscious to the ground and convulses all over. Other seizures show "
                    "up only as a brief stare, twitching of an arm or strange sensations."
                ),
                "causes": (
                    "Causes are scars or malformations in the brain, the consequences of a "
                    "stroke, injury or inflammation, but also hereditary factors. In many "
                    "people the cause stays unknown."
                ),
                "diagnostics": (
                    "The neurologist takes the history and records the brain waves (EEG). "
                    "Magnetic resonance imaging looks for changes in the brain."
                ),
                "therapy": (
                    "With antiseizure medicines many people become seizure-free. Regular "
                    "intake, enough sleep and avoiding known triggers are important. In "
                    "selected cases an operation or a nerve stimulator helps."
                ),
                "red_flags": (
                    "A seizure that lasts longer than five minutes, several seizures in a "
                    "row, a first seizure or injuries from the fall – call the emergency "
                    "number 144 (Austria) at once. Do not put anything into the mouth "
                    "during a seizure."
                ),
            },
            "keywords_en": [
                "Epilepsy",
                "Seizure",
                "Convulsions",
                "EEG",
                "Antiseizure medicines",
                "Neurologist",
            ],
        },
        "Parkinson-Krankheit": {
            "title_en": "Parkinson disease",
            "sections_en": {
                "definition": (
                    "Parkinson disease is a slowly progressing disease of the brain in "
                    "which the nerve cells that produce the messenger dopamine are lost."
                ),
                "symptoms": (
                    "Main symptoms are slowed movements, muscle stiffness, a tremor at rest "
                    "and unsteady posture. Early signs can be a reduced sense of smell, "
                    "sleep problems and constipation."
                ),
                "causes": (
                    "Why the cells are lost is not fully understood. Age, genetic factors "
                    "and environmental influences play a role."
                ),
                "diagnostics": (
                    "The neurologist makes the diagnosis from the symptoms and the physical "
                    "examination. Imaging mainly serves to rule out other causes."
                ),
                "therapy": (
                    "Medicines that replace or imitate dopamine relieve the symptoms well. "
                    "Exercise, physiotherapy and speech therapy complement them. In "
                    "selected cases deep brain stimulation can help."
                ),
                "red_flags": (
                    "New falls, hallucinations or confusion, a sudden marked worsening of "
                    "mobility or swallowing problems with choking should be checked by a "
                    "doctor promptly."
                ),
            },
            "keywords_en": [
                "Parkinson disease",
                "Tremor",
                "Dopamine",
                "Stiffness",
                "Levodopa",
                "Physiotherapy",
            ],
        },
        "Multiple Sklerose": {
            "title_en": "Multiple sclerosis",
            "sections_en": {
                "definition": (
                    "Multiple sclerosis (MS) is a chronic inflammatory disease of the "
                    "nervous system in which the immune system attacks the protective "
                    "sheath of the nerve fibres in the brain and spinal cord."
                ),
                "symptoms": (
                    "Common signs are vision problems, abnormal sensations and numbness, "
                    "paralysis, balance problems and marked tiredness. The symptoms often "
                    "come in relapses and partly go away again."
                ),
                "causes": (
                    "The cause has not been fully clarified. A combination of inherited "
                    "tendency and environmental factors is suspected. Women are affected "
                    "more often, and the disease usually starts between 20 and 40 years of "
                    "age."
                ),
                "diagnostics": (
                    "The neurologist relies on the history, a neurological examination, "
                    "magnetic resonance imaging of brain and spinal cord and an "
                    "examination of the spinal fluid."
                ),
                "therapy": (
                    "In an acute relapse high-dose cortisone is usually given. In the long "
                    "term, medicines that act on the immune system reduce the number of "
                    "relapses. Physiotherapy and rehabilitation complement the treatment."
                ),
                "red_flags": (
                    "Newly occurring paralysis, a sudden loss of vision or severe balance "
                    "problems are a reason for a prompt neurological examination; for "
                    "swallowing or breathing problems call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "Multiple sclerosis",
                "MS",
                "Relapse",
                "Myelin",
                "Immune system",
                "Rehabilitation",
            ],
        },
        "Spannungskopfschmerz": {
            "title_en": "Tension-type headache",
            "sections_en": {
                "definition": (
                    "Tension-type headache is the most common form of headache. It feels "
                    "dull and pressing, like a band around the head."
                ),
                "symptoms": (
                    "The pain affects both sides of the head, is mild to moderate and does "
                    "not get worse with physical activity. Nausea is usually absent, and "
                    "sensitivity to light or noise is only slight."
                ),
                "causes": (
                    "Tense neck and shoulder muscles, stress, lack of sleep, sitting at a "
                    "screen for long periods and drinking too little play a role."
                ),
                "diagnostics": (
                    "The diagnosis follows from the description of the symptoms. A headache "
                    "diary helps. Further tests are only needed if there are unusual signs."
                ),
                "therapy": (
                    "Heat, exercise, relaxation techniques and breaks help. Pain relievers "
                    "should be taken on no more than ten days a month, to avoid a constant "
                    "headache caused by the medicine itself."
                ),
                "red_flags": (
                    "A suddenly starting worst headache, fever with a stiff neck, "
                    "paralysis, speech or vision problems, or a headache after an accident "
                    "need to be checked at once – call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Tension-type headache",
                "Headache",
                "Neck tension",
                "Stress",
                "Pain relievers",
                "Headache diary",
            ],
        },
    },
)
