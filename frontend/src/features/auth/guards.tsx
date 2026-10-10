import { Loader2, ShieldX } from 'lucide-react'
import type { ReactNode } from 'react'
import { Link, Navigate, useLocation } from 'react-router'
import { EmptyState } from '@/components/feedback/EmptyState'
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
        <Loader2 className="size-5 animate-spin" aria-label="Anmeldung wird geprüft" />
      </div>
    )
  }
  if (status === 'anonymous') {
    const next = encodeURIComponent(location.pathname + location.search)
    return <Navigate to={`/login?next=${next}`} replace />
  }
  return <>{children}</>
}

export function ForbiddenPage() {
  return (
    <EmptyState
      icon={ShieldX}
      title="Keine Berechtigung"
      text="Diese Seite ist für deine Rolle nicht freigegeben."
      action={
        <Button asChild variant="outline">
          <Link to="/">Zur Startseite</Link>
        </Button>
      }
    />
  )
}

/** Inside RequireAuth: shows ForbiddenPage unless the user has one of the roles. */
export function RequireRole({ roles, children }: { roles: Role[]; children: ReactNode }) {
  const { user } = useAuth()
  if (!user || !roles.includes(user.role)) return <ForbiddenPage />
  return <>{children}</>
}
