/** German texts: the source of the key set. English lives in messages.en.ts. */
export const de = {
  // language switch
  'lang.switch': 'Sprache',
  'lang.en': 'Englisch',
  'lang.de': 'Deutsch',

  // shared
  'error.status': 'Fehler {status}',
  'notice.prototype': 'Prototyp mit Beispieldaten – keine medizinische Beratung.',

  // roles
  'role.admin': 'Admin',
  'role.doctor': 'Ärztin / Arzt',
  'role.patient': 'Patient:in',

  // entry sections (same names as app/content.py)
  'section.definition': 'Definition',
  'section.symptoms': 'Symptome',
  'section.causes': 'Ursachen',
  'section.diagnostics': 'Diagnostik',
  'section.therapy': 'Therapie',
  'section.red_flags': 'Warnzeichen',

  // specialties (the German name is the stored value)
  'category.HNO': 'HNO',
  'category.Augenheilkunde': 'Augenheilkunde',
  'category.Neurologie': 'Neurologie',
  'category.Kardiologie': 'Kardiologie',
  'category.Pneumologie': 'Pneumologie',
  'category.Gastroenterologie': 'Gastroenterologie',
  'category.Endokrinologie': 'Endokrinologie',
  'category.Urologie': 'Urologie',
  'category.Gynäkologie': 'Gynäkologie',
  'category.Dermatologie': 'Dermatologie',
  'category.Orthopädie': 'Orthopädie',
  'category.Pädiatrie': 'Pädiatrie',
  'category.Psychiatrie': 'Psychiatrie',
  'category.Infektiologie': 'Infektiologie',
  'category.Innere Medizin': 'Innere Medizin',
  'category.Allgemeinmedizin': 'Allgemeinmedizin',

  // document types
  'docType.Symptom': 'Symptom',
  'docType.Diagnose': 'Diagnose',
  'docType.Beschreibung': 'Beschreibung',
  'docType.Anamnese': 'Anamnese',
  'docType.Befund': 'Befund',
  'docType.Leitlinie': 'Leitlinie',

  // app shell and navigation
  'app.tagline': 'Medizinische Wissensdatenbank',
  'nav.main': 'Hauptnavigation',
  'nav.home': 'Startseite',
  'nav.knowledge': 'Wissensdatenbank',
  'nav.assistant': 'KI-Assistent',
  'nav.admin': 'Admin',
  'nav.logout': 'Abmelden',
  'nav.expand': 'Seitenleiste ausklappen',
  'nav.collapse': 'Seitenleiste einklappen',
  'nav.expandShort': 'Ausklappen',
  'nav.collapseShort': 'Einklappen',
  'nav.openMenu': 'Menü öffnen',
  'nav.title': 'Navigation',
  'nav.description': 'Hauptnavigation von MedKB',
  'search.placeholder': 'Einträge, Symptome, Diagnosen suchen…',
  'shortcut.ctrl': 'Strg',
  'action.newEntry': 'Neuer Eintrag',
  'action.retry': 'Erneut versuchen',

  // command palette
  'palette.title': 'Befehlspalette',
  'palette.description': 'Einträge suchen und Aktionen ausführen',
  'palette.placeholder': 'Einträge durchsuchen…',
  'palette.searching': 'Suche läuft…',
  'palette.empty': 'Keine Einträge gefunden.',
  'palette.hits': 'Treffer',
  'palette.recent': 'Zuletzt geändert',
  'palette.actions': 'Aktionen',
  'palette.openKb': 'Wissensdatenbank öffnen',
  'palette.dashboard': 'Zum Dashboard',
  'palette.theme': 'Hell / Dunkel wechseln',
  'palette.open': 'öffnen',
  'palette.close': 'Esc schließen',

  // theme
  'theme.label': 'Farbschema',
  'theme.light': 'Hell',
  'theme.dark': 'Dunkel',
  'theme.system': 'System',

  // login
  'login.title': 'Anmelden',
  'login.lead': 'Medizinisches Wissen, nachvollziehbar nach Fachgebieten geordnet.',
  'login.about': 'Suche, erklärbare Klassifikation und Archiv – aus einer Diplomarbeit an der TGM Wien entstanden.',
  'login.pickRole': 'Wähle eine Rolle, um die Demo ohne Passwort zu öffnen.',
  'login.useAccount': 'Melde dich mit deinem Zugang an.',
  'login.expired': 'Sitzung abgelaufen – bitte erneut anmelden.',
  'login.preparing': 'Anmeldung wird vorbereitet…',
  'login.demoFailed': 'Demo-Zugänge konnten nicht geladen werden. Der Server startet eventuell gerade.',
  'login.withUsername': 'Mit Benutzername anmelden',
  'login.username': 'Benutzername',
  'login.password': 'Passwort',
  'login.submit': 'Anmelden',
  'login.doctor.title': 'Fachansicht',
  'login.doctor.can1': 'Alle Einträge lesen',
  'login.doctor.can2': 'Klassifikation mit Begründung',
  'login.patient.title': 'Einfach nachschlagen',
  'login.patient.can1': 'Themen suchen und lesen',
  'login.patient.can2': 'Ohne Klassifikationsdetails',
  'login.admin.title': 'Wissensbasis pflegen',
  'login.admin.can1': 'Einträge anlegen und bearbeiten',
  'login.admin.can2': 'Archiv, Protokoll, Nutzer',
  'login.openAs.doctor': 'Als Ärztin / Arzt öffnen',
  'login.openAs.patient': 'Als Patient:in öffnen',
  'login.openAs.admin': 'Als Admin öffnen',

  // access control
  'auth.checking': 'Anmeldung wird geprüft',
  'forbidden.title': 'Keine Berechtigung',
  'forbidden.need.admin': 'nur für Admins',
  'forbidden.need.doctor': 'nur für Ärztinnen und Ärzte',
  'forbidden.need.patient': 'nur für Patient:innen',
  'forbidden.or': ' oder ',
  'forbidden.noRole': 'für deine Rolle nicht freigegeben',
  'forbidden.text': 'Diese Seite ist {need}. Mit einer anderen Rolle kannst du sie öffnen.',
  'forbidden.switch': 'Rolle wechseln',
  'forbidden.home': 'Zur Startseite',

  // errors and empty pages
  'error.unknown': 'Unbekannter Fehler',
  'error.crashed': 'Diese Ansicht ist abgestürzt',
  'error.reload': 'Neu laden',
  'error.loadFailed': 'Daten konnten nicht geladen werden',
  'notFound.title': 'Seite nicht gefunden',
  'notFound.text': 'Diese Adresse gibt es in MedKB nicht. Vielleicht hilft die Suche weiter.',
  'notFound.action': 'Zum Dashboard',
} as const

export type MessageKey = keyof typeof de
