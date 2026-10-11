import { Skeleton } from '@/components/ui/skeleton'
import { useI18n } from '@/i18n/context'

/** Shown for the moment a page's code is still loading. */
export function PageSkeleton() {
  const { t } = useI18n()
  return (
    <div aria-busy="true" aria-label={t('page.loading')} className="flex flex-col gap-6">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-5 w-full max-w-xl" />
      <Skeleton className="h-72 rounded-xl" />
    </div>
  )
}
