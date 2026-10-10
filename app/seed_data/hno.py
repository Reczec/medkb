from app.seed_data.links import medlineplus, who

ENTRIES = [
    {
        "title": "Akute Mittelohrentzündung (Otitis media)",
        "doc_type": "Diagnose",
        "expected_category": "HNO",
        "term_en": "Otitis media",
        "icd11_code": "AB00",
        "medications": ["ibuprofen", "amoxicillin"],
        "sections": {
            "definition": (
                "Die akute Mittelohrentzündung (Otitis media) ist eine meist bakterielle oder "
                "virale Entzündung der Schleimhaut im Mittelohr, die häufig nach einem Infekt "
                "der oberen Atemwege auftritt."
            ),
            "symptoms": (
                "Typisch sind starke, oft pochende Ohrenschmerzen, Fieber und ein vermindertes "
                "Hörvermögen. Kleinkinder greifen sich häufig ans Ohr und sind unruhig."
            ),
            "causes": (
                "Über die Ohrtrompete gelangen Erreger aus dem Nasen-Rachen-Raum ins Mittelohr. "
                "Kinder sind häufiger betroffen, weil ihre Ohrtrompete kürzer ist."
            ),
            "diagnostics": (
                "Bei der Ohrspiegelung zeigt sich das Trommelfell gerötet und vorgewölbt, "
                "manchmal tritt Sekret aus dem Gehörgang aus."
            ),
            "therapy": (
                "Schmerzmittel und abschwellende Nasentropfen lindern die Beschwerden. "
                "Antibiotika werden nur bei schweren oder anhaltenden Verläufen eingesetzt."
            ),
            "red_flags": (
                "Schwellung und Rötung hinter dem Ohr, starke Kopfschmerzen, Nackensteifigkeit "
                "oder Benommenheit können auf Komplikationen hinweisen und gehören sofort "
                "ärztlich abgeklärt."
            ),
        },
        "further_reading": [medlineplus("earinfections", "Ear Infections")],
    },
    {
        "title": "Tinnitus – Ohrgeräusche",
        "doc_type": "Symptom",
        "expected_category": "HNO",
        "term_en": "Tinnitus",
        "icd11_code": "MC41",
        "sections": {
            "definition": (
                "Bei einem Tinnitus nehmen Betroffene Geräusche wie Pfeifen, Summen oder "
                "Rauschen wahr, ohne dass eine äußere Schallquelle vorhanden ist."
            ),
            "symptoms": (
                "Die Ohrgeräusche können ein- oder beidseitig, dauerhaft oder zeitweise "
                "auftreten. Viele Betroffene leiden zusätzlich unter Schlafproblemen und "
                "Konzentrationsstörungen."
            ),
            "causes": (
                "Häufige Auslöser sind Lärmbelastung, ein Hörsturz, altersbedingter Hörverlust "
                "oder Stress. Oft lässt sich keine eindeutige Ursache finden."
            ),
            "diagnostics": (
                "Die HNO-ärztliche Abklärung umfasst die Untersuchung von Gehörgang und "
                "Trommelfell sowie einen Hörtest, um behandelbare Ursachen auszuschließen."
            ),
            "therapy": (
                "Behandelt wird die Ursache, falls bekannt. Bei chronischem Tinnitus helfen "
                "Aufklärung, Hörgeräte bei Hörverlust und verhaltenstherapeutische Verfahren, "
                "besser mit den Geräuschen umzugehen."
            ),
            "red_flags": (
                "Ein plötzlicher Hörverlust, pulssynchrones Ohrgeräusch oder begleitender "
                "Schwindel sollten rasch HNO-ärztlich untersucht werden."
            ),
        },
        "further_reading": [
            medlineplus("tinnitus", "Tinnitus"),
            who("deafness-and-hearing-loss", "Deafness and hearing loss"),
        ],
    },
    {
        "title": "Akute Nasennebenhöhlenentzündung (Sinusitis)",
        "doc_type": "Diagnose",
        "expected_category": "HNO",
        "term_en": "Sinusitis",
        "icd11_code": "CA01",
        "medications": ["ibuprofen"],
        "sections": {
            "definition": (
                "Die akute Sinusitis ist eine Entzündung der Schleimhaut der "
                "Nasennebenhöhlen, die meist im Rahmen eines Schnupfens entsteht."
            ),
            "symptoms": (
                "Typisch sind Druckgefühl und Schmerzen über Stirn oder Wangen, die sich beim "
                "Vorbeugen verstärken, eine verstopfte Nase, eitriger Schnupfen und ein "
                "eingeschränkter Geruchssinn."
            ),
            "causes": (
                "Meist sind Viren die Ursache, seltener Bakterien. Engstellen wie eine "
                "verkrümmte Nasenscheidewand oder Polypen begünstigen die Entzündung."
            ),
            "diagnostics": (
                "Die Diagnose wird in der Regel klinisch gestellt. Bei Komplikationen oder "
                "wiederkehrender Sinusitis folgen eine Nasenendoskopie oder Bildgebung."
            ),
            "therapy": (
                "Nasenspülungen mit Salzlösung, abschwellende Nasensprays für wenige Tage und "
                "Schmerzmittel lindern die Beschwerden. Die meisten Verläufe heilen innerhalb "
                "von zwei Wochen aus."
            ),
            "red_flags": (
                "Schwellung um das Auge, Sehstörungen, sehr starke Kopfschmerzen oder hohes "
                "Fieber erfordern eine sofortige HNO-ärztliche Untersuchung."
            ),
        },
        "further_reading": [medlineplus("sinusitis", "Sinusitis")],
    },
]
