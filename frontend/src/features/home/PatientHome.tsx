import { PhoneCall, Search } from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router'
import { ErrorState } from '@/components/feedback/ErrorState'
import { SpecialtyStrip } from '@/components/specialty/SpecialtyStrip'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { RecentList } from '@/features/dashboard/RecentList'
import { useI18n } from '@/i18n/context'
import { useStats } from '@/lib/queries'

const EXAMPLES = ['home.example1', 'home.example2', 'home.example3', 'home.example4'] as const

/** Start page for patients: search first, topics as filing tabs, no statistics. */
export function PatientHome() {
  const navigate = useNavigate()
  const stats = useStats()
  const { t } = useI18n()
  const [query, setQuery] = useState('')

  const search = (text: string) => {
    const q = text.trim()
    navigate(q ? `/wissen?q=${encodeURIComponent(q)}` : '/wissen')
  }

  return (
    <div className="flex flex-col gap-10">
      <section className="flex flex-col gap-5">
        <h1 className="text-3xl font-semibold tracking-tight">{t('home.title')}</h1>
        <form
          role="search"
          onSubmit={(event) => {
            event.preventDefault()
            search(query)
          }}
          className="flex max-w-3xl flex-col gap-3 sm:flex-row"
        >
          <label className="relative flex-1">
            <span className="sr-only">{t('filters.terms')}</span>
            <Search
              className="pointer-events-none absolute top-1/2 left-4 size-5 -translate-y-1/2 text-muted-foreground"
              aria-hidden
            />
            <Input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder={t('home.placeholder')}
              className="h-14 bg-card pl-12 text-lg shadow-sheet"
              maxLength={200}
            />
          </label>
          <Button type="submit" className="h-14 px-6 text-base">
            {t('home.search')}
          </Button>
        </form>
        <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
          <span>{t('home.popular')}</span>
          {EXAMPLES.map((key) => (
            <button
              key={key}
              type="button"
              onClick={() => search(t(key))}
              className="rounded-full border bg-card px-3 py-1 text-foreground/85 transition-colors hover:border-primary/40 hover:text-foreground"
            >
              {t(key)}
            </button>
          ))}
        </div>
      </section>

      <p className="max-w-3xl text-sm text-muted-foreground">
        {t('home.aiPrefix')}{' '}
        <Link to="/assistent" className="text-primary underline underline-offset-4">
          {t('home.aiLink')}
        </Link>
      </p>

      <aside
        role="note"
        className="flex max-w-3xl items-start gap-3 rounded-xl border border-red-500/25 bg-red-500/5 p-4"
      >
        <PhoneCall className="mt-0.5 size-5 shrink-0 text-red-600 dark:text-red-400" aria-hidden />
        <p className="text-sm">
          <strong>{t('home.emergencyLead')}</strong> {t('home.emergencyBefore')}{' '}
          <strong className="tabular">144</strong> {t('home.emergencyAfter')}
        </p>
      </aside>

      {stats.error && <ErrorState error={stats.error} onRetry={() => stats.refetch()} />}
      {stats.isPending && <Skeleton className="h-40 rounded-xl" />}
      {stats.data && (
        <>
          <section className="flex flex-col gap-3">
            <h2 className="text-base font-semibold">{t('home.topics')}</h2>
            <SpecialtyStrip items={stats.data.categories} showShare={false} />
          </section>
          <RecentList items={stats.data.recent} title={t('home.more')} showTimes={false} />
        </>
      )}

    </div>
  )
}
