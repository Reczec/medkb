import { fireEvent, screen } from '@testing-library/react'
import { CommandPalette, openCommandPalette } from '@/components/layout/CommandPalette'
import { Sidebar } from '@/components/layout/Sidebar'
import { Topbar } from '@/components/layout/Topbar'
import { ForbiddenPage } from '@/features/auth/guards'
import { LoginPage } from '@/features/auth/LoginPage'
import { NotFoundPage } from '@/features/NotFoundPage'
import { PLAIN_FIELDS, TEST_USERS, mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

const en = { lang: 'en' as const }

it('shows the navigation in English with a language switch', () => {
  renderWithProviders(<Sidebar />, { ...en, user: TEST_USERS.admin })
  const nav = screen.getByRole('navigation', { name: 'Main navigation' })
  expect(nav).toHaveTextContent('Home')
  expect(nav).toHaveTextContent('Knowledge base')
  expect(nav).toHaveTextContent('AI assistant')
  expect(nav).toHaveTextContent('Admin')
  expect(screen.getByRole('button', { name: 'Sign out' })).toBeInTheDocument()
  expect(screen.getByText('Medical knowledge base')).toBeInTheDocument()
  expect(screen.getByText('Prototype with example data – not medical advice.')).toBeInTheDocument()
  expect(screen.getByRole('group', { name: 'Language' })).toBeInTheDocument()
})

it('shows a doctor’s role label in English', () => {
  renderWithProviders(<Sidebar />, { ...en, user: TEST_USERS.doctor })
  expect(screen.getByText('Doctor')).toBeInTheDocument()
})

it('switches the whole sidebar to German with the language switch', () => {
  renderWithProviders(<Sidebar />, { ...en, user: TEST_USERS.admin })
  fireEvent.click(screen.getByRole('button', { name: 'German' }))
  expect(screen.getByRole('navigation', { name: 'Hauptnavigation' })).toHaveTextContent('Startseite')
  expect(screen.getByRole('button', { name: 'Abmelden' })).toBeInTheDocument()
})

it('names the top bar actions in English', () => {
  renderWithProviders(<Topbar onOpenMenu={() => {}} />, { ...en, user: TEST_USERS.admin })
  expect(screen.getByText('Search entries, symptoms, diagnoses…')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /New entry/ })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Open menu' })).toBeInTheDocument()
})

it('opens the command palette in English', async () => {
  mockFetch({ '/api/documents': { items: [], total: 0, limit: 8, offset: 0 } })
  renderWithProviders(<CommandPalette />, { ...en })
  openCommandPalette()
  expect(await screen.findByPlaceholderText('Search entries…')).toBeInTheDocument()
  expect(screen.getByText('Open knowledge base')).toBeInTheDocument()
  expect(screen.getByText('Go to dashboard')).toBeInTheDocument()
})

it('lists entries in the palette with their English titles', async () => {
  const doc = {
    id: 7,
    title: 'Migräne',
    content: 'Text',
    category: 'Neurologie',
    doc_type: 'Diagnose',
    keywords: [],
    source: null,
    auto_classified: true,
    ...PLAIN_FIELDS,
    title_en: 'Migraine',
    created_at: '2026-10-01T10:00:00Z',
    updated_at: '2026-10-01T10:00:00Z',
  }
  mockFetch({ '/api/documents': { items: [doc], total: 1, limit: 8, offset: 0 } })
  renderWithProviders(<CommandPalette />, { ...en })
  openCommandPalette()
  expect(await screen.findByText('Migraine')).toBeInTheDocument()
  expect(screen.queryByText('Migräne')).not.toBeInTheDocument()
})

it('shows the login page in English by default', async () => {
  mockFetch({ '/api/auth/options': { demo_mode: true } })
  renderWithProviders(<LoginPage />, { ...en, path: '/login', route: '/login', withAuth: true })
  expect(await screen.findByRole('heading', { level: 1, name: 'Sign in' })).toBeInTheDocument()
  expect(await screen.findByRole('button', { name: /Open as doctor/ })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Open as patient/ })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Open as admin/ })).toBeInTheDocument()
  expect(screen.getByText('Sign in with a username')).toBeInTheDocument()
  expect(screen.getAllByRole('group', { name: 'Language' }).length).toBeGreaterThan(0)
})

it('switches the login page to German', async () => {
  mockFetch({ '/api/auth/options': { demo_mode: true } })
  renderWithProviders(<LoginPage />, { ...en, path: '/login', route: '/login', withAuth: true })
  await screen.findByRole('button', { name: /Open as doctor/ })
  fireEvent.click(screen.getAllByRole('button', { name: 'German' })[0])
  expect(await screen.findByRole('heading', { level: 1, name: 'Anmelden' })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Als Ärztin \/ Arzt öffnen/ })).toBeInTheDocument()
})

it('explains missing permission in English', () => {
  renderWithProviders(<ForbiddenPage roles={['admin']} />, { ...en })
  expect(screen.getByRole('heading', { name: 'No permission' })).toBeInTheDocument()
  expect(screen.getByText(/This page is for admins only/)).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Switch role' })).toBeInTheDocument()
})

it('shows the not-found page in English', () => {
  renderWithProviders(<NotFoundPage />, { ...en })
  expect(screen.getByText('Page not found')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Go to dashboard' })).toBeInTheDocument()
})
