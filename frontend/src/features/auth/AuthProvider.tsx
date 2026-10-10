import { useQueryClient } from '@tanstack/react-query'
import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'
import { AuthContext, type AuthContextValue, type AuthStatus } from '@/features/auth/context'
import { UNAUTHORIZED_EVENT, api } from '@/lib/api'
import { tokenStore, type AuthUser, type Role, type TokenResponse } from '@/lib/auth'

interface State {
  user: AuthUser | null
  status: AuthStatus
}

/** Holds the logged-in user. Must sit inside QueryClientProvider; works with or without a router. */
export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient()
  const [state, setState] = useState<State>(() =>
    tokenStore.get() ? { user: null, status: 'loading' } : { user: null, status: 'anonymous' },
  )
  const [expired, setExpired] = useState(false)

  // A stored token from an earlier visit: ask the server who it belongs to.
  useEffect(() => {
    if (state.status !== 'loading') return
    let active = true
    api<AuthUser>('/api/auth/me')
      .then((user) => active && setState({ user, status: 'authenticated' }))
      .catch(() => {
        if (!active) return
        tokenStore.clear()
        setState({ user: null, status: 'anonymous' })
      })
    return () => {
      active = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- only for the initial token
  }, [])

  useEffect(() => {
    const onUnauthorized = () => {
      queryClient.clear()
      setExpired(true)
      setState({ user: null, status: 'anonymous' })
    }
    window.addEventListener(UNAUTHORIZED_EVENT, onUnauthorized)
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, onUnauthorized)
  }, [queryClient])

  const accept = useCallback(
    (response: TokenResponse) => {
      tokenStore.set(response.access_token)
      queryClient.clear()
      setExpired(false)
      setState({ user: response.user, status: 'authenticated' })
    },
    [queryClient],
  )

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      expired,
      login: async (username, password) =>
        accept(
          await api<TokenResponse>('/api/auth/login', {
            method: 'POST',
            body: { username, password },
          }),
        ),
      loginDemo: async (role: Role) =>
        accept(await api<TokenResponse>('/api/auth/demo', { method: 'POST', body: { role } })),
      logout: () => {
        tokenStore.clear()
        queryClient.clear()
        setExpired(false)
        setState({ user: null, status: 'anonymous' })
      },
    }),
    [state, expired, accept, queryClient],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
