import { createContext, useContext } from 'react'
import type { AuthUser, Role } from '@/lib/auth'

export type AuthStatus = 'loading' | 'anonymous' | 'authenticated'

export interface AuthContextValue {
  user: AuthUser | null
  status: AuthStatus
  /** True after a running session ended with a 401 (token expired or server restarted). */
  expired: boolean
  login: (username: string, password: string) => Promise<void>
  loginDemo: (role: Role) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)

export function useAuth(): AuthContextValue {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used inside <AuthProvider>')
  return value
}
