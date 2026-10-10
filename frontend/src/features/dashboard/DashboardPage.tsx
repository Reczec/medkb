import { ErrorState } from '@/components/feedback/ErrorState'
import { CountUp } from '@/components/motion/CountUp'
import { SpecialtyStrip } from '@/components/specialty/SpecialtyStrip'
import { Skeleton } from '@/components/ui/skeleton'
import { useAuth } from '@/features/auth/context'
import { ActivityChart } from '@/features/dashboard/ActivityChart'
import { ActivityFeed } from '@/features/dashboard/ActivityFeed'
import { DocTypeBars } from '@/features/dashboard/DocTypeBars'
import { RecentList } from '@/features/dashboard/RecentList'
import { useStats } from '@/lib/queries'
import type { Stats } from '@/lib/types'

function Summary({ stats }: { stats: Stats }) {
  const specialties = stats.categories.filter((c) => c.count > 0).length
  const changes = stats.activity.reduce((sum, day) => sum + day.count, 0)
  const rate = stats.total > 0 ? Math.round((stats.auto_classified / stats.total) * 100) : null
  const strong = 'font-semibold text-foreground'

  return (
    <p data-testid="summary" className="max-w-3xl text-lg leading-relaxed text-muted-foreground">
      <strong className={strong}>
        <CountUp value={stats.total} />
      </strong>{' '}
      Einträge in{' '}
      <strong className={strong}>
        <CountUp value={specialties} />
      </strong>{' '}
      Fachgebieten,{' '}
      <strong className={strong}>
        {rate === null ? '–' : <CountUp value={rate} suffix=" %" />}
      </strong>{' '}
      davon automatisch klassifiziert und{' '}
      <strong className={strong}>
        <CountUp value={changes} />
      </strong>{' '}
      {changes === 1 ? 'Änderung' : 'Änderungen'} in den letzten 30 Tagen.
    </p>
  )
}

function DashboardSkeleton() {
  return (
    <div aria-busy="true" aria-label="Dashboard wird geladen" className="flex flex-col gap-6">
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

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold tracking-tight">Überblick</h1>
        {data && <Summary stats={data} />}
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
          <RecentList items={data.recent} />
          {user?.role === 'admin' && <ActivityFeed />}
        </>
      )}
    </div>
  )
}
