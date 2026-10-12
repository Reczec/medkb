import { Archive, Download, History, Loader2, Plus } from 'lucide-react'
import { useState } from 'react'
import { toast } from 'sonner'
import { EmptyState } from '@/components/feedback/EmptyState'
import { ErrorState } from '@/components/feedback/ErrorState'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { useI18n } from '@/i18n/context'
import { api } from '@/lib/api'
import { formatDate, formatNumber } from '@/lib/format'
import type { Lang } from '@/i18n/lang'
import { useArchives, useCreateArchive, useRestoreArchive } from '@/lib/queries'
import type { ArchiveInfo } from '@/lib/types'

const formatSize = (bytes: number, lang: Lang) =>
  bytes < 1024 ? `${bytes} B` : `${formatNumber(Math.round(bytes / 102.4) / 10, lang)} KB`

async function download(name: string) {
  try {
    const response = await api(`/api/archives/${encodeURIComponent(name)}`, { raw: true })
    const url = URL.createObjectURL(await response.blob())
    const link = document.createElement('a')
    link.href = url
    link.download = name
    link.click()
    URL.revokeObjectURL(url)
  } catch (error) {
    toast.error((error as Error).message)
  }
}

export function ArchivesPanel() {
  const archives = useArchives()
  const create = useCreateArchive()
  const restore = useRestoreArchive()
  const [pending, setPending] = useState<ArchiveInfo | null>(null)
  const { t, lang } = useI18n()

  const makeArchive = () =>
    create.mutate(undefined, {
      onSuccess: (info) => toast.success(t('archives.created', { count: info.document_count })),
      onError: (error) => toast.error(error.message),
    })

  const confirmRestore = () => {
    if (!pending) return
    restore.mutate(pending.name, {
      onSuccess: (result) =>
        toast.success(
          t('archives.restored', { count: result.restored, backup: result.backup.name }),
        ),
      onError: (error) => toast.error(error.message),
    })
    setPending(null)
  }

  return (
    <section className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="max-w-xl text-sm text-muted-foreground">
          {t('archives.intro')}
        </p>
        <Button onClick={makeArchive} disabled={create.isPending}>
          {create.isPending ? <Loader2 className="animate-spin" aria-hidden /> : <Plus aria-hidden />}
          {t('archives.create')}
        </Button>
      </div>

      {archives.error && <ErrorState error={archives.error} onRetry={() => archives.refetch()} />}
      {archives.isPending && <Skeleton className="h-40 rounded-xl" />}
      {archives.data?.length === 0 && (
        <EmptyState icon={Archive} title={t('archives.emptyTitle')} text={t('archives.emptyText')} />
      )}

      {archives.data && archives.data.length > 0 && (
        <ul className="divide-y overflow-hidden rounded-xl border bg-card shadow-sheet">
          {archives.data.map((info) => (
            <li key={info.name} className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center">
              <div className="flex min-w-0 flex-1 items-center gap-3">
                <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-accent text-primary">
                  <Archive className="size-[18px]" aria-hidden />
                </span>
                <div className="min-w-0">
                  <p className="truncate font-mono text-sm">{info.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {formatDate(info.created_at, lang)} ·{' '}
                    {t('archives.count', { count: info.document_count })} ·{' '}
                    {formatSize(info.size_bytes, lang)}
                  </p>
                </div>
              </div>
              <div className="flex shrink-0 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => download(info.name)}
                  aria-label={t('archives.downloadLabel', { name: info.name })}
                >
                  <Download aria-hidden /> {t('archives.download')}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPending(info)}
                  aria-label={t('archives.restoreLabel', { name: info.name })}
                >
                  <History aria-hidden /> {t('archives.restore')}
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}

      <AlertDialog open={pending !== null} onOpenChange={(open) => !open && setPending(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{t('archives.dialogTitle')}</AlertDialogTitle>
            <AlertDialogDescription>
              {pending &&
                t('archives.dialogText', { count: pending.document_count, name: pending.name })}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{t('doc.cancel')}</AlertDialogCancel>
            <AlertDialogAction onClick={confirmRestore}>{t('archives.restore')}</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  )
}
