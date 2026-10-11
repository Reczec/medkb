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

  // app shell and navigation
  'app.tagline': 'Medical knowledge base',
  'nav.main': 'Main navigation',
  'nav.home': 'Home',
  'nav.knowledge': 'Knowledge base',
  'nav.assistant': 'AI assistant',
  'nav.admin': 'Admin',
  'nav.logout': 'Sign out',
  'nav.expand': 'Expand sidebar',
  'nav.collapse': 'Collapse sidebar',
  'nav.expandShort': 'Expand',
  'nav.collapseShort': 'Collapse',
  'nav.openMenu': 'Open menu',
  'nav.title': 'Navigation',
  'nav.description': 'MedKB main navigation',
  'search.placeholder': 'Search entries, symptoms, diagnoses…',
  'shortcut.ctrl': 'Ctrl',
  'action.newEntry': 'New entry',
  'action.retry': 'Try again',

  // command palette
  'palette.title': 'Command palette',
  'palette.description': 'Search entries and run actions',
  'palette.placeholder': 'Search entries…',
  'palette.searching': 'Searching…',
  'palette.empty': 'No entries found.',
  'palette.hits': 'Results',
  'palette.recent': 'Recently changed',
  'palette.actions': 'Actions',
  'palette.openKb': 'Open knowledge base',
  'palette.dashboard': 'Go to dashboard',
  'palette.theme': 'Switch light / dark',
  'palette.open': 'open',
  'palette.close': 'Esc to close',

  // theme
  'theme.label': 'Colour scheme',
  'theme.light': 'Light',
  'theme.dark': 'Dark',
  'theme.system': 'System',

  // login
  'login.title': 'Sign in',
  'login.lead': 'Medical knowledge, organised by specialty and easy to trace.',
  'login.about': 'Search, explainable classification and archive – built from a diploma thesis at TGM Vienna.',
  'login.pickRole': 'Pick a role to open the demo without a password.',
  'login.useAccount': 'Sign in with your account.',
  'login.expired': 'Session expired – please sign in again.',
  'login.preparing': 'Preparing sign-in…',
  'login.demoFailed': 'Demo access could not be loaded. The server may be starting up.',
  'login.withUsername': 'Sign in with a username',
  'login.username': 'Username',
  'login.password': 'Password',
  'login.submit': 'Sign in',
  'login.doctor.title': 'Clinical view',
  'login.doctor.can1': 'Read all entries',
  'login.doctor.can2': 'Classification with reasoning',
  'login.patient.title': 'Simple look-up',
  'login.patient.can1': 'Search and read topics',
  'login.patient.can2': 'Without classification details',
  'login.admin.title': 'Maintain the knowledge base',
  'login.admin.can1': 'Create and edit entries',
  'login.admin.can2': 'Archive, change log, users',
  'login.openAs.doctor': 'Open as doctor',
  'login.openAs.patient': 'Open as patient',
  'login.openAs.admin': 'Open as admin',

  // access control
  'auth.checking': 'Checking sign-in',
  'forbidden.title': 'No permission',
  'forbidden.need.admin': 'for admins only',
  'forbidden.need.doctor': 'for doctors only',
  'forbidden.need.patient': 'for patients only',
  'forbidden.or': ' or ',
  'forbidden.noRole': 'not available for your role',
  'forbidden.text': 'This page is {need}. You can open it with another role.',
  'forbidden.switch': 'Switch role',
  'forbidden.home': 'Go to home',

  // errors and empty pages
  'error.unknown': 'Unknown error',
  'error.crashed': 'This view crashed',
  'error.reload': 'Reload',
  'error.loadFailed': 'Data could not be loaded',
  'notFound.title': 'Page not found',
  'notFound.text': 'This address does not exist in MedKB. The search may help.',
  'notFound.action': 'Go to dashboard',
}
