import { useQuery } from '@tanstack/react-query'
import { ArrowRight, HeartHandshake, Loader2, ShieldCheck, Stethoscope, type LucideIcon } from 'lucide-react'
import { motion, useReducedMotion } from 'motion/react'
import { useState } from 'react'
import { Navigate, useSearchParams } from 'react-router'
import { BrandMark } from '@/components/layout/BrandMark'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useAuth } from '@/features/auth/context'
import { api } from '@/lib/api'
import type { Role } from '@/lib/auth'
import { cn } from '@/lib/utils'

interface DemoRole {
  role: Role
  label: string
  title: string
  icon: LucideIcon
  color: string
  can: string[]
}

const DEMO_ROLES: DemoRole[] = [
  {
    role: 'doctor',
    label: 'Ärztin / Arzt',
    title: 'Fachansicht',
    icon: Stethoscope,
    color: 'oklch(0.62 0.1 196)',
    can: ['Alle Einträge in Fachsprache', 'Klassifikation mit Begründung'],
  },
  {
    role: 'patient',
    label: 'Patient:in',
    title: 'Einfach informiert',
    icon: HeartHandshake,
    color: 'oklch(0.62 0.14 55)',
    can: ['Themen suchen und lesen', 'Ohne Fachdetails'],
  },
  {
    role: 'admin',
    label: 'Admin',
    title: 'Wissensbasis pflegen',
    icon: ShieldCheck,
    color: 'oklch(0.62 0.12 265)',
    can: ['Einträge anlegen und bearbeiten', 'Archiv, Protokoll, Nutzer'],
  },
]

function safeNext(value: string | null) {
  // Only same-site paths: never redirect to another origin after login.
  return value && value.startsWith('/') && !value.startsWith('//') ? value : '/'
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
        <Input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" className="h-11" />
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

export function LoginPage() {
  const { status, expired, loginDemo } = useAuth()
  const [params] = useSearchParams()
  const reduced = useReducedMotion()
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
    <div className="grid min-h-dvh lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
      <aside className="flex flex-col justify-between gap-10 bg-rail px-6 py-8 text-rail-foreground sm:px-10 lg:py-12">
        <div className="flex items-center gap-3">
          <BrandMark className="size-9 text-rail-foreground" />
          <div className="leading-tight">
            <div className="text-lg font-semibold">MedKB</div>
            <div className="text-sm text-rail-muted">Medizinische Wissensdatenbank</div>
          </div>
        </div>
        <div className="max-w-md">
          <p className="text-2xl leading-snug font-semibold sm:text-3xl">
            Medizinisches Wissen, nachvollziehbar nach Fachgebieten geordnet.
          </p>
          <p className="mt-4 text-rail-muted">
            Suche, erklärbare Klassifikation und Archiv – aus einer Diplomarbeit an der TGM Wien
            entstanden.
          </p>
        </div>
        <p className="text-xs text-rail-muted">Prototyp mit Beispieldaten – keine medizinische Beratung.</p>
      </aside>

      <main className="flex items-center justify-center px-4 py-10 sm:px-8">
        <div className="flex w-full max-w-xl flex-col gap-6">
          <header className="flex flex-col gap-1">
            <h1 className="text-3xl font-semibold tracking-tight">Anmelden</h1>
            <p className="text-muted-foreground">
              {demo ? 'Wähle eine Rolle, um die Demo ohne Passwort zu öffnen.' : 'Melde dich mit deinem Zugang an.'}
            </p>
          </header>

          {expired && (
            <p role="status" className="rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm">
              Sitzung abgelaufen – bitte erneut anmelden.
            </p>
          )}

          {options.isPending && <Loader2 className="size-5 animate-spin text-muted-foreground" aria-label="Lädt" />}

          {demo && (
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
                      onClick={() => enter(item.role)}
                      disabled={pending !== null}
                      className="group flex h-full w-full flex-col text-left focus-visible:outline-none disabled:cursor-wait"
                    >
                      <span
                        className="relative z-10 ml-3 -mb-px inline-flex h-7 items-center gap-1.5 self-start overflow-hidden rounded-t-lg border border-b-0 px-2.5 text-xs font-semibold transition-transform duration-200 group-hover:-translate-y-1"
                        style={{
                          background: `color-mix(in oklch, ${item.color} 16%, var(--card))`,
                          borderColor: `color-mix(in oklch, ${item.color} 35%, var(--border))`,
                        }}
                      >
                        <span className="absolute inset-x-0 top-0 h-[3px]" style={{ background: item.color }} aria-hidden />
                        <Icon className="size-3.5" style={{ color: item.color }} aria-hidden />
                        {item.label}
                      </span>
                      <span
                        className={cn(
                          'flex flex-1 flex-col gap-3 rounded-xl border bg-card p-4 shadow-sheet transition-shadow duration-200',
                          'group-hover:shadow-lift group-focus-visible:ring-2 group-focus-visible:ring-ring',
                        )}
                      >
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
                            <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" aria-hidden />
                          )}
                          Ansehen
                        </span>
                      </span>
                    </button>
                  </motion.li>
                )
              })}
            </ul>
          )}

          {demoError && (
            <p role="alert" className="rounded-lg bg-destructive/10 px-3 py-2 text-sm text-destructive">
              {demoError}
            </p>
          )}

          {options.data &&
            (demo ? (
              <details className="group rounded-xl border bg-card px-4 py-3 shadow-sheet">
                <summary className="cursor-pointer text-sm font-medium text-muted-foreground select-none group-open:mb-3">
                  Mit Benutzername anmelden
                </summary>
                <PasswordForm />
              </details>
            ) : (
              <div className="rounded-xl border bg-card p-5 shadow-sheet">
                <PasswordForm />
              </div>
            ))}
        </div>
      </main>
    </div>
  )
}
