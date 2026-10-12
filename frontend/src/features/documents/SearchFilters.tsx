import { Search, X } from 'lucide-react'
import { SpecialtyStrip } from '@/components/specialty/SpecialtyStrip'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useI18n } from '@/i18n/context'
import type { CountItem } from '@/lib/types'

const ALL = '__all__'

interface SearchFiltersProps {
  query: string
  onQueryChange: (value: string) => void
  category: string
  onCategoryChange: (value: string) => void
  docType: string
  onDocTypeChange: (value: string) => void
  docTypes: string[]
  specialties: CountItem[]
}

export function SearchFilters(props: SearchFiltersProps) {
  const { t, categoryLabel, docTypeLabel } = useI18n()
  const active = [
    props.category && {
      label: categoryLabel(props.category),
      clear: () => props.onCategoryChange(''),
    },
    props.docType && { label: docTypeLabel(props.docType), clear: () => props.onDocTypeChange('') },
  ].filter(Boolean) as { label: string; clear: () => void }[]

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-3 sm:flex-row">
        <label className="relative flex-1">
          <span className="sr-only">{t('filters.terms')}</span>
          <Search
            className="pointer-events-none absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-muted-foreground"
            aria-hidden
          />
          <Input
            type="search"
            value={props.query}
            onChange={(event) => props.onQueryChange(event.target.value)}
            placeholder={t('filters.placeholder')}
            className="h-11 bg-card pl-10 text-base shadow-sheet"
            maxLength={200}
          />
        </label>
        <Select
          value={props.docType || ALL}
          onValueChange={(value) => props.onDocTypeChange(value === ALL ? '' : value)}
        >
          <SelectTrigger className="h-11! w-full bg-card shadow-sheet sm:w-52" aria-label={t('filters.docType')}>
            <SelectValue />
          </SelectTrigger>
          <SelectContent position="popper" align="end">
            <SelectItem value={ALL}>{t('filters.allTypes')}</SelectItem>
            {props.docTypes.map((type) => (
              <SelectItem key={type} value={type}>
                {docTypeLabel(type)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <SpecialtyStrip
        items={props.specialties}
        active={props.category}
        onSelect={props.onCategoryChange}
      />

      {active.length > 0 && (
        <ul aria-label={t('filters.active')} className="flex flex-wrap items-center gap-2">
          {active.map((filter) => (
            <li key={filter.label}>
              <button
                type="button"
                onClick={filter.clear}
                aria-label={t('filters.remove', { name: filter.label })}
                className="inline-flex h-7 items-center gap-1.5 rounded-full border bg-card pr-2 pl-3 text-sm transition-colors hover:border-destructive/40 hover:text-destructive"
              >
                {filter.label}
                <X className="size-3.5" aria-hidden />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
