import { ArrowUpRight } from 'lucide-react'
import { SourcePanel } from '@/features/documents/sources/SourcePanel'
import { useIcd11 } from '@/lib/queries'

export function Icd11Panel({ documentId, enabled }: { documentId: number; enabled: boolean }) {
  const query = useIcd11(documentId, enabled)
  return (
    <SourcePanel
      source="WHO ICD-11"
      shortName="ICD-11"
      query={query}
      emptyText="Für diesen Eintrag ist kein ICD-11-Code hinterlegt oder die WHO kennt ihn nicht."
      notConfiguredText="ICD-11 ist auf diesem Server nicht eingerichtet (WHO-API-Zugang fehlt)."
    >
      {(entry) => (
        <div className="flex flex-col gap-3">
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <span className="rounded-md bg-muted px-2 py-0.5 font-mono text-lg font-semibold tracking-tight">
              {entry.code}
            </span>
            <span className="text-lg font-semibold [overflow-wrap:anywhere]">{entry.title}</span>
          </div>
          {entry.definition && (
            <p className="max-w-[68ch] text-[17px] leading-relaxed">{entry.definition}</p>
          )}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
            <a
              href={entry.url}
              target="_blank"
              rel="noreferrer noopener"
              className="inline-flex items-center gap-1 font-medium text-primary underline-offset-4 hover:underline"
            >
              Im ICD-11-Browser öffnen <ArrowUpRight className="size-4" aria-hidden />
            </a>
            <span className="text-xs text-muted-foreground">
              Version <span className="tabular">{entry.release}</span>
              {entry.language === 'de' && ' · Deutsche Fassung: WHO-Prerelease'}
            </span>
          </div>
        </div>
      )}
    </SourcePanel>
  )
}
