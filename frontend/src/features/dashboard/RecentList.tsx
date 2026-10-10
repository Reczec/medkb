import { ArrowRight } from 'lucide-react'
import { Link } from 'react-router'
import { categoryStyle } from '@/lib/categories'
import { formatDate, formatRelative } from '@/lib/format'
import type { RecentItem } from '@/lib/types'

export function RecentList({ items }: { items: RecentItem[] }) {
  return (
    <section className="rounded-xl border bg-card shadow-sheet">
      <div className="flex items-center justify-between px-5 pt-5 pb-3">
        <h2 className="text-base font-semibold">Zuletzt bearbeitet</h2>
        <Link
          to="/wissen"
          className="inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline"
        >
          Alle Einträge <ArrowRight className="size-3.5" aria-hidden />
        </Link>
      </div>
      {items.length === 0 ? (
        <p className="px-5 pb-5 text-sm text-muted-foreground">Noch keine Einträge.</p>
      ) : (
        <ul className="divide-y">
          {items.map((item) => {
            const style = categoryStyle(item.category)
            const Icon = style.icon
            return (
              <li key={item.id}>
                <Link
                  to={`/wissen/${item.id}`}
                  className="group flex items-center gap-3 px-5 py-3 transition-colors hover:bg-muted/60 focus-visible:bg-muted/60 focus-visible:outline-none"
                >
                  <span
                    className="flex size-9 shrink-0 items-center justify-center rounded-lg"
                    style={{ background: style.soft, color: style.color }}
                  >
                    <Icon className="size-[18px]" aria-hidden />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">{item.title}</span>
                    <span className="block text-xs text-muted-foreground">{item.category}</span>
                  </span>
                  <time
                    dateTime={item.updated_at}
                    title={formatDate(item.updated_at)}
                    className="shrink-0 text-xs text-muted-foreground"
                  >
                    {formatRelative(item.updated_at)}
                  </time>
                  <ArrowRight
                    className="size-4 shrink-0 -translate-x-1 text-muted-foreground opacity-0 transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                    aria-hidden
                  />
                </Link>
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}
