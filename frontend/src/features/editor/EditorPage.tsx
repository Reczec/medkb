import { ArrowLeft, ListPlus, Loader2, Save } from 'lucide-react'
import { useRef, useState } from 'react'
import { Link, useBlocker, useNavigate, useParams } from 'react-router'
import { toast } from 'sonner'
import { ErrorState } from '@/components/feedback/ErrorState'
import { DocumentNotFound } from '@/features/documents/DocumentNotFound'
import { ScoreBars } from '@/components/specialty/ScoreBars'
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
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { Textarea } from '@/components/ui/textarea'
import { AUTO, CategoryPicker } from '@/features/editor/CategoryPicker'
import { KeywordInput, mergeKeywords } from '@/features/editor/KeywordInput'
import { SectionFields } from '@/features/editor/SectionFields'
import { useDebounced } from '@/hooks/useDebounced'
import { ApiError } from '@/lib/api'
import {
  useClassify,
  useCreateDocument,
  useDocument,
  useMeta,
  useUpdateDocument,
} from '@/lib/queries'
import { cleanSections, composeContent } from '@/lib/sections'
import type { Document, DocumentCreate, DocumentUpdate, Meta, Sections } from '@/lib/types'

interface FormState {
  title: string
  content: string
  docType: string
  category: string
  keywords: string[]
  source: string
  termEn: string
  icd11Code: string
  medications: string[]
  mode: 'text' | 'sections'
  sections: Sections
}

function initialState(meta: Meta, document?: Document): FormState {
  if (!document) {
    return { title: '', content: '', docType: meta.doc_types[0] ?? '', category: AUTO, keywords: [], source: '', termEn: '', icd11Code: '', medications: [], mode: 'text', sections: {} }
  }
  return {
    title: document.title,
    content: document.content,
    docType: document.doc_type,
    category: document.auto_classified ? AUTO : document.category,
    keywords: document.keywords,
    source: document.source ?? '',
    termEn: document.term_en ?? '',
    icd11Code: document.icd11_code ?? '',
    medications: document.medications,
    mode: document.sections ? 'sections' : 'text',
    sections: cleanSections(document.sections ?? {}),
  }
}

function createPayload(form: FormState): DocumentCreate {
  const payload: DocumentCreate = {
    title: form.title.trim(),
    ...(form.mode === 'sections' ? { sections: cleanSections(form.sections) } : { content: form.content.trim() }),
    doc_type: form.docType,
    term_en: form.termEn.trim() || null,
    icd11_code: form.icd11Code.trim() || null,
    medications: form.medications,
  }
  if (form.category !== AUTO) payload.category = form.category
  if (form.keywords.length > 0) payload.keywords = form.keywords
  if (form.source.trim()) payload.source = form.source.trim()
  return payload
}

/** Only the fields that differ from the loaded entry. */
function updatePayload(form: FormState, initial: FormState): DocumentUpdate {
  const payload: DocumentUpdate = {}
  if (form.title.trim() !== initial.title) payload.title = form.title.trim()
  if (form.mode === 'sections') {
    if (initial.mode !== 'sections' || JSON.stringify(cleanSections(form.sections)) !== JSON.stringify(initial.sections)) {
      payload.sections = cleanSections(form.sections)
    }
  } else if (initial.mode !== 'text' || form.content.trim() !== initial.content) {
    payload.content = form.content.trim()
  }
  if (form.termEn.trim() !== initial.termEn) payload.term_en = form.termEn.trim() || null
  if (form.icd11Code.trim() !== initial.icd11Code) payload.icd11_code = form.icd11Code.trim() || null
  if (form.medications.join('\n') !== initial.medications.join('\n')) payload.medications = form.medications
  if (form.docType !== initial.docType) payload.doc_type = form.docType
  if (form.source.trim() !== initial.source) payload.source = form.source.trim() || null
  if (form.keywords.join('\n') !== initial.keywords.join('\n')) payload.keywords = form.keywords
  if (form.category !== initial.category) {
    if (form.category === AUTO) payload.reclassify = true
    else payload.category = form.category
  } else if (form.category === AUTO && ('title' in payload || 'content' in payload || 'sections' in payload)) {
    // The classifier stays in charge: new text means a new suggestion.
    payload.reclassify = true
  }
  // Without keywords the server would replace the visible ones with its own suggestion.
  if (payload.reclassify) payload.keywords = form.keywords
  return payload
}

function Field({ id, label, hint, children }: { id: string; label: string; hint?: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-medium">
        {label}
      </label>
      {children}
      {hint && <p className="text-xs text-muted-foreground">{hint}</p>}
    </div>
  )
}

