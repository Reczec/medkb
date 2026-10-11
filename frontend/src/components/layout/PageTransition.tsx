import { AnimatePresence, motion, useReducedMotion } from 'motion/react'
import { Suspense } from 'react'
import { useLocation, useOutlet } from 'react-router'
import { PageSkeleton } from '@/components/layout/PageSkeleton'

/**
 * Fades route content in; with reduced motion only the opacity changes.
 *
 * Enter-only on purpose: with an exit animation (mode="wait") the next page waits for the old
 * one to finish leaving, and on slow machines that wait never ended after saving in the
 * editor, so the new page stayed blank. Without an exit the old page leaves at once.
 * `initial={false}` keeps the first page after load (and everything in it) unanimated.
 */
export function PageTransition() {
  const location = useLocation()
  const outlet = useOutlet()
  const reduced = useReducedMotion()

  return (
    <AnimatePresence initial={false}>
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: reduced ? 0 : 10 }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.28, ease: [0.16, 1, 0.3, 1] } }}
      >
        <Suspense fallback={<PageSkeleton />}>{outlet}</Suspense>
      </motion.div>
    </AnimatePresence>
  )
}
