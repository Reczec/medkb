import { Phone, TriangleAlert } from 'lucide-react'
import { useId } from 'react'
import { SECTION_LABELS, SECTION_ORDER } from '@/lib/sections'
import type { Sections } from '@/lib/types'

const EMERGENCY = /\b144\b/

function WarningSigns({ text }: { text: string }) {
  const id = useId()
  return (
    <section
      aria-labelledby={id}
      className="rounded-xl border border-destructive/25 bg-destructive/[0.06] px-5 py-4"
    >
      <h2 id={id} className="flex items-center gap-2 text-base font-semibold">
        <TriangleAlert className="size-[18px] shrink-0 text-destructive" aria-hidden />
        {SECTION_LABELS.red_flags}
      </h2>
      <p className="mt-1.5 whitespace-pre-line [overflow-wrap:anywhere]">{text}</p>
      {EMERGENCY.test(text) && (
        <p className="mt-3 inline-flex items-center gap-2 rounded-lg bg-destructive/10 px-2.5 py-1 text-sm font-semibold text-destructive">
          <Phone className="size-3.5" aria-hidden />
          Im Notfall: 144
        </p>
      )}
    </section>
  )
}

/** A structured entry on its reading sheet: fixed section order, warning signs set apart last. */
export function SectionedContent({ sections }: { sections: Sections }) {
  const text = (key: keyof Sections) => sections[key]?.trim() || null
  const body = SECTION_ORDER.filter((key) => key !== 'red_flags' && text(key))
  const redFlags = text('red_flags')

  return (
    <div className="flex max-w-[68ch] flex-col gap-6 text-[17px] leading-relaxed">
      {body.map((key) => (
        <section key={key}>
          <h2 className="text-base font-semibold">{SECTION_LABELS[key]}</h2>
          <p className="mt-1 whitespace-pre-line [overflow-wrap:anywhere]">{text(key)}</p>
        </section>
      ))}
      {redFlags && <WarningSigns text={redFlags} />}
    </div>
  )
}