function EditorForm({ meta, document }: { meta: Meta; document?: Document }) {
  const navigate = useNavigate()
  const [initial] = useState(() => initialState(meta, document))
  const [form, setForm] = useState(initial)
  const leaving = useRef(false)
  const create = useCreateDocument()
  const update = useUpdateDocument(document?.id ?? 0)
  const saving = create.isPending || update.isPending

  const set = <K extends keyof FormState>(key: K, value: FormState[K]) =>
    setForm((current) => ({ ...current, [key]: value }))

  const title = useDebounced(form.title, 400)
  const debouncedForm = useDebounced(form, 400)
  const classification = useClassify(title, debouncedForm.mode === 'sections'
    ? { sections: cleanSections(debouncedForm.sections) }
    : { content: debouncedForm.content })
  const suggestion = classification.data

  const changes = document ? updatePayload(form, initial) : null
  const dirty = document ? Object.keys(changes!).length > 0 : JSON.stringify(form) !== JSON.stringify(initial)
  const valid = form.title.trim().length >= 3 && (form.mode === 'sections'
    ? Object.keys(cleanSections(form.sections)).length > 0
    : form.content.trim().length >= 10)

  const changeMode = (mode: FormState['mode']) => {
    setForm((current) => {
      if (mode === current.mode) return current
      return mode === 'sections'
        ? { ...current, mode, sections: { definition: current.content } }
        : { ...current, mode, content: composeContent(current.sections) }
    })
  }

  const blocker = useBlocker(
    ({ currentLocation, nextLocation }) =>
      dirty && !leaving.current && currentLocation.pathname !== nextLocation.pathname,
  )

  const finish = (saved: Document, message: string) => {
    leaving.current = true
    toast.success(message)
    navigate(`/wissen/${saved.id}`)
  }

  const submit = (event: React.FormEvent) => {
    event.preventDefault()
    if (!valid || saving) return
    const onError = (error: Error) =>
      toast.error(
        error instanceof ApiError && error.status === 404
          ? 'Eintrag existiert nicht mehr (Demo wurde zurückgesetzt)'
          : error.message,
      )
    if (document) {
      if (!dirty) {
        leaving.current = true
        navigate(`/wissen/${document.id}`)
        return
      }
      update.mutate(changes!, { onSuccess: (saved) => finish(saved, 'Änderungen gespeichert.'), onError })
    } else {
      create.mutate(createPayload(form), {
        onSuccess: (saved) => finish(saved, `„${saved.title}“ angelegt.`),
        onError,
      })
    }
  }

  const fresh = suggestion?.keywords.filter(
    (k) => !form.keywords.some((existing) => existing.toLowerCase() === k.toLowerCase()),
  )

  return (
    <form onSubmit={submit} className="grid grid-cols-1 items-start gap-6 lg:grid-cols-3" noValidate>
      <div className="flex min-w-0 flex-col gap-5 rounded-xl border bg-card p-5 shadow-sheet sm:p-6 lg:col-span-2">
        <Field id="title" label="Titel" hint="Mindestens 3 Zeichen.">
          <Input
            id="title"
            value={form.title}
            onChange={(event) => set('title', event.target.value)}
            maxLength={200}
            className="h-11 text-base"
            placeholder="z. B. Herzrasen bei Belastung"
          />
        </Field>

        <div className="grid gap-5 sm:grid-cols-2">
          <Field id="doc-type" label="Dokumenttyp">
            <Select value={form.docType} onValueChange={(value) => set('docType', value)}>
              <SelectTrigger id="doc-type" className="h-11! w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent position="popper">
                {meta.doc_types.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Field>
          <Field id="source" label="Quelle (optional)">
            <Input
              id="source"
              value={form.source}
              onChange={(event) => set('source', event.target.value)}
              maxLength={200}
              className="h-11"
              placeholder="z. B. Leitlinie, Lehrbuch"
            />
          </Field>
        </div>

        <div className="grid gap-5 sm:grid-cols-2">
          <Field id="term-en" label="Fachbegriff (en)" hint="Optional, für die PubMed-Suche.">
            <Input id="term-en" value={form.termEn} onChange={(event) => set('termEn', event.target.value)} maxLength={200} className="h-11" placeholder="z. B. Migraine" />
          </Field>
          <Field id="icd11-code" label="ICD-11-Code" hint="Optional, z. B. 8A80 oder 8A80.1.">
            <Input id="icd11-code" value={form.icd11Code} onChange={(event) => set('icd11Code', event.target.value)} maxLength={20} className="h-11" />
          </Field>
        </div>

        <Field id="medications" label="Wirkstoffe (en)">
          <KeywordInput id="medications" value={form.medications} onChange={(value) => set('medications', value)} maxItems={10} maxLength={60} addLabel="Wirkstoff hinzufügen" emptyHint="Optional: bis zu 10 Wirkstoffe auf Englisch, für die openFDA-Abfrage." />
        </Field>

        <div className="flex flex-col gap-2">
          <span id="content-mode-label" className="text-sm font-medium">Textaufbau</span>
          <div role="group" aria-labelledby="content-mode-label" className="flex w-fit gap-1 rounded-lg border bg-muted p-1">
            <Button type="button" variant={form.mode === 'text' ? 'outline' : 'ghost'} aria-pressed={form.mode === 'text'} onClick={() => changeMode('text')}>Freitext</Button>
            <Button type="button" variant={form.mode === 'sections' ? 'outline' : 'ghost'} aria-pressed={form.mode === 'sections'} onClick={() => changeMode('sections')}>Abschnitte</Button>
          </div>
        </div>

        {form.mode === 'sections' ? (
          <SectionFields value={form.sections} onChange={(value) => set('sections', value)} />
        ) : <Field id="content" label="Inhalt" hint="Mindestens 10 Zeichen. Leerzeilen trennen Absätze.">
          <Textarea
            id="content"
            value={form.content}
            onChange={(event) => set('content', event.target.value)}
            maxLength={50_000}
            className="min-h-56 w-full min-w-0 text-base leading-relaxed [field-sizing:content] [overflow-wrap:anywhere]"
            placeholder="Beschreibung, Symptome, Ursachen, Diagnostik, Therapie …"
          />
        </Field>}

        <div className="flex flex-col gap-2">
          <span id="category-label" className="text-sm font-medium">
            Fachgebiet
          </span>
          <CategoryPicker
            categories={meta.categories}
            value={form.category}
            onChange={(value) => set('category', value)}
            suggestion={suggestion?.category}
          />
        </div>

        <Field id="keywords" label="Schlagwörter">
          <KeywordInput id="keywords" value={form.keywords} onChange={(value) => set('keywords', value)} />
        </Field>

        <div className="flex flex-wrap items-center justify-end gap-3 border-t pt-5">
          <Button asChild variant="ghost">
            <Link to={document ? `/wissen/${document.id}` : '/wissen'}>Abbrechen</Link>
          </Button>
          <Button type="submit" disabled={!valid || saving}>
            {saving ? <Loader2 className="animate-spin" aria-hidden /> : <Save aria-hidden />}
            Speichern
          </Button>
        </div>
      </div>

      <aside
        aria-label="Live-Klassifikation"
        className="flex min-w-0 flex-col gap-4 rounded-xl border bg-card p-5 shadow-sheet lg:sticky lg:top-24"
      >
        <div>
          <h2 className="text-base font-semibold">Live-Klassifikation</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Regelbasiert, aktualisiert sich beim Tippen.
          </p>
        </div>
        {!suggestion && (
          <p className="rounded-lg bg-muted px-3 py-3 text-sm text-muted-foreground">
            {form.mode === 'sections'
              ? 'Titel und mindestens einen Abschnitt ausfüllen, dann erscheint ein Vorschlag.'
              : 'Titel und mindestens 10 Zeichen Inhalt eingeben, dann erscheint ein Vorschlag.'}
          </p>
        )}
        {suggestion && (
          <>
            <p className="text-sm" aria-live="polite">
              {suggestion.fallback ? (
                <>Zu wenige Fachbegriffe – Rückfall auf <strong>{suggestion.category}</strong></>
              ) : (
                <>
                  Vorschlag: <strong>{suggestion.category}</strong>{' '}
                  <span className="text-muted-foreground">
                    (Konfidenz {Math.round(suggestion.confidence * 100)} %)
                  </span>
                </>
              )}
            </p>
            <ScoreBars scores={suggestion.scores} winner={suggestion.category} />
            {fresh && fresh.length > 0 && (
              <Button
                type="button"
                variant="outline"
                onClick={() => set('keywords', mergeKeywords(form.keywords, fresh))}
              >
                <ListPlus aria-hidden /> {fresh.length} Schlagwörter übernehmen
              </Button>
            )}
          </>
        )}
      </aside>

      <AlertDialog open={blocker.state === 'blocked'}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Änderungen verwerfen?</AlertDialogTitle>
            <AlertDialogDescription>
              Du hast ungespeicherte Änderungen. Wenn du die Seite verlässt, gehen sie verloren.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => blocker.reset?.()}>Weiter bearbeiten</AlertDialogCancel>
            <AlertDialogAction variant="destructive" onClick={() => blocker.proceed?.()}>
              Verwerfen
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </form>
  )
}

export function EditorPage() {
  const params = useParams()
  const id = params.id ? Number(params.id) : undefined
  const meta = useMeta()
  const document = useDocument(id ?? 0)
  const editing = id !== undefined

  if (editing && !(Number.isInteger(id) && id > 0)) return <DocumentNotFound />
  if (document.error instanceof ApiError && document.error.status === 404) return <DocumentNotFound />

  const error = meta.error ?? (editing ? document.error : null)
  const ready = meta.data && (!editing || document.data)

  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-2">
        <Link
          to={editing ? `/wissen/${id}` : '/wissen'}
          className="inline-flex w-fit items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="size-4" aria-hidden /> Zurück
        </Link>
        <h1 className="text-3xl font-semibold tracking-tight">
          {editing ? 'Eintrag bearbeiten' : 'Neuer Eintrag'}
        </h1>
      </header>

      {error && <ErrorState error={error} onRetry={() => (meta.error ? meta.refetch() : document.refetch())} />}
      {!error && !ready && <Skeleton className="h-[520px] rounded-xl" />}
      {ready && <EditorForm key={id ?? 'new'} meta={meta.data!} document={editing ? document.data : undefined} />}
    </div>
  )
}
