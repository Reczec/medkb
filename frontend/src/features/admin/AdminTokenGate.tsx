import { KeyRound, Loader2, ShieldCheck } from 'lucide-react'
import { useEffect, useState, type ReactNode } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ADMIN_TOKEN_KEY, ApiError, api } from '@/lib/api'

type GateState = 'checking' | 'locked' | 'open'

function messageFor(error: unknown) {
  if (error instanceof ApiError && error.status === 401) return 'Admin-Token ungültig'
  if (error instanceof ApiError && error.status === 503)
    return 'Admin-Funktionen sind deaktiviert (ADMIN_TOKEN ist am Server nicht gesetzt).'
  return error instanceof Error ? error.message : 'Anmeldung fehlgeschlagen'
}

/** Asks for the shared admin token and checks it against the server before showing children. */
export function AdminTokenGate({ children }: { children: (logout: () => void) => ReactNode }) {
  const [state, setState] = useState<GateState>(() =>
    sessionStorage.getItem(ADMIN_TOKEN_KEY) ? 'checking' : 'locked',
  )
  const [token, setToken] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const verify = async () => {
    try {
      await api('/api/audit?limit=1', { admin: true })
      setState('open')
      setError(null)
    } catch (err) {
      sessionStorage.removeItem(ADMIN_TOKEN_KEY)
      setState('locked')
      setError(messageFor(err))
    }
  }

  useEffect(() => {
    if (state === 'checking') void verify()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- run once for a stored token
  }, [])

  const submit = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!token.trim()) return
    setBusy(true)
    sessionStorage.setItem(ADMIN_TOKEN_KEY, token.trim())
    await verify()
    setBusy(false)
  }

  const logout = () => {
    sessionStorage.removeItem(ADMIN_TOKEN_KEY)
    setToken('')
    setState('locked')
  }

  if (state === 'open') return <>{children(logout)}</>
  if (state === 'checking') {
    return (
      <p className="flex items-center gap-2 text-muted-foreground">
        <Loader2 className="size-4 animate-spin" aria-hidden /> Zugang wird geprüft…
      </p>
    )
  }

  return (
    <form
      onSubmit={submit}
      className="mx-auto mt-6 flex w-full max-w-md flex-col gap-4 rounded-xl border bg-card p-6 shadow-sheet"
    >
      <div className="flex size-11 items-center justify-center rounded-xl bg-accent text-primary">
        <ShieldCheck className="size-6" aria-hidden />
      </div>
      <div>
        <h2 className="text-lg font-semibold">Admin-Zugang</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Archive und Änderungsprotokoll sind geschützt. Das Token steht in der Server-Konfiguration
          (<code className="text-xs">ADMIN_TOKEN</code>).
        </p>
      </div>
      <label className="flex flex-col gap-1.5 text-sm font-medium">
        Admin-Token
        <div className="relative">
          <KeyRound
            className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground"
            aria-hidden
          />
          <Input
            type="password"
            autoComplete="off"
            value={token}
            onChange={(event) => setToken(event.target.value)}
            className="h-11 pl-9"
          />
        </div>
      </label>
      {error && (
        <p role="alert" className="rounded-lg bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </p>
      )}
      <Button type="submit" disabled={busy || !token.trim()} className="h-10">
        {busy && <Loader2 className="animate-spin" aria-hidden />}
        Anmelden
      </Button>
    </form>
  )
}
