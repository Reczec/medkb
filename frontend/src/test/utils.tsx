import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'
import type { ReactElement } from 'react'
import { AuthProvider } from '@/features/auth/AuthProvider'
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
  } = {},
) {
  const router = createMemoryRouter([{ path: route, element: ui }, ...routes], {
    initialEntries: [path],
  })
  const routed = <RouterProvider router={router} />
  const result = render(
    <QueryClientProvider client={client}>
      {withAuth ? <AuthProvider>{routed}</AuthProvider> : routed}
    </QueryClientProvider>,
  )
  return { ...result, router, client }
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
