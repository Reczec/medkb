import { fireEvent, screen, within } from '@testing-library/react'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { PatientHome } from '@/features/home/PatientHome'
import type { Stats } from '@/lib/types'
import { mockFetch, renderWithProviders, TEST_USERS } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

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
      ...['Innere Medizin', 'Dermatologie', 'Orthopädie', 'Pädiatrie', 'Psychiatrie', 'Allgemeinmedizin'].map((name) => ({ name, count: 0 })),
    ],
    doc_types: [
      { name: 'Symptom', count: 6 },
      { name: 'Diagnose', count: 10 },
    ],
    recent: [{ id: 4, title: 'Migräne', category: 'Neurologie', updated_at: '2026-09-30T10:00:00Z' }],
    activity,
    ...overrides,
  }
}

it('summarises the knowledge base', async () => {
  mockFetch({ '/api/stats': makeStats() })
  renderWithProviders(<DashboardPage />)
  const summary = await screen.findByTestId('summary')
  expect(within(summary).getByText('16')).toBeInTheDocument()
  expect(within(summary).getByText('3')).toBeInTheDocument()
  expect(within(summary).getByText('75 %')).toBeInTheDocument()
  expect(within(summary).getByText('5')).toBeInTheDocument()
})

it('shows a dash for the auto-classification rate of an empty base', async () => {
  mockFetch({ '/api/stats': makeStats({ total: 0, auto_classified: 0, categories: [], recent: [] }) })
  renderWithProviders(<DashboardPage />)
  expect(within(await screen.findByTestId('summary')).getByText('–')).toBeInTheDocument()
})

it('lists specialties with entries as tabs that open the filtered list', async () => {
  mockFetch({ '/api/stats': makeStats() })
  const { router } = renderWithProviders(<DashboardPage />, {
    routes: [{ path: '/wissen', element: <p>Liste</p> }],
  })
  const strip = await screen.findByRole('navigation', { name: 'Fachgebiete' })
  expect(within(strip).getAllByRole('link')).toHaveLength(3)
  fireEvent.click(within(strip).getByRole('link', { name: /Kardiologie/ }))
  expect(router.state.location.pathname).toBe('/wissen')
  expect(router.state.location.search).toBe('?category=Kardiologie')
})

it('links recent entries to their detail page', async () => {
  mockFetch({ '/api/stats': makeStats() })
  renderWithProviders(<DashboardPage />)
  expect(await screen.findByRole('link', { name: /Migräne/ })).toHaveAttribute('href', '/wissen/4')
})

it('offers a retry when loading fails', async () => {
  mockFetch({ '/api/stats': new Response(JSON.stringify({ detail: 'Boom' }), { status: 500 }) })
  renderWithProviders(<DashboardPage />)
  expect(await screen.findByText('Daten konnten nicht geladen werden')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Erneut versuchen/ })).toBeInTheDocument()
})

it('uses the singular for one change', async () => {
  const stats = makeStats()
  stats.activity = stats.activity.map((day, i) => ({ ...day, count: i === 29 ? 1 : 0 }))
  mockFetch({ '/api/stats': stats })
  renderWithProviders(<DashboardPage />)
  expect(await screen.findByTestId('summary')).toHaveTextContent(/1 Änderung in den letzten 30 Tagen/)
})

it('shows latest studies grouped by specialty for doctors', async () => {
  mockFetch({
    '/api/stats': makeStats(),
    '/api/sources/latest-studies': {
      status: 'ok', fetched_at: '2026-10-11T10:00:00Z', data: [
        { category: 'Neurologie', studies: [{ pmid: '123', title: 'Migraine review', journal: 'Neurology', year: 2026, authors: ['A Smith'], more_authors: false, url: 'https://pubmed.ncbi.nlm.nih.gov/123/' }] },
        { category: 'Kardiologie', studies: [{ pmid: '456', title: 'Heart review', journal: 'Heart', year: 2026, authors: [], more_authors: false, url: 'https://pubmed.ncbi.nlm.nih.gov/456/' }] },
      ],
    },
  })
  renderWithProviders(<DashboardPage />, { user: TEST_USERS.doctor })
  const tile = await screen.findByRole('region', { name: 'Neueste Studien' })
  expect(await within(tile).findByRole('link', { name: /Migraine review/ })).toHaveAttribute('href', 'https://pubmed.ncbi.nlm.nih.gov/123/')
  expect(within(tile).getByRole('link', { name: /Heart review/ })).toHaveAttribute('target', '_blank')
  expect(within(tile).getByText('Neurologie')).toBeInTheDocument()
  expect(within(tile).getByText('Kardiologie')).toBeInTheDocument()
  expect(within(tile).getByText('PubMed · NCBI')).toBeInTheDocument()
})

it('does not request studies on the patient home', async () => {
  const fetchMock = mockFetch({ '/api/stats': makeStats() })
  renderWithProviders(<PatientHome />, { user: TEST_USERS.patient })
  await screen.findByRole('heading', { name: 'Themen nach Fachgebiet' })
  expect(fetchMock.mock.calls.some(([url]) => String(url).includes('latest-studies'))).toBe(false)
  expect(screen.queryByRole('region', { name: 'Neueste Studien' })).not.toBeInTheDocument()
})

it('keeps the dashboard usable when PubMed is unavailable', async () => {
  mockFetch({ '/api/stats': makeStats(), '/api/sources/latest-studies': { status: 'unavailable', fetched_at: null, data: null } })
  renderWithProviders(<DashboardPage />, { user: TEST_USERS.doctor })
  expect(await screen.findByText('PubMed ist gerade nicht erreichbar.')).toBeInTheDocument()
  expect(screen.getByTestId('summary')).toBeInTheDocument()
})
