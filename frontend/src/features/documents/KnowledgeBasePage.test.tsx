import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { KnowledgeBasePage } from '@/features/documents/KnowledgeBasePage'
import type { Document } from '@/lib/types'
import { mockFetch, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const meta = { categories: ['HNO', 'Neurologie'], doc_types: ['Symptom', 'Diagnose'], default_category: 'Allgemeinmedizin' }
const stats = {
  total: 3, auto_classified: 3, recent: [], activity: [], doc_types: [],
  categories: [{ name: 'HNO', count: 1 }, { name: 'Neurologie', count: 2 }],
}

function doc(overrides: Partial<Document> = {}): Document {
  return {
    id: 1, title: 'Migräne', content: 'Anfallsartige Kopfschmerzen.', category: 'Neurologie',
    doc_type: 'Symptom', keywords: ['Kopfschmerz'], source: null, auto_classified: true,
    created_at: '2026-10-01T10:00:00Z', updated_at: '2026-10-01T10:00:00Z', ...overrides,
  }
}

const list = (items: Document[], total = items.length) => ({ items, total, limit: 10, offset: 0 })

function requested(fetchMock: ReturnType<typeof mockFetch>, predicate: (url: URL) => boolean) {
  return fetchMock.mock.calls.some(([input]) => {
    const url = new URL(String(input), 'http://x')
    return url.pathname === '/api/documents' && predicate(url)
  })
}

it('searches after the user stops typing', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([doc()]) })
  renderWithProviders(<KnowledgeBasePage />, { path: '/wissen' })
  fireEvent.change(await screen.findByRole('searchbox'), { target: { value: 'kopf' } })
  await waitFor(() => expect(requested(fetchMock, (u) => u.searchParams.get('q') === 'kopf')).toBe(true))
})

it('encodes special characters and shows an empty state', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([]) })
  renderWithProviders(<KnowledgeBasePage />, { path: '/wissen' })
  fireEvent.change(await screen.findByRole('searchbox'), { target: { value: '100% "Ohr_"' } })
  await waitFor(() =>
    expect(requested(fetchMock, (u) => u.searchParams.get('q') === '100% "Ohr_"')).toBe(true),
  )
  expect(await screen.findByText('Keine Einträge gefunden')).toBeInTheDocument()
})

it('filters by the specialty in the URL and lets the user remove it', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([doc({ category: 'HNO', title: 'Tinnitus' })]) })
  const { router } = renderWithProviders(<KnowledgeBasePage />, { path: '/wissen?category=HNO' })
  await waitFor(() => expect(requested(fetchMock, (u) => u.searchParams.get('category') === 'HNO')).toBe(true))
  const active = await screen.findByRole('list', { name: 'Aktive Filter' })
  fireEvent.click(within(active).getByRole('button', { name: 'Filter HNO entfernen' }))
  await waitFor(() => expect(router.state.location.search).toBe(''))
})

it('selects a specialty from the filing tabs', async () => {
  mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([doc()]) })
  const { router } = renderWithProviders(<KnowledgeBasePage />, { path: '/wissen' })
  const strip = await screen.findByRole('navigation', { name: 'Fachgebiete' })
  fireEvent.click(await within(strip).findByRole('button', { name: /Neurologie/ }))
  await waitFor(() => expect(router.state.location.search).toBe('?category=Neurologie'))
})

it('clamps long titles and summarises extra keywords', async () => {
  const keywords = Array.from({ length: 20 }, (_, i) => `Wort${i}`)
  mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([doc({ title: 'T'.repeat(300), keywords })]) })
  renderWithProviders(<KnowledgeBasePage />, { path: '/wissen' })
  expect(await screen.findByText('+15')).toBeInTheDocument()
})

it('pages through results', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([doc()], 23) })
  renderWithProviders(<KnowledgeBasePage />, { path: '/wissen' })
  expect(await screen.findByText(/1–10 von 23/)).toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: /Weiter/ }))
  await waitFor(() => expect(requested(fetchMock, (u) => u.searchParams.get('offset') === '10')).toBe(true))
})

it('clears the search box when the address loses its query', async () => {
  mockFetch({ '/api/meta': meta, '/api/stats': stats, '/api/documents': list([doc()]) })
  const { router } = renderWithProviders(<KnowledgeBasePage />, { path: '/wissen' })
  const box = await screen.findByRole('searchbox')
  fireEvent.change(box, { target: { value: 'kopf' } })
  await waitFor(() => expect(router.state.location.search).toBe('?q=kopf'))
  await router.navigate('/wissen')
  await waitFor(() => expect(screen.getByRole('searchbox')).toHaveValue(''))
})
