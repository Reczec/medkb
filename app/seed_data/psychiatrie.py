from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Depressive Episode",
        "doc_type": "Diagnose",
        "expected_category": "Psychiatrie",
        "term_en": "Depressive disorder",
        "icd11_code": "6A70",
        "medications": ["sertraline", "escitalopram"],
        "sections": {
            "definition": (
                "Eine depressive Episode ist eine psychische Erkrankung mit gedrückter Stimmung, "
                "Antriebslosigkeit und Verlust von Interesse oder Freude über mindestens zwei "
                "Wochen."
            ),
            "symptoms": (
                "Häufig kommen Schlafstörungen, Konzentrationsprobleme, Appetitveränderungen, "
                "Schuldgefühle und Hoffnungslosigkeit hinzu."
            ),
            "causes": (
                "Es wirken Veranlagung, belastende Lebensereignisse, chronischer Stress und "
                "körperliche Erkrankungen zusammen."
            ),
            "diagnostics": (
                "Die Diagnose stellen Ärztinnen, Psychiater oder Psychotherapeutinnen im "
                "Gespräch, oft unterstützt durch Fragebögen; körperliche Ursachen werden "
                "ausgeschlossen."
            ),
            "therapy": (
                "Depressionen sind gut behandelbar, etwa durch Psychotherapie und "
                "gegebenenfalls Antidepressiva. Bewegung und eine feste Tagesstruktur "
                "unterstützen."
            ),
            "red_flags": (
                "Bei Suizidgedanken ist sofortige Hilfe wichtig: in Österreich die "
                "Telefonseelsorge unter 142, im akuten Notfall Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("depression", "Depression"),
            who("depression", "Depression"),
        ],
    },
    {
        "title": "Generalisierte Angststörung",
        "doc_type": "Diagnose",
        "expected_category": "Psychiatrie",
        "term_en": "Generalized anxiety disorder",
        "icd11_code": "6B00",
        "medications": ["escitalopram"],
        "sections": {
            "definition": (
                "Bei der generalisierten Angststörung bestehen über Monate anhaltende, "
                "übermäßige Sorgen und Ängste, die sich kaum kontrollieren lassen."
            ),
            "symptoms": (
                "Typisch sind ständige Anspannung, Nervosität, Schlafstörungen, "
                "Muskelverspannungen, Konzentrationsprobleme und körperliche Beschwerden wie "
                "Herzklopfen."
            ),
            "causes": (
                "Veranlagung, belastende Erfahrungen und erlernte Denkmuster tragen zur "
                "Entstehung der Angststörung bei."
            ),
            "diagnostics": (
                "Die Diagnose erfolgt im psychiatrischen oder psychotherapeutischen Gespräch; "
                "körperliche Ursachen wie eine Schilddrüsenüberfunktion werden ausgeschlossen."
            ),
            "therapy": (
                "Am wirksamsten ist kognitive Verhaltenstherapie, bei Bedarf ergänzt durch "
                "Medikamente. Entspannungsverfahren und Bewegung helfen zusätzlich."
            ),
            "red_flags": (
                "Brustschmerz mit Atemnot sollte nicht vorschnell als Panik gedeutet werden – "
                "im Zweifel Notruf 144. Bei Suizidgedanken sofort Hilfe holen."
            ),
        },
        "further_reading": [
            medlineplus("anxiety", "Anxiety"),
            who("anxiety-disorders", "Anxiety disorders"),
        ],
    },
    {
        "title": "Burnout",
        "doc_type": "Beschreibung",
        "expected_category": "Psychiatrie",
        "term_en": "Burnout",
        "icd11_code": "QD85",
        "sections": {
            "definition": (
                "Burnout beschreibt einen Zustand der Erschöpfung infolge chronischer, nicht "
                "bewältigter Belastung am Arbeitsplatz. In der ICD-11 ist es keine "
                "psychische Erkrankung, sondern ein Faktor, der die Gesundheit beeinflusst."
            ),
            "symptoms": (
                "Typisch sind emotionale Erschöpfung, zunehmende Distanz zur Arbeit, "
                "Zynismus und das Gefühl verminderter Leistungsfähigkeit."
            ),
            "diagnostics": (
                "Wichtig ist die Abgrenzung zur Depression und zu körperlichen Ursachen der "
                "Erschöpfung durch ärztliche und psychiatrische Abklärung."
            ),
            "therapy": (
                "Hilfreich sind Entlastung, Veränderungen der Arbeitssituation, "
                "Stressbewältigung und bei Bedarf Psychotherapie."
            ),
            "red_flags": (
                "Hoffnungslosigkeit oder Suizidgedanken sind Zeichen einer ernsten Krise – "
                "Telefonseelsorge 142, im Notfall Notruf 144."
            ),
        },
        "further_reading": [
            medlineplus("stress", "Stress"),
            who("mental-health-at-work", "Mental health at work"),
        ],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Depressive Episode": {
            "title_en": "Depressive episode",
            "sections_en": {
                "definition": (
                    "A depressive episode is a mental illness with low mood, lack of drive "
                    "and loss of interest or pleasure lasting at least two weeks."
                ),
                "symptoms": (
                    "Sleep problems, difficulty concentrating, changes in appetite, feelings "
                    "of guilt and hopelessness often come on top."
                ),
                "causes": (
                    "Predisposition, stressful life events, chronic stress and physical "
                    "illnesses act together."
                ),
                "diagnostics": (
                    "Doctors, psychiatrists or psychotherapists make the diagnosis in a "
                    "conversation, often supported by questionnaires; physical causes are "
                    "ruled out."
                ),
                "therapy": (
                    "Depression is well treatable, for example with psychotherapy and, if "
                    "appropriate, antidepressants. Exercise and a regular daily routine "
                    "support recovery."
                ),
                "red_flags": (
                    "With thoughts of suicide, immediate help is important: in Austria the "
                    "crisis line 142, in an acute emergency the emergency number 144."
                ),
            },
            "keywords_en": [
                "Depression",
                "Low mood",
                "Lack of drive",
                "Psychotherapy",
                "Antidepressants",
                "Sleep",
            ],
        },
        "Generalisierte Angststörung": {
            "title_en": "Generalised anxiety disorder",
            "sections_en": {
                "definition": (
                    "In generalised anxiety disorder, excessive worries and fears that are "
                    "hard to control last for months."
                ),
                "symptoms": (
                    "Typical are constant tension, nervousness, sleep problems, muscle "
                    "tension, difficulty concentrating and physical complaints such as "
                    "palpitations."
                ),
                "causes": (
                    "Predisposition, stressful experiences and learned thought patterns "
                    "contribute to the development of the anxiety disorder."
                ),
                "diagnostics": (
                    "The diagnosis is made in a psychiatric or psychotherapeutic "
                    "conversation; physical causes such as an overactive thyroid are ruled "
                    "out."
                ),
                "therapy": (
                    "Cognitive behavioural therapy works best, supplemented by medicines if "
                    "needed. Relaxation techniques and exercise help in addition."
                ),
                "red_flags": (
                    "Chest pain with shortness of breath should not be dismissed too quickly "
                    "as panic – if in doubt call the emergency number 144 (Austria). With "
                    "thoughts of suicide, get help at once."
                ),
            },
            "keywords_en": [
                "Anxiety",
                "Worries",
                "Panic",
                "Behavioural therapy",
                "Tension",
                "Sleep",
            ],
        },
        "Burnout": {
            "title_en": "Burnout",
            "sections_en": {
                "definition": (
                    "Burnout describes a state of exhaustion resulting from chronic workplace "
                    "stress that has not been successfully managed. In ICD-11 it is not a "
                    "mental illness but a factor that influences health."
                ),
                "symptoms": (
                    "Typical are emotional exhaustion, growing distance from work, cynicism "
                    "and a feeling of reduced performance."
                ),
                "diagnostics": (
                    "It is important to distinguish it from depression and from physical "
                    "causes of exhaustion through medical and psychiatric assessment."
                ),
                "therapy": (
                    "Relief, changes to the work situation, stress management and, if needed, "
                    "psychotherapy help."
                ),
                "red_flags": (
                    "Hopelessness or thoughts of suicide are signs of a serious crisis – "
                    "crisis line 142 in Austria, in an emergency the emergency number 144."
                ),
            },
            "keywords_en": [
                "Burnout",
                "Exhaustion",
                "Work stress",
                "Cynicism",
                "Depression",
                "Stress management",
            ],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Chronische Schlafstörung (Insomnie)",
            "doc_type": "Diagnose",
            "expected_category": "Psychiatrie",
            "term_en": "Chronic insomnia",
            "icd11_code": "7A00",
            "medications": ["zolpidem"],
            "sections": {
                "definition": (
                    "Bei der chronischen Insomnie bestehen Ein- oder Durchschlafstörungen "
                    "mindestens dreimal pro Woche über mehr als drei Monate, mit "
                    "Beeinträchtigungen am Tag."
                ),
                "symptoms": (
                    "Betroffene liegen lange wach, wachen nachts oder früh am Morgen auf und "
                    "fühlen sich tagsüber müde, unkonzentriert und gereizt. Oft entsteht eine "
                    "Angst vor dem Schlafengehen."
                ),
                "causes": (
                    "Stress, Sorgen, Depression, Angststörungen, Schichtarbeit, "
                    "unregelmäßige Schlafzeiten, Koffein, Alkohol sowie körperliche "
                    "Erkrankungen und Schmerzen können die Schlafstörung auslösen oder "
                    "aufrechterhalten."
                ),
                "diagnostics": (
                    "Ein Schlaftagebuch über zwei Wochen und das ärztliche Gespräch ordnen die "
                    "Beschwerden ein. Körperliche Ursachen wie eine Schlafapnoe oder "
                    "Schilddrüsenstörung werden ausgeschlossen."
                ),
                "therapy": (
                    "Die erste Wahl ist eine kognitive Verhaltenstherapie bei Insomnie sowie "
                    "Schlafhygiene: feste Zeiten, ruhiges Schlafzimmer, kein Koffein am Abend. "
                    "Schlafmittel werden nur kurzzeitig eingesetzt, da sie abhängig machen "
                    "können."
                ),
                "red_flags": (
                    "Gedanken, sich das Leben zu nehmen, starke Niedergeschlagenheit oder "
                    "Einschlafen am Steuer erfordern rasche Hilfe: Telefonseelsorge 142, in "
                    "akuter Gefahr Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("insomnia", "Insomnia"),
                medlineplus("sleepdisorders", "Sleep disorders"),
            ],
        },
        {
            "title": "Panikstörung",
            "doc_type": "Diagnose",
            "expected_category": "Psychiatrie",
            "term_en": "Panic disorder",
            "icd11_code": "6B01",
            "medications": ["sertraline", "paroxetine"],
            "sections": {
                "definition": (
                    "Bei der Panikstörung treten wiederholt plötzliche Angstanfälle "
                    "(Panikattacken) ohne erkennbaren äußeren Anlass auf, verbunden mit der "
                    "Sorge vor weiteren Anfällen."
                ),
                "symptoms": (
                    "Herzrasen, Atemnot, Schwindel, Zittern, Schwitzen, Engegefühl in der "
                    "Brust und Todesangst. Die Attacke erreicht nach wenigen Minuten ihren "
                    "Höhepunkt und klingt meist innerhalb einer halben Stunde ab."
                ),
                "causes": (
                    "Eine erbliche Veranlagung, belastende Lebensereignisse, anhaltender "
                    "Stress und erhöhte Körperwahrnehmung wirken zusammen. Die Angst vor den "
                    "Körperreaktionen verstärkt den Teufelskreis."
                ),
                "diagnostics": (
                    "Zuerst werden körperliche Ursachen wie Herz-, Lungen- oder "
                    "Schilddrüsenerkrankungen ausgeschlossen. Die Diagnose stellen "
                    "Fachärzte für Psychiatrie oder Psychotherapeuten im Gespräch."
                ),
                "therapy": (
                    "Die Verhaltenstherapie mit Aufklärung und schrittweiser Konfrontation "
                    "ist besonders wirksam. Antidepressiva können ergänzend helfen. "
                    "Entspannungsverfahren und Bewegung unterstützen die Behandlung."
                ),
                "red_flags": (
                    "Erstmalige Brustschmerzen, Atemnot oder Ohnmacht sollten immer "
                    "körperlich abgeklärt werden, da sie auch von Herz oder Lunge kommen "
                    "können – im Zweifel Notruf 144. Bei Suizidgedanken Telefonseelsorge 142."
                ),
            },
            "further_reading": [
                medlineplus("panicdisorder", "Panic disorder"),
                who("anxiety-disorders", "Anxiety disorders"),
            ],
        },
        {
            "title": "Posttraumatische Belastungsstörung (PTBS)",
            "doc_type": "Diagnose",
            "expected_category": "Psychiatrie",
            "term_en": "Post-traumatic stress disorder",
            "icd11_code": "6B40",
            "medications": ["sertraline"],
            "sections": {
                "definition": (
                    "Eine posttraumatische Belastungsstörung kann nach einem extrem "
                    "belastenden Ereignis entstehen, etwa nach einem schweren Unfall, Gewalt "
                    "oder Krieg."
                ),
                "symptoms": (
                    "Wiederkehrende belastende Erinnerungen und Albträume (Flashbacks), "
                    "Vermeidung von Erinnerungen, Schreckhaftigkeit, Schlafstörungen und ein "
                    "Gefühl innerer Taubheit. Die Beschwerden dauern Wochen bis Jahre."
                ),
                "causes": (
                    "Ausgelöst wird sie durch ein traumatisches Erlebnis. Ob eine Störung "
                    "entsteht, hängt von Art und Dauer der Belastung, früheren Erfahrungen "
                    "und der Unterstützung danach ab."
                ),
                "diagnostics": (
                    "Fachleute für Psychiatrie oder Psychotherapie stellen die Diagnose in "
                    "einem ausführlichen Gespräch, oft mit Fragebögen. Begleiterkrankungen "
                    "wie Depression werden miterfasst."
                ),
                "therapy": (
                    "Traumafokussierte Psychotherapie, etwa mit EMDR oder "
                    "Verhaltenstherapie, ist die wichtigste Behandlung. Medikamente können "
                    "begleitend eingesetzt werden. Stabilität und Sicherheit stehen am "
                    "Anfang."
                ),
                "red_flags": (
                    "Suizidgedanken, Selbstverletzung oder das Gefühl, die Kontrolle zu "
                    "verlieren, sind ein Anlass für sofortige Hilfe: Telefonseelsorge 142, "
                    "in akuter Gefahr Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("posttraumaticstressdisorder", "Post-traumatic stress disorder"),
                who("post-traumatic-stress-disorder", "Post-traumatic stress disorder"),
            ],
        },
    ],
    {
        "Chronische Schlafstörung (Insomnie)": {
            "title_en": "Chronic sleep disorder (insomnia)",
            "sections_en": {
                "definition": (
                    "In chronic insomnia there are problems falling asleep or staying "
                    "asleep at least three times a week for more than three months, with "
                    "impairment during the day."
                ),
                "symptoms": (
                    "People lie awake for a long time, wake up at night or early in the "
                    "morning and feel tired, unable to concentrate and irritable during "
                    "the day. A fear of going to bed often develops."
                ),
                "causes": (
                    "Stress, worries, depression, anxiety disorders, shift work, "
                    "irregular sleep times, caffeine, alcohol, as well as physical "
                    "illnesses and pain can trigger or maintain the sleep disorder."
                ),
                "diagnostics": (
                    "A sleep diary over two weeks and a conversation with the doctor put "
                    "the symptoms in context. Physical causes such as sleep apnoea or a "
                    "thyroid disorder are ruled out."
                ),
                "therapy": (
                    "The first choice is cognitive behavioural therapy for insomnia and "
                    "sleep hygiene: fixed times, a quiet bedroom, no caffeine in the "
                    "evening. Sleeping pills are used only for a short time, as they can "
                    "cause dependence."
                ),
                "red_flags": (
                    "Thoughts of taking one's own life, marked low mood or falling asleep "
                    "at the wheel need prompt help: telephone counselling 142 (Austria), "
                    "and in acute danger the emergency number 144."
                ),
            },
            "keywords_en": [
                "Insomnia",
                "Sleep disorder",
                "Sleep hygiene",
                "Sleep diary",
                "Behavioural therapy",
                "Tiredness",
            ],
        },
        "Panikstörung": {
            "title_en": "Panic disorder",
            "sections_en": {
                "definition": (
                    "In panic disorder, sudden attacks of anxiety (panic attacks) occur "
                    "repeatedly without an obvious external cause, together with a worry "
                    "about further attacks."
                ),
                "symptoms": (
                    "Racing heart, breathlessness, dizziness, trembling, sweating, "
                    "tightness in the chest and fear of death. The attack peaks after a "
                    "few minutes and usually fades within half an hour."
                ),
                "causes": (
                    "An inherited tendency, stressful life events, lasting stress and "
                    "heightened awareness of the body work together. The fear of the "
                    "body's reactions reinforces the vicious circle."
                ),
                "diagnostics": (
                    "First, physical causes such as heart, lung or thyroid diseases are "
                    "ruled out. Psychiatrists or psychotherapists make the diagnosis in a "
                    "conversation."
                ),
                "therapy": (
                    "Behavioural therapy with information and step-by-step exposure is "
                    "particularly effective. Antidepressants can help in addition. "
                    "Relaxation techniques and exercise support the treatment."
                ),
                "red_flags": (
                    "First-time chest pain, breathlessness or fainting should always be "
                    "checked physically, since they can also come from the heart or lung "
                    "– if in doubt call the emergency number 144 (Austria). For suicidal "
                    "thoughts call the telephone counselling line 142."
                ),
            },
            "keywords_en": [
                "Panic disorder",
                "Panic attack",
                "Anxiety",
                "Racing heart",
                "Behavioural therapy",
                "Antidepressants",
            ],
        },
        "Posttraumatische Belastungsstörung (PTBS)": {
            "title_en": "Post-traumatic stress disorder (PTSD)",
            "sections_en": {
                "definition": (
                    "Post-traumatic stress disorder can develop after an extremely "
                    "distressing event, for example after a serious accident, violence or "
                    "war."
                ),
                "symptoms": (
                    "Recurring distressing memories and nightmares (flashbacks), avoiding "
                    "reminders, being easily startled, sleep problems and a feeling of "
                    "inner numbness. The symptoms last weeks to years."
                ),
                "causes": (
                    "It is triggered by a traumatic experience. Whether a disorder "
                    "develops depends on the type and duration of the stress, earlier "
                    "experiences and the support afterwards."
                ),
                "diagnostics": (
                    "Psychiatrists or psychotherapists make the diagnosis in a detailed "
                    "conversation, often with questionnaires. Accompanying illnesses such "
                    "as depression are also recorded."
                ),
                "therapy": (
                    "Trauma-focused psychotherapy, for example with EMDR or behavioural "
                    "therapy, is the most important treatment. Medicines can be used "
                    "alongside it. Stability and safety come first."
                ),
                "red_flags": (
                    "Suicidal thoughts, self-harm or the feeling of losing control are a "
                    "reason to get help at once: telephone counselling 142 (Austria), and "
                    "in acute danger the emergency number 144."
                ),
            },
            "keywords_en": [
                "PTSD",
                "Trauma",
                "Flashbacks",
                "Nightmares",
                "Psychotherapy",
                "EMDR",
            ],
        },
    },
)
