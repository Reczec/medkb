import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { PatientHome } from '@/features/home/PatientHome'
import type { Stats } from '@/lib/types'
import { TEST_USERS, mockFetch, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const en = { lang: 'en' as const }

function makeStats(overrides: Partial<Stats> = {}): Stats {
  const activity = Array.from({ length: 30 }, (_, i) => ({
    date: `2026-09-${String(i + 1).padStart(2, '0')}`,
    count: i >= 27 ? [1, 2, 2][i - 27] : 0,
  }))
  return {
    total: 16,
    auto_classified: 12,
    categories: [
      { name: 'HNO', count: 2 },
      { name: 'Neurologie', count: 9 },
      { name: 'Kardiologie', count: 5 },
      { name: 'Dermatologie', count: 0 },
    ],
    doc_types: [
      { name: 'Symptom', count: 6 },
      { name: 'Diagnose', count: 10 },
    ],
    recent: [
      { id: 4, title: 'Migräne', title_en: 'Migraine', category: 'Neurologie', updated_at: new Date(Date.now() - 3 * 3600_000).toISOString() },
      { id: 5, title: 'Nur Deutsch', title_en: null, category: 'HNO', updated_at: new Date(Date.now() - 86_400_000).toISOString() },
    ],
    activity,
    ...overrides,
  }
}

const audit = [
  { id: 2, timestamp: new Date(Date.now() - 5 * 60_000).toISOString(), action: 'update', document_id: 4, actor: 'demo-admin', detail: 'Migräne (title)' },
]

it('summarises the knowledge base in English', async () => {
  mockFetch({ '/api/stats': makeStats(), '/api/audit': audit, '/api/ai/usage': { today: 3, limit: 500 } })
  renderWithProviders(<DashboardPage />, en)
  expect(await screen.findByRole('heading', { level: 1, name: 'Overview' })).toBeInTheDocument()
  expect(await screen.findByTestId('summary')).toHaveTextContent(
    '16 entries in 3 specialties, 75 % of them classified automatically and 5 changes in the last 30 days.',
  )
})

it('uses the English singular for one change', async () => {
  const stats = makeStats()
  stats.activity = stats.activity.map((day, i) => ({ ...day, count: i === 29 ? 1 : 0 }))
  mockFetch({ '/api/stats': stats })
  renderWithProviders(<DashboardPage />, { ...en, user: TEST_USERS.doctor })
  expect(await screen.findByTestId('summary')).toHaveTextContent(/1 change in the last 30 days/)
})

it('shows English headings, English titles and relative times', async () => {
  mockFetch({ '/api/stats': makeStats(), '/api/audit': audit, '/api/ai/usage': { today: 3, limit: 500 } })
  renderWithProviders(<DashboardPage />, en)
  expect(await screen.findByRole('heading', { name: 'Changes in the last 30 days' })).toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'By document type' })).toBeInTheDocument()
  expect(screen.getByText('Diagnosis')).toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'Recently edited' })).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'All entries' })).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /Migraine/ })).toHaveAttribute('href', '/wissen/4')
  expect(screen.getByRole('link', { name: /Nur Deutsch/ })).toBeInTheDocument()
  expect(screen.getByText(/changed 3 hours ago/)).toBeInTheDocument()
  expect(screen.getAllByText('Neurology').length).toBeGreaterThan(0)
  expect(screen.getByText('total', { exact: false })).toBeInTheDocument()
})

it('shows the admin activity feed and AI usage in English', async () => {
  mockFetch({ '/api/stats': makeStats(), '/api/audit': audit, '/api/ai/usage': { today: 3, limit: 500 } })
  renderWithProviders(<DashboardPage />, en)
  const feed = await screen.findByRole('region', { name: 'Activity' })
  expect(within(feed).getByRole('link', { name: /Change log/ })).toHaveAttribute('href', '/admin')
  expect(await within(feed).findByText('Edited')).toBeInTheDocument()
  expect(await screen.findByText(/AI requests today/)).toBeInTheDocument()
  expect(screen.getByText('(UTC, whole demo)')).toBeInTheDocument()
})

it('names the studies tile in English for doctors', async () => {
  mockFetch({
    '/api/stats': makeStats(),
    '/api/sources/latest-studies': { status: 'unavailable', fetched_at: null, data: null },
    '/api/ai/usage': { today: 0, limit: 500 },
  })
  renderWithProviders(<DashboardPage />, { ...en, user: TEST_USERS.doctor })
  expect(await screen.findByRole('region', { name: 'Latest studies' })).toBeInTheDocument()
  expect(await screen.findByText('PubMed is currently unreachable.')).toBeInTheDocument()
})

it('greets patients in English with English quick searches', async () => {
  mockFetch({ '/api/stats': makeStats() })
  const { router } = renderWithProviders(<PatientHome />, {
    ...en,
    user: TEST_USERS.patient,
    routes: [{ path: '/wissen', element: <p>List</p> }],
  })
  expect(await screen.findByRole('heading', { level: 1, name: 'What are you looking for?' })).toBeInTheDocument()
  expect(screen.getByRole('searchbox', { name: 'Search terms' })).toHaveAttribute('placeholder', 'Symptom or topic')
  expect(screen.getByText(/call emergency services immediately on/)).toHaveTextContent(/144/)
  expect(screen.getByRole('link', { name: 'Ask the AI assistant a question' })).toHaveAttribute('href', '/assistent')
  expect(await screen.findByRole('heading', { name: 'Topics by specialty' })).toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'Topics to read next' })).toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: 'Headache' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen'))
  expect(router.state.location.search).toBe('?q=Headache')
})

it('keeps the German quick searches in German', async () => {
  mockFetch({ '/api/stats': makeStats() })
  renderWithProviders(<PatientHome />, { lang: 'de', user: TEST_USERS.patient })
  expect(await screen.findByRole('button', { name: 'Kopfschmerzen' })).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Headache' })).not.toBeInTheDocument()
})
