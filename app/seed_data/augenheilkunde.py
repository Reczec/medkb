from app.seed_data.english import with_english
from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Grauer Star (Katarakt)",
        "doc_type": "Diagnose",
        "expected_category": "Augenheilkunde",
        "term_en": "Cataract",
        "icd11_code": "9B10",
        "sections": {
            "definition": (
                "Beim grauen Star (Katarakt) trübt sich die Augenlinse zunehmend ein. Er ist "
                "weltweit eine der häufigsten Ursachen für Sehverlust."
            ),
            "symptoms": (
                "Betroffene sehen verschwommen wie durch einen Schleier, sind blendempfindlich, "
                "besonders nachts beim Autofahren, und nehmen Farben blasser wahr."
            ),
            "causes": (
                "Meist ist die Linsentrübung altersbedingt. Diabetes, Rauchen, starke "
                "UV-Belastung und manche Medikamente wie Kortison fördern sie."
            ),
            "diagnostics": (
                "Der Augenarzt untersucht die Linse mit der Spaltlampe und prüft die Sehschärfe."
            ),
            "therapy": (
                "Wirksam ist nur die Operation: Die getrübte Linse wird entfernt und durch eine "
                "Kunstlinse ersetzt. Der Eingriff gehört zu den häufigsten Operationen."
            ),
            "red_flags": (
                "Ein plötzlicher Sehverlust gehört nicht zum grauen Star und muss sofort "
                "augenärztlich abgeklärt werden."
            ),
        },
        "further_reading": [
            medlineplus("cataract", "Cataract"),
            who("blindness-and-visual-impairment", "Blindness and vision impairment"),
        ],
    },
    {
        "title": "Grüner Star (Glaukom)",
        "doc_type": "Diagnose",
        "expected_category": "Augenheilkunde",
        "term_en": "Glaucoma",
        "icd11_code": "9C61",
        "medications": ["latanoprost", "timolol"],
        "sections": {
            "definition": (
                "Der grüne Star (Glaukom) ist eine Erkrankung, bei der der Sehnerv "
                "fortschreitend geschädigt wird, häufig verbunden mit erhöhtem "
                "Augeninnendruck."
            ),
            "symptoms": (
                "Lange Zeit bemerken Betroffene nichts. Später fallen Teile des "
                "Gesichtsfelds aus, zunächst am Rand, sodass der Schaden oft spät auffällt."
            ),
            "causes": (
                "Risikofaktoren sind ein erhöhter Augeninnendruck, höheres Alter, familiäre "
                "Belastung und starke Kurzsichtigkeit."
            ),
            "diagnostics": (
                "Beim Augenarzt werden der Augeninnendruck gemessen, der Sehnerv beurteilt "
                "und das Gesichtsfeld geprüft."
            ),
            "therapy": (
                "Augentropfen senken den Augeninnendruck; reichen sie nicht, kommen Laser oder "
                "Operation in Frage. Bereits verlorene Sehkraft lässt sich nicht "
                "zurückgewinnen."
            ),
            "red_flags": (
                "Plötzliche starke Augenschmerzen mit rotem Auge, verschwommenem Sehen, "
                "Übelkeit und Kopfschmerzen können ein akuter Glaukomanfall sein – ein "
                "Notfall, sofort Augenklinik oder Notruf 144."
            ),
        },
        "further_reading": [medlineplus("glaucoma", "Glaucoma")],
    },
    {
        "title": "Bindehautentzündung (Konjunktivitis)",
        "doc_type": "Diagnose",
        "expected_category": "Augenheilkunde",
        "term_en": "Conjunctivitis",
        "icd11_code": "9A60",
        "sections": {
            "definition": (
                "Die Konjunktivitis ist eine Entzündung der Bindehaut des Auges. Sie ist "
                "häufig und meist harmlos."
            ),
            "symptoms": (
                "Das Auge ist gerötet, juckt oder brennt, tränt und kann verklebt sein. Ein "
                "Fremdkörpergefühl ist typisch; die Sehschärfe bleibt meist erhalten."
            ),
            "causes": (
                "Auslöser sind Viren, Bakterien, Allergien oder Reizungen, etwa durch Rauch, "
                "Kontaktlinsen oder trockene Luft."
            ),
            "diagnostics": (
                "Die Diagnose stellt der Augenarzt anhand des Befunds an der Spaltlampe; "
                "selten wird ein Abstrich genommen."
            ),
            "therapy": (
                "Je nach Ursache helfen Tränenersatzmittel, antiallergische oder "
                "antibiotische Augentropfen. Gute Handhygiene verhindert die Ansteckung."
            ),
            "red_flags": (
                "Starke Schmerzen, Lichtscheu oder eine Verschlechterung des Sehens sprechen "
                "gegen eine einfache Bindehautentzündung und müssen augenärztlich abgeklärt "
                "werden."
            ),
        },
        "further_reading": [medlineplus("pinkeye", "Pink Eye")],
    },
]

