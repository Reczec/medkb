import { ListChecks, UserPen } from 'lucide-react'
import { ScoreBars } from '@/components/specialty/ScoreBars'
import { Skeleton } from '@/components/ui/skeleton'
import { useI18n } from '@/i18n/context'
import { useClassify } from '@/lib/queries'
import type { Document } from '@/lib/types'

/** Re-runs the rule-based classifier on the entry and shows why it lands where it does. */
export function ClassificationExplainer({ document }: { document: Document }) {
  const { data, isPending, error } = useClassify(document.title, document.content)
  const { t, lang, categoryLabel } = useI18n()
  const disagrees = data && data.category !== document.category

  return (
    <section aria-label={t('cls.title')} className="rounded-xl border bg-card p-5 shadow-sheet">
      <h2 className="text-base font-semibold">{t('cls.title')}</h2>
      <p className="mt-1 flex items-center gap-1.5 text-sm text-muted-foreground">
        {document.auto_classified ? (
          <>
            <ListChecks className="size-3.5" aria-hidden /> {t('cls.byRules')}
          </>
        ) : (
          <>
            <UserPen className="size-3.5" aria-hidden /> {t('cls.manual')}
          </>
        )}
      </p>

      {isPending && (
        <div className="mt-4 flex flex-col gap-3">
          <Skeleton className="h-6" />
          <Skeleton className="h-6 w-4/5" />
          <Skeleton className="h-6 w-3/5" />
        </div>
      )}
      {error && (
        <p className="mt-4 text-sm text-destructive">{t('cls.unavailable')}</p>
      )}

      {data && (
        <>
          <ScoreBars scores={data.scores} winner={data.category} className="mt-4" />
          {disagrees && (
            <p className="mt-3 rounded-lg bg-muted px-3 py-2 text-sm">
              {t('cls.disagreeBefore')}
              <strong>{categoryLabel(data.category)}</strong>
              {t('cls.disagreeAfter')}
            </p>
          )}
          {data.fallback && (
            <p className="mt-3 text-sm text-muted-foreground">
              {t('cls.fallback', { category: categoryLabel(data.category) })}
            </p>
          )}
          {data.matched_terms.length > 0 && (
            <div className="mt-4">
              <h3 className="text-xs font-medium text-muted-foreground">{t('cls.terms')}</h3>
              <ul className="mt-2 flex flex-wrap gap-1.5">
                {data.matched_terms.map((term) => (
                  <li
                    key={term}
                    className="max-w-full rounded-md border border-dashed px-2 py-0.5 font-mono text-xs break-all"
                  >
                    {term}
                  </li>
                ))}
              </ul>
              {lang === 'en' && (
                <p className="mt-2 text-xs text-muted-foreground">{t('cls.germanNote')}</p>
              )}
            </div>
          )}
        </>
      )}
    </section>
  )
}
