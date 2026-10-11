import { Textarea } from '@/components/ui/textarea'
import { useI18n } from '@/i18n/context'
import { SECTION_ORDER } from '@/lib/sections'
import type { Sections } from '@/lib/types'

interface SectionFieldsProps {
  value: Sections
  onChange: (value: Sections) => void
  /** Element id prefix; the English version uses its own so both sets can be open. */
  idPrefix?: string
  /** Appended to every label, e.g. " (English)". */
  labelSuffix?: string
}

export function SectionFields({ value, onChange, idPrefix = 'section', labelSuffix = '' }: SectionFieldsProps) {
  const { t } = useI18n()
  return (
    <div className="flex flex-col gap-5">
      {SECTION_ORDER.map((key) => (
        <div key={key} className="flex flex-col gap-1.5">
          <label htmlFor={`${idPrefix}-${key}`} className="text-sm font-medium">
            {t(`section.${key}`)}
            {labelSuffix}
          </label>
          <Textarea
            id={`${idPrefix}-${key}`}
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
