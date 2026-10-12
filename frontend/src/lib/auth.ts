export type Role = 'admin' | 'doctor' | 'patient'

export interface AuthUser {
  id: number
  username: string
  display_name: string
  role: Role
}

export interface TokenResponse {
  access_token: string
  token_type: 'bearer'
  user: AuthUser
}

const KEY = 'token'

/** The login token lives in sessionStorage: it survives reloads, not closing the tab. */
export const tokenStore = {
  get(): string | null {
    try {
      return sessionStorage.getItem(KEY)
    } catch {
      return null
    }
  },
  set(token: string) {
    try {
      sessionStorage.setItem(KEY, token)
    } catch {
      // storage blocked: the login lasts until the next reload
    }
  },
  clear() {
    try {
      sessionStorage.removeItem(KEY)
    } catch {
      // nothing stored
    }
  },
}
