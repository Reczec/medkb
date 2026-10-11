import { ArrowUpRight } from 'lucide-react'
import { StudyAI } from '@/features/ai/StudyAI'
import { SourcePanel } from '@/features/documents/sources/SourcePanel'
import { useI18n } from '@/i18n/context'
import { useStudies } from '@/lib/queries'
import type { Study } from '@/lib/types'

export function authorLine(study: Pick<Study, 'authors' | 'more_authors'>): string {
  const names = study.authors.join(', ')
  return study.more_authors ? `${names} et al.` : names
}

/** One study as a list row; shared with the dashboard tile. */
export function StudyItem({ study }: { study: Study }) {
  const { t } = useI18n()
  return (
    <li>
      <a
        href={study.url}
        target="_blank"
        rel="noreferrer noopener"
        className="group -mx-3 flex items-start gap-3 rounded-lg px-3 py-2.5 transition-colors hover:bg-accent/60"
      >
        <span className="min-w-0 flex-1">
          <span className="block font-medium leading-snug [overflow-wrap:anywhere] group-hover:text-primary">
            {study.title}
          </span>
          <span className="mt-1 flex flex-wrap gap-x-2 text-xs text-muted-foreground">
            {study.journal && <span>{study.journal}</span>}
            {study.journal && study.year && <span aria-hidden>·</span>}
            {study.year && <span className="tabular">{study.year}</span>}
          </span>
          {study.authors.length > 0 && (
            <span className="mt-0.5 block text-xs text-muted-foreground">{authorLine(study)}</span>
          )}
          <span className="sr-only">{t('studies.opens')}</span>
        </span>
        <ArrowUpRight
          className="mt-0.5 size-4 shrink-0 text-muted-foreground transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-primary"
          aria-hidden
        />
      </a>
      <StudyAI pmid={study.pmid} />
    </li>
  )
}

export function StudiesPanel({
  documentId,
  termEn,
  enabled,
}: {
  documentId: number
  termEn: string | null
  enabled: boolean
}) {
  const query = useStudies(documentId, enabled)
  const { t } = useI18n()
  return (
    <SourcePanel
      source="PubMed · NCBI"
      shortName="PubMed"
      query={query}
      caption={termEn ? t('studies.caption', { term: termEn }) : undefined}
      emptyText={termEn ? t('studies.empty') : t('studies.noTerm')}
    >
      {(studies) => (
        <ul className="flex flex-col gap-0.5">
          {studies.map((study) => (
            <StudyItem key={study.pmid} study={study} />
          ))}
        </ul>
      )}
    </SourcePanel>
  )
}
