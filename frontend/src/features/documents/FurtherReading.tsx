import { ArrowUpRight } from 'lucide-react'
import { useId } from 'react'
import { useI18n } from '@/i18n/context'
import { linkLabel } from '@/i18n/localized'
import type { FurtherReadingLink } from '@/lib/types'

function host(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, '')
  } catch {
    return url
  }
}

/** Checked links to public health portals (gesundheit.gv.at, WHO, NIH MedlinePlus). */
export function FurtherReading({ links }: { links: FurtherReadingLink[] }) {
  const id = useId()
  const { t, lang } = useI18n()
  if (links.length === 0) return null
  return (
    <section aria-labelledby={id} className="rounded-xl border bg-card p-5 shadow-sheet">
      <h2 id={id} className="text-base font-semibold">
        {t('reading.title')}
      </h2>
      <ul className="mt-3 flex flex-col gap-1">
        {links.map((link) => (
          <li key={link.url}>
            <a
              href={link.url}
              target="_blank"
              rel="noreferrer noopener"
              className="group -mx-2 flex items-start gap-2 rounded-lg px-2 py-1.5 transition-colors hover:bg-accent/60"
            >
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-medium [overflow-wrap:anywhere] group-hover:text-primary">
                  {linkLabel(link, lang)}
                </span>
                <span className="block text-xs text-muted-foreground">{host(link.url)}</span>
                <span className="sr-only">{t('reading.newTab')}</span>
              </span>
              <ArrowUpRight
                className="mt-0.5 size-4 shrink-0 text-muted-foreground transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-primary"
                aria-hidden
              />
            </a>
          </li>
        ))}
      </ul>
    </section>
  )
}
