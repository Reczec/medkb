import { ListChecks } from 'lucide-react'
import { categoryStyle } from '@/lib/categories'
import { cn } from '@/lib/utils'

export const AUTO = 'auto'

interface CategoryPickerProps {
  categories: string[]
  /** AUTO or a category name. */
  value: string
  onChange: (value: string) => void
  suggestion?: string
}

/** Radio group of specialty chips; the first option keeps the classifier in charge. */
export function CategoryPicker({ categories, value, onChange, suggestion }: CategoryPickerProps) {
  const chip =
    'inline-flex h-9 items-center gap-2 rounded-lg border bg-card px-3 text-sm transition-[background-color,border-color,box-shadow] duration-150 focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none'

  return (
    <div role="radiogroup" aria-labelledby="category-label" className="flex flex-wrap gap-2">
      <button
        type="button"
        role="radio"
        aria-checked={value === AUTO}
        onClick={() => onChange(AUTO)}
        className={cn(
          chip,
          value === AUTO
            ? 'border-primary bg-accent font-medium text-accent-foreground shadow-sheet'
            : 'hover:bg-muted',
        )}
      >
        <ListChecks className="size-4 text-primary" aria-hidden />
        Automatisch
        {suggestion && <span className="text-muted-foreground">· Vorschlag: {suggestion}</span>}
      </button>
      {categories.map((name) => {
        const style = categoryStyle(name)
        const selected = value === name
        return (
          <button
            key={name}
            type="button"
            role="radio"
            aria-checked={selected}
            onClick={() => onChange(name)}
            className={cn(chip, selected ? 'font-medium shadow-sheet' : 'hover:bg-muted')}
            style={selected ? { borderColor: style.color, background: style.soft } : undefined}
          >
            <span className="size-2 rounded-full" style={{ background: style.color }} aria-hidden />
            {name}
          </button>
        )
      })}
    </div>
  )
}
