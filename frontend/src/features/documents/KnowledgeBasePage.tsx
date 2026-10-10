import { ChevronLeft, ChevronRight, Loader2 } from 'lucide-react'
import { AnimatePresence, motion, useReducedMotion } from 'motion/react'
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router'
import { EmptyState } from '@/components/feedback/EmptyState'
import { ErrorState } from '@/components/feedback/ErrorState'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { DocumentCard } from '@/features/documents/DocumentCard'
import { SearchFilters } from '@/features/documents/SearchFilters'
import { useDebounced } from '@/hooks/useDebounced'
import { useDocuments, useMeta, useStats } from '@/lib/queries'

const PAGE_SIZE = 10

export function KnowledgeBasePage() {
  const [params, setParams] = useSearchParams()
  const reduced = useReducedMotion()
  const urlQuery = params.get('q') ?? ''
  const category = params.get('category') ?? ''
  const docType = params.get('type') ?? ''
  const page = Math.max(1, Number(params.get('page')) || 1)

  const [query, setQuery] = useState(urlQuery)
  const debounced = useDebounced(query, 300)

  /** Updates URL parameters; every filter change starts again on page 1. */
  const update = (changes: Record<string, string>) => {
    setParams(
      (current) => {
        const next = new URLSearchParams(current)
        for (const [key, value] of Object.entries(changes)) {
          if (value) next.set(key, value)
          else next.delete(key)
        }
        if (!('page' in changes)) next.delete('page')
        return next
      },
      { replace: true },
    )
  }

  useEffect(() => {
    if (debounced.trim() !== urlQuery) update({ q: debounced.trim() })
    // eslint-disable-next-line react-hooks/exhaustive-deps -- only react to the typed text
  }, [debounced])

  const meta = useMeta()
  const stats = useStats()
  const documents = useDocuments({
    q: urlQuery,
    category,
    docType,
    offset: (page - 1) * PAGE_SIZE,
    limit: PAGE_SIZE,
  })

  const total = documents.data?.total ?? 0
  const items = documents.data?.items ?? []
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE))
  const first = total === 0 ? 0 : (page - 1) * PAGE_SIZE + 1
  const last = Math.min(page * PAGE_SIZE, total)

  const resetFilters = () => {
    setQuery('')
    setParams({}, { replace: true })
  }

  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-1">
        <h1 className="text-3xl font-semibold tracking-tight">Wissensdatenbank</h1>
        <p className="text-muted-foreground">
          Alle Suchbegriffe müssen vorkommen, Treffer im Titel zählen am meisten.
        </p>
      </header>

      <SearchFilters
        query={query}
        onQueryChange={setQuery}
        category={category}
        onCategoryChange={(value) => update({ category: value })}
        docType={docType}
        onDocTypeChange={(value) => update({ type: value })}
        docTypes={meta.data?.doc_types ?? []}
        specialties={stats.data?.categories ?? []}
      />

      <div className="flex min-h-6 items-center gap-2 text-sm text-muted-foreground" aria-live="polite">
        {documents.data && (
          <span className="tabular">
            {first}–{last} von {total} {total === 1 ? 'Eintrag' : 'Einträgen'}
          </span>
        )}
        {documents.isFetching && <Loader2 className="size-4 animate-spin" aria-label="Lädt" />}
      </div>

      {documents.error && (
        <ErrorState error={documents.error} onRetry={() => documents.refetch()} />
      )}

      {documents.isPending && (
        <div className="grid gap-5 lg:grid-cols-2">
          {Array.from({ length: 4 }, (_, i) => (
            <Skeleton key={i} className="h-56 rounded-xl" />
          ))}
        </div>
      )}

      {documents.data && items.length === 0 && (
        <EmptyState
          title="Keine Einträge gefunden"
          text="Versuche weniger oder andere Suchbegriffe oder entferne Filter."
          action={
            <Button variant="outline" onClick={resetFilters}>
              Filter zurücksetzen
            </Button>
          }
        />
      )}

      {items.length > 0 && (
        <motion.ul layout={!reduced} className="grid gap-5 lg:grid-cols-2">
          <AnimatePresence mode="popLayout" initial={false}>
            {items.map((document, index) => (
              <motion.li
                key={document.id}
                layout={!reduced}
                initial={reduced ? false : { opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.97, transition: { duration: 0.15 } }}
                transition={{ delay: index * 0.035, duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
              >
                <DocumentCard document={document} />
              </motion.li>
            ))}
          </AnimatePresence>
        </motion.ul>
      )}

      {pages > 1 && (
        <nav aria-label="Seiten" className="flex items-center justify-between gap-3">
          <Button
            variant="outline"
            disabled={page <= 1}
            onClick={() => update({ page: page - 1 > 1 ? String(page - 1) : '' })}
          >
            <ChevronLeft aria-hidden /> Zurück
          </Button>
          <span className="tabular text-sm text-muted-foreground">
            Seite {page} von {pages}
          </span>
          <Button
            variant="outline"
            disabled={page >= pages}
            onClick={() => update({ page: String(page + 1) })}
          >
            Weiter <ChevronRight aria-hidden />
          </Button>
        </nav>
      )}
    </div>
  )
}
