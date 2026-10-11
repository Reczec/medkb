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
} as const

export type MessageKey = keyof typeof de