ENTRIES = with_english(
    ENTRIES,
    {
        "Grauer Star (Katarakt)": {
            "title_en": "Cataract",
            "sections_en": {
                "definition": (
                    "With a cataract, the lens of the eye gradually becomes cloudy. It is one "
                    "of the most common causes of vision loss worldwide."
                ),
                "symptoms": (
                    "Affected people see blurred, as if through a veil, are sensitive to "
                    "glare, especially when driving at night, and perceive colours as paler."
                ),
                "causes": (
                    "The clouding is usually age-related. Diabetes, smoking, strong UV "
                    "exposure and some medicines such as cortisone promote it."
                ),
                "diagnostics": (
                    "The eye doctor examines the lens with a slit lamp and checks visual acuity."
                ),
                "therapy": (
                    "Only surgery helps: the clouded lens is removed and replaced with an "
                    "artificial lens. The operation is one of the most common surgical "
                    "procedures."
                ),
                "red_flags": (
                    "Sudden vision loss is not part of a cataract and must be assessed by an "
                    "eye doctor immediately."
                ),
            },
            "keywords_en": [
                "Cataract",
                "Lens",
                "Blurred vision",
                "Glare",
                "Eye surgery",
                "Visual acuity",
            ],
        },
        "Grüner Star (Glaukom)": {
            "title_en": "Glaucoma",
            "sections_en": {
                "definition": (
                    "Glaucoma is a disease in which the optic nerve is progressively damaged, "
                    "often together with raised pressure inside the eye."
                ),
                "symptoms": (
                    "For a long time affected people notice nothing. Later, parts of the "
                    "visual field are lost, first at the edges, so the damage is often "
                    "noticed late."
                ),
                "causes": (
                    "Risk factors are raised eye pressure, higher age, family history and "
                    "marked short-sightedness."
                ),
                "diagnostics": (
                    "At the eye doctor, the eye pressure is measured, the optic nerve is "
                    "assessed and the visual field is tested."
                ),
                "therapy": (
                    "Eye drops lower the eye pressure; if they are not enough, laser "
                    "treatment or surgery come into consideration. Vision that has already "
                    "been lost cannot be regained."
                ),
                "red_flags": (
                    "Sudden severe eye pain with a red eye, blurred vision, nausea and "
                    "headache can be an acute glaucoma attack – an emergency, go to an eye "
                    "clinic at once or call the emergency number 144 (Austria)."
                ),
            },
            "keywords_en": [
                "Glaucoma",
                "Eye pressure",
                "Optic nerve",
                "Visual field",
                "Eye drops",
                "Vision loss",
            ],
        },
        "Bindehautentzündung (Konjunktivitis)": {
            "title_en": "Conjunctivitis (pink eye)",
            "sections_en": {
                "definition": (
                    "Conjunctivitis is an inflammation of the conjunctiva, the thin membrane "
                    "of the eye. It is common and usually harmless."
                ),
                "symptoms": (
                    "The eye is red, itches or burns, waters and may be stuck together. A "
                    "feeling of a foreign body is typical; visual acuity is usually "
                    "preserved."
                ),
                "causes": (
                    "Triggers are viruses, bacteria, allergies or irritation, for example "
                    "from smoke, contact lenses or dry air."
                ),
                "diagnostics": (
                    "The eye doctor makes the diagnosis from the findings under the slit "
                    "lamp; a swab is rarely taken."
                ),
                "therapy": (
                    "Depending on the cause, artificial tears or antiallergic or antibiotic "
                    "eye drops help. Good hand hygiene prevents spreading."
                ),
                "red_flags": (
                    "Severe pain, sensitivity to light or worsening vision speak against "
                    "simple conjunctivitis and must be assessed by an eye doctor."
                ),
            },
            "keywords_en": [
                "Conjunctivitis",
                "Pink eye",
                "Red eye",
                "Itching",
                "Eye drops",
                "Allergy",
            ],
        },
    },
)
