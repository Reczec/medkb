import { PhoneCall, Search } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router'
import { ErrorState } from '@/components/feedback/ErrorState'
import { SpecialtyStrip } from '@/components/specialty/SpecialtyStrip'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { RecentList } from '@/features/dashboard/RecentList'
import { useStats } from '@/lib/queries'

const EXAMPLES = ['Kopfschmerzen', 'Husten', 'Rückenschmerzen', 'Bluthochdruck']

/** Start page for patients: search first, topics as filing tabs, no statistics. */
export function PatientHome() {
  const navigate = useNavigate()
  const stats = useStats()
  const [query, setQuery] = useState('')

  const search = (text: string) => {
    const q = text.trim()
    navigate(q ? `/wissen?q=${encodeURIComponent(q)}` : '/wissen')
  }

  return (
    <div className="flex flex-col gap-10">
      <section className="flex flex-col gap-5">
        <h1 className="text-3xl font-semibold tracking-tight">Wonach suchst du?</h1>
        <form
          role="search"
          onSubmit={(event) => {
            event.preventDefault()
            search(query)
          }}
          className="flex max-w-3xl flex-col gap-3 sm:flex-row"
        >
          <label className="relative flex-1">
            <span className="sr-only">Suchbegriffe</span>
            <Search
              className="pointer-events-none absolute top-1/2 left-4 size-5 -translate-y-1/2 text-muted-foreground"
              aria-hidden
            />
            <Input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Beschwerde oder Thema"
              className="h-14 bg-card pl-12 text-lg shadow-sheet"
              maxLength={200}
            />
          </label>
          <Button type="submit" className="h-14 px-6 text-base">
            Suchen
          </Button>
        </form>
        <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
          <span>Häufig gesucht:</span>
          {EXAMPLES.map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => search(example)}
              className="rounded-full border bg-card px-3 py-1 text-foreground/85 transition-colors hover:border-primary/40 hover:text-foreground"
            >
              {example}
            </button>
          ))}
        </div>
      </section>

      <aside
        role="note"
        className="flex max-w-3xl items-start gap-3 rounded-xl border border-red-500/25 bg-red-500/5 p-4"
      >
        <PhoneCall className="mt-0.5 size-5 shrink-0 text-red-600 dark:text-red-400" aria-hidden />
        <p className="text-sm">
          <strong>Notfall?</strong> Bei Brustschmerzen, Atemnot, Lähmungen oder Bewusstlosigkeit
          sofort den Rettungsdienst unter <strong className="tabular">144</strong> anrufen. MedKB
          ersetzt keine ärztliche Beratung.
        </p>
      </aside>

      {stats.error && <ErrorState error={stats.error} onRetry={() => stats.refetch()} />}
      {stats.isPending && <Skeleton className="h-40 rounded-xl" />}
      {stats.data && (
        <>
          <section className="flex flex-col gap-3">
            <h2 className="text-base font-semibold">Themen nach Fachgebiet</h2>
            <SpecialtyStrip items={stats.data.categories} showShare={false} />
          </section>
          <RecentList items={stats.data.recent} title="Themen zum Weiterlesen" showTimes={false} />
        </>
      )}

    </div>
  )
}
