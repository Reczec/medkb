import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { AdminPage } from '@/features/admin/AdminPage'
import { mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

const archive = {
  name: 'medkb-archive-20261010-120000.json',
  created_at: '2026-10-10T12:00:00Z',
  size_bytes: 20480,
  document_count: 16,
}
const audit = [
  { id: 3, timestamp: '2026-10-10T12:00:00Z', action: 'archive', document_id: null, detail: archive.name },
  { id: 2, timestamp: '2026-10-10T11:00:00Z', action: 'update', document_id: 4, detail: 'Migräne (title)' },
]

type Call = [string, RequestInit | undefined]
const calls = (fetchMock: ReturnType<typeof mockFetch>) => fetchMock.mock.calls as unknown as Call[]

async function logIn(token: string) {
  fireEvent.change(await screen.findByLabelText('Admin-Token'), { target: { value: token } })
  fireEvent.click(screen.getByRole('button', { name: 'Anmelden' }))
}

it('rejects a wrong token and forgets it', async () => {
  mockFetch({
    '/api/audit': new Response(JSON.stringify({ detail: 'Invalid or missing admin token.' }), {
      status: 401,
    }),
  })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  await logIn('falsch')
  expect(await screen.findByText('Admin-Token ungültig')).toBeInTheDocument()
  expect(sessionStorage.getItem('adminToken')).toBeNull()
})

it('explains when admin functions are disabled on the server', async () => {
  mockFetch({
    '/api/audit': new Response(JSON.stringify({ detail: 'disabled' }), { status: 503 }),
  })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  await logIn('egal')
  expect(await screen.findByText(/Admin-Funktionen sind deaktiviert/)).toBeInTheDocument()
})

it('opens the admin area with a valid token and sends it', async () => {
  const fetchMock = mockFetch({ '/api/audit': audit, '/api/archives': [archive] })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  await logIn('richtig')
  expect(await screen.findByRole('tab', { name: /Archive/ })).toBeInTheDocument()
  expect(await screen.findByText(archive.name)).toBeInTheDocument()
  const first = calls(fetchMock)[0]
  expect(new Headers(first[1]?.headers).get('X-Admin-Token')).toBe('richtig')
  expect(sessionStorage.getItem('adminToken')).toBe('richtig')
})

it('restores an archive after confirmation', async () => {
  sessionStorage.setItem('adminToken', 'richtig')
  const fetchMock = mockFetch({
    '/api/audit': audit,
    '/api/archives': [archive],
    [`/api/archives/${archive.name}/restore`]: { restored: 16, backup: { ...archive, name: 'medkb-archive-pre-restore.json' } },
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
  sessionStorage.setItem('adminToken', 'richtig')
  mockFetch({ '/api/audit': audit, '/api/archives': [archive] })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  const tab = await screen.findByRole('tab', { name: /Änderungsprotokoll/ })
  fireEvent.mouseDown(tab)
  fireEvent.click(tab)
  expect(await screen.findByText('Migräne (title)')).toBeInTheDocument()
  expect(screen.getByText('Bearbeitet')).toBeInTheDocument()
})
