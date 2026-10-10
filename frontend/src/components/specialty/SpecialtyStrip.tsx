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
 * The signature element: specialties as labelled filing tabs rising from one drawer edge.
 * Each tab's width is its share of the entries; narrow tabs keep icon and count and show the
 * name as a tooltip. On phones the drawer scrolls sideways.
 */
export function SpecialtyStrip({ items, active, onSelect, className }: SpecialtyStripProps) {
  const reduced = useReducedMotion()
  const filled = items.filter((item) => item.count > 0).sort((a, b) => b.count - a.count)
  const empty = items.length - filled.length
  const filtering = Boolean(active)

  return (
    <nav aria-label="Fachgebiete" className={className}>
      <ul className="flex items-end gap-1 overflow-x-auto border-b-2 px-1 pt-2 [scrollbar-width:none] sm:overflow-visible">
        {filled.map((item, index) => {
          const style = categoryStyle(item.name)
          const Icon = style.icon
          const selected = active === item.name
          const dimmed = filtering && !selected
          const content = (
            <>
              <span
                className="absolute inset-x-0 top-0 transition-[height,opacity] duration-300"
                style={{ background: style.color, height: selected ? 5 : 3, opacity: dimmed ? 0.35 : 1 }}
                aria-hidden
              />
              <span className="flex min-w-0 items-center gap-2">
                <span
                  className="flex size-7 shrink-0 items-center justify-center rounded-md transition-opacity duration-300"
                  style={{ background: style.soft, color: style.color, opacity: dimmed ? 0.5 : 1 }}
                >
                  <Icon className="size-4" aria-hidden />
                </span>
                <span className="truncate text-sm font-medium @max-[118px]:sr-only">{item.name}</span>
              </span>
              <span className="tabular text-sm font-semibold text-muted-foreground">{item.count}</span>
            </>
          )
          const tabClass = cn(
            'relative -mb-0.5 flex w-full items-center justify-between gap-2 overflow-hidden rounded-t-xl border border-b-0 px-2.5 pt-1 text-left',
            'transition-[height,background-color,box-shadow] duration-200 ease-out',
            'focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none focus-visible:ring-inset',
            selected
              ? 'z-10 h-14 shadow-[0_-6px_16px_-10px_oklch(0.3_0.03_220/0.35)]'
              : 'h-12 bg-card hover:h-[52px] hover:bg-accent/60',
          )
          const tabStyle = selected
            ? { background: `color-mix(in oklch, ${style.color} 14%, var(--background))` }
            : undefined
          return (
            <motion.li
              key={item.name}
              className="@container min-w-[132px] shrink-0 sm:min-w-[56px] sm:shrink"
              style={{ flexGrow: item.count, flexBasis: 0 }}
              title={item.name}
              initial={reduced ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.04, duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            >
              {onSelect ? (
                <button
                  type="button"
                  aria-pressed={selected}
                  className={tabClass}
                  style={tabStyle}
                  onClick={() => onSelect(selected ? '' : item.name)}
                >
                  {content}
                </button>
              ) : (
                <Link
                  to={`/wissen?category=${encodeURIComponent(item.name)}`}
                  className={tabClass}
                  style={tabStyle}
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
