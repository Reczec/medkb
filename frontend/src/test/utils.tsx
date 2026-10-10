import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'
import type { ReactElement } from 'react'
import { AuthProvider } from '@/features/auth/AuthProvider'
import { AuthContext, type AuthContextValue } from '@/features/auth/context'
import type { AuthUser } from '@/lib/auth'
import { createMemoryRouter, RouterProvider, type RouteObject } from 'react-router'

export function makeQueryClient() {
  return new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0 } } })
}

/** Renders `ui` at `path` inside a router; extra routes let tests assert navigation. */
export function renderWithProviders(
  ui: ReactElement,
  {
    path = '/',
    route = '*',
    routes = [] as RouteObject[],
    client = makeQueryClient(),
    withAuth = false,
    user = TEST_USERS.admin as AuthUser | null,
  } = {},
) {
  const router = createMemoryRouter([{ path: route, element: ui }, ...routes], {
    initialEntries: [path],
  })
  const routed = <RouterProvider router={router} />
  const auth: AuthContextValue = {
    user,
    status: user ? 'authenticated' : 'anonymous',
    expired: false,
    login: vi.fn(),
    loginDemo: vi.fn(),
    logout: vi.fn(),
  }
  const result = render(
    <QueryClientProvider client={client}>
      {withAuth ? (
        <AuthProvider>{routed}</AuthProvider>
      ) : (
        <AuthContext.Provider value={auth}>{routed}</AuthContext.Provider>
      )}
    </QueryClientProvider>,
  )
  return { ...result, router, client, auth }
}

/** fetch mock that answers by URL substring: { '/api/stats': body | Response }. */
export function mockFetch(routes: Record<string, unknown>) {
  const fn = vi.fn(async (input: RequestInfo | URL) => {
    const url = typeof input === 'string' ? input : input.toString()
    const key = Object.keys(routes)
      .sort((a, b) => b.length - a.length)
      .find((k) => url.includes(k))
    if (key === undefined) return new Response(JSON.stringify({ detail: 'Not Found' }), { status: 404 })
    const value = routes[key]
    if (value instanceof Response) return value.clone()
    return new Response(JSON.stringify(value), { status: 200 })
  })
  vi.stubGlobal('fetch', fn)
  return fn
}

export const TEST_USERS: Record<'admin' | 'doctor' | 'patient', AuthUser> = {
  admin: { id: 1, username: 'demo-admin', display_name: 'Admin', role: 'admin' },
  doctor: { id: 2, username: 'demo-doctor', display_name: 'Dr. Demo', role: 'doctor' },
  patient: { id: 3, username: 'demo-patient', display_name: 'Patient Demo', role: 'patient' },
}
