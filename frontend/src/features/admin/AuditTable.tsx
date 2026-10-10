import { Link } from 'react-router'
import { ErrorState } from '@/components/feedback/ErrorState'
import { Skeleton } from '@/components/ui/skeleton'
import { formatDate, formatRelative } from '@/lib/format'
import { useAudit } from '@/lib/queries'
import { cn } from '@/lib/utils'

const ACTIONS: Record<string, { label: string; className: string }> = {
  create: { label: 'Angelegt', className: 'bg-emerald-500/12 text-emerald-700 dark:text-emerald-300' },
  update: { label: 'Bearbeitet', className: 'bg-sky-500/12 text-sky-700 dark:text-sky-300' },
  delete: { label: 'Gelöscht', className: 'bg-red-500/12 text-red-700 dark:text-red-300' },
  archive_create: { label: 'Archiviert', className: 'bg-violet-500/12 text-violet-700 dark:text-violet-300' },
  archive_restore: { label: 'Wiederhergestellt', className: 'bg-violet-500/12 text-violet-700 dark:text-violet-300' },
}

export function AuditTable() {
  const audit = useAudit(100)

  if (audit.error) return <ErrorState error={audit.error} onRetry={() => audit.refetch()} />
  if (audit.isPending) return <Skeleton className="h-64 rounded-xl" />
  if (audit.data.length === 0) {
    return <p className="text-sm text-muted-foreground">Noch keine Änderungen protokolliert.</p>
  }

  return (
    <div className="overflow-x-auto rounded-xl border bg-card shadow-sheet">
      <table className="w-full min-w-[560px] text-sm">
        <thead>
          <tr className="border-b text-left text-xs text-muted-foreground">
            <th className="px-5 py-3 font-medium">Zeit</th>
            <th className="px-3 py-3 font-medium">Aktion</th>
            <th className="px-3 py-3 font-medium">Eintrag</th>
            <th className="px-5 py-3 font-medium">Detail</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {audit.data.map((entry) => {
            const action = ACTIONS[entry.action] ?? { label: entry.action, className: 'bg-muted' }
            return (
              <tr key={entry.id} className="transition-colors hover:bg-muted/50">
                <td className="px-5 py-3 whitespace-nowrap text-muted-foreground">
                  <time dateTime={entry.timestamp} title={formatDate(entry.timestamp)}>
                    {formatRelative(entry.timestamp)}
                  </time>
                </td>
                <td className="px-3 py-3">
                  <span className={cn('inline-flex rounded-md px-2 py-0.5 text-xs font-medium', action.className)}>
                    {action.label}
                  </span>
                </td>
                <td className="tabular px-3 py-3">
                  {entry.document_id !== null && entry.action !== 'delete' ? (
                    <Link to={`/wissen/${entry.document_id}`} className="text-primary hover:underline">
                      #{entry.document_id}
                    </Link>
                  ) : (
                    <span className="text-muted-foreground">{entry.document_id ? `#${entry.document_id}` : '—'}</span>
                  )}
                </td>
                <td className="max-w-[28rem] truncate px-5 py-3" title={entry.detail}>
                  {entry.detail}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
