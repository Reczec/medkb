import { ArrowRight } from 'lucide-react'
import { Link } from 'react-router'
import { FileTab } from '@/components/specialty/FileTab'
import { useI18n } from '@/i18n/context'
import { formatDate, formatRelative } from '@/lib/format'
import type { RecentItem } from '@/lib/types'

/** The last edited entries as a row of filed sheets, each under its specialty tab. */
interface RecentListProps {
  items: RecentItem[]
  title?: string
  /** Editorial "changed …" stamps; off for patients. */
  showTimes?: boolean
}

export function RecentList({ items, title, showTimes = true }: RecentListProps) {
  const { t, lang } = useI18n()
  return (
    <section className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold">{title ?? t('recent.title')}</h2>
        <Link
          to="/wissen"
          className="inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline"
        >
          {t('recent.all')} <ArrowRight className="size-3.5" aria-hidden />
        </Link>
      </div>
      {items.length === 0 ? (
        <p className="text-sm text-muted-foreground">{t('recent.empty')}</p>
      ) : (
        <ul className="grid grid-cols-1 gap-x-4 gap-y-5 sm:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => (
            <li key={item.id} className="min-w-0">
              <Link
                to={`/wissen/${item.id}`}
                className="group flex h-full flex-col focus-visible:outline-none"
              >
                <FileTab
                  name={item.category}
                  className="relative z-10 ml-3 -mb-px self-start transition-transform duration-200 ease-out group-hover:-translate-y-1"
                />
                <span className="flex flex-1 flex-col justify-between gap-3 rounded-xl border bg-card p-4 shadow-sheet transition-shadow duration-200 group-hover:shadow-lift group-focus-visible:ring-2 group-focus-visible:ring-ring">
                  <span className="line-clamp-2 font-medium [overflow-wrap:anywhere]">{(lang === 'en' && item.title_en) || item.title}</span>
                  {showTimes && (
                    <time
                      dateTime={item.updated_at}
                      title={formatDate(item.updated_at, lang)}
                      className="text-xs text-muted-foreground"
                    >
                      {t('card.changed', { time: formatRelative(item.updated_at, lang) })}
                    </time>
                  )}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
