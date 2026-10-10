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
import { api } from '@/lib/api'
import { formatDate, formatNumber } from '@/lib/format'
import { useArchives, useCreateArchive, useRestoreArchive } from '@/lib/queries'
import type { ArchiveInfo } from '@/lib/types'

const formatSize = (bytes: number) =>
  bytes < 1024 ? `${bytes} B` : `${formatNumber(Math.round(bytes / 102.4) / 10)} KB`

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

  const makeArchive = () =>
    create.mutate(undefined, {
      onSuccess: (info) => toast.success(`Archiv mit ${info.document_count} Einträgen erstellt.`),
      onError: (error) => toast.error(error.message),
    })

  const confirmRestore = () => {
    if (!pending) return
    restore.mutate(pending.name, {
      onSuccess: (result) =>
        toast.success(
          `${result.restored} Einträge wiederhergestellt. Sicherung: ${result.backup.name}`,
        ),
      onError: (error) => toast.error(error.message),
    })
    setPending(null)
  }

  return (
    <section className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="max-w-xl text-sm text-muted-foreground">
          Ein Archiv ist ein JSON-Export aller Einträge. Vor jeder Wiederherstellung wird automatisch
          eine Sicherung des aktuellen Stands angelegt.
        </p>
        <Button onClick={makeArchive} disabled={create.isPending}>
          {create.isPending ? <Loader2 className="animate-spin" aria-hidden /> : <Plus aria-hidden />}
          Archiv erstellen
        </Button>
      </div>

      {archives.error && <ErrorState error={archives.error} onRetry={() => archives.refetch()} />}
      {archives.isPending && <Skeleton className="h-40 rounded-xl" />}
      {archives.data?.length === 0 && (
        <EmptyState icon={Archive} title="Noch keine Archive" text="Erstelle das erste Archiv mit einem Klick." />
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
                    {formatDate(info.created_at)} · {info.document_count} Einträge ·{' '}
                    {formatSize(info.size_bytes)}
                  </p>
                </div>
              </div>
              <div className="flex shrink-0 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => download(info.name)}
                  aria-label={`${info.name} herunterladen`}
                >
                  <Download aria-hidden /> Download
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPending(info)}
                  aria-label={`${info.name} wiederherstellen`}
                >
                  <History aria-hidden /> Wiederherstellen
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}

      <AlertDialog open={pending !== null} onOpenChange={(open) => !open && setPending(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Archiv wiederherstellen?</AlertDialogTitle>
            <AlertDialogDescription>
              Alle aktuellen Einträge werden durch die {pending?.document_count} Einträge aus „
              {pending?.name}“ ersetzt. Vorher wird automatisch eine Sicherung erstellt.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Abbrechen</AlertDialogCancel>
            <AlertDialogAction onClick={confirmRestore}>Wiederherstellen</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  )
}
