import { fireEvent, screen, waitFor } from '@testing-library/react'
import { HomePage } from '@/features/home/HomePage'
import { TEST_USERS, mockFetch, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const stats = {
  total: 3,
  auto_classified: 3,
  categories: [{ name: 'Neurologie', count: 2 }, { name: 'HNO', count: 1 }],
  doc_types: [{ name: 'Symptom', count: 3 }],
  recent: [{ id: 4, title: 'Migräne', category: 'Neurologie', updated_at: '2026-10-09T10:00:00Z' }],
  activity: Array.from({ length: 30 }, (_, i) => ({ date: `2026-09-${String(i + 1).padStart(2, '0')}`, count: 0 })),
}

it('greets patients with a search instead of statistics', async () => {
  mockFetch({ '/api/stats': stats })
  renderWithProviders(<HomePage />, { user: TEST_USERS.patient })
  expect(await screen.findByRole('heading', { level: 1, name: 'Wonach suchst du?' })).toBeInTheDocument()
  expect(screen.getByText(/144/)).toBeInTheDocument()
  expect(await screen.findByRole('link', { name: /Migräne/ })).toBeInTheDocument()
  expect(screen.queryByText('Änderungen der letzten 30 Tage')).not.toBeInTheDocument()
  expect(screen.queryByTestId('summary')).not.toBeInTheDocument()
  expect(screen.queryByText(/Hallo/)).not.toBeInTheDocument()
  expect(screen.queryByText('Anteil der Einträge')).not.toBeInTheDocument()
  expect(screen.queryByText(/geändert/)).not.toBeInTheDocument()
  expect(screen.queryByText(/in Arbeit/)).not.toBeInTheDocument()
})

it('sends the search to the knowledge base', async () => {
  mockFetch({ '/api/stats': stats })
  const { router } = renderWithProviders(<HomePage />, {
    user: TEST_USERS.patient,
    routes: [{ path: '/wissen', element: <p>Liste</p> }],
  })
  const box = await screen.findByRole('searchbox', { name: 'Suchbegriffe' })
  fireEvent.change(box, { target: { value: 'husten' } })
  fireEvent.submit(box.closest('form')!)
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen'))
  expect(router.state.location.search).toBe('?q=husten')
})

it('shows the dashboard to doctors', async () => {
  mockFetch({ '/api/stats': stats })
  renderWithProviders(<HomePage />, { user: TEST_USERS.doctor })
  expect(await screen.findByTestId('summary')).toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'Wonach suchst du?' })).not.toBeInTheDocument()
})
