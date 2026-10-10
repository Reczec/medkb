import { ChevronRight, Pencil, Trash2 } from 'lucide-react'
import { Link, useNavigate, useParams } from 'react-router'
import { toast } from 'sonner'
import { ErrorState } from '@/components/feedback/ErrorState'
import { FileTab } from '@/components/specialty/FileTab'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { ClassificationExplainer } from '@/features/documents/ClassificationExplainer'
import { DocumentNotFound } from '@/features/documents/DocumentNotFound'
import { ApiError } from '@/lib/api'
import { formatDate, formatRelative } from '@/lib/format'
import { useDeleteDocument, useDocument } from '@/lib/queries'
import type { Document } from '@/lib/types'

function Details({ document }: { document: Document }) {
  const rows: [string, string][] = [
    ['Dokumenttyp', document.doc_type],
    ['Quelle', document.source ?? '—'],
    ['Erstellt', formatDate(document.created_at)],
    ['Geändert', formatDate(document.updated_at)],
  ]
  return (
    <section className="rounded-xl border bg-card p-5 shadow-sheet">
      <h2 className="text-base font-semibold">Details</h2>
      <dl className="mt-3 grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
        {rows.map(([label, value]) => (
          <div key={label} className="contents">
            <dt className="text-muted-foreground">{label}</dt>
            <dd className="min-w-0 [overflow-wrap:anywhere]">{value}</dd>
          </div>
        ))}
      </dl>
      {document.keywords.length > 0 && (
        <>
          <h3 className="mt-5 text-xs font-medium text-muted-foreground">Schlagwörter</h3>
          <ul className="mt-2 flex flex-wrap gap-1.5">
            {document.keywords.map((keyword) => (
              <li key={keyword} className="max-w-full rounded-md bg-muted px-2 py-0.5 text-xs break-all">
                {keyword}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  )
}

function DeleteButton({ document }: { document: Document }) {
  const remove = useDeleteDocument()
  const navigate = useNavigate()

  const confirm = (event: React.MouseEvent) => {
    event.preventDefault()
    remove.mutate(document.id, {
      onSuccess: () => {
        toast.success(`„${document.title}“ wurde gelöscht.`)
        navigate('/wissen')
      },
      onError: (error) => toast.error(error.message),
    })
  }

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="ghost" className="text-destructive hover:text-destructive">
          <Trash2 aria-hidden /> Löschen
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Eintrag endgültig löschen?</AlertDialogTitle>
          <AlertDialogDescription>
            „{document.title}“ wird gelöscht. Im Änderungsprotokoll bleibt der Vorgang sichtbar;
            wiederherstellen lässt er sich nur über ein Archiv.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Abbrechen</AlertDialogCancel>
          <AlertDialogAction variant="destructive" onClick={confirm} disabled={remove.isPending}>
            Endgültig löschen
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

export function DocumentPage() {
  const id = Number(useParams().id)
  const { data: document, error, isPending, refetch } = useDocument(id)

  if (!(Number.isInteger(id) && id > 0)) return <DocumentNotFound />
  if (error instanceof ApiError && error.status === 404) return <DocumentNotFound />
  if (error) return <ErrorState error={error} onRetry={() => refetch()} />
  if (isPending || !document) {
    return (
      <div className="flex flex-col gap-4" aria-busy="true">
        <Skeleton className="h-5 w-48" />
        <Skeleton className="h-10 w-2/3" />
        <Skeleton className="h-80 rounded-xl" />
      </div>
    )
  }

  const paragraphs = document.content.split(/\n\s*\n/).filter((p) => p.trim())

  return (
    <div className="flex flex-col gap-6">
      <nav aria-label="Pfad" className="flex items-center gap-1 text-sm text-muted-foreground">
        <Link to="/wissen" className="hover:text-foreground">
          Wissensdatenbank
        </Link>
        <ChevronRight className="size-3.5" aria-hidden />
        <Link
          to={`/wissen?category=${encodeURIComponent(document.category)}`}
          className="hover:text-foreground"
        >
          {document.category}
        </Link>
      </nav>

      <header className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="flex min-w-0 flex-col gap-2">
          <h1 className="text-3xl font-semibold tracking-tight [overflow-wrap:anywhere] lg:text-4xl">
            {document.title}
          </h1>
          <p className="flex flex-wrap items-center gap-x-2 text-sm text-muted-foreground">
            <span className="font-medium text-foreground/80">{document.doc_type}</span>
            <span aria-hidden>·</span>
            <span>geändert {formatRelative(document.updated_at)}</span>
          </p>
        </div>
        <div className="flex shrink-0 gap-2">
          <Button asChild variant="outline">
            <Link to={`/wissen/${document.id}/bearbeiten`}>
              <Pencil aria-hidden /> Bearbeiten
            </Link>
          </Button>
          <DeleteButton document={document} />
        </div>
      </header>

      <div className="grid grid-cols-1 items-start gap-6 lg:grid-cols-3">
        <div className="flex min-w-0 flex-col lg:col-span-2">
          <FileTab name={document.category} size="md" className="relative z-10 ml-5 -mb-px self-start" />
          <article className="rounded-xl border bg-card px-6 pt-6 pb-7 shadow-sheet">
            <div className="flex max-w-[68ch] flex-col gap-4 text-[17px] leading-relaxed">
              {paragraphs.map((paragraph, index) => (
                <p key={index} className="whitespace-pre-line [overflow-wrap:anywhere]">
                  {paragraph}
                </p>
              ))}
            </div>
          </article>
        </div>

        <aside className="flex min-w-0 flex-col gap-6">
          <ClassificationExplainer document={document} />
          <Details document={document} />
        </aside>
      </div>
    </div>
  )
}
