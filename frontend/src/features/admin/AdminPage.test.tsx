import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { AdminPage } from '@/features/admin/AdminPage'
import { mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

const archive = {
  name: 'archive_20261010_120000.json',
  created_at: '2026-10-10T12:00:00Z',
  size_bytes: 20480,
  document_count: 16,
}
const audit = [
  { id: 3, timestamp: '2026-10-10T12:00:00Z', action: 'archive_create', document_id: null, detail: archive.name },
  { id: 2, timestamp: '2026-10-10T11:00:00Z', action: 'update', document_id: 4, detail: 'Migräne (title)' },
]

type Call = [string, RequestInit | undefined]
const calls = (fetchMock: ReturnType<typeof mockFetch>) => fetchMock.mock.calls as unknown as Call[]

it('restores an archive after confirmation', async () => {
  const fetchMock = mockFetch({
    '/api/audit': audit,
    '/api/archives': [archive],
    [`/api/archives/${archive.name}/restore`]: { restored: 16, backup: { ...archive, name: 'archive_20261010_120500.json' } },
  })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  fireEvent.click(await screen.findByRole('button', { name: `${archive.name} wiederherstellen` }))
  const dialog = await screen.findByRole('alertdialog')
  fireEvent.click(within(dialog).getByRole('button', { name: 'Wiederherstellen' }))
  await waitFor(() =>
    expect(
      calls(fetchMock).some(
        ([url, init]) =>
          url === `/api/archives/${archive.name}/restore` && init?.method === 'POST',
      ),
    ).toBe(true),
  )
})

it('shows the change log with readable actions', async () => {
  mockFetch({ '/api/audit': audit, '/api/archives': [archive] })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  const tab = await screen.findByRole('tab', { name: /Änderungsprotokoll/ })
  fireEvent.mouseDown(tab)
  fireEvent.click(tab)
  expect(await screen.findByText('Migräne (title)')).toBeInTheDocument()
  expect(screen.getByText('Bearbeitet')).toBeInTheDocument()
  expect(screen.getByText('Archiviert')).toBeInTheDocument()
})
