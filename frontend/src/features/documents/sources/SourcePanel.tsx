import type { UseQueryResult } from '@tanstack/react-query'
import { CloudOff, RotateCw, SearchX, Settings2 } from 'lucide-react'
import type { ReactNode } from 'react'
import { ErrorState } from '@/components/feedback/ErrorState'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { useI18n } from '@/i18n/context'
import { formatRelative } from '@/lib/format'
import type { SourceResult } from '@/lib/types'

interface SourcePanelProps<T> {
  /** Shown name of the source, e.g. "PubMed · NCBI". */
  source: string
  /** Short name for messages, e.g. "PubMed". */
  shortName: string
  query: UseQueryResult<SourceResult<T>>
  emptyText: string
  notConfiguredText?: string
  /** One line under the header, e.g. what was searched for. */
  caption?: ReactNode
  children: (data: T) => ReactNode
}

function Notice({ icon, children }: { icon: ReactNode; children: ReactNode }) {
  return (
    <div className="flex items-start gap-3 rounded-xl bg-muted/70 px-4 py-3.5 text-sm">
      <span className="mt-0.5 shrink-0 text-muted-foreground [&_svg]:size-4">{icon}</span>
      <div className="min-w-0 flex-1">{children}</div>
    </div>
  )
}

/**
 * The frame every external source shares: who answered and when, and an honest state for
 * loading, no result, not reachable and not set up. A source never breaks the page.
 */
export function SourcePanel<T>({
  source,
  shortName,
  query,
  emptyText,
  notConfiguredText,
  caption,
  children,
}: SourcePanelProps<T>) {
  const result = query.data
  const { t, lang } = useI18n()
  const retry = () => query.refetch()

  let body: ReactNode
  if (query.isPending) {
    body = (
      <div aria-busy="true" aria-label={t('source.loading', { name: shortName })} className="flex flex-col gap-4">
        {[0, 1, 2].map((i) => (
          <div key={i} className="flex flex-col gap-2">
            <Skeleton className="h-4 w-11/12" />
            <Skeleton className="h-3 w-1/2" />
          </div>
        ))}
      </div>
    )
  } else if (query.isError) {
    body = <ErrorState error={query.error} onRetry={retry} />
  } else if (!result || result.status === 'unavailable') {
    body = (
      <Notice icon={<CloudOff />}>
        <p className="font-medium">{t('source.unreachable', { name: shortName })}</p>
        <p className="mt-0.5 text-muted-foreground">{t('source.unreachableHint')}</p>
        <Button variant="outline" size="sm" className="mt-3" onClick={retry} disabled={query.isFetching}>
          <RotateCw aria-hidden className={query.isFetching ? 'animate-spin' : undefined} />{' '}
          {t('action.retry')}
        </Button>
      </Notice>
    )
  } else if (result.status === 'not_configured') {
    body = (
      <Notice icon={<Settings2 />}>
        <p>{notConfiguredText ?? t('source.notConfigured', { name: shortName })}</p>
      </Notice>
    )
  } else if (result.status === 'empty' || result.data === null) {
    body = (
      <Notice icon={<SearchX />}>
        <p>{emptyText}</p>
      </Notice>
    )
  } else {
    body = children(result.data)
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <p className="text-xs font-medium text-muted-foreground">{source}</p>
        {result?.fetched_at && (
          <p className="text-xs text-muted-foreground">
            {t('source.retrieved', { time: formatRelative(result.fetched_at, lang) })}
          </p>
        )}
      </div>
      {caption && <p className="-mt-2 text-sm text-muted-foreground">{caption}</p>}
      {body}
    </div>
  )
}
