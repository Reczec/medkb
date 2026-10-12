import { ErrorState } from '@/components/feedback/ErrorState'
import { CountUp } from '@/components/motion/CountUp'
import { SpecialtyStrip } from '@/components/specialty/SpecialtyStrip'
import { Skeleton } from '@/components/ui/skeleton'
import { useAuth } from '@/features/auth/context'
import { useI18n } from '@/i18n/context'
import { ActivityChart } from '@/features/dashboard/ActivityChart'
import { ActivityFeed } from '@/features/dashboard/ActivityFeed'
import { DocTypeBars } from '@/features/dashboard/DocTypeBars'
import { RecentList } from '@/features/dashboard/RecentList'
import { LatestStudies } from '@/features/dashboard/LatestStudies'
import { useStats } from '@/lib/queries'
import { AIUsage } from '@/features/ai/AIUsage'
import type { Stats } from '@/lib/types'

function Summary({ stats }: { stats: Stats }) {
  const { t } = useI18n()
  const specialties = stats.categories.filter((c) => c.count > 0).length
  const changes = stats.activity.reduce((sum, day) => sum + day.count, 0)
  const rate = stats.total > 0 ? Math.round((stats.auto_classified / stats.total) * 100) : null
  const strong = 'font-semibold text-foreground'

  return (
    <p data-testid="summary" className="max-w-3xl text-lg leading-relaxed text-muted-foreground">
      <strong className={strong}>
        <CountUp value={stats.total} />
      </strong>{' '}
      {t('dash.summary.entries', { count: stats.total })}{' '}
      <strong className={strong}>
        <CountUp value={specialties} />
      </strong>{' '}
      {t('dash.summary.specialties', { count: specialties })}{' '}
      <strong className={strong}>
        {rate === null ? '–' : <CountUp value={rate} suffix=" %" />}
      </strong>{' '}
      {t('dash.summary.classified')}{' '}
      <strong className={strong}>
        <CountUp value={changes} />
      </strong>{' '}
      {t('dash.summary.changes', { count: changes })}
    </p>
  )
}

function DashboardSkeleton() {
  const { t } = useI18n()
  return (
    <div aria-busy="true" aria-label={t('dash.loading')} className="flex flex-col gap-6">
      <Skeleton className="h-7 w-2/3 max-w-xl" />
      <div className="flex gap-1.5">
        {[5, 3, 2, 2].map((grow, i) => (
          <Skeleton key={i} className="h-12 rounded-t-lg" style={{ flexGrow: grow }} />
        ))}
      </div>
      <div className="grid gap-6 lg:grid-cols-3">
        <Skeleton className="h-72 rounded-xl lg:col-span-2" />
        <Skeleton className="h-72 rounded-xl" />
      </div>
    </div>
  )
}

export function DashboardPage() {
  const { data, error, refetch, isPending } = useStats()
  const { user } = useAuth()
  const { t } = useI18n()

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold tracking-tight">{t('dash.title')}</h1>
        {data && <Summary stats={data} />}
        {(user?.role === 'admin' || user?.role === 'doctor') && <AIUsage />}
      </header>

      {isPending && <DashboardSkeleton />}
      {error && <ErrorState error={error} onRetry={() => refetch()} />}

      {data && (
        <>
          <SpecialtyStrip items={data.categories} />
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <ActivityChart activity={data.activity} />
            </div>
            <DocTypeBars items={data.doc_types} />
          </div>
          <div className="grid min-w-0 items-start gap-6 xl:grid-cols-2">
            <RecentList items={data.recent} />
            {(user?.role === 'doctor' || user?.role === 'admin') && <LatestStudies />}
          </div>
          {user?.role === 'admin' && <ActivityFeed />}
        </>
      )}
    </div>
  )
}
