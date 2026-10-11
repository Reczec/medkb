from app.seed_data.english import with_english
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

ENTRIES = with_english(
    ENTRIES,
    {
        "Akute Mittelohrentzündung (Otitis media)": {
            "title_en": "Acute middle ear infection (otitis media)",
            "sections_en": {
                "definition": (
                    "Acute otitis media is a usually bacterial or viral inflammation of the "
                    "lining of the middle ear that often follows an infection of the upper "
                    "airways."
                ),
                "symptoms": (
                    "Typical signs are severe, often throbbing ear pain, fever and reduced "
                    "hearing. Young children often tug at the ear and are restless."
                ),
                "causes": (
                    "Germs travel from the nose and throat through the Eustachian tube into "
                    "the middle ear. Children are affected more often because their "
                    "Eustachian tube is shorter."
                ),
                "diagnostics": (
                    "Looking into the ear shows a reddened, bulging eardrum; sometimes fluid "
                    "runs out of the ear canal."
                ),
                "therapy": (
                    "Pain relievers and decongestant nose drops ease the symptoms. "
                    "Antibiotics are used only for severe or persistent courses."
                ),
                "red_flags": (
                    "Swelling and redness behind the ear, severe headache, stiff neck or "
                    "drowsiness can point to complications and need immediate medical "
                    "assessment."
                ),
            },
            "keywords_en": [
                "Ear infection",
                "Otitis media",
                "Earache",
                "Eardrum",
                "Fever",
                "Hearing loss",
            ],
        },
        "Tinnitus – Ohrgeräusche": {
            "title_en": "Tinnitus – ringing in the ears",
            "sections_en": {
                "definition": (
                    "With tinnitus, affected people perceive sounds such as ringing, buzzing "
                    "or hissing although there is no external sound source."
                ),
                "symptoms": (
                    "The noises can be in one or both ears, constant or intermittent. Many "
                    "people also suffer from sleep problems and difficulty concentrating."
                ),
                "causes": (
                    "Common triggers are noise exposure, sudden hearing loss, age-related "
                    "hearing loss or stress. Often no clear cause can be found."
                ),
                "diagnostics": (
                    "The ENT examination includes looking at the ear canal and eardrum and a "
                    "hearing test to rule out treatable causes."
                ),
                "therapy": (
                    "The cause is treated if it is known. For chronic tinnitus, education, "
                    "hearing aids for hearing loss and behavioural therapy help people cope "
                    "better with the noises."
                ),
                "red_flags": (
                    "Sudden hearing loss, a pulse-synchronous noise or accompanying dizziness "
                    "should be examined by an ENT specialist promptly."
                ),
            },
            "keywords_en": ["Tinnitus", "Ringing", "Hearing loss", "Noise", "Eardrum", "Stress"],
        },
        "Akute Nasennebenhöhlenentzündung (Sinusitis)": {
            "title_en": "Acute sinusitis",
            "sections_en": {
                "definition": (
                    "Acute sinusitis is an inflammation of the lining of the paranasal "
                    "sinuses that usually develops during a cold."
                ),
                "symptoms": (
                    "Typical signs are pressure and pain over the forehead or cheeks that "
                    "worsens when bending forward, a blocked nose, purulent nasal discharge "
                    "and a reduced sense of smell."
                ),
                "causes": (
                    "Viruses are usually the cause, bacteria less often. Narrow passages such "
                    "as a crooked nasal septum or polyps promote the inflammation."
                ),
                "diagnostics": (
                    "The diagnosis is usually made clinically. For complications or recurrent "
                    "sinusitis, nasal endoscopy or imaging follows."
                ),
                "therapy": (
                    "Saline nasal rinses, decongestant nasal sprays for a few days and pain "
                    "relievers ease the symptoms. Most cases clear up within two weeks."
                ),
                "red_flags": (
                    "Swelling around the eye, vision problems, very severe headache or high "
                    "fever require an immediate ENT examination."
                ),
            },
            "keywords_en": [
                "Sinusitis",
                "Sinuses",
                "Blocked nose",
                "Facial pain",
                "Cold",
                "Nasal discharge",
            ],
        },
    },
)
