import { AnimatePresence, motion, useReducedMotion } from 'motion/react'
import { useLocation, useOutlet } from 'react-router'

/** Cross-fades route content; with reduced motion only the opacity changes. */
export function PageTransition() {
  const location = useLocation()
  const outlet = useOutlet()
  const reduced = useReducedMotion()
  const offset = reduced ? 0 : 10

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: offset }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.28, ease: [0.16, 1, 0.3, 1] } }}
        exit={{ opacity: 0, y: -offset / 2, transition: { duration: 0.14, ease: 'easeIn' } }}
      >
        {outlet}
      </motion.div>
    </AnimatePresence>
  )
}
