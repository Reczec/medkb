from app.seed_data.english import with_english
from app.seed_data.links import gesundheit_gv, medlineplus

ENTRIES = [
    {
        "title": "Neurodermitis (atopisches Ekzem)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "term_en": "Atopic dermatitis",
        "icd11_code": "EA80",
        "medications": ["hydrocortisone", "tacrolimus"],
        "sections": {
            "definition": (
                "Die Neurodermitis ist eine chronisch-entzündliche Hauterkrankung, die in "
                "Schüben verläuft und häufig im Kindesalter beginnt."
            ),
            "symptoms": (
                "Typisch sind starker Juckreiz und trockene, gerötete, teils nässende "
                "Hautstellen, bei Erwachsenen oft in Ellenbeugen und Kniekehlen."
            ),
            "causes": (
                "Eine gestörte Hautbarriere und ein überempfindliches Immunsystem wirken "
                "zusammen. Auslöser für Schübe sind etwa Stress, Schwitzen, Wolle oder "
                "Infekte."
            ),
            "diagnostics": (
                "Der Hautarzt stellt die Diagnose anhand des Hautbilds und der "
                "Krankengeschichte; Allergietests klären mögliche Auslöser."
            ),
            "therapy": (
                "Basis ist konsequentes Eincremen mit rückfettender Pflege. Im Schub helfen "
                "entzündungshemmende Cremes, bei schweren Formen moderne Systemtherapien."
            ),
            "red_flags": (
                "Plötzlich auftretende schmerzhafte Bläschen und Fieber bei Neurodermitis "
                "können eine gefährliche Herpes-Infektion der Haut sein – rasch zum Arzt."
            ),
        },
        "further_reading": [
            gesundheit_gv("haut-haare-naegel/neurodermitis", "Neurodermitis"),
            medlineplus("eczema", "Eczema"),
        ],
    },
    {
        "title": "Schuppenflechte (Psoriasis)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "term_en": "Psoriasis",
        "icd11_code": "EA90",
        "medications": ["calcipotriene", "methotrexate"],
        "sections": {
            "definition": (
                "Die Psoriasis ist eine chronisch-entzündliche Erkrankung, bei der sich die "
                "Haut stark beschleunigt erneuert. Sie ist nicht ansteckend."
            ),
            "symptoms": (
                "Typisch sind scharf begrenzte, gerötete Herde mit silbrigen Schuppen, oft an "
                "Ellenbogen, Knien und Kopfhaut. Auch Nägel und Gelenke können beteiligt sein."
            ),
            "causes": (
                "Eine erbliche Veranlagung und das Immunsystem spielen die Hauptrolle; Stress, "
                "Infekte und Verletzungen der Haut können Schübe auslösen."
            ),
            "diagnostics": (
                "Die Diagnose erfolgt meist anhand des typischen Hautbilds durch den Hautarzt."
            ),
            "therapy": (
                "Je nach Schwere kommen Cremes, Lichttherapie oder innerliche Medikamente und "
                "Biologika zum Einsatz."
            ),
            "red_flags": (
                "Großflächig gerötete Haut am ganzen Körper mit Fieber oder Schüttelfrost ist "
                "ein Notfall und muss sofort behandelt werden."
            ),
        },
        "further_reading": [medlineplus("psoriasis", "Psoriasis")],
    },
    {
        "title": "Gürtelrose (Herpes zoster)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "term_en": "Herpes zoster",
        "icd11_code": "1E91",
        "medications": ["valacyclovir", "acyclovir"],
        "sections": {
            "definition": (
                "Die Gürtelrose ist eine Reaktivierung des Windpockenvirus, das nach einer "
                "Windpockenerkrankung in den Nervenknoten verbleibt."
            ),
            "symptoms": (
                "Nach brennenden Schmerzen tritt ein gürtelförmiger, einseitiger "
                "Hautausschlag mit Bläschen auf, meist am Rumpf."
            ),
            "causes": (
                "Ein nachlassendes Immunsystem durch Alter, Stress oder Erkrankungen lässt das "
                "ruhende Virus wieder aktiv werden."
            ),
            "diagnostics": (
                "Das typische einseitige Hautbild genügt meist für die Diagnose beim Hautarzt "
                "oder Hausarzt."
            ),
            "therapy": (
                "Virushemmende Medikamente wirken am besten in den ersten Tagen. Eine gute "
                "Schmerzbehandlung beugt anhaltenden Nervenschmerzen vor; für Ältere gibt es "
                "eine Impfung."
            ),
            "red_flags": (
                "Ein Ausschlag im Gesicht, besonders nahe dem Auge, muss am selben Tag "
                "ärztlich behandelt werden."
            ),
        },
        "further_reading": [medlineplus("shingles", "Shingles")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Neurodermitis (atopisches Ekzem)": {
            "title_en": "Atopic dermatitis (eczema)",
            "sections_en": {
                "definition": (
                    "Atopic dermatitis is a chronic inflammatory skin disease that runs in "
                    "flares and often begins in childhood."
                ),
                "symptoms": (
                    "Typical are severe itching and dry, reddened, sometimes weeping skin "
                    "patches, in adults often in the elbow creases and behind the knees."
                ),
                "causes": (
                    "A disturbed skin barrier and an overreactive immune system act together. "
                    "Triggers for flares are, for example, stress, sweating, wool or "
                    "infections."
                ),
                "diagnostics": (
                    "The skin doctor makes the diagnosis from the skin appearance and the "
                    "history; allergy tests clarify possible triggers."
                ),
                "therapy": (
                    "The basis is consistent moisturising with rich skin care. During a "
                    "flare, anti-inflammatory creams help; severe forms are treated with "
                    "modern systemic therapies."
                ),
                "red_flags": (
                    "Painful blisters and fever appearing suddenly in atopic dermatitis can "
                    "be a dangerous herpes infection of the skin – see a doctor quickly."
                ),
            },
            "keywords_en": [
                "Eczema",
                "Atopic dermatitis",
                "Itching",
                "Dry skin",
                "Flare",
                "Skin care",
            ],
        },
        "Schuppenflechte (Psoriasis)": {
            "title_en": "Psoriasis",
            "sections_en": {
                "definition": (
                    "Psoriasis is a chronic inflammatory disease in which the skin renews "
                    "itself much faster than normal. It is not contagious."
                ),
                "symptoms": (
                    "Typical are sharply defined, reddened patches with silvery scales, often "
                    "on the elbows, knees and scalp. Nails and joints can also be involved."
                ),
                "causes": (
                    "A hereditary predisposition and the immune system play the main role; "
                    "stress, infections and skin injuries can trigger flares."
                ),
                "diagnostics": (
                    "The diagnosis is usually made from the typical skin appearance by the "
                    "skin doctor."
                ),
                "therapy": (
                    "Depending on severity, creams, light therapy or internal medicines and "
                    "biologics are used."
                ),
                "red_flags": (
                    "Widespread reddened skin over the whole body with fever or shivering is "
                    "an emergency and must be treated at once."
                ),
            },
            "keywords_en": [
                "Psoriasis",
                "Scales",
                "Skin",
                "Light therapy",
                "Joints",
                "Immune system",
            ],
        },
        "Gürtelrose (Herpes zoster)": {
            "title_en": "Shingles (herpes zoster)",
            "sections_en": {
                "definition": (
                    "Shingles is a reactivation of the chickenpox virus, which stays in the "
                    "nerve ganglia after a chickenpox infection."
                ),
                "symptoms": (
                    "After burning pain, a belt-shaped, one-sided rash with blisters appears, "
                    "usually on the trunk."
                ),
                "causes": (
                    "A declining immune system due to age, stress or illness lets the dormant "
                    "virus become active again."
                ),
                "diagnostics": (
                    "The typical one-sided skin picture is usually enough for the diagnosis "
                    "by the skin doctor or family doctor."
                ),
                "therapy": (
                    "Antiviral medicines work best in the first days. Good pain treatment "
                    "prevents lasting nerve pain; a vaccination is available for older "
                    "people."
                ),
                "red_flags": (
                    "A rash on the face, especially near the eye, must be treated by a doctor "
                    "the same day."
                ),
            },
            "keywords_en": [
                "Shingles",
                "Herpes zoster",
                "Blisters",
                "Nerve pain",
                "Antiviral",
                "Vaccination",
            ],
        },
    },
)


