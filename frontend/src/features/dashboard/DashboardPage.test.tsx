import { fireEvent, screen, within } from '@testing-library/react'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import type { Stats } from '@/lib/types'
import { mockFetch, renderWithProviders } from '@/test/utils'

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
