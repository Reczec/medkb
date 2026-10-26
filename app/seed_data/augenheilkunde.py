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


EXTRA = with_english(
    [
        {
            "title": "Kurzsichtigkeit (Myopie)",
            "doc_type": "Diagnose",
            "expected_category": "Augenheilkunde",
            "term_en": "Myopia",
            "icd11_code": "9D00.0",
            "medications": [],
            "sections": {
                "definition": (
                    "Bei der Kurzsichtigkeit sieht man nahe Dinge scharf, weit entfernte "
                    "Dinge aber unscharf, weil der Augapfel zu lang oder die Brechkraft zu "
                    "stark ist."
                ),
                "symptoms": (
                    "Entfernte Schilder, die Tafel oder Gesichter werden verschwommen "
                    "gesehen. Betroffene kneifen die Augen zusammen, und manchmal treten "
                    "Kopfschmerzen oder müde Augen auf."
                ),
                "causes": (
                    "Die Veranlagung ist erblich. Viel Naharbeit und wenig Aufenthalt im "
                    "Freien begünstigen die Entwicklung im Kindes- und Jugendalter."
                ),
                "diagnostics": (
                    "Die Augenärztin oder der Augenarzt misst die Sehschärfe mit einer "
                    "Sehprobe und bestimmt die nötige Stärke der Brille durch eine "
                    "Refraktionsmessung."
                ),
                "therapy": (
                    "Brille oder Kontaktlinsen gleichen die Fehlsichtigkeit aus. Eine "
                    "Laserbehandlung der Hornhaut ist bei Erwachsenen unter bestimmten "
                    "Voraussetzungen möglich. Bei Kindern kann der Augenarzt das Fortschreiten "
                    "bremsen."
                ),
                "red_flags": (
                    "Plötzlich auftretende Lichtblitze, ein Rußregen vor dem Auge oder ein "
                    "Schatten im Gesichtsfeld können eine Netzhautablösung anzeigen – sofort "
                    "zum Augenarzt oder in die Augenambulanz, bei Unsicherheit Notruf 144."
                ),
            },
            "further_reading": [medlineplus("refractiveerrors", "Refractive errors")],
        },
        {
            "title": "Diabetische Retinopathie",
            "doc_type": "Diagnose",
            "expected_category": "Augenheilkunde",
            "term_en": "Diabetic retinopathy",
            "icd11_code": "9B71.0",
            "medications": [],
            "sections": {
                "definition": (
                    "Die diabetische Retinopathie ist eine Schädigung der Netzhautgefäße am "
                    "Auge als Folge eines langjährig erhöhten Blutzuckers."
                ),
                "symptoms": (
                    "Im Frühstadium bemerken Betroffene meist nichts. Später kommen "
                    "verschwommenes Sehen, dunkle Flecken im Gesichtsfeld oder ein plötzlicher "
                    "Sehverlust hinzu."
                ),
                "causes": (
                    "Ein dauerhaft hoher Blutzucker, zusammen mit Bluthochdruck und erhöhten "
                    "Blutfetten, schädigt die kleinen Gefäße der Netzhaut."
                ),
                "diagnostics": (
                    "Die Augenärztin untersucht bei geweiteter Pupille den Augenhintergrund. "
                    "Ergänzend werden Bilder der Netzhaut angefertigt. Menschen mit Diabetes "
                    "sollten diese Kontrolle regelmäßig wahrnehmen."
                ),
                "therapy": (
                    "Wichtig sind gut eingestellter Blutzucker und Blutdruck. Je nach Stadium "
                    "helfen Laserbehandlung der Netzhaut oder Medikamente, die ins Auge "
                    "gespritzt werden."
                ),
                "red_flags": (
                    "Ein plötzlicher Sehverlust, ein dunkler Vorhang vor dem Auge oder viele "
                    "neue schwarze Punkte erfordern eine sofortige augenärztliche Abklärung, "
                    "außerhalb der Ordinationszeiten in der Augenambulanz."
                ),
            },
            "further_reading": [medlineplus("diabeticeyeproblems", "Diabetic eye problems")],
        },
        {
            "title": "Gerstenkorn (Hordeolum)",
            "doc_type": "Diagnose",
            "expected_category": "Augenheilkunde",
            "term_en": "Hordeolum",
            "icd11_code": "9A01.2",
            "medications": [],
            "sections": {
                "definition": (
                    "Ein Gerstenkorn ist eine schmerzhafte, eitrige Entzündung einer "
                    "Talgdrüse am Rand des Augenlids."
                ),
                "symptoms": (
                    "Am Lidrand entsteht eine gerötete, druckempfindliche Schwellung, oft mit "
                    "einem gelblichen Eiterpunkt. Das Lid ist geschwollen, das Auge tränt und "
                    "fühlt sich fremdkörperartig an."
                ),
                "causes": (
                    "Meist verursachen Bakterien, vor allem Staphylokokken, die Entzündung. "
                    "Begünstigend wirken Lidrandentzündungen und unsaubere Kontaktlinsen."
                ),
                "diagnostics": (
                    "Die Diagnose stellt die Augenärztin oder der Hausarzt durch Ansehen des "
                    "Lids. Ein Hagelkorn ist eine schmerzlose, verhärtete Lidschwellung und "
                    "davon zu unterscheiden."
                ),
                "therapy": (
                    "Warme Umschläge mehrmals täglich fördern die Entleerung. Nicht ausdrücken. "
                    "Bei Bedarf verordnet die Ärztin eine antibiotische Augensalbe, selten ist "
                    "ein kleiner Schnitt nötig."
                ),
                "red_flags": (
                    "Eine rasch zunehmende Rötung und Schwellung des ganzen Lids, Fieber oder "
                    "Sehstörungen sind Warnzeichen für eine Ausbreitung der Entzündung – am "
                    "selben Tag ärztlich vorstellen."
                ),
            },
            "further_reading": [medlineplus("eyeinfections", "Eye infections")],
        },
    ],
    {
        "Kurzsichtigkeit (Myopie)": {
            "title_en": "Short-sightedness (myopia)",
            "sections_en": {
                "definition": (
                    "With short-sightedness, near objects look sharp but distant ones look "
                    "blurred, because the eyeball is too long or the focusing power is too "
                    "strong."
                ),
                "symptoms": (
                    "Distant signs, the board or faces look blurred. People squint, and "
                    "sometimes headaches or tired eyes occur."
                ),
                "causes": (
                    "The tendency is inherited. A lot of close work and little time outdoors "
                    "promote its development in childhood and adolescence."
                ),
                "diagnostics": (
                    "The eye doctor measures visual acuity with an eye chart and determines "
                    "the strength of the glasses needed by measuring the refraction."
                ),
                "therapy": (
                    "Glasses or contact lenses correct the refractive error. Laser treatment "
                    "of the cornea is possible for adults under certain conditions. In "
                    "children, the eye doctor can slow down the progression."
                ),
                "red_flags": (
                    "Sudden flashes of light, a shower of dark spots in front of the eye or "
                    "a shadow in the field of vision can indicate a detached retina – go to "
                    "the eye doctor or an eye emergency clinic at once, and call the "
                    "emergency number 144 (Austria) if unsure."
                ),
            },
            "keywords_en": [
                "Myopia",
                "Short-sightedness",
                "Glasses",
                "Contact lenses",
                "Refraction",
                "Eye doctor",
            ],
        },
        "Diabetische Retinopathie": {
            "title_en": "Diabetic retinopathy",
            "sections_en": {
                "definition": (
                    "Diabetic retinopathy is damage to the blood vessels of the retina at the "
                    "back of the eye, caused by blood sugar that stays high for many years."
                ),
                "symptoms": (
                    "In the early stage people usually notice nothing. Later, blurred "
                    "vision, dark spots in the field of vision or a sudden loss of sight "
                    "are added."
                ),
                "causes": (
                    "Permanently high blood sugar, together with high blood pressure and "
                    "raised blood fats, damages the small vessels of the retina."
                ),
                "diagnostics": (
                    "The eye doctor examines the back of the eye with a dilated pupil. "
                    "Pictures of the retina are taken in addition. People with diabetes "
                    "should keep these check-ups regularly."
                ),
                "therapy": (
                    "Well-controlled blood sugar and blood pressure are important. "
                    "Depending on the stage, laser treatment of the retina or medicines "
                    "injected into the eye help."
                ),
                "red_flags": (
                    "A sudden loss of vision, a dark curtain in front of the eye or many "
                    "new black spots need an immediate examination by an eye doctor, "
                    "outside office hours in an eye emergency clinic."
                ),
            },
            "keywords_en": [
                "Diabetic retinopathy",
                "Retina",
                "Diabetes",
                "Vision loss",
                "Laser treatment",
                "Eye check-up",
            ],
        },
        "Gerstenkorn (Hordeolum)": {
            "title_en": "Stye (hordeolum)",
            "sections_en": {
                "definition": (
                    "A stye is a painful, purulent inflammation of an oil gland at the edge "
                    "of the eyelid."
                ),
                "symptoms": (
                    "A red, tender swelling develops at the edge of the lid, often with a "
                    "yellowish pus point. The lid is swollen, the eye waters and feels as "
                    "if there were a foreign body in it."
                ),
                "causes": (
                    "Bacteria, mostly staphylococci, usually cause the inflammation. "
                    "Inflammation of the lid margin and unclean contact lenses make it more "
                    "likely."
                ),
                "diagnostics": (
                    "The eye doctor or family doctor makes the diagnosis by looking at the "
                    "lid. A chalazion is a painless, hardened swelling of the lid and has "
                    "to be told apart from it."
                ),
                "therapy": (
                    "Warm compresses several times a day help it to drain. Do not squeeze "
                    "it. If needed, the doctor prescribes an antibiotic eye ointment; a "
                    "small cut is rarely necessary."
                ),
                "red_flags": (
                    "Quickly increasing redness and swelling of the whole lid, fever or "
                    "vision problems are warning signs that the infection is spreading – "
                    "see a doctor on the same day."
                ),
            },
            "keywords_en": [
                "Stye",
                "Hordeolum",
                "Eyelid",
                "Warm compress",
                "Staphylococci",
                "Chalazion",
            ],
        },
    },
)
