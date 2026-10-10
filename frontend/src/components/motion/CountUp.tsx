import { animate, useReducedMotion } from 'motion/react'
import { useEffect, useState } from 'react'
import { formatNumber } from '@/lib/format'

interface CountUpProps {
  value: number
  suffix?: string
  duration?: number
}

/** Counts from 0 to `value` on mount (jumps straight there with reduced motion). */
export function CountUp({ value, suffix = '', duration = 0.9 }: CountUpProps) {
  const reduced = useReducedMotion()
  const [animated, setAnimated] = useState(0)

  useEffect(() => {
    if (reduced) return
    const controls = animate(0, value, {
      duration,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (latest) => setAnimated(Math.round(latest)),
    })
    return () => controls.stop()
  }, [value, reduced, duration])

  return (
    <span className="tabular">
      {formatNumber(reduced ? value : animated)}
      {suffix}
    </span>
  )
}
