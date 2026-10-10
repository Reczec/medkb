import { ChevronDown, Info, Pill } from 'lucide-react'
import { SourcePanel } from '@/features/documents/sources/SourcePanel'
import { useMedications } from '@/lib/queries'
import type { MedicationLabel } from '@/lib/types'

const FIELDS: [keyof MedicationLabel, string][] = [
  ['indications', 'Anwendungsgebiet'],
  ['warnings', 'Warnhinweise'],
  ['adverse_reactions', 'Nebenwirkungen'],
]

function LabelCard({ label, open }: { label: MedicationLabel; open: boolean }) {
  return (
    <details open={open} className="group rounded-xl border bg-card">
      <summary className="flex cursor-pointer list-none items-center gap-3 rounded-xl px-4 py-3 hover:bg-accent/50 [&::-webkit-details-marker]:hidden">
        <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
          <Pill className="size-4" aria-hidden />
        </span>
        <span className="min-w-0 flex-1">
          <span className="block font-medium">{label.ingredient}</span>
          {label.brand_names.length > 0 && (
            <span className="block truncate text-xs text-muted-foreground">
              z. B. {label.brand_names.join(', ')}
            </span>
          )}
        </span>
        <ChevronDown
          className="size-4 shrink-0 text-muted-foreground transition-transform duration-200 group-open:rotate-180"
          aria-hidden
        />
      </summary>
      <dl className="flex flex-col gap-3 border-t px-4 py-3.5 text-sm">
        {FIELDS.map(([key, title]) => {
          const text = label[key]
          if (!text || typeof text !== 'string') return null
          return (
            <div key={key}>
              <dt className="text-xs font-medium text-muted-foreground">{title}</dt>
              <dd lang="en" className="mt-0.5 leading-relaxed [overflow-wrap:anywhere]">
                {text}
              </dd>
            </div>
          )
        })}
      </dl>
    </details>
  )
}

export function MedicationsPanel({ documentId, enabled }: { documentId: number; enabled: boolean }) {
  const query = useMedications(documentId, enabled)
  return (
    <SourcePanel
      source="openFDA · U.S. Food and Drug Administration"
      shortName="openFDA"
      query={query}
      emptyText="Für diesen Eintrag sind keine Wirkstoffe hinterlegt."
    >
      {(data) => (
        <div className="flex flex-col gap-3">
          <p className="flex items-start gap-2 rounded-lg bg-muted/70 px-3 py-2 text-xs text-muted-foreground">
            <Info className="mt-px size-3.5 shrink-0" aria-hidden />
            US-FDA-Produktinformation, englisch und gekürzt – nicht für Dosierungs- oder
            Therapieentscheidungen.
          </p>
          {data.found.map((label, index) => (
            <LabelCard key={label.ingredient} label={label} open={index === 0} />
          ))}
          {data.missing.length > 0 && (
            <p className="text-sm text-muted-foreground">
              Kein FDA-Label gefunden für: {data.missing.join(', ')}
            </p>
          )}
        </div>
      )}
    </SourcePanel>
  )
}
