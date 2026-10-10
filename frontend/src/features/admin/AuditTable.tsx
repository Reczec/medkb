import { Link } from 'react-router'
import { ErrorState } from '@/components/feedback/ErrorState'
import { Skeleton } from '@/components/ui/skeleton'
import { formatDate, formatRelative } from '@/lib/format'
import { auditAction } from '@/lib/audit'
import { useAudit } from '@/lib/queries'
import { cn } from '@/lib/utils'

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
            <th className="px-3 py-3 font-medium">Wer</th>
            <th className="px-3 py-3 font-medium">Eintrag</th>
            <th className="px-5 py-3 font-medium">Detail</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {audit.data.map((entry) => {
            const action = auditAction(entry.action)
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
                <td className="px-3 py-3 font-mono text-xs whitespace-nowrap">{entry.actor ?? '—'}</td>
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
