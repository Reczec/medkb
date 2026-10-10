import { useQuery } from '@tanstack/react-query'
import {
  ArrowRight,
  ChevronRight,
  HeartHandshake,
  Loader2,
  RotateCw,
  ShieldCheck,
  Stethoscope,
  type LucideIcon,
} from 'lucide-react'
import { motion, useReducedMotion } from 'motion/react'
import { useState } from 'react'
import { Navigate, useSearchParams } from 'react-router'
import { BrandMark } from '@/components/layout/BrandMark'
import { ThemeToggle } from '@/components/layout/ThemeToggle'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useAuth } from '@/features/auth/context'
import { api } from '@/lib/api'
import type { Role } from '@/lib/auth'
import { safeNext } from '@/lib/redirect'

interface DemoRole {
  role: Role
  label: string
  title: string
  icon: LucideIcon
  can: string[]
}

const DEMO_ROLES: DemoRole[] = [
  {
    role: 'doctor',
    label: 'Ärztin / Arzt',
    title: 'Fachansicht',
    icon: Stethoscope,
    can: ['Alle Einträge lesen', 'Klassifikation mit Begründung'],
  },
  {
    role: 'patient',
    label: 'Patient:in',
    title: 'Einfach nachschlagen',
    icon: HeartHandshake,
    can: ['Themen suchen und lesen', 'Ohne Klassifikationsdetails'],
  },
  {
    role: 'admin',
    label: 'Admin',
    title: 'Wissensbasis pflegen',
    icon: ShieldCheck,
    can: ['Einträge anlegen und bearbeiten', 'Archiv, Protokoll, Nutzer'],
  },
]

// Roles are not specialties: one shared accent, told apart by icon and label (Filing Colour Rule).
const TAB_STYLE = {
  background: 'color-mix(in oklab, var(--primary) 14%, var(--card))',
  borderColor: 'color-mix(in oklab, var(--primary) 35%, var(--border))',
}

function PasswordForm() {
  const { login } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const submit = async (event: React.FormEvent) => {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await login(username.trim(), password)
    } catch (err) {
      setError((err as Error).message)
      setBusy(false)
    }
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-3">
      <label className="flex flex-col gap-1.5 text-sm font-medium">
        Benutzername
        <Input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
          className="h-11"
        />
      </label>
      <label className="flex flex-col gap-1.5 text-sm font-medium">
        Passwort
        <Input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          className="h-11"
        />
      </label>
      {error && (
        <p role="alert" className="rounded-lg bg-destructive/10 px-3 py-2 text-sm text-destructive">
          {error}
        </p>
      )}
      <Button type="submit" className="h-11" disabled={busy || !username.trim() || !password}>
        {busy && <Loader2 className="animate-spin" aria-hidden />}
        Anmelden
      </Button>
    </form>
  )
}

