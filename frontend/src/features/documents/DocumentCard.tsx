import { ListChecks, UserPen } from 'lucide-react'
import { useId } from 'react'
import { Link } from 'react-router'
import { FileTab } from '@/components/specialty/FileTab'
import { formatDate, formatRelative } from '@/lib/format'
import type { Document } from '@/lib/types'

const VISIBLE_KEYWORDS = 5

/** A record sheet with its labelled specialty tab on top. */
export function DocumentCard({ document }: { document: Document }) {
  const extra = document.keywords.length - VISIBLE_KEYWORDS
  const titleId = useId()

  return (
    <Link
      to={`/wissen/${document.id}`}
      aria-labelledby={titleId}
      className="group flex h-full flex-col focus-visible:outline-none"
    >
      <FileTab
        name={document.category}
        className="relative z-10 ml-4 -mb-px self-start transition-transform duration-200 ease-out group-hover:-translate-y-1"
      />
      <article className="relative flex flex-1 flex-col gap-3 rounded-xl border bg-card p-5 shadow-sheet transition-[box-shadow,border-color] duration-200 ease-out group-hover:shadow-lift group-focus-visible:ring-2 group-focus-visible:ring-ring">
        <h2
          id={titleId}
          className="line-clamp-2 text-lg leading-snug font-semibold [overflow-wrap:anywhere]"
        >
          {document.title}
        </h2>
        <p className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-muted-foreground">
          <span className="font-medium text-foreground/80">{document.doc_type}</span>
          <span aria-hidden>·</span>
          <time dateTime={document.updated_at} title={formatDate(document.updated_at)}>
            geändert {formatRelative(document.updated_at)}
          </time>
          <span aria-hidden>·</span>
          {document.auto_classified ? (
            <span className="inline-flex items-center gap-1" title="Fachgebiet nach Regeln bestimmt">
              <ListChecks className="size-3.5" aria-hidden /> regelbasiert
            </span>
          ) : (
            <span className="inline-flex items-center gap-1" title="Fachgebiet manuell gesetzt">
              <UserPen className="size-3.5" aria-hidden /> manuell
            </span>
          )}
        </p>
        <p className="line-clamp-3 text-sm leading-relaxed [overflow-wrap:anywhere] text-muted-foreground">
          {document.content}
        </p>

        {document.keywords.length > 0 && (
          <ul className="mt-auto flex flex-wrap gap-1.5 pt-1" aria-label="Schlagwörter">
            {document.keywords.slice(0, VISIBLE_KEYWORDS).map((keyword) => (
              <li
                key={keyword}
                className="max-w-[12rem] truncate rounded-md bg-muted px-2 py-0.5 text-xs text-foreground/80"
              >
                {keyword}
              </li>
            ))}
            {extra > 0 && (
              <li className="rounded-md px-1.5 py-0.5 text-xs text-muted-foreground">+{extra}</li>
            )}
          </ul>
        )}
      </article>
    </Link>
  )
}
