"""Example entries: short, general textbook-style descriptions. No patient data.

``expected_category`` is what the rule-based classifier is expected to choose; the test suite
checks this, which doubles as a small accuracy check of the classifier.
"""

SOURCE = "Beispieldaten (allgemeines Lehrwissen, keine medizinische Beratung)"

SEED_DOCUMENTS: list[dict[str, str]] = [
    {
        "title": "Akute Mittelohrentzündung (Otitis media)",
        "doc_type": "Diagnose",
        "expected_category": "HNO",
        "content": (
            "Die akute Mittelohrentzündung (Otitis media) tritt häufig nach einem Infekt der "
            "oberen Atemwege auf. Typische Beschwerden sind starke Ohrenschmerzen, Fieber und "
            "ein vermindertes Hörvermögen. Bei der Untersuchung zeigt sich das Trommelfell "
            "gerötet und vorgewölbt. Schmerzmittel lindern die Beschwerden, Antibiotika werden "
            "nur bei schweren oder anhaltenden Verläufen eingesetzt."
        ),
    },
    {
        "title": "Tinnitus – Ohrgeräusche",
        "doc_type": "Symptom",
        "expected_category": "HNO",
        "content": (
            "Bei einem Tinnitus nehmen Betroffene Geräusche wie Pfeifen oder Rauschen wahr, "
            "ohne dass eine äußere Schallquelle vorhanden ist. Häufige Auslöser sind "
            "Lärmbelastung, Stress oder ein Hörsturz. Wichtig ist eine Abklärung beim "
            "HNO-Arzt, um behandelbare Ursachen auszuschließen."
        ),
    },
    {
        "title": "Migräne",
        "doc_type": "Symptom",
        "expected_category": "Neurologie",
        "content": (
            "Migräne ist eine anfallsartige Kopfschmerzerkrankung, die meist einseitig und "
            "pulsierend auftritt. Begleitend können Übelkeit, Licht- und Lärmempfindlichkeit "
            "sowie eine Aura mit Sehstörungen auftreten. Ein Anfall dauert unbehandelt oft "
            "mehrere Stunden bis drei Tage. Auslöser sind individuell verschieden, etwa "
            "Stress, Schlafmangel oder bestimmte Lebensmittel."
        ),
    },
    {
        "title": "Schlaganfall – Warnzeichen",
        "doc_type": "Diagnose",
        "expected_category": "Neurologie",
        "content": (
            "Ein Schlaganfall entsteht durch eine Durchblutungsstörung oder Blutung im "
            "Gehirn. Warnzeichen sind plötzliche Lähmungen oder Taubheitsgefühle einer "
            "Körperseite, Sprachstörungen, Sehstörungen und starker Schwindel. Bei diesen "
            "Anzeichen muss sofort der Notruf gewählt werden, da jede Minute zählt."
        ),
    },
    {
        "title": "Anamnese bei Kopfschmerzen",
        "doc_type": "Anamnese",
        "expected_category": "Neurologie",
        "content": (
            "Bei der Anamnese von Kopfschmerzen werden unter anderem Beginn, Dauer, "
            "Lokalisation, Schmerzcharakter, Begleitsymptome wie Übelkeit oder Sehstörungen "
            "sowie auslösende Faktoren erfragt. Zusätzlich sind frühere Erkrankungen, "
            "Medikamenteneinnahme und familiäre Häufung von Bedeutung. Warnzeichen wie ein "
            "plötzlich einsetzender, nie zuvor erlebter Vernichtungskopfschmerz erfordern "
            "eine sofortige Abklärung."
        ),
    },
    {
        "title": "Diabetes mellitus Typ 2",
        "doc_type": "Diagnose",
        "expected_category": "Endokrinologie",
        "content": (
            "Beim Diabetes mellitus Typ 2 spricht der Körper schlechter auf Insulin an, "
            "wodurch der Blutzucker dauerhaft erhöht ist. Typische Anzeichen sind starker "
            "Durst, häufiges Wasserlassen und Müdigkeit. Zu den wichtigsten Maßnahmen zählen "
            "Gewichtsreduktion, Bewegung und eine ausgewogene Ernährung; zusätzlich können "
            "Medikamente nötig sein. Regelmäßige Kontrollen des Langzeitzuckerwerts (HbA1c) "
            "sind empfohlen."
        ),
    },
    {
        "title": "Sodbrennen und Reflux",
        "doc_type": "Symptom",
        "expected_category": "Gastroenterologie",
        "content": (
            "Sodbrennen entsteht, wenn Magensäure in die Speiseröhre zurückfließt. Betroffene "
            "spüren ein Brennen hinter dem Brustbein, oft nach üppigen Mahlzeiten oder im "
            "Liegen. Bei häufigem Auftreten kann eine Refluxkrankheit vorliegen, die ärztlich "
            "abgeklärt werden sollte."
        ),
    },
    {
        "title": "Bluthochdruck (arterielle Hypertonie)",
        "doc_type": "Diagnose",
        "expected_category": "Kardiologie",
        "content": (
            "Bluthochdruck ist ein dauerhaft erhöhter Blutdruck und bleibt oft lange "
            "unbemerkt. Unbehandelt erhöht er das Risiko für Herzinfarkt, Schlaganfall und "
            "Nierenschäden. Die Diagnose erfolgt durch wiederholte Blutdruckmessungen, "
            "ergänzt durch ein EKG und Laboruntersuchungen. Zur Behandlung zählen "
            "Lebensstiländerungen und bei Bedarf Medikamente."
        ),
    },
    {
        "title": "Vorhofflimmern",
        "doc_type": "Symptom",
        "expected_category": "Kardiologie",
        "content": (
            "Vorhofflimmern ist die häufigste anhaltende Herzrhythmusstörung. Betroffene "
            "spüren Herzrasen, einen unregelmäßigen Puls oder Atemnot, manche bemerken keine "
            "Beschwerden. Da sich Blutgerinnsel bilden können, besteht ein erhöhtes "
            "Schlaganfallrisiko. Ein EKG sichert die Diagnose."
        ),
    },
    {
        "title": "Neurodermitis (atopisches Ekzem)",
        "doc_type": "Diagnose",
        "expected_category": "Dermatologie",
        "content": (
            "Die Neurodermitis ist eine chronisch-entzündliche Hauterkrankung mit starkem "
            "Juckreiz und trockener, geröteter Haut. Sie verläuft in Schüben und beginnt "
            "häufig im Kindesalter. Zur Basisbehandlung gehören konsequentes Eincremen mit "
            "rückfettenden Pflegeprodukten und das Meiden individueller Auslöser."
        ),
    },
    {
        "title": "Rückenschmerzen",
        "doc_type": "Symptom",
        "expected_category": "Orthopädie",
        "content": (
            "Rückenschmerzen gehören zu den häufigsten Beschwerden und sind meist "
            "unspezifisch, das heißt ohne klar erkennbare strukturelle Ursache. Bewegung und "
            "das Beibehalten alltäglicher Aktivitäten fördern in der Regel die Heilung. Ein "
            "Arzt sollte aufgesucht werden, wenn Lähmungserscheinungen, Taubheitsgefühle im "
            "Genitalbereich oder Fieber hinzukommen."
        ),
    },
    {
        "title": "Kniearthrose (Gonarthrose)",
        "doc_type": "Diagnose",
        "expected_category": "Orthopädie",
        "content": (
            "Bei der Kniearthrose nutzt sich der Gelenkknorpel im Kniegelenk ab. Typisch sind "
            "Anlaufschmerzen, Steifigkeit am Morgen und Schmerzen bei Belastung. "
            "Gewichtsreduktion, gezielte Bewegungstherapie und Kräftigung der "
            "Oberschenkelmuskulatur können die Beschwerden lindern. Bei fortgeschrittenem "
            "Verlauf kommt ein Gelenkersatz in Betracht."
        ),
    },
    {
        "title": "Windpocken (Varizellen)",
        "doc_type": "Diagnose",
        "expected_category": "Pädiatrie",
        "content": (
            "Windpocken sind eine hochansteckende Viruserkrankung, die vor allem bei Kindern "
            "auftritt. Typisch sind ein juckender Hautausschlag mit Bläschen in verschiedenen "
            "Entwicklungsstadien und leichtes Fieber. Die Krankheit heilt meist "
            "komplikationslos aus; eine Impfung ist möglich und wird für Kinder empfohlen."
        ),
    },
    {
        "title": "Depressive Episode",
        "doc_type": "Diagnose",
        "expected_category": "Psychiatrie",
        "content": (
            "Eine depressive Episode ist gekennzeichnet durch gedrückte Stimmung, "
            "Antriebslosigkeit und den Verlust von Interesse oder Freude über mindestens zwei "
            "Wochen. Häufig kommen Schlafstörungen, Konzentrationsprobleme und "
            "Appetitveränderungen hinzu. Depressionen sind gut behandelbar, etwa durch "
            "Psychotherapie und gegebenenfalls Medikamente. Bei Suizidgedanken ist sofortige "
            "Hilfe wichtig, in Österreich z. B. die Telefonseelsorge unter 142."
        ),
    },
    {
        "title": "Erkältung (grippaler Infekt)",
        "doc_type": "Beschreibung",
        "expected_category": "Allgemeinmedizin",
        "content": (
            "Eine Erkältung wird durch Viren ausgelöst und klingt in der Regel nach sieben "
            "bis zehn Tagen von selbst ab. Typisch sind Schnupfen, Halskratzen, Husten und "
            "leichtes Fieber. Behandelt werden vor allem die Symptome: ausreichend trinken, "
            "sich schonen, bei Bedarf fiebersenkende Mittel. Bei hohem Fieber, Atemnot oder "
            "einer Verschlechterung nach einigen Tagen sollte ärztlicher Rat eingeholt werden."
        ),
    },
    {
        "title": "Impfungen und Vorsorgeuntersuchungen im Erwachsenenalter",
        "doc_type": "Leitlinie",
        "expected_category": "Allgemeinmedizin",
        "content": (
            "Regelmäßige Vorsorgeuntersuchungen helfen, Erkrankungen früh zu erkennen. In "
            "Österreich steht dazu die Vorsorgeuntersuchung zur Verfügung. Zusätzlich "
            "empfiehlt der österreichische Impfplan Auffrischungen, zum Beispiel gegen "
            "Tetanus und Diphtherie, sowie weitere Impfungen je nach Alter und Risikofaktoren."
        ),
    },
]
