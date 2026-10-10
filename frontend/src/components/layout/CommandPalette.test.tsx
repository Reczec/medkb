import { fireEvent, screen, waitFor } from '@testing-library/react'
import { CommandPalette } from '@/components/layout/CommandPalette'
import { mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

it('opens with Ctrl+K', async () => {
  mockFetch({ '/api/documents': { items: [], total: 0, limit: 8, offset: 0 } })
  renderWithProviders(<CommandPalette />)
  fireEvent.keyDown(window, { key: 'k', ctrlKey: true })
  expect(await screen.findByPlaceholderText('Einträge durchsuchen…')).toBeInTheDocument()
})

it('lists matching entries and navigates to them', async () => {
  const fetchMock = mockFetch({
    '/api/documents': {
      items: [{ id: 7, title: 'Migräne', category: 'Neurologie', doc_type: 'Symptom', content: '', keywords: [], source: null, auto_classified: true, created_at: '', updated_at: '' }],
      total: 1,
      limit: 8,
      offset: 0,
    },
  })
  const { router } = renderWithProviders(<CommandPalette />, {
    routes: [{ path: '/wissen/:id', element: <p>Detail</p> }],
  })
  fireEvent.keyDown(window, { key: 'k', ctrlKey: true })
  fireEvent.change(await screen.findByPlaceholderText('Einträge durchsuchen…'), { target: { value: 'migr' } })
  await waitFor(() =>
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('q=migr'))).toBe(true),
  )
  fireEvent.click(await screen.findByText('Migräne'))
  expect(router.state.location.pathname).toBe('/wissen/7')
})
