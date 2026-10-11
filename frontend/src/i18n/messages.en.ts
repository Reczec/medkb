import type { MessageKey } from '@/i18n/messages.de'

/** English texts: sentence case, British spelling (en-GB). Every German key needs an entry. */
export const en: Record<MessageKey, string> = {
  // language switch
  'lang.switch': 'Language',
  'lang.en': 'English',
  'lang.de': 'German',

  // shared
  'error.status': 'Error {status}',
  'notice.prototype': 'Prototype with example data – not medical advice.',

  // roles
  'role.admin': 'Admin',
  'role.doctor': 'Doctor',
  'role.patient': 'Patient',

  // entry sections
  'section.definition': 'Definition',
  'section.symptoms': 'Symptoms',
  'section.causes': 'Causes',
  'section.diagnostics': 'Diagnostics',
  'section.therapy': 'Therapy',
  'section.red_flags': 'Warning signs',

  // specialties
  'category.HNO': 'ENT',
  'category.Augenheilkunde': 'Ophthalmology',
  'category.Neurologie': 'Neurology',
  'category.Kardiologie': 'Cardiology',
  'category.Pneumologie': 'Pulmonology',
  'category.Gastroenterologie': 'Gastroenterology',
  'category.Endokrinologie': 'Endocrinology',
  'category.Urologie': 'Urology',
  'category.Gynäkologie': 'Gynaecology',
  'category.Dermatologie': 'Dermatology',
  'category.Orthopädie': 'Orthopaedics',
  'category.Pädiatrie': 'Paediatrics',
  'category.Psychiatrie': 'Psychiatry',
  'category.Infektiologie': 'Infectious diseases',
  'category.Innere Medizin': 'Internal medicine',
  'category.Allgemeinmedizin': 'General practice',

  // document types
  'docType.Symptom': 'Symptom',
  'docType.Diagnose': 'Diagnosis',
  'docType.Beschreibung': 'Description',
  'docType.Anamnese': 'Medical history',
  'docType.Befund': 'Finding',
  'docType.Leitlinie': 'Guideline',
}