EXTRA = with_english(
    [
        {
            "title": "Akne",
            "doc_type": "Diagnose",
            "expected_category": "Dermatologie",
            "term_en": "Acne",
            "icd11_code": "ED80",
            "medications": ["benzoyl peroxide", "adapalene", "isotretinoin"],
            "sections": {
                "definition": (
                    "Akne ist eine häufige Hauterkrankung, bei der die Talgdrüsen und "
                    "Haarfollikel entzündet sind. Sie betrifft vor allem Gesicht, Brust und "
                    "Rücken."
                ),
                "symptoms": (
                    "Mitesser, Pickel, gerötete Knötchen und Pusteln, in schweren Fällen "
                    "schmerzhafte Knoten und Narben. Die Haut ist oft fettig."
                ),
                "causes": (
                    "Hormonelle Veränderungen in der Pubertät steigern die Talgproduktion, "
                    "dazu kommen verstopfte Poren und Bakterien auf der Haut. Veranlagung, "
                    "bestimmte Medikamente und Kosmetika können eine Rolle spielen."
                ),
                "diagnostics": (
                    "Die Hautärztin oder der Hautarzt erkennt Akne am Hautbild und stuft den "
                    "Schweregrad ein. Bei Frauen mit Zyklusstörungen werden Hormone "
                    "untersucht."
                ),
                "therapy": (
                    "Milde Formen behandeln Cremes mit Benzoylperoxid oder Retinoiden. Bei "
                    "stärkerer Akne kommen Antibiotika, hormonelle Therapie oder "
                    "Isotretinoin zum Einsatz. Pickel nicht ausdrücken, die Haut mild "
                    "reinigen."
                ),
                "red_flags": (
                    "Isotretinoin darf in der Schwangerschaft nicht eingenommen werden. "
                    "Plötzlich sehr schmerzhafte, tief sitzende Entzündungen mit Fieber oder "
                    "starker seelischer Belastung sollten dermatologisch abgeklärt werden."
                ),
            },
            "further_reading": [medlineplus("acne", "Acne")],
        },
        {
            "title": "Nesselsucht (Urtikaria)",
            "doc_type": "Diagnose",
            "expected_category": "Dermatologie",
            "term_en": "Urticaria",
            "icd11_code": "EB00",
            "medications": ["cetirizine", "prednisolone"],
            "sections": {
                "definition": (
                    "Bei der Nesselsucht treten juckende, erhabene Quaddeln auf der Haut auf, "
                    "die nach Stunden wieder verschwinden. Eine akute Urtikaria dauert "
                    "weniger als sechs Wochen, eine chronische länger."
                ),
                "symptoms": (
                    "Stark juckende, rote bis blasse Quaddeln, die ihre Stelle wechseln. "
                    "Manchmal schwellen Lippen oder Augenlider an."
                ),
                "causes": (
                    "Auslöser sind Infekte, Medikamente, Nahrungsmittel, Insektenstiche, "
                    "Kälte, Druck oder Hitze. Bei der chronischen Form bleibt die Ursache "
                    "oft unklar."
                ),
                "diagnostics": (
                    "Die Hautärztin fragt nach Auslösern und führt ein Beschwerdetagebuch. "
                    "Bei Verdacht auf Allergie folgen Haut- oder Bluttests."
                ),
                "therapy": (
                    "Auslöser meiden und Antihistaminika einnehmen, bei Bedarf in höherer "
                    "Dosierung. Bei schweren Schüben kann kurzzeitig Kortison nötig sein, bei "
                    "chronischem Verlauf stehen weitere Medikamente zur Verfügung."
                ),
                "red_flags": (
                    "Schwellung von Zunge, Rachen oder Gesicht, Atemnot, Schwindel oder "
                    "Kreislaufprobleme nach Kontakt mit einem Auslöser können eine "
                    "allergische Notfallreaktion sein – sofort Notruf 144."
                ),
            },
            "further_reading": [medlineplus("hives", "Hives")],
        },
        {
            "title": "Schwarzer Hautkrebs (Melanom)",
            "doc_type": "Diagnose",
            "expected_category": "Dermatologie",
            "term_en": "Melanoma",
            "icd11_code": "2C30",
            "medications": [],
            "sections": {
                "definition": (
                    "Das Melanom ist ein bösartiger Tumor der pigmentbildenden Zellen der "
                    "Haut. Es ist seltener als andere Hautkrebsarten, aber gefährlicher."
                ),
                "symptoms": (
                    "Ein neuer oder sich verändernder Fleck: ungleichmäßig geformt, "
                    "unscharf begrenzt, mehrfarbig, größer als sechs Millimeter oder mit "
                    "wachsender Erhebung (ABCDE-Regel). Auch Juckreiz oder Bluten sind "
                    "möglich."
                ),
                "causes": (
                    "Hauptursache ist übermäßige UV-Strahlung, vor allem Sonnenbrände in der "
                    "Kindheit und Solarien. Viele Muttermale, helle Haut und familiäre "
                    "Häufung erhöhen das Risiko."
                ),
                "diagnostics": (
                    "Die Hautärztin betrachtet verdächtige Muttermale mit dem Dermatoskop. "
                    "Ein auffälliger Fleck wird operativ entfernt und feingeweblich "
                    "untersucht."
                ),
                "therapy": (
                    "Im frühen Stadium reicht meist die vollständige operative Entfernung. "
                    "Bei fortgeschrittener Erkrankung kommen Immuntherapie oder gezielte "
                    "Medikamente zum Einsatz. Regelmäßige Hautkrebs-Vorsorge verbessert die "
                    "Heilungschancen."
                ),
                "red_flags": (
                    "Ein Muttermal, das sich in Form, Farbe oder Größe verändert, blutet "
                    "oder nässt, sollte zeitnah dermatologisch kontrolliert werden. Je "
                    "früher die Entfernung, desto besser die Prognose."
                ),
            },
            "further_reading": [
                medlineplus("melanoma", "Melanoma"),
                medlineplus("skincancer", "Skin cancer"),
            ],
        },
        {
            "title": "Nagelpilz und Fußpilz",
            "doc_type": "Diagnose",
            "expected_category": "Dermatologie",
            "term_en": "Dermatophytosis",
            "icd11_code": "1F28",
            "medications": ["terbinafine", "clotrimazole"],
            "sections": {
                "definition": (
                    "Fuß- und Nagelpilz sind Pilzinfektionen der Haut zwischen den Zehen, "
                    "an den Fußsohlen und an den Zehen- oder Fingernägeln, meist durch "
                    "Fadenpilze (Dermatophyten)."
                ),
                "symptoms": (
                    "Beim Fußpilz jucken und schuppen die Zehenzwischenräume, die Haut ist "
                    "gerötet und rissig. Beim Nagelpilz werden Nägel gelblich, verdickt und "
                    "brüchig."
                ),
                "causes": (
                    "Die Pilze gedeihen in feuchtwarmer Umgebung, etwa in Schwimmbädern, "
                    "Saunen und Gemeinschaftsduschen. Schwitzende Füße, enge Schuhe, "
                    "Diabetes und eine schwache Abwehr begünstigen die Infektion."
                ),
                "diagnostics": (
                    "Die Ärztin sieht sich die betroffene Stelle an und entnimmt "
                    "Schuppen oder Nagelspäne für eine mikroskopische Untersuchung und "
                    "Pilzkultur."
                ),
                "therapy": (
                    "Fußpilz wird mit Antipilzcremes über mehrere Wochen behandelt. Bei "
                    "Nagelpilz kommen spezielle Nagellacke, in hartnäckigen Fällen "
                    "Tabletten zum Einsatz. Füße gut trocknen und Schuhe wechseln."
                ),
                "red_flags": (
                    "Rötung und Schwellung mit Schmerzen, Fieber oder rote Streifen am "
                    "Bein können auf eine bakterielle Entzündung hinweisen; Menschen mit "
                    "Diabetes sollten Fußveränderungen früh ärztlich abklären lassen."
                ),
            },
            "further_reading": [
                medlineplus("athletesfoot", "Athlete's foot"),
                medlineplus("fungalinfections", "Fungal infections"),
            ],
        },
    ],
    {
        "Akne": {
            "title_en": "Acne",
            "sections_en": {
                "definition": (
                    "Acne is a common skin disease in which the oil glands and hair "
                    "follicles are inflamed. It mainly affects the face, chest and back."
                ),
                "symptoms": (
                    "Blackheads, pimples, red nodules and pustules, in severe cases "
                    "painful lumps and scars. The skin is often oily."
                ),
                "causes": (
                    "Hormonal changes in puberty increase oil production, and blocked "
                    "pores and bacteria on the skin add to it. Inherited tendency, "
                    "certain medicines and cosmetics can play a role."
                ),
                "diagnostics": (
                    "The skin doctor recognises acne from the appearance of the skin and "
                    "grades its severity. In women with cycle disorders, hormones are "
                    "examined."
                ),
                "therapy": (
                    "Mild forms are treated with creams containing benzoyl peroxide or "
                    "retinoids. In more severe acne, antibiotics, hormonal therapy or "
                    "isotretinoin are used. Do not squeeze pimples and clean the skin "
                    "gently."
                ),
                "red_flags": (
                    "Isotretinoin must not be taken during pregnancy. Suddenly very "
                    "painful, deep inflammation with fever or marked emotional distress "
                    "should be assessed by a skin doctor."
                ),
            },
            "keywords_en": [
                "Acne",
                "Pimples",
                "Skin",
                "Sebaceous glands",
                "Retinoids",
                "Dermatologist",
            ],
        },
        "Nesselsucht (Urtikaria)": {
            "title_en": "Hives (urticaria)",
            "sections_en": {
                "definition": (
                    "In hives, itchy, raised wheals appear on the skin and go away again "
                    "after hours. Acute urticaria lasts less than six weeks, chronic "
                    "urticaria longer."
                ),
                "symptoms": (
                    "Strongly itching, red to pale wheals that move from place to place. "
                    "Sometimes the lips or eyelids swell."
                ),
                "causes": (
                    "Triggers are infections, medicines, foods, insect stings, cold, "
                    "pressure or heat. In the chronic form the cause often stays unclear."
                ),
                "diagnostics": (
                    "The skin doctor asks about triggers and keeps a symptom diary. If an "
                    "allergy is suspected, skin or blood tests follow."
                ),
                "therapy": (
                    "Avoid triggers and take antihistamines, if needed in a higher dose. "
                    "In severe flare-ups cortisone can be needed for a short time; in a "
                    "chronic course further medicines are available."
                ),
                "red_flags": (
                    "Swelling of the tongue, throat or face, breathlessness, dizziness or "
                    "circulation problems after contact with a trigger can be an allergic "
                    "emergency – call the emergency number 144 (Austria) at once."
                ),
            },
            "keywords_en": [
                "Hives",
                "Urticaria",
                "Wheals",
                "Itching",
                "Antihistamines",
                "Allergy",
            ],
        },
        "Schwarzer Hautkrebs (Melanom)": {
            "title_en": "Malignant melanoma (skin cancer)",
            "sections_en": {
                "definition": (
                    "Melanoma is a malignant tumour of the pigment-forming cells of the "
                    "skin. It is rarer than other types of skin cancer but more dangerous."
                ),
                "symptoms": (
                    "A new or changing spot: irregular in shape, with blurred edges, "
                    "several colours, larger than six millimetres or with a growing "
                    "raised area (ABCDE rule). Itching or bleeding are also possible."
                ),
                "causes": (
                    "The main cause is excessive UV radiation, above all sunburns in "
                    "childhood and sunbeds. Many moles, fair skin and cases in the family "
                    "raise the risk."
                ),
                "diagnostics": (
                    "The skin doctor looks at suspicious moles with a dermatoscope. A "
                    "conspicuous spot is removed surgically and examined under the "
                    "microscope."
                ),
                "therapy": (
                    "In an early stage, complete surgical removal is usually enough. In "
                    "advanced disease, immunotherapy or targeted medicines are used. "
                    "Regular skin cancer screening improves the chances of cure."
                ),
                "red_flags": (
                    "A mole that changes in shape, colour or size, bleeds or weeps should "
                    "be checked by a skin doctor promptly. The earlier the removal, the "
                    "better the outlook."
                ),
            },
            "keywords_en": [
                "Melanoma",
                "Skin cancer",
                "Mole",
                "UV radiation",
                "ABCDE rule",
                "Skin screening",
            ],
        },
        "Nagelpilz und Fußpilz": {
            "title_en": "Nail fungus and athlete's foot",
            "sections_en": {
                "definition": (
                    "Athlete's foot and nail fungus are fungal infections of the skin "
                    "between the toes, on the soles and on the toenails or fingernails, "
                    "usually caused by thread fungi (dermatophytes)."
                ),
                "symptoms": (
                    "In athlete's foot the spaces between the toes itch and flake, and "
                    "the skin is red and cracked. In nail fungus nails become yellowish, "
                    "thickened and brittle."
                ),
                "causes": (
                    "The fungi thrive in a warm, moist environment, such as swimming "
                    "pools, saunas and shared showers. Sweaty feet, tight shoes, diabetes "
                    "and weak defences favour the infection."
                ),
                "diagnostics": (
                    "The doctor looks at the affected area and takes skin flakes or nail "
                    "clippings for a microscopic examination and fungal culture."
                ),
                "therapy": (
                    "Athlete's foot is treated with antifungal creams over several weeks. "
                    "In nail fungus special nail varnishes and, in stubborn cases, tablets "
                    "are used. Dry the feet well and change shoes."
                ),
                "red_flags": (
                    "Redness and swelling with pain, fever or red streaks on the leg can "
                    "point to a bacterial infection; people with diabetes should have "
                    "changes to the feet checked by a doctor early."
                ),
            },
            "keywords_en": [
                "Athlete's foot",
                "Nail fungus",
                "Fungal infection",
                "Dermatophytes",
                "Antifungal",
                "Feet",
            ],
        },
    },
)
