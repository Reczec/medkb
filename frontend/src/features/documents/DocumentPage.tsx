import { BookOpenText, ChevronRight, FileText, Hash, Pencil, Pill, Trash2, MessageSquareText } from 'lucide-react'
import { DocumentAI } from '@/features/ai/DocumentAI'
import { useId } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router'
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Icd11Panel } from '@/features/documents/sources/Icd11Panel'
import { MedicationsPanel } from '@/features/documents/sources/MedicationsPanel'
import { StudiesPanel } from '@/features/documents/sources/StudiesPanel'
import { useAuth } from '@/features/auth/context'
import { ClassificationExplainer } from '@/features/documents/ClassificationExplainer'
import { DocumentNotFound } from '@/features/documents/DocumentNotFound'
import { FurtherReading } from '@/features/documents/FurtherReading'
import { SectionedContent } from '@/features/documents/SectionedContent'
import { useI18n } from '@/i18n/context'
import { localized } from '@/i18n/localized'
import type { TranslationKey } from '@/i18n/translate'
import { ApiError } from '@/lib/api'
import { formatDate, formatRelative } from '@/lib/format'
import { useDeleteDocument, useDocument } from '@/lib/queries'
import type { Document } from '@/lib/types'

function Details({ document, keywords }: { document: Document; keywords: string[] }) {
  const id = useId()
  const { t, lang, docTypeLabel } = useI18n()
  const rows: [string, string][] = [
    [t('doc.docType'), docTypeLabel(document.doc_type)],
    ...(document.term_en ? [[t('doc.termEn'), document.term_en] as [string, string]] : []),
    ...(document.icd11_code ? [[t('doc.icd11'), document.icd11_code] as [string, string]] : []),
    [t('doc.source'), document.source ?? '—'],
    [t('doc.created'), formatDate(document.created_at, lang)],
    [t('doc.changedAt'), formatDate(document.updated_at, lang)],
  ]
  return (
    <section aria-labelledby={id} className="rounded-xl border bg-card p-5 shadow-sheet">
      <h2 id={id} className="text-base font-semibold">
        {t('doc.details')}
      </h2>
      <dl className="mt-3 grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
        {rows.map(([label, value]) => (
          <div key={label} className="contents">
            <dt className="text-muted-foreground">{label}</dt>
            <dd className="min-w-0 [overflow-wrap:anywhere]">{value}</dd>
          </div>
        ))}
      </dl>
      {keywords.length > 0 && (
        <>
          <h3 className="mt-5 text-xs font-medium text-muted-foreground">{t('card.keywords')}</h3>
          <ul className="mt-2 flex flex-wrap gap-1.5">
            {keywords.map((keyword) => (
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
  const { t, lang } = useI18n()
  const title = localized(document, lang).title

  const confirm = (event: React.MouseEvent) => {
    event.preventDefault()
    remove.mutate(document.id, {
      onSuccess: () => {
        toast.success(t('doc.deleted', { title }))
        navigate('/wissen')
      },
      onError: (error) => toast.error(error.message),
    })
  }

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="ghost" className="text-destructive hover:text-destructive">
          <Trash2 aria-hidden /> {t('doc.delete')}
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{t('doc.deleteTitle')}</AlertDialogTitle>
          <AlertDialogDescription>{t('doc.deleteText', { title })}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>{t('doc.cancel')}</AlertDialogCancel>
          <AlertDialogAction variant="destructive" onClick={confirm} disabled={remove.isPending}>
            {t('doc.deleteConfirm')}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

const VIEWS: { value: string; label: TranslationKey; icon: typeof FileText }[] = [
  { value: 'inhalt', label: 'view.content', icon: FileText },
  { value: 'ki', label: 'view.ai', icon: MessageSquareText },
  { value: 'icd11', label: 'view.icd11', icon: Hash },
  { value: 'studien', label: 'view.studies', icon: BookOpenText },
  { value: 'medikamente', label: 'view.medications', icon: Pill },
]

/** Staff view: the sheet carries tabs; each source loads when its tab is first opened. */
function SourceTabs({ document, content }: { document: Document; content: React.ReactNode }) {
  const [params, setParams] = useSearchParams()
  const { t } = useI18n()
  const views = VIEWS.filter((v) => v.value !== 'medikamente' || document.medications.length > 0)
  const requested = params.get('tab')
  const tab = views.some((v) => v.value === requested) ? requested! : 'inhalt'
  const select = (value: string) =>
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev)
        if (value === 'inhalt') next.delete('tab')
        else next.set('tab', value)
        return next
      },
      { replace: true },
    )

  // Radix mounts only the active tab's content, so a panel fetches on first opening;
  // the query cache (10 min) keeps it from fetching again when the tab is reopened.
  return (
    <Tabs value={tab} onValueChange={select} className="gap-0">
      <article className="rounded-xl border bg-card shadow-sheet">
        <TabsList
          variant="line"
          aria-label={t('view.label')}
          className="h-12! w-full justify-start gap-1 overflow-x-auto border-b px-4"
        >
          {views.map(({ value, label, icon: Icon }) => (
            <TabsTrigger key={value} value={value} className="flex-none px-3">
              <Icon aria-hidden /> {t(label)}
            </TabsTrigger>
          ))}
        </TabsList>
        <div className="px-6 pt-6 pb-7 text-base">
          <TabsContent value="inhalt">{content}</TabsContent>
          <TabsContent value="ki"><DocumentAI key={document.id} documentId={document.id} summaryOnly /></TabsContent>
          <TabsContent value="icd11">
            <Icd11Panel documentId={document.id} enabled />
          </TabsContent>
          <TabsContent value="studien">
            <StudiesPanel documentId={document.id} termEn={document.term_en} enabled />
          </TabsContent>
          {document.medications.length > 0 && (
            <TabsContent value="medikamente">
              <MedicationsPanel documentId={document.id} enabled />
            </TabsContent>
          )}
        </div>
      </article>
    </Tabs>
  )
}

export function DocumentPage() {
  const id = Number(useParams().id)
  const { data: document, error, isPending, refetch } = useDocument(id)
  const { user } = useAuth()
  const { t, lang, categoryLabel, docTypeLabel } = useI18n()
  const isAdmin = user?.role === 'admin'
  const showsClassification = user?.role === 'admin' || user?.role === 'doctor'

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

  const text = localized(document, lang)
  const paragraphs = text.content.split(/\n\s*\n/).filter((p) => p.trim())
  const content = text.sections ? (
    <SectionedContent sections={text.sections} />
  ) : (
    <div className="flex max-w-[68ch] flex-col gap-4 text-[17px] leading-relaxed">
      {paragraphs.map((paragraph, index) => (
        <p key={index} className="whitespace-pre-line [overflow-wrap:anywhere]">
          {paragraph}
        </p>
      ))}
    </div>
  )

  return (
    <div className="flex flex-col gap-6">
      <nav aria-label={t('doc.path')} className="flex items-center gap-1 text-sm text-muted-foreground">
        <Link to="/wissen" className="hover:text-foreground">
          {t('nav.knowledge')}
        </Link>
        <ChevronRight className="size-3.5" aria-hidden />
        <Link
          to={`/wissen?category=${encodeURIComponent(document.category)}`}
          className="hover:text-foreground"
        >
          {categoryLabel(document.category)}
        </Link>
      </nav>

      <header className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="flex min-w-0 flex-col gap-2">
          <h1 className="text-3xl font-semibold tracking-tight [overflow-wrap:anywhere] lg:text-4xl">
            {text.title}
          </h1>
          <p className="flex flex-wrap items-center gap-x-2 text-sm text-muted-foreground">
            <span className="font-medium text-foreground/80">{docTypeLabel(document.doc_type)}</span>
            {document.ai_generated && (
              <span className="rounded-md bg-muted px-2 py-0.5 text-xs">{t('doc.aiGenerated')}</span>
            )}
            <span aria-hidden>·</span>
            <span>{t('card.changed', { time: formatRelative(document.updated_at, lang) })}</span>
          </p>
        </div>
        {isAdmin && (
        <div className="flex shrink-0 gap-2">
          <Button asChild variant="outline">
            <Link to={`/wissen/${document.id}/bearbeiten`}>
              <Pencil aria-hidden /> {t('doc.edit')}
            </Link>
          </Button>
          <DeleteButton document={document} />
        </div>
        )}
      </header>

      {text.fallback && (
        <p role="status" className="w-fit rounded-lg bg-muted px-3 py-1.5 text-sm text-muted-foreground">
          {t('doc.onlyGerman')}
        </p>
      )}

      <div className="grid grid-cols-1 items-start gap-6 lg:grid-cols-3">
        <div className="flex min-w-0 flex-col lg:col-span-2">
          <FileTab name={document.category} size="md" className="relative z-10 ml-5 -mb-px self-start" />
          {showsClassification ? (
            <SourceTabs document={document} content={content} />
          ) : (
            <article className="rounded-xl border bg-card px-6 pt-6 pb-7 shadow-sheet">
              {content}
            </article>
          )}
        </div>

        <aside className="flex min-w-0 flex-col gap-6">
          {showsClassification && <ClassificationExplainer document={document} />}
          <Details document={document} keywords={text.keywords} />
          <div className="rounded-xl border bg-card p-5 shadow-sheet"><DocumentAI key={document.id} documentId={document.id} /></div>
          <FurtherReading links={document.further_reading} />
        </aside>
      </div>
    </div>
  )
}
