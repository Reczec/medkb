import { motion, useReducedMotion } from 'motion/react'
import { Link } from 'react-router'
import { categoryStyle } from '@/lib/categories'
import type { CountItem } from '@/lib/types'
import { cn } from '@/lib/utils'

interface SpecialtyStripProps {
  items: CountItem[]
  /** Selected specialty (filter mode). */
  active?: string
  /** Filter mode: tabs are toggle buttons. Without it, tabs link to the filtered list. */
  onSelect?: (name: string) => void
  className?: string
}

/**
 * The signature element: specialties as colour-coded filing tabs whose widths follow the
 * number of entries. Only specialties with entries are shown.
 */
export function SpecialtyStrip({ items, active, onSelect, className }: SpecialtyStripProps) {
  const reduced = useReducedMotion()
  const filled = items.filter((item) => item.count > 0).sort((a, b) => b.count - a.count)
  const empty = items.length - filled.length

  return (
    <nav aria-label="Fachgebiete" className={className}>
      <ul className="flex gap-1.5 overflow-x-auto pb-1 [scrollbar-width:none] sm:flex-wrap sm:overflow-visible">
        {filled.map((item, index) => {
          const style = categoryStyle(item.name)
          const Icon = style.icon
          const selected = active === item.name
          const dimmed = active !== undefined && active !== '' && !selected
          const content = (
            <>
              <span
                className="absolute inset-x-0 top-0 h-1 rounded-t-[inherit] transition-[height] duration-300"
                style={{ background: style.color, height: selected ? 6 : undefined }}
                aria-hidden
              />
              <span className="flex items-center gap-2">
                <span
                  className="flex size-7 shrink-0 items-center justify-center rounded-md"
                  style={{ background: style.soft, color: style.color }}
                >
                  <Icon className="size-4" aria-hidden />
                </span>
                <span className="truncate text-sm font-medium">{item.name}</span>
              </span>
              <span className="tabular text-sm font-semibold text-muted-foreground">{item.count}</span>
            </>
          )
          const tabClass = cn(
            'relative flex h-12 w-full items-center justify-between gap-3 overflow-hidden rounded-t-lg rounded-b-md border bg-card px-3 pt-1 text-left shadow-sheet',
            'transition-[transform,box-shadow,opacity] duration-200 ease-out hover:-translate-y-0.5 hover:shadow-lift',
            'focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none',
            selected && '-translate-y-1 shadow-lift',
            dimmed && 'opacity-60 hover:opacity-100',
          )
          return (
            <motion.li
              key={item.name}
              className="min-w-[168px] shrink-0 sm:min-w-[150px] sm:shrink"
              style={{ flexGrow: item.count }}
              initial={reduced ? false : { opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.04, duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            >
              {onSelect ? (
                <button
                  type="button"
                  aria-pressed={selected}
                  className={tabClass}
                  onClick={() => onSelect(selected ? '' : item.name)}
                >
                  {content}
                </button>
              ) : (
                <Link
                  to={`/wissen?category=${encodeURIComponent(item.name)}`}
                  className={tabClass}
                >
                  {content}
                </Link>
              )}
            </motion.li>
          )
        })}
      </ul>
      {empty > 0 && (
        <p className="mt-2 text-xs text-muted-foreground">
          {empty === 1 ? '1 weiteres Fachgebiet' : `${empty} weitere Fachgebiete`} ohne Einträge
        </p>
      )}
    </nav>
  )
}
