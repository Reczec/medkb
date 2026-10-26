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


EXTRA = with_english(
    [
        {
            "title": "Heuschnupfen (allergische Rhinitis)",
            "doc_type": "Diagnose",
            "expected_category": "HNO",
            "term_en": "Allergic rhinitis",
            "icd11_code": "CA08.0",
            "medications": ["loratadine", "cetirizine", "fluticasone"],
            "sections": {
                "definition": (
                    "Heuschnupfen ist eine allergische Entzündung der Nasenschleimhaut, die "
                    "durch Pollen oder andere Allergene in der Luft ausgelöst wird."
                ),
                "symptoms": (
                    "Typisch sind Niesattacken, eine laufende oder verstopfte Nase sowie "
                    "juckende, tränende Augen und ein Juckreiz im Gaumen. Die Beschwerden "
                    "treten saisonal bei Pollenflug oder ganzjährig bei Hausstaubmilben- und "
                    "Tierhaarallergie auf."
                ),
                "causes": (
                    "Das Immunsystem reagiert überempfindlich auf eigentlich harmlose Stoffe "
                    "wie Gräser-, Birken- oder Haselpollen. Eine familiäre Neigung zu "
                    "Allergien (Atopie) erhöht das Risiko."
                ),
                "diagnostics": (
                    "Die HNO-Ärztin oder der Allergologe erfragt den Verlauf der Beschwerden "
                    "im Jahr und führt einen Hauttest (Prick-Test) oder eine Blutuntersuchung "
                    "auf spezifische Antikörper durch."
                ),
                "therapy": (
                    "Allergenkontakt möglichst meiden, Antihistaminika und kortisonhaltige "
                    "Nasensprays lindern die Beschwerden. Eine spezifische Immuntherapie "
                    "(Hyposensibilisierung) kann die Allergie langfristig abschwächen."
                ),
                "red_flags": (
                    "Pfeifende Atmung, Atemnot oder Engegefühl in der Brust können auf ein "
                    "Asthma hinweisen und gehören ärztlich abgeklärt. Bei Atemnot oder "
                    "Schwellung von Gesicht und Zunge sofort Notruf 144."
                ),
            },
            "further_reading": [medlineplus("hayfever", "Hay fever")],
        },
        {
            "title": "Akute Mandelentzündung (Tonsillitis)",
            "doc_type": "Diagnose",
            "expected_category": "HNO",
            "term_en": "Tonsillitis",
            "icd11_code": "CA03",
            "medications": ["penicillin V", "ibuprofen", "paracetamol"],
            "sections": {
                "definition": (
                    "Bei der akuten Mandelentzündung sind die Gaumenmandeln im Rachen "
                    "entzündet, meist durch Viren, seltener durch Bakterien."
                ),
                "symptoms": (
                    "Starke Halsschmerzen, Schluckbeschwerden, Fieber, gerötete und "
                    "geschwollene Mandeln, teils mit weißlichen Belägen, sowie geschwollene "
                    "Lymphknoten am Hals."
                ),
                "causes": (
                    "Auslöser sind in den meisten Fällen Erkältungsviren. Bakterielle "
                    "Mandelentzündungen werden vor allem durch Streptokokken verursacht und "
                    "durch Tröpfcheninfektion übertragen."
                ),
                "diagnostics": (
                    "Die Ärztin oder der Arzt untersucht den Rachen und tastet den Hals ab. "
                    "Ein Abstrich mit Schnelltest zeigt, ob Streptokokken beteiligt sind."
                ),
                "therapy": (
                    "Bei Virusinfekten helfen Ruhe, ausreichend Flüssigkeit sowie Schmerz- und "
                    "Fiebermittel. Bakterielle Infektionen mit Streptokokken werden mit einem "
                    "Antibiotikum behandelt. Bei häufigen Rückfällen kann eine Operation der "
                    "Mandeln erwogen werden."
                ),
                "red_flags": (
                    "Sehr starke einseitige Schmerzen, eine Kieferklemme, kaum noch mögliches "
                    "Schlucken, Atemnot oder eine kloßige Sprache können auf einen Abszess "
                    "hinweisen – umgehend ärztlich abklären lassen, bei Atemnot Notruf 144."
                ),
            },
            "further_reading": [medlineplus("tonsillitis", "Tonsillitis")],
        },
        {
            "title": "Hörsturz",
            "doc_type": "Diagnose",
            "expected_category": "HNO",
            "term_en": "Sudden sensorineural hearing loss",
            "icd11_code": "AB55",
            "medications": ["prednisolone"],
            "sections": {
                "definition": (
                    "Ein Hörsturz ist ein plötzlicher, meist einseitiger Hörverlust des "
                    "Innenohrs ohne erkennbare äußere Ursache."
                ),
                "symptoms": (
                    "Das Gehör wird innerhalb von Stunden schlechter, oft begleitet von einem "
                    "Druckgefühl im Ohr, Ohrgeräuschen (Tinnitus) und manchmal Schwindel. "
                    "Schmerzen treten in der Regel nicht auf."
                ),
                "causes": (
                    "Die genaue Ursache ist meist unklar. Diskutiert werden Durchblutungs- "
                    "störungen des Innenohrs, Virusinfekte und Stress."
                ),
                "diagnostics": (
                    "Der Ohrenarzt untersucht das Trommelfell und führt einen Hörtest "
                    "(Audiometrie) durch. Andere Ursachen wie ein Ohrpfropf, eine "
                    "Mittelohrentzündung oder ein Tumor am Hörnerv werden ausgeschlossen."
                ),
                "therapy": (
                    "Die Behandlung sollte rasch beginnen und besteht meist aus hochdosiertem "
                    "Kortison. Ein Teil der Betroffenen erholt sich vollständig, bei anderen "
                    "bleibt ein Resthörverlust."
                ),
                "red_flags": (
                    "Ein plötzlicher Hörverlust ist ein dringender HNO-Befund und sollte noch "
                    "am selben Tag untersucht werden. Zusätzliche Lähmungen, Sprach- oder "
                    "Sehstörungen sprechen für einen Schlaganfall – sofort Notruf 144."
                ),
            },
            "further_reading": [
                medlineplus("hearingdisordersanddeafness", "Hearing disorders and deafness")
            ],
        },
    ],
    {
        "Heuschnupfen (allergische Rhinitis)": {
            "title_en": "Hay fever (allergic rhinitis)",
            "sections_en": {
                "definition": (
                    "Hay fever is an allergic inflammation of the lining of the nose, "
                    "triggered by pollen or other allergens in the air."
                ),
                "symptoms": (
                    "Typical signs are sneezing fits, a runny or blocked nose, itchy, watery "
                    "eyes and an itchy palate. The symptoms occur seasonally during the "
                    "pollen season, or all year round with house dust mite or pet allergy."
                ),
                "causes": (
                    "The immune system reacts too strongly to substances that are actually "
                    "harmless, such as grass, birch or hazel pollen. A family tendency to "
                    "allergies (atopy) raises the risk."
                ),
                "diagnostics": (
                    "The ear, nose and throat doctor or allergist asks about the course of "
                    "the symptoms over the year and performs a skin prick test or a blood "
                    "test for specific antibodies."
                ),
                "therapy": (
                    "Avoid contact with the allergen where possible; antihistamines and "
                    "cortisone nasal sprays relieve the symptoms. Specific immunotherapy "
                    "(desensitisation) can weaken the allergy in the long term."
                ),
                "red_flags": (
                    "Wheezing, shortness of breath or tightness in the chest can point to "
                    "asthma and should be checked by a doctor. For breathlessness or "
                    "swelling of the face or tongue call the emergency number 144 (Austria) "
                    "at once."
                ),
            },
            "keywords_en": [
                "Hay fever",
                "Allergic rhinitis",
                "Pollen",
                "Sneezing",
                "Antihistamines",
                "Immunotherapy",
            ],
        },
        "Akute Mandelentzündung (Tonsillitis)": {
            "title_en": "Acute tonsillitis",
            "sections_en": {
                "definition": (
                    "In acute tonsillitis the palatine tonsils in the throat are inflamed, "
                    "usually because of viruses and less often because of bacteria."
                ),
                "symptoms": (
                    "Severe sore throat, pain when swallowing, fever, red and swollen "
                    "tonsils, sometimes with whitish coating, and swollen lymph nodes in the "
                    "neck."
                ),
                "causes": (
                    "In most cases cold viruses are the trigger. Bacterial tonsillitis is "
                    "mainly caused by streptococci and spreads through droplets."
                ),
                "diagnostics": (
                    "The doctor examines the throat and feels the neck. A swab with a rapid "
                    "test shows whether streptococci are involved."
                ),
                "therapy": (
                    "For viral infections rest, enough fluids and pain and fever relievers "
                    "help. Bacterial infections with streptococci are treated with an "
                    "antibiotic. If the infection keeps coming back, an operation on the "
                    "tonsils can be considered."
                ),
                "red_flags": (
                    "Very severe pain on one side, a stiff jaw, hardly being able to "
                    "swallow, breathlessness or a muffled voice can point to an abscess – "
                    "have it checked at once, and call the emergency number 144 (Austria) "
                    "for breathlessness."
                ),
            },
            "keywords_en": [
                "Tonsillitis",
                "Sore throat",
                "Tonsils",
                "Streptococci",
                "Fever",
                "Antibiotic",
            ],
        },
        "Hörsturz": {
            "title_en": "Sudden hearing loss",
            "sections_en": {
                "definition": (
                    "Sudden hearing loss is a sudden, usually one-sided loss of hearing in "
                    "the inner ear without an obvious external cause."
                ),
                "symptoms": (
                    "Hearing gets worse within hours, often with a feeling of pressure in "
                    "the ear, ringing in the ear (tinnitus) and sometimes dizziness. Pain "
                    "does not usually occur."
                ),
                "causes": (
                    "The exact cause is usually unclear. Circulation problems of the inner "
                    "ear, viral infections and stress are being discussed."
                ),
                "diagnostics": (
                    "The ear doctor examines the eardrum and performs a hearing test "
                    "(audiometry). Other causes such as an earwax plug, a middle ear "
                    "infection or a tumour of the hearing nerve are ruled out."
                ),
                "therapy": (
                    "Treatment should start quickly and usually consists of high-dose "
                    "cortisone. Some people recover completely, in others some hearing loss "
                    "remains."
                ),
                "red_flags": (
                    "Sudden hearing loss is an urgent ear, nose and throat finding and "
                    "should be examined on the same day. Additional paralysis, speech or "
                    "vision problems point to a stroke – call the emergency number 144 "
                    "(Austria) at once."
                ),
            },
            "keywords_en": [
                "Sudden hearing loss",
                "Hearing",
                "Inner ear",
                "Tinnitus",
                "Audiometry",
                "Cortisone",
            ],
        },
    },
)
