from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Windpocken (Varizellen)",
        "doc_type": "Diagnose",
        "expected_category": "Pädiatrie",
        "term_en": "Chickenpox",
        "icd11_code": "1E90",
        "sections": {
            "definition": (
                "Windpocken sind eine hochansteckende Kinderkrankheit, ausgelöst durch das "
                "Varizella-Zoster-Virus."
            ),
            "symptoms": (
                "Typisch ist ein juckender Ausschlag mit Bläschen in verschiedenen "
                "Entwicklungsstadien am ganzen Körper, dazu leichtes Fieber."
            ),
            "causes": (
                "Die Übertragung erfolgt über Tröpfchen und den Inhalt der Bläschen; "
                "ungeimpfte Kinder im Kindergartenalter erkranken am häufigsten."
            ),
            "diagnostics": ("Der Kinderarzt erkennt Windpocken meist am typischen Ausschlag."),
            "therapy": (
                "Behandelt werden die Beschwerden: juckreizstillende Lotionen, kurze "
                "Fingernägel und bei Bedarf fiebersenkende Mittel. Die Impfung wird für "
                "Kinder empfohlen."
            ),
            "red_flags": (
                "Atemnot, Benommenheit, Krampfanfälle oder stark gerötete, eitrige Bläschen "
                "erfordern sofort ärztliche Hilfe."
            ),
        },
        "further_reading": [medlineplus("chickenpox", "Chickenpox")],
    },
    {
        "title": "Scharlach",
        "doc_type": "Diagnose",
        "expected_category": "Pädiatrie",
        "term_en": "Scarlet fever",
        "icd11_code": "1B50",
        "medications": ["penicillin"],
        "sections": {
            "definition": (
                "Scharlach ist eine bakterielle Kinderkrankheit durch Streptokokken, die vor "
                "allem Kinder im Schul- und Kindergartenalter betrifft."
            ),
            "symptoms": (
                "Typisch sind Halsschmerzen, Fieber, eine himbeerrote Zunge und ein "
                "feinfleckiger, samtiger Ausschlag, der in den Leisten beginnt."
            ),
            "causes": (
                "Die Bakterien werden über Tröpfchen übertragen. Man kann mehrmals an "
                "Scharlach erkranken."
            ),
            "diagnostics": (
                "Ein Rachenabstrich mit Schnelltest weist die Streptokokken in der "
                "kinderärztlichen Praxis nach."
            ),
            "therapy": (
                "Antibiotika verkürzen die Krankheit und senken das Risiko für Komplikationen. "
                "Nach 24 Stunden Behandlung sind Kinder meist nicht mehr ansteckend."
            ),
            "red_flags": (
                "Atemnot, Schluckunfähigkeit, starke Schwellung am Hals oder Teilnahmslosigkeit "
                "erfordern sofort ärztliche Hilfe."
            ),
        },
        "further_reading": [medlineplus("streptococcalinfections", "Streptococcal Infections")],
    },
    {
        "title": "Fieber bei Säuglingen und Kleinkindern",
        "doc_type": "Symptom",
        "expected_category": "Pädiatrie",
        "term_en": "Fever in children",
        "icd11_code": "MG26",
        "medications": ["acetaminophen", "ibuprofen"],
        "sections": {
            "definition": (
                "Fieber ist bei Kindern eine häufige und meist sinnvolle Abwehrreaktion. Ab "
                "38,5 °C spricht man bei Säuglingen und Kleinkindern von Fieber."
            ),
            "symptoms": (
                "Das Kind ist warm, müde oder quengelig, trinkt weniger und hat oft einen "
                "schnelleren Puls."
            ),
            "causes": (
                "Meist stecken harmlose virale Infekte dahinter, seltener bakterielle "
                "Infektionen wie eine Mittelohr- oder Harnwegsentzündung."
            ),
            "diagnostics": (
                "Entscheidend ist der Allgemeinzustand des Kindes. Der Kinderarzt sucht die "
                "Ursache durch Untersuchung und bei Bedarf Urin- oder Bluttests."
            ),
            "therapy": (
                "Ausreichend trinken und Ruhe sind wichtig. Fiebersenkende Mittel dienen dem "
                "Wohlbefinden, nicht dem Senken um jeden Preis."
            ),
            "red_flags": (
                "Fieber bei Säuglingen unter drei Monaten, Teilnahmslosigkeit, "
                "Nackensteifigkeit, Atemnot, ein Ausschlag, der sich nicht wegdrücken lässt, "
                "oder ein Krampfanfall: sofort Kinderarzt oder Notruf 144."
            ),
        },
        "further_reading": [medlineplus("fever", "Fever")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Windpocken (Varizellen)": {
            "title_en": "Chickenpox (varicella)",
            "sections_en": {
                "definition": (
                    "Chickenpox is a highly contagious childhood illness caused by the "
                    "varicella-zoster virus."
                ),
                "symptoms": (
                    "Typical is an itchy rash with blisters in different stages across the "
                    "whole body, together with mild fever."
                ),
                "causes": (
                    "It spreads by droplets and the content of the blisters; unvaccinated "
                    "children of nursery age fall ill most often."
                ),
                "diagnostics": (
                    "The paediatrician usually recognises chickenpox from the typical rash."
                ),
                "therapy": (
                    "The symptoms are treated: itch-relieving lotions, short fingernails and, "
                    "if needed, fever-lowering medicines. Vaccination is recommended for "
                    "children."
                ),
                "red_flags": (
                    "Shortness of breath, drowsiness, seizures or strongly reddened, purulent "
                    "blisters need medical help at once."
                ),
            },
            "keywords_en": [
                "Chickenpox",
                "Varicella",
                "Rash",
                "Blisters",
                "Children",
                "Vaccination",
            ],
        },
        "Scharlach": {
            "title_en": "Scarlet fever",
            "sections_en": {
                "definition": (
                    "Scarlet fever is a bacterial childhood illness caused by streptococci "
                    "that mainly affects children of school and nursery age."
                ),
                "symptoms": (
                    "Typical are a sore throat, fever, a raspberry-red tongue and a fine, "
                    "sandpaper-like rash that starts in the groin."
                ),
                "causes": (
                    "The bacteria spread by droplets. One can get scarlet fever more than once."
                ),
                "diagnostics": (
                    "A throat swab with a rapid test detects the streptococci in the "
                    "paediatric practice."
                ),
                "therapy": (
                    "Antibiotics shorten the illness and lower the risk of complications. "
                    "After 24 hours of treatment children are usually no longer contagious."
                ),
                "red_flags": (
                    "Shortness of breath, being unable to swallow, marked swelling of the "
                    "neck or listlessness need medical help at once."
                ),
            },
            "keywords_en": [
                "Scarlet fever",
                "Streptococci",
                "Sore throat",
                "Rash",
                "Antibiotics",
                "Children",
            ],
        },
        "Fieber bei Säuglingen und Kleinkindern": {
            "title_en": "Fever in babies and young children",
            "sections_en": {
                "definition": (
                    "Fever is a common and usually useful defence reaction in children. In "
                    "babies and young children, fever starts at 38.5 °C."
                ),
                "symptoms": (
                    "The child feels warm, is tired or fretful, drinks less and often has a "
                    "faster pulse."
                ),
                "causes": (
                    "Usually harmless viral infections are behind it, less often bacterial "
                    "infections such as an ear or urinary tract infection."
                ),
                "diagnostics": (
                    "The child's general condition is decisive. The paediatrician looks for "
                    "the cause by examination and, if needed, urine or blood tests."
                ),
                "therapy": (
                    "Drinking enough and rest are important. Fever-lowering medicines serve "
                    "comfort, not lowering the temperature at any price."
                ),
                "red_flags": (
                    "Fever in babies under three months, listlessness, a stiff neck, "
                    "shortness of breath, a rash that does not fade under pressure or a "
                    "seizure: see a paediatrician at once or call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": ["Fever", "Baby", "Child", "Temperature", "Paediatrician", "Seizure"],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Masern",
            "doc_type": "Diagnose",
            "expected_category": "Pädiatrie",
            "term_en": "Measles",
            "icd11_code": "1F03",
            "medications": ["paracetamol"],
            "sections": {
                "definition": (
                    "Masern sind eine hochansteckende Viruserkrankung, die vor allem bei "
                    "Kindern auftritt und schwere Komplikationen verursachen kann."
                ),
                "symptoms": (
                    "Zuerst kommen hohes Fieber, Husten, Schnupfen und gerötete Augen. Nach "
                    "einigen Tagen folgt ein roter, fleckiger Hautausschlag, der hinter den "
                    "Ohren beginnt. Weiße Flecken in der Mundschleimhaut sind typisch."
                ),
                "causes": (
                    "Das Masernvirus wird über winzige Tröpfchen beim Husten und Niesen "
                    "übertragen und ist schon beim Aufenthalt im selben Raum ansteckend."
                ),
                "diagnostics": (
                    "Die Kinderärztin erkennt die Masern am Krankheitsbild. Ein "
                    "Laborbefund bestätigt die Diagnose; die Erkrankung ist meldepflichtig."
                ),
                "therapy": (
                    "Es gibt keine ursächliche Behandlung. Bettruhe, viel Trinken und "
                    "fiebersenkende Mittel lindern die Beschwerden. Die Schutzimpfung "
                    "(zwei Dosen, meist als Kombinationsimpfung) schützt zuverlässig."
                ),
                "red_flags": (
                    "Atemnot, anhaltendes hohes Fieber, starke Ohrenschmerzen, "
                    "Verwirrtheit, Krampfanfälle oder Nackensteifigkeit können auf eine "
                    "Lungen- oder Gehirnentzündung hinweisen – sofort Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("measles", "Measles"),
                who("measles", "Measles"),
            ],
        },
        {
            "title": "Pseudokrupp (Krupp-Syndrom)",
            "doc_type": "Diagnose",
            "expected_category": "Pädiatrie",
            "term_en": "Croup",
            "icd11_code": "CA06.0",
            "medications": ["prednisolone", "dexamethasone"],
            "sections": {
                "definition": (
                    "Beim Pseudokrupp ist die Schleimhaut im Bereich des Kehlkopfes "
                    "geschwollen. Er betrifft vor allem Kleinkinder zwischen sechs Monaten "
                    "und drei Jahren und tritt häufig nachts auf."
                ),
                "symptoms": (
                    "Bellender Husten, Heiserkeit und ein pfeifendes Geräusch beim "
                    "Einatmen (Stridor). Bei schweren Verläufen sind die Atembewegungen "
                    "angestrengt, und das Kind ist unruhig."
                ),
                "causes": (
                    "Meist lösen Viren, besonders Parainfluenzaviren, den Infekt der oberen "
                    "Atemwege aus. Kalte Nachtluft und Aufregung verstärken die Beschwerden."
                ),
                "diagnostics": (
                    "Die Ärztin hört den typischen Husten und beurteilt die Atmung. Eine "
                    "Bildgebung ist meist nicht nötig."
                ),
                "therapy": (
                    "Ruhe bewahren, das Kind aufrecht halten und frische, kühle Luft "
                    "zuführen. Kortison (als Saft oder Zäpfchen) lässt die Schwellung "
                    "abklingen. Bei schwerer Atemnot werden im Krankenhaus Medikamente "
                    "zum Inhalieren gegeben."
                ),
                "red_flags": (
                    "Starke Atemnot, ein Einziehen am Brustkorb, blaue Lippen, Speicheln "
                    "bei fieberhafter Erkrankung oder ein sehr müdes Kind sind "
                    "Notfallzeichen – sofort Notruf 144."
                ),
            },
            "further_reading": [medlineplus("croup", "Croup")],
        },
        {
            "title": "Aufmerksamkeitsdefizit-/Hyperaktivitätsstörung (ADHS)",
            "doc_type": "Diagnose",
            "expected_category": "Psychiatrie",
            "term_en": "Attention deficit hyperactivity disorder",
            "icd11_code": "6A05",
            "medications": ["methylphenidate"],
            "sections": {
                "definition": (
                    "ADHS ist eine Entwicklungsstörung, bei der Aufmerksamkeit, "
                    "Impulskontrolle und Aktivität deutlich von der Altersnorm abweichen "
                    "und den Alltag in Schule und Familie beeinträchtigen."
                ),
                "symptoms": (
                    "Kinder sind unaufmerksam, leicht ablenkbar, zappelig und impulsiv. Sie "
                    "haben Mühe, Aufgaben zu beenden oder zu warten. Bei manchen steht die "
                    "Unaufmerksamkeit ohne Hyperaktivität im Vordergrund."
                ),
                "causes": (
                    "Erbliche Faktoren spielen eine große Rolle. Frühgeburt, "
                    "Rauchen oder Alkohol in der Schwangerschaft und weitere Einflüsse können "
                    "beitragen. Erziehung allein verursacht ADHS nicht."
                ),
                "diagnostics": (
                    "Kinderärztin, Kinderpsychiater oder Psychologen erheben die "
                    "Entwicklung mit Fragebögen, Gesprächen und Tests. Andere Ursachen wie "
                    "Hör- oder Sehprobleme werden ausgeschlossen."
                ),
                "therapy": (
                    "Die Behandlung kombiniert Aufklärung, Elterntraining, Maßnahmen in der "
                    "Schule und Verhaltenstherapie. In ausgeprägten Fällen können "
                    "Medikamente helfen, die ärztlich eingestellt und kontrolliert werden."
                ),
                "red_flags": (
                    "Selbstverletzung, Äußerungen über Suizid, aggressives Verhalten "
                    "gegen sich oder andere oder Alkohol- und Drogenkonsum sollten rasch "
                    "fachärztlich abgeklärt werden; in akuter Gefahr Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus(
                    "attentiondeficithyperactivitydisorder",
                    "Attention deficit hyperactivity disorder",
                )
            ],
        },
    ],
    {
        "Masern": {
            "title_en": "Measles",
            "sections_en": {
                "definition": (
                    "Measles is a highly contagious viral disease that occurs mainly in "
                    "children and can cause serious complications."
                ),
                "symptoms": (
                    "First come high fever, cough, a runny nose and red eyes. After a few "
                    "days a red, blotchy rash follows that starts behind the ears. White "
                    "spots in the lining of the mouth are typical."
                ),
                "causes": (
                    "The measles virus spreads through tiny droplets when coughing and "
                    "sneezing and is infectious simply from being in the same room."
                ),
                "diagnostics": (
                    "The paediatrician recognises measles from the picture of the "
                    "illness. A laboratory result confirms the diagnosis; the disease has "
                    "to be reported."
                ),
                "therapy": (
                    "There is no treatment of the cause. Bed rest, plenty of fluids and "
                    "fever-lowering medicines ease the symptoms. The vaccination (two "
                    "doses, usually as a combination vaccine) protects reliably."
                ),
                "red_flags": (
                    "Breathlessness, persistent high fever, severe earache, confusion, "
                    "seizures or a stiff neck can point to pneumonia or inflammation of "
                    "the brain – call the emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Measles",
                "Rash",
                "Fever",
                "Vaccination",
                "Children",
                "Contagious",
            ],
        },
        "Pseudokrupp (Krupp-Syndrom)": {
            "title_en": "Croup",
            "sections_en": {
                "definition": (
                    "In croup the lining around the voice box is swollen. It mainly "
                    "affects toddlers between six months and three years of age and "
                    "often occurs at night."
                ),
                "symptoms": (
                    "A barking cough, hoarseness and a whistling sound when breathing in "
                    "(stridor). In severe cases breathing movements are laboured and the "
                    "child is restless."
                ),
                "causes": (
                    "Viruses, especially parainfluenza viruses, usually trigger the "
                    "infection of the upper airways. Cold night air and excitement make "
                    "the symptoms worse."
                ),
                "diagnostics": (
                    "The doctor hears the typical cough and assesses the breathing. "
                    "Imaging is usually not needed."
                ),
                "therapy": (
                    "Stay calm, keep the child upright and provide fresh, cool air. "
                    "Cortisone (as syrup or suppository) makes the swelling go down. In "
                    "severe breathlessness, medicines for inhalation are given in "
                    "hospital."
                ),
                "red_flags": (
                    "Severe breathlessness, drawing in at the chest, blue lips, drooling "
                    "with a feverish illness or a very sleepy child are emergency signs – "
                    "call the emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Croup",
                "Barking cough",
                "Stridor",
                "Toddlers",
                "Cortisone",
                "Breathlessness",
            ],
        },
        "Aufmerksamkeitsdefizit-/Hyperaktivitätsstörung (ADHS)": {
            "title_en": "Attention deficit hyperactivity disorder (ADHD)",
            "sections_en": {
                "definition": (
                    "ADHD is a developmental disorder in which attention, impulse "
                    "control and activity differ markedly from the norm for the age and "
                    "affect everyday life at school and in the family."
                ),
                "symptoms": (
                    "Children are inattentive, easily distracted, fidgety and impulsive. "
                    "They have trouble finishing tasks or waiting. In some, inattention "
                    "without hyperactivity is in the foreground."
                ),
                "causes": (
                    "Inherited factors play a large role. Premature birth, smoking or "
                    "alcohol in pregnancy and other influences can contribute. Parenting "
                    "alone does not cause ADHD."
                ),
                "diagnostics": (
                    "The paediatrician, child psychiatrist or psychologist assesses "
                    "development with questionnaires, conversations and tests. Other "
                    "causes such as hearing or vision problems are ruled out."
                ),
                "therapy": (
                    "Treatment combines information, parent training, measures at school "
                    "and behavioural therapy. In marked cases medicines can help, which "
                    "are set up and monitored by a doctor."
                ),
                "red_flags": (
                    "Self-harm, statements about suicide, aggressive behaviour against "
                    "oneself or others, or alcohol and drug use should be assessed by a "
                    "specialist promptly; in acute danger call the emergency number 144 "
                    "(Austria)."
                ),
            },
            "keywords_en": [
                "ADHD",
                "Attention",
                "Hyperactivity",
                "Impulsivity",
                "Behavioural therapy",
                "Child",
            ],
        },
    },
)
