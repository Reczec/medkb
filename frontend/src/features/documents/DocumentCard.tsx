import { Sparkles } from 'lucide-react'
import { useId } from 'react'
import { Link } from 'react-router'
import { CategoryBadge } from '@/components/specialty/CategoryBadge'
import { categoryStyle } from '@/lib/categories'
import { formatDate, formatRelative } from '@/lib/format'
import type { Document } from '@/lib/types'

const VISIBLE_KEYWORDS = 5

/** A record sheet with a coloured filing tab sticking out above it. */
export function DocumentCard({ document }: { document: Document }) {
  const style = categoryStyle(document.category)
  const extra = document.keywords.length - VISIBLE_KEYWORDS
  const titleId = useId()

  return (
    <Link
      to={`/wissen/${document.id}`}
      aria-labelledby={titleId}
      className="group relative block h-full pt-2.5 focus-visible:outline-none"
    >
      <span
        className="absolute top-0 left-5 h-3.5 w-16 rounded-t-md transition-[width] duration-300 ease-out group-hover:w-24"
        style={{ background: style.color }}
        aria-hidden
      />
      <article className="relative flex h-full flex-col gap-3 rounded-xl border bg-card p-5 shadow-sheet transition-[transform,box-shadow,border-color] duration-200 ease-out group-hover:-translate-y-0.5 group-hover:shadow-lift group-focus-visible:ring-2 group-focus-visible:ring-ring">
        <div className="flex flex-wrap items-center gap-2">
          <CategoryBadge name={document.category} />
          <span className="text-xs text-muted-foreground">{document.doc_type}</span>
          {document.auto_classified && (
            <span
              className="ml-auto inline-flex items-center gap-1 text-xs text-muted-foreground"
              title="Fachgebiet automatisch bestimmt"
            >
              <Sparkles className="size-3.5" aria-hidden />
              <span className="sr-only">automatisch klassifiziert</span>
            </span>
          )}
        </div>

        <h2 id={titleId} className="line-clamp-2 text-lg leading-snug font-semibold break-words">
          {document.title}
        </h2>
        <p className="line-clamp-3 text-sm leading-relaxed break-words text-muted-foreground">
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

        <time
          dateTime={document.updated_at}
          title={formatDate(document.updated_at)}
          className="text-xs text-muted-foreground"
        >
          Geändert {formatRelative(document.updated_at)}
        </time>
      </article>
    </Link>
  )
}
