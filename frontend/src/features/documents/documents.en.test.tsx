import { fireEvent, screen, within } from '@testing-library/react'
import { DocumentCard } from '@/features/documents/DocumentCard'
import { DocumentPage } from '@/features/documents/DocumentPage'
import { KnowledgeBasePage } from '@/features/documents/KnowledgeBasePage'
import { Icd11Panel } from '@/features/documents/sources/Icd11Panel'
import { MedicationsPanel } from '@/features/documents/sources/MedicationsPanel'
import { StudiesPanel } from '@/features/documents/sources/StudiesPanel'
import type { Document } from '@/lib/types'
import { PLAIN_FIELDS, TEST_USERS, mockFetch, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const en = { lang: 'en' as const }

const translated: Document = {
  id: 7,
  title: 'Migräne',
  content: 'Deutscher Volltext.',
  category: 'Neurologie',
  doc_type: 'Diagnose',
  keywords: ['Kopfschmerz'],
  source: null,
  auto_classified: true,
  ...PLAIN_FIELDS,
  sections: { definition: 'Deutsche Definition.', symptoms: 'Deutsche Symptome.' },
  title_en: 'Migraine',
  content_en: 'English full text.',
  sections_en: { definition: 'A recurrent headache disorder.', red_flags: 'Call 144.' },
  keywords_en: ['Headache', 'Aura'],
  further_reading: [
    { label: 'WHO-Faktenblatt (englisch): Migraine', label_en: 'WHO fact sheet: Migraine', url: 'https://www.who.int/x' },
  ],
  created_at: '2026-10-01T10:00:00Z',
  updated_at: new Date(Date.now() - 5 * 60_000).toISOString(),
}
const germanOnly: Document = {
  ...translated,
  id: 8,
  title: 'Nur Deutsch',
  title_en: null,
  content_en: null,
  sections_en: null,
  keywords_en: [],
  sections: null,
  content: 'Nur ein deutscher Text.',
}

const classification = {
  category: 'Neurologie',
  confidence: 0.9,
  fallback: false,
  scores: { Neurologie: 9 },
  matched_terms: ['migräne'],
  keywords: [],
}

const renderPage = (doc: Document, user = TEST_USERS.doctor, path = `/wissen/${doc.id}`) =>
  renderWithProviders(<DocumentPage />, { ...en, user, path, route: '/wissen/:id' })

it('shows an entry in English with English sections, details and link labels', async () => {
  mockFetch({ '/api/documents/7': translated, '/api/classify': classification })
  renderPage(translated, TEST_USERS.patient)
  expect(await screen.findByRole('heading', { level: 1, name: 'Migraine' })).toBeInTheDocument()
  expect(screen.getByRole('heading', { level: 2, name: 'Definition' })).toBeInTheDocument()
  expect(screen.getByText('A recurrent headache disorder.')).toBeInTheDocument()
  expect(screen.getByRole('heading', { level: 2, name: 'Warning signs' })).toBeInTheDocument()
  expect(screen.queryByText('Deutsche Definition.')).not.toBeInTheDocument()
  expect(screen.getAllByText('Neurology').length).toBeGreaterThan(0)
  expect(screen.getByRole('link', { name: /WHO fact sheet: Migraine/ })).toBeInTheDocument()
  expect(screen.getByRole('region', { name: 'Further reading' })).toBeInTheDocument()
  expect(screen.queryByText('Only available in German')).not.toBeInTheDocument()
})

it('shows English details and English keywords', async () => {
  mockFetch({ '/api/documents/7': translated, '/api/classify': classification })
  renderPage(translated)
  const details = await screen.findByRole('region', { name: 'Details' })
  expect(within(details).getByText('Document type')).toBeInTheDocument()
  expect(within(details).getByText('Diagnosis')).toBeInTheDocument()
  expect(within(details).getByText('Headache')).toBeInTheDocument()
  expect(within(details).queryByText('Kopfschmerz')).not.toBeInTheDocument()
})

it('shows German text with a note when an entry has no English version', async () => {
  mockFetch({ '/api/documents/8': germanOnly, '/api/classify': classification })
  renderPage(germanOnly)
  expect(await screen.findByRole('heading', { level: 1, name: 'Nur Deutsch' })).toBeInTheDocument()
  expect(screen.getByText('Nur ein deutscher Text.')).toBeInTheDocument()
  expect(screen.getByRole('status')).toHaveTextContent('Only available in German')
})

it('marks German fallback text as German for screen readers', async () => {
  mockFetch({ '/api/documents/8': germanOnly, '/api/classify': classification })
  renderPage(germanOnly)
  expect(await screen.findByRole('heading', { level: 1, name: 'Nur Deutsch' })).toHaveAttribute('lang', 'de')
  expect(screen.getByText('Nur ein deutscher Text.').closest('[lang]')).toHaveAttribute('lang', 'de')
})

it('does not mark translated text as German', async () => {
  mockFetch({ '/api/documents/7': translated, '/api/classify': classification })
  renderPage(translated)
  expect(await screen.findByRole('heading', { level: 1, name: 'Migraine' })).not.toHaveAttribute('lang')
})

it('marks the German title of a card without English version', () => {
  renderWithProviders(<DocumentCard document={germanOnly} />, { ...en, user: TEST_USERS.patient })
  expect(screen.getByRole('heading', { name: 'Nur Deutsch' })).toHaveAttribute('lang', 'de')
})

it('names the tabs in English and explains the classifier language', async () => {
  mockFetch({ '/api/documents/7': translated, '/api/classify': classification })
  renderPage(translated)
  const tabs = await screen.findByRole('tablist', { name: 'View' })
  expect(within(tabs).getByRole('tab', { name: /Content/ })).toBeInTheDocument()
  expect(within(tabs).getByRole('tab', { name: /AI summary/ })).toBeInTheDocument()
  expect(within(tabs).getByRole('tab', { name: /Studies/ })).toBeInTheDocument()
  const explainer = await screen.findByRole('region', { name: 'Classification' })
  expect(within(explainer).getByText('Specialty determined by rules')).toBeInTheDocument()
  expect(within(explainer).getByText(/works on German text/)).toBeInTheDocument()
})

it('shows the English title, text and specialty on a card', () => {
  renderWithProviders(<DocumentCard document={translated} />, { ...en, user: TEST_USERS.patient })
  expect(screen.getByRole('link', { name: 'Migraine' })).toBeInTheDocument()
  expect(screen.getByText('English full text.')).toBeInTheDocument()
  expect(screen.getByText('Neurology')).toBeInTheDocument()
  expect(screen.getByText('Headache')).toBeInTheDocument()
  expect(screen.getByText(/changed 5 minutes ago/)).toBeInTheDocument()
})

it('lists the knowledge base in English', async () => {
  mockFetch({
    '/api/documents': { items: [translated], total: 1, limit: 10, offset: 0 },
    '/api/stats': {
      total: 1, auto_classified: 1, recent: [], activity: [], doc_types: [],
      categories: [{ name: 'Neurologie', count: 1 }],
    },
    '/api/meta': { categories: ['Neurologie'], doc_types: ['Diagnose'], default_category: 'Allgemeinmedizin' },
  })
  renderWithProviders(<KnowledgeBasePage />, { ...en, path: '/wissen', route: '/wissen' })
  expect(await screen.findByRole('heading', { level: 1, name: 'Knowledge base' })).toBeInTheDocument()
  expect(await screen.findByText('1–1 of 1 entry')).toBeInTheDocument()
  expect(screen.getByRole('navigation', { name: 'Specialties' })).toBeInTheDocument()
  expect(screen.getByText('Migraine')).toBeInTheDocument()
})

it('says nothing found in English with a reset action', async () => {
  mockFetch({
    '/api/documents': { items: [], total: 0, limit: 10, offset: 0 },
    '/api/stats': { total: 0, auto_classified: 0, recent: [], activity: [], doc_types: [], categories: [] },
    '/api/meta': { categories: [], doc_types: [], default_category: 'Allgemeinmedizin' },
  })
  renderWithProviders(<KnowledgeBasePage />, { ...en, path: '/wissen?q=zzz', route: '/wissen' })
  expect(await screen.findByText('No entries found')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Reset filters' })).toBeInTheDocument()
})

it('shows the ICD-11 panel in English', async () => {
  mockFetch({
    '/api/sources/documents/7/icd11': {
      status: 'ok',
      fetched_at: new Date(Date.now() - 5 * 60_000).toISOString(),
      data: { code: '8A80', title: 'Migraine', definition: 'Recurrent headaches.', url: 'https://icd.who.int/x', release: '2026-01', language: 'en' },
    },
  })
  renderWithProviders(<Icd11Panel documentId={7} enabled />, en)
  expect(await screen.findByText('Migraine')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /Open in the ICD-11 browser/ })).toBeInTheDocument()
  expect(screen.getByText(/retrieved 5 minutes ago/)).toBeInTheDocument()
  expect(screen.queryByText(/WHO prerelease/)).not.toBeInTheDocument()
})

it('shows English wording for studies, unavailable sources and medications', async () => {
  mockFetch({
    '/api/sources/documents/7/studies': { status: 'unavailable', fetched_at: null, data: null },
    '/api/sources/documents/7/medications': {
      status: 'ok',
      fetched_at: null,
      data: { found: [], missing: ['sumatriptan'] },
    },
  })
  renderWithProviders(
    <>
      <StudiesPanel documentId={7} termEn="Migraine" enabled />
      <MedicationsPanel documentId={7} enabled />
    </>,
    en,
  )
  expect(await screen.findByText('PubMed is currently unreachable.')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Try again/ })).toBeInTheDocument()
  expect(await screen.findByText(/US FDA product information/)).toBeInTheDocument()
  expect(screen.getByText('No FDA label found for: sumatriptan')).toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: /Try again/ }))
})
