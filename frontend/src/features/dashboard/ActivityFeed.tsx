import { ArrowRight } from 'lucide-react'
import { Link } from 'react-router'
import { Skeleton } from '@/components/ui/skeleton'
import { useI18n } from '@/i18n/context'
import { auditAction } from '@/lib/audit'
import { formatDate, formatRelative } from '@/lib/format'
import { useAudit } from '@/lib/queries'
import { cn } from '@/lib/utils'

/** Admin dashboard: the latest changes and who made them. */
export function ActivityFeed() {
  const audit = useAudit(8)
  const { t, lang } = useI18n()

  return (
    <section aria-label={t('feed.title')} className="rounded-xl border bg-card shadow-sheet">
      <div className="flex items-center justify-between px-5 pt-5 pb-3">
        <h2 className="text-base font-semibold">{t('feed.title')}</h2>
        <Link
          to="/admin"
          className="inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline"
        >
          {t('feed.log')} <ArrowRight className="size-3.5" aria-hidden />
        </Link>
      </div>
      {audit.isPending && <Skeleton className="mx-5 mb-5 h-24" />}
      {audit.error && (
        <p className="px-5 pb-5 text-sm text-muted-foreground">{t('feed.unavailable')}</p>
      )}
      {audit.data && (
        <ol className="divide-y">
          {audit.data.map((entry) => {
            const action = auditAction(entry.action)
            return (
              <li
                key={entry.id}
                className="flex flex-wrap items-center gap-x-3 gap-y-1 px-5 py-2.5 text-sm"
              >
                <span
                  className={cn('inline-flex items-center gap-1 rounded-md px-2 py-0.5 text-xs font-medium', action.className)}
                >
                  <action.icon className="size-3.5" aria-hidden />
                  {action.key ? t(action.key) : action.raw}
                </span>
                <span className="min-w-0 flex-1 truncate">{entry.detail}</span>
                <span className="font-mono text-xs text-muted-foreground">{entry.actor ?? '—'}</span>
                <time
                  dateTime={entry.timestamp}
                  title={formatDate(entry.timestamp, lang)}
                  className="text-xs text-muted-foreground"
                >
                  {formatRelative(entry.timestamp, lang)}
                </time>
              </li>
            )
          })}
        </ol>
      )}
    </section>
  )
}
