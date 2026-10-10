import { motion, useReducedMotion } from 'motion/react'
import { Link } from 'react-router'
import { categoryStyle } from '@/lib/categories'
import type { CountItem } from '@/lib/types'
import { cn } from '@/lib/utils'

interface SpecialtyStripProps {
  items: CountItem[]
  /** The captioned share bar under the tabs (off where no statistics belong). */
  showShare?: boolean
  /** Selected specialty (filter mode). */
  active?: string
  /** Filter mode: tabs are toggle buttons. Without it, tabs link to the filtered list. */
  onSelect?: (name: string) => void
  className?: string
}

/**
 * The signature element: specialties as labelled filing tabs standing on one neutral drawer
 * edge, each tab showing its full name. A separate, captioned bar below shows each specialty's
 * share of the entries, so proportion never costs legibility. On narrow screens the tabs scroll.
 */
export function SpecialtyStrip({
  items,
  active,
  onSelect,
  className,
  showShare = true,
}: SpecialtyStripProps) {
  const reduced = useReducedMotion()
  const filled = items.filter((item) => item.count > 0).sort((a, b) => b.count - a.count)
  const empty = items.length - filled.length
  const filtering = Boolean(active)

  return (
    <nav aria-label="Fachgebiete" className={className}>
      <ul className="flex items-end gap-1 overflow-x-auto border-b-2 px-1 pt-2">
        {filled.map((item, index) => {
          const style = categoryStyle(item.name)
          const selected = active === item.name
          const dimmed = filtering && !selected
          const content = (
            <>
              <span
                className="absolute inset-x-0 top-0 transition-[height,opacity] duration-300"
                style={{ background: style.color, height: selected ? 5 : 3, opacity: dimmed ? 0.35 : 1 }}
                aria-hidden
              />
              <span data-tab-label className="text-[13px] font-medium whitespace-nowrap">
                {item.name}
              </span>
              <span className="tabular text-[13px] font-semibold text-muted-foreground">
                {item.count}
              </span>
            </>
          )
          const tabClass = cn(
            'relative -mb-0.5 flex items-center gap-2 overflow-hidden rounded-t-lg border border-b-0 px-3 pt-0.5 whitespace-nowrap',
            'transition-[height,background-color,box-shadow] duration-200 ease-out',
            'focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none focus-visible:ring-inset',
            selected
              ? 'z-10 h-12 shadow-[0_-6px_16px_-10px_oklch(0.3_0.03_220/0.35)]'
              : 'h-10 bg-card hover:h-11 hover:bg-accent/60',
          )
          const tabStyle = selected
            ? { background: `color-mix(in oklab, ${style.color} 14%, var(--background))` }
            : undefined
          return (
            <motion.li
              key={item.name}
              className="shrink-0"
              initial={reduced ? false : { opacity: 0, y: 10 }}
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

      {showShare && (
      <div className="mt-4 flex items-center gap-3">
        <span className="shrink-0 text-xs text-muted-foreground">Anteil der Einträge</span>
        <div className="flex h-2 flex-1 gap-0.5 overflow-hidden rounded-full" aria-hidden>
        {filled.map((item, index) => {
          const style = categoryStyle(item.name)
          const dimmed = filtering && active !== item.name
          return (
            <motion.span
              key={item.name}
              data-share={item.name}
              title={`${item.name}: ${item.count}`}
              className="h-full min-w-1 transition-opacity duration-300"
              style={{ flexGrow: item.count, flexBasis: 0, background: style.color, opacity: dimmed ? 0.3 : 1 }}
              initial={reduced ? false : { scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ delay: 0.15 + index * 0.04, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            />
          )
        })}
        </div>
      </div>
      )}

      {empty > 0 && (
        <p className="mt-2 text-xs text-muted-foreground">
          {empty === 1 ? '1 weiteres Fachgebiet' : `${empty} weitere Fachgebiete`} ohne Einträge
        </p>
      )}
    </nav>
  )
}
