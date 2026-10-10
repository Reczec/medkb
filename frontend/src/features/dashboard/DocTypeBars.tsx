import { motion, useReducedMotion } from 'motion/react'
import { Link } from 'react-router'
import type { CountItem } from '@/lib/types'

export function DocTypeBars({ items }: { items: CountItem[] }) {
  const reduced = useReducedMotion()
  const max = Math.max(1, ...items.map((item) => item.count))

  return (
    <section className="rounded-xl border bg-card p-5 shadow-sheet">
      <h2 className="text-base font-semibold">Nach Dokumenttyp</h2>
      <ul className="mt-4 flex flex-col gap-3">
        {items.map((item, index) => (
          <li key={item.name}>
            <Link
              to={`/wissen?type=${encodeURIComponent(item.name)}`}
              className="group block rounded-md focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none"
            >
              <div className="flex items-baseline justify-between text-sm">
                <span className="text-foreground/90 group-hover:text-foreground">{item.name}</span>
                <span className="tabular font-medium text-muted-foreground">{item.count}</span>
              </div>
              <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-muted">
                <motion.div
                  className="h-full rounded-full bg-primary/80 group-hover:bg-primary"
                  initial={reduced ? false : { width: 0 }}
                  animate={{ width: `${(item.count / max) * 100}%` }}
                  transition={{ delay: 0.15 + index * 0.05, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
