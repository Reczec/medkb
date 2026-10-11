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
