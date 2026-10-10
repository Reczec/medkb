import { Loader2, ShieldX } from 'lucide-react'
import type { ReactNode } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/features/auth/context'
import type { Role } from '@/lib/auth'

/** Renders children only for logged-in users; everyone else goes to /login?next=… */
export function RequireAuth({ children }: { children: ReactNode }) {
  const { status } = useAuth()
  const location = useLocation()

  if (status === 'loading') {
    return (
      <div className="flex min-h-dvh items-center justify-center text-muted-foreground" aria-busy="true">
        <Loader2 className="size-5 animate-spin" aria-hidden />
        <span className="sr-only">Anmeldung wird geprüft</span>
      </div>
    )
  }
  if (status === 'anonymous') {
    const next = encodeURIComponent(location.pathname + location.search)
    return <Navigate to={`/login?next=${next}`} replace />
  }
  return <>{children}</>
}

const ROLE_NEEDS: Record<Role, string> = {
  admin: 'nur für Admins',
  doctor: 'nur für Ärztinnen und Ärzte',
  patient: 'nur für Patient:innen',
}

export function ForbiddenPage({ roles = [] }: { roles?: Role[] }) {
  const { logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const need = roles.map((role) => ROLE_NEEDS[role]).join(' oder ')

  const switchRole = () => {
    logout()
    navigate(`/login?next=${encodeURIComponent(location.pathname + location.search)}`)
  }

  return (
    <section className="flex max-w-xl flex-col gap-4">
      <span className="flex size-12 items-center justify-center rounded-xl bg-muted text-muted-foreground">
        <ShieldX className="size-6" aria-hidden />
      </span>
      <h1 className="text-3xl font-semibold tracking-tight">Keine Berechtigung</h1>
      <p className="text-muted-foreground">
        Diese Seite ist {need || 'für deine Rolle nicht freigegeben'}. Mit einer anderen Rolle
        kannst du sie öffnen.
      </p>
      <div className="flex flex-wrap gap-2">
        <Button onClick={switchRole}>Rolle wechseln</Button>
        <Button asChild variant="outline">
          <Link to="/">Zur Startseite</Link>
        </Button>
      </div>
    </section>
  )
}

/** Inside RequireAuth: shows ForbiddenPage unless the user has one of the roles. */
export function RequireRole({ roles, children }: { roles: Role[]; children: ReactNode }) {
  const { user } = useAuth()
  if (!user || !roles.includes(user.role)) return <ForbiddenPage roles={roles} />
  return <>{children}</>
}
