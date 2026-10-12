import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { AdminPage } from '@/features/admin/AdminPage'
import { mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

const en = { lang: 'en' as const }

const archive = {
  name: 'archive_20261010_120000.json',
  created_at: '2026-10-10T12:00:00Z',
  size_bytes: 20480,
  document_count: 16,
}
const audit = [
  { id: 3, timestamp: '2026-10-10T12:00:00Z', action: 'archive_create', document_id: null, actor: 'demo-admin', detail: archive.name },
  { id: 2, timestamp: '2026-10-10T11:00:00Z', action: 'update', document_id: 4, actor: 'demo-admin', detail: 'Migräne (title)' },
]
const users = [
  { id: 1, username: 'demo-admin', display_name: 'Admin', role: 'admin', created_at: '2026-10-01T10:00:00Z' },
  { id: 2, username: 'demo-doctor', display_name: 'Dr. Demo', role: 'doctor', created_at: '2026-10-01T10:00:00Z' },
]

type Call = [string, RequestInit | undefined]
const calls = (fetchMock: ReturnType<typeof mockFetch>) => fetchMock.mock.calls as unknown as Call[]

const open = async (name: RegExp) => {
  const tab = await screen.findByRole('tab', { name })
  fireEvent.mouseDown(tab)
  fireEvent.click(tab)
}

it('names the administration and its tabs in English', async () => {
  mockFetch({ '/api/audit': audit, '/api/archives': [archive] })
  renderWithProviders(<AdminPage />, { ...en, path: '/admin' })
  expect(await screen.findByRole('heading', { level: 1, name: 'Administration' })).toBeInTheDocument()
  expect(screen.getByText('Manage archives, follow changes, review accounts.')).toBeInTheDocument()
  expect(screen.getByRole('tab', { name: /Archives/ })).toBeInTheDocument()
  expect(screen.getByRole('tab', { name: /Change log/ })).toBeInTheDocument()
  expect(screen.getByRole('tab', { name: /Users/ })).toBeInTheDocument()
})

it('lists and restores archives with English wording', async () => {
  const fetchMock = mockFetch({
    '/api/audit': audit,
    '/api/archives': [archive],
    [`/api/archives/${archive.name}/restore`]: { restored: 16, backup: { ...archive, name: 'archive_20261010_120500.json' } },
  })
  renderWithProviders(<AdminPage />, { ...en, path: '/admin' })
  expect(await screen.findByText(/16 entries/)).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Create archive' })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: `Download ${archive.name}` })).toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: `Restore ${archive.name}` }))
  const dialog = await screen.findByRole('alertdialog')
  expect(within(dialog).getByText('Restore archive?')).toBeInTheDocument()
  expect(within(dialog).getByRole('button', { name: 'Cancel' })).toBeInTheDocument()
  fireEvent.click(within(dialog).getByRole('button', { name: 'Restore' }))
  await waitFor(() =>
    expect(
      calls(fetchMock).some(
        ([url, init]) => url === `/api/archives/${archive.name}/restore` && init?.method === 'POST',
      ),
    ).toBe(true),
  )
})

it('shows the change log with English headers and actions', async () => {
  mockFetch({ '/api/audit': audit, '/api/archives': [archive] })
  renderWithProviders(<AdminPage />, { ...en, path: '/admin' })
  await open(/Change log/)
  expect(await screen.findByText('Migräne (title)')).toBeInTheDocument()
  expect(screen.getByRole('columnheader', { name: 'Time' })).toBeInTheDocument()
  expect(screen.getByRole('columnheader', { name: 'Who' })).toBeInTheDocument()
  expect(screen.getByText('Edited')).toBeInTheDocument()
  expect(screen.getByText('Archived')).toBeInTheDocument()
})

it('shows users with English roles', async () => {
  mockFetch({ '/api/audit': audit, '/api/archives': [archive], '/api/users': users })
  renderWithProviders(<AdminPage />, { ...en, path: '/admin' })
  await open(/Users/)
  const table = await screen.findByRole('table', { name: 'Users' })
  expect(within(table).getByText('Doctor')).toBeInTheDocument()
  expect(within(table).getByRole('columnheader', { name: 'Role' })).toBeInTheDocument()
  expect(screen.getByText(/random passwords/)).toBeInTheDocument()
})
