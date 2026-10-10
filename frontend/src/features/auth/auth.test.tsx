import { act, fireEvent, screen, waitFor } from '@testing-library/react'
import { LoginPage } from '@/features/auth/LoginPage'
import { RequireAuth, RequireRole } from '@/features/auth/guards'
import { UNAUTHORIZED_EVENT } from '@/lib/api'
import { tokenStore } from '@/lib/auth'
import { mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

const doctor = { id: 2, username: 'demo-doctor', display_name: 'Dr. Demo', role: 'doctor' }
const patient = { id: 3, username: 'demo-patient', display_name: 'Patient Demo', role: 'patient' }
const token = (user: object) => ({ access_token: 'tok', token_type: 'bearer', user })

type Call = [string, RequestInit | undefined]

describe('LoginPage', () => {
  it('logs in with a demo role and goes to the requested page', async () => {
    const fetchMock = mockFetch({ '/api/auth/options': { demo_mode: true }, '/api/auth/demo': token(doctor) })
    const { router } = renderWithProviders(<LoginPage />, {
      path: '/login?next=%2Fwissen',
      route: '/login',
      withAuth: true,
      routes: [{ path: '/wissen', element: <p>Liste</p> }],
    })
    fireEvent.click(await screen.findByRole('button', { name: /Ärztin \/ Arzt/ }))
    await waitFor(() => expect(router.state.location.pathname).toBe('/wissen'))
    const demo = (fetchMock.mock.calls as unknown as Call[]).find(([url]) => url === '/api/auth/demo')!
    expect(JSON.parse(String(demo[1]?.body))).toEqual({ role: 'doctor' })
    expect(tokenStore.get()).toBe('tok')
  })

  it('shows only the form when demo mode is off', async () => {
    mockFetch({ '/api/auth/options': { demo_mode: false } })
    renderWithProviders(<LoginPage />, { path: '/login', route: '/login', withAuth: true })
    expect(await screen.findByLabelText('Benutzername')).toBeVisible()
    expect(screen.queryByRole('button', { name: /Ärztin \/ Arzt/ })).not.toBeInTheDocument()
  })

  it('reports wrong credentials', async () => {
    mockFetch({
      '/api/auth/options': { demo_mode: false },
      '/api/auth/login': new Response(JSON.stringify({ detail: 'Benutzername oder Passwort falsch' }), {
        status: 401,
      }),
    })
    renderWithProviders(<LoginPage />, { path: '/login', route: '/login', withAuth: true })
    fireEvent.change(await screen.findByLabelText('Benutzername'), { target: { value: 'admin' } })
    fireEvent.change(screen.getByLabelText('Passwort'), { target: { value: 'falsch' } })
    fireEvent.click(screen.getByRole('button', { name: 'Anmelden' }))
    expect(await screen.findByText('Benutzername oder Passwort falsch')).toBeInTheDocument()
  })
})

describe('guards', () => {
  it('sends visitors without a login to the login page', async () => {
    mockFetch({})
    const { router } = renderWithProviders(
      <RequireAuth>
        <p>Geheim</p>
      </RequireAuth>,
      { path: '/wissen', withAuth: true, routes: [{ path: '/login', element: <p>Login</p> }] },
    )
    await waitFor(() => expect(router.state.location.pathname).toBe('/login'))
    expect(router.state.location.search).toBe('?next=%2Fwissen')
  })

  it('blocks a role that is not allowed', async () => {
    tokenStore.set('tok')
    mockFetch({ '/api/auth/me': patient })
    renderWithProviders(
      <RequireAuth>
        <RequireRole roles={['admin']}>
          <p>Admin-Bereich</p>
        </RequireRole>
      </RequireAuth>,
      { path: '/admin', withAuth: true },
    )
    expect(await screen.findByText('Keine Berechtigung')).toBeInTheDocument()
    expect(screen.queryByText('Admin-Bereich')).not.toBeInTheDocument()
  })

  it('returns to the login page with a hint when the session expires', async () => {
    tokenStore.set('tok')
    mockFetch({ '/api/auth/me': doctor, '/api/auth/options': { demo_mode: true } })
    const { router } = renderWithProviders(
      <RequireAuth>
        <p>Drinnen</p>
      </RequireAuth>,
      { path: '/wissen', withAuth: true, routes: [{ path: '/login', element: <LoginPage /> }] },
    )
    expect(await screen.findByText('Drinnen')).toBeInTheDocument()
    act(() => {
      window.dispatchEvent(new Event(UNAUTHORIZED_EVENT))
    })
    await waitFor(() => expect(router.state.location.pathname).toBe('/login'))
    expect(await screen.findByText(/Sitzung abgelaufen/)).toBeInTheDocument()
  })
})