function RoleCards({ onEnter, pending }: { onEnter: (role: Role) => void; pending: Role | null }) {
  const reduced = useReducedMotion()
  return (
    <ul className="grid grid-cols-1 gap-x-4 gap-y-5 sm:grid-cols-3">
      {DEMO_ROLES.map((item, index) => {
        const Icon = item.icon
        return (
          <motion.li
            key={item.role}
            className="min-w-0"
            initial={reduced ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.06, duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
          >
            <button
              type="button"
              onClick={() => onEnter(item.role)}
              disabled={pending !== null}
              className="group flex h-full w-full flex-col text-left focus-visible:outline-none disabled:cursor-wait"
            >
              <span
                className="relative z-10 ml-3 -mb-px inline-flex h-7 items-center gap-1.5 self-start overflow-hidden rounded-t-lg border border-b-0 px-2.5 text-xs font-semibold transition-transform duration-200 group-hover:-translate-y-1"
                style={TAB_STYLE}
              >
                <span className="absolute inset-x-0 top-0 h-[3px] bg-primary" aria-hidden />
                <Icon className="size-3.5 text-primary" aria-hidden />
                {item.label}
              </span>
              <span className="flex flex-1 flex-col gap-3 rounded-xl border bg-card p-4 shadow-sheet transition-shadow duration-200 group-hover:shadow-lift group-focus-visible:ring-2 group-focus-visible:ring-ring">
                <span className="font-semibold">{item.title}</span>
                <span className="flex flex-col gap-1 text-sm text-muted-foreground">
                  {item.can.map((line) => (
                    <span key={line}>{line}</span>
                  ))}
                </span>
                <span className="mt-auto inline-flex items-center gap-1 text-sm font-medium text-primary">
                  {pending === item.role ? (
                    <Loader2 className="size-4 animate-spin" aria-hidden />
                  ) : (
                    <ArrowRight
                      className="size-4 transition-transform group-hover:translate-x-0.5"
                      aria-hidden
                    />
                  )}
                  Als {item.label} öffnen
                </span>
              </span>
            </button>
          </motion.li>
        )
      })}
    </ul>
  )
}

export function LoginPage() {
  const { status, expired, loginDemo } = useAuth()
  const [params] = useSearchParams()
  const [pending, setPending] = useState<Role | null>(null)
  const [demoError, setDemoError] = useState<string | null>(null)
  const options = useQuery({
    queryKey: ['auth-options'],
    queryFn: () => api<{ demo_mode: boolean }>('/api/auth/options'),
    staleTime: Infinity,
  })

  if (status === 'authenticated') return <Navigate to={safeNext(params.get('next'))} replace />

  const demo = options.data?.demo_mode === true

  const enter = async (role: Role) => {
    setPending(role)
    setDemoError(null)
    try {
      await loginDemo(role)
    } catch (err) {
      setDemoError((err as Error).message)
      setPending(null)
    }
  }

  return (
    <div className="flex min-h-dvh">
      {/* The same petrol rail as inside the app: brand, notice and theme, nothing more. */}
      <aside className="hidden w-[248px] shrink-0 flex-col bg-rail text-rail-foreground md:flex">
        <div className="flex h-16 items-center gap-3 px-4">
          <BrandMark className="size-8 shrink-0 text-rail-foreground" />
          <div className="min-w-0 leading-tight">
            <div className="text-[15px] font-semibold tracking-tight">MedKB</div>
            <div className="truncate text-xs text-rail-muted">Medizinische Wissensdatenbank</div>
          </div>
        </div>
        <div className="mt-auto flex flex-col gap-3 border-t border-rail-border p-3">
          <p className="px-1 text-[11px] leading-snug text-rail-muted">
            Prototyp mit Beispieldaten – keine medizinische Beratung.
          </p>
          <ThemeToggle />
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 items-center gap-3 border-b px-4 md:hidden">
          <BrandMark className="size-8 shrink-0 text-foreground" />
          <span className="font-semibold">MedKB</span>
        </header>

        <main className="flex flex-1 items-center justify-center px-4 py-10 sm:px-8">
          <div className="flex w-full max-w-2xl flex-col gap-6">
            <header className="flex flex-col gap-2">
              <h1 className="text-3xl font-semibold tracking-tight">Anmelden</h1>
              <p className="text-lg text-foreground/85">
                Medizinisches Wissen, nachvollziehbar nach Fachgebieten geordnet.
              </p>
              <p className="text-sm text-muted-foreground">
                {demo
                  ? 'Wähle eine Rolle, um die Demo ohne Passwort zu öffnen.'
                  : 'Melde dich mit deinem Zugang an.'}
              </p>
            </header>

            {expired && (
              <p
                role="alert"
                className="rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm"
              >
                Sitzung abgelaufen – bitte erneut anmelden.
              </p>
            )}

            {options.isPending && (
              <p role="status" className="flex items-center gap-2 text-sm text-muted-foreground">
                <Loader2 className="size-4 animate-spin" aria-hidden /> Anmeldung wird vorbereitet…
              </p>
            )}

            {demo && <RoleCards onEnter={enter} pending={pending} />}

            {demoError && (
              <p role="alert" className="rounded-lg bg-destructive/10 px-3 py-2 text-sm text-destructive">
                {demoError}
              </p>
            )}

            {options.isError && (
              <div
                role="alert"
                className="flex flex-wrap items-center gap-3 rounded-lg border bg-muted/60 px-3 py-2 text-sm"
              >
                <span className="flex-1">
                  Demo-Zugänge konnten nicht geladen werden. Der Server startet eventuell gerade.
                </span>
                <Button variant="outline" size="sm" onClick={() => options.refetch()}>
                  <RotateCw aria-hidden /> Erneut versuchen
                </Button>
              </div>
            )}

            {demo ? (
              <details className="group rounded-xl border bg-card px-4 py-3 shadow-sheet">
                <summary className="flex cursor-pointer list-none items-center gap-2 text-sm font-medium text-muted-foreground select-none group-open:mb-3 [&::-webkit-details-marker]:hidden">
                  <ChevronRight
                    className="size-4 transition-transform duration-200 group-open:rotate-90"
                    aria-hidden
                  />
                  Mit Benutzername anmelden
                </summary>
                <PasswordForm />
              </details>
            ) : (
              (options.data || options.isError) && (
                <div className="rounded-xl border bg-card p-5 shadow-sheet">
                  <PasswordForm />
                </div>
              )
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
