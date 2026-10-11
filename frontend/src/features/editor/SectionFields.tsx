import { Textarea } from '@/components/ui/textarea'
import { SECTION_LABELS, SECTION_ORDER } from '@/lib/sections'
import type { Sections } from '@/lib/types'

export function SectionFields({ value, onChange }: { value: Sections; onChange: (value: Sections) => void }) {
  return (
    <div className="flex flex-col gap-5">
      {SECTION_ORDER.map((key) => (
        <div key={key} className="flex flex-col gap-1.5">
          <label htmlFor={`section-${key}`} className="text-sm font-medium">{SECTION_LABELS[key]}</label>
          <Textarea
            id={`section-${key}`}
            value={value[key] ?? ''}
            onChange={(event) => onChange({ ...value, [key]: event.target.value })}
            maxLength={5000}
            className="min-h-28 w-full min-w-0 text-base leading-relaxed [field-sizing:content] [overflow-wrap:anywhere]"
          />
        </div>
      ))}
    </div>
  )
}
