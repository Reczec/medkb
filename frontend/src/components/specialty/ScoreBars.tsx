import { motion, useReducedMotion } from 'motion/react'
import { categoryStyle } from '@/lib/categories'
import { toScoreBars } from '@/lib/scores'
import { cn } from '@/lib/utils'

interface ScoreBarsProps {
  scores: Record<string, number>
  /** Highlighted category (the classifier's choice). */
  winner?: string
  max?: number
  className?: string
}

/** Classifier scores as bars in specialty colours; widths animate when the scores change. */
export function ScoreBars({ scores, winner, max = 5, className }: ScoreBarsProps) {
  const reduced = useReducedMotion()
  const bars = toScoreBars(scores, max)

  if (bars.length === 0) {
    return (
      <p className={cn('text-sm text-muted-foreground', className)}>
        Noch keine Fachbegriffe erkannt.
      </p>
    )
  }

  return (
    <ul className={cn('flex flex-col gap-2.5', className)}>
      {bars.map((bar) => {
        const style = categoryStyle(bar.name)
        const isWinner = bar.name === winner
        return (
          <motion.li
            key={bar.name}
            layout={!reduced}
            transition={{ type: 'spring', stiffness: 380, damping: 34 }}
          >
            <div className="flex items-baseline justify-between gap-2 text-sm">
              <span className={cn('truncate', isWinner ? 'font-semibold' : 'text-muted-foreground')}>
                {bar.name}
              </span>
              <span className="tabular shrink-0 text-xs text-muted-foreground">{bar.score}</span>
            </div>
            <div className="mt-1 h-2 overflow-hidden rounded-full bg-muted">
              <motion.div
                className="h-full rounded-full"
                style={{ background: style.color, opacity: isWinner || !winner ? 1 : 0.45 }}
                initial={reduced ? false : { width: 0 }}
                animate={{ width: `${Math.max(bar.share * 100, 4)}%` }}
                transition={{ duration: reduced ? 0 : 0.55, ease: [0.16, 1, 0.3, 1] }}
              />
            </div>
          </motion.li>
        )
      })}
    </ul>
  )
}
