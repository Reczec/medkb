import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { Toaster } from 'sonner'
import { Sidebar } from '@/components/layout/Sidebar'
import { AdminPage } from '@/features/admin/AdminPage'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { DocumentCard } from '@/features/documents/DocumentCard'
import { DocumentPage } from '@/features/documents/DocumentPage'
import { EditorPage } from '@/features/editor/EditorPage'
import { TEST_USERS, mockFetch, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const doc = {
  id: 5,
  title: 'Migräne',
  content: 'Anfallsartige Kopfschmerzen.',
  category: 'Neurologie',
  doc_type: 'Symptom',
  keywords: [],
  source: null,
  auto_classified: true,
  created_at: '2026-10-01T10:00:00Z',
  updated_at: '2026-10-01T10:00:00Z',
}
const classification = {
  category: 'Neurologie',
  confidence: 1,
  fallback: false,
  scores: { Neurologie: 9 },
  matched_terms: ['kopfschmerz'],
  keywords: [],
}
const audit = [
  { id: 9, timestamp: '2026-10-10T12:00:00Z', action: 'update', actor: 'demo-admin', document_id: 5, detail: 'Migräne (title)' },
]
const stats = {
  total: 1, auto_classified: 1, categories: [{ name: 'Neurologie', count: 1 }], doc_types: [],
  recent: [], activity: [],
}

const detail = (role: keyof typeof TEST_USERS) => {
  mockFetch({ '/api/documents/5': doc, '/api/classify': classification })
  return renderWithProviders(<DocumentPage />, { path: '/wissen/5', route: '/wissen/:id', user: TEST_USERS[role] })
}

describe('detail page by role', () => {
  it('patients read without classification or edit actions', async () => {
    detail('patient')
    expect(await screen.findByRole('heading', { level: 1, name: 'Migräne' })).toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'Klassifikation' })).not.toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Bearbeiten/ })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Löschen/ })).not.toBeInTheDocument()
  })

  it('doctors see the classification but cannot edit', async () => {
    detail('doctor')
    expect(await screen.findByRole('region', { name: 'Klassifikation' })).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Bearbeiten/ })).not.toBeInTheDocument()
  })

  it('admins can edit and delete', async () => {
    detail('admin')
    expect(await screen.findByRole('link', { name: /Bearbeiten/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Löschen/ })).toBeInTheDocument()
  })
})

it('hides the rule-based marker on cards for patients', () => {
  renderWithProviders(<DocumentCard document={doc} />, { user: TEST_USERS.patient })
  expect(screen.queryByText(/regelbasiert/)).not.toBeInTheDocument()
})

describe('sidebar', () => {
  it('shows the admin area only to admins and offers logout', () => {
    const { auth } = renderWithProviders(<Sidebar />, { user: TEST_USERS.admin })
    expect(screen.getByRole('link', { name: /Admin/ })).toBeInTheDocument()
    expect(screen.getByText('Admin', { selector: '[data-user-name]' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Abmelden/ }))
    expect(auth.logout).toHaveBeenCalled()
  })

  it('patients get no admin link', () => {
    renderWithProviders(<Sidebar />, { user: TEST_USERS.patient })
    expect(screen.queryByRole('link', { name: /^Admin$/ })).not.toBeInTheDocument()
    expect(screen.getByText('Patient Demo')).toBeInTheDocument()
  })
})

it('admin page lists the users', async () => {
  mockFetch({
    '/api/archives': [],
    '/api/audit': audit,
    '/api/users': [
      { id: 1, username: 'demo-admin', display_name: 'Admin', role: 'admin', created_at: '2026-10-10T10:00:00Z' },
      { id: 3, username: 'demo-patient', display_name: 'Patient Demo', role: 'patient', created_at: '2026-10-10T10:00:00Z' },
    ],
  })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  const tab = await screen.findByRole('tab', { name: /Nutzer/ })
  fireEvent.mouseDown(tab)
  fireEvent.click(tab)
  const table = await screen.findByRole('table', { name: 'Nutzer' })
  expect(within(table).getByText('demo-patient')).toBeInTheDocument()
  expect(within(table).getByText('Patient:in')).toBeInTheDocument()
})

it('the change log shows who made a change', async () => {
  mockFetch({ '/api/archives': [], '/api/audit': audit, '/api/users': [] })
  renderWithProviders(<AdminPage />, { path: '/admin' })
  const tab = await screen.findByRole('tab', { name: /Änderungsprotokoll/ })
  fireEvent.mouseDown(tab)
  fireEvent.click(tab)
  expect(await screen.findByText('demo-admin')).toBeInTheDocument()
})

describe('dashboard activity feed', () => {
  it('admins see recent changes with the actor', async () => {
    mockFetch({ '/api/stats': stats, '/api/audit': audit })
    renderWithProviders(<DashboardPage />, { user: TEST_USERS.admin })
    const feed = await screen.findByRole('region', { name: 'Aktivität' })
    expect(await within(feed).findByText('demo-admin')).toBeInTheDocument()
  })

  it('doctors do not load the change log', async () => {
    const fetchMock = mockFetch({ '/api/stats': stats })
    renderWithProviders(<DashboardPage />, { user: TEST_USERS.doctor })
    await screen.findByTestId('summary')
    expect(screen.queryByRole('region', { name: 'Aktivität' })).not.toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/api/audit'))).toBe(false)
  })
})

it('explains a save that hits an entry removed by the demo reset', async () => {
  mockFetch({
    '/api/meta': { categories: ['Neurologie'], doc_types: ['Symptom'], default_category: 'Allgemeinmedizin' },
    '/api/classify': classification,
    '/api/documents/5': doc,
  })
  renderWithProviders(
    <>
      <EditorPage />
      <Toaster />
    </>,
    { path: '/wissen/5/bearbeiten', route: '/wissen/:id/bearbeiten' },
  )
  fireEvent.change(await screen.findByLabelText('Quelle (optional)'), { target: { value: 'Neu' } })
  mockFetch({ '/api/documents/5': new Response(JSON.stringify({ detail: 'Document not found.' }), { status: 404 }) })
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() =>
    expect(screen.getByText('Eintrag existiert nicht mehr (Demo wurde zurückgesetzt)')).toBeInTheDocument(),
  )
})
