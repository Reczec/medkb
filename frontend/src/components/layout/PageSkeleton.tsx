import { Skeleton } from '@/components/ui/skeleton'

/** Shown for the moment a page's code is still loading. */
export function PageSkeleton() {
  return (
    <div aria-busy="true" aria-label="Seite wird geladen" className="flex flex-col gap-6">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-5 w-full max-w-xl" />
      <Skeleton className="h-72 rounded-xl" />
    </div>
  )
}
