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
