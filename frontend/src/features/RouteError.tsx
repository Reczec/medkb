import { RotateCw } from 'lucide-react'
import { isRouteErrorResponse, useRouteError } from 'react-router'
import { ErrorState } from '@/components/feedback/ErrorState'
import { useI18n } from '@/i18n/context'

/** Last line of defence: a render error inside a route never shows a raw stack trace. */
export function RouteError() {
  const error = useRouteError()
  const { t } = useI18n()
  const shown = isRouteErrorResponse(error)
    ? new Error(`${error.status} ${error.statusText}`)
    : error instanceof Error
      ? error
      : new Error(t('error.unknown'))

  return (
    <div className="mx-auto flex min-h-dvh max-w-xl flex-col justify-center gap-4 p-6">
      <ErrorState error={shown} title={t('error.crashed')} />
      <button
        type="button"
        onClick={() => window.location.reload()}
        className="inline-flex items-center gap-2 self-start rounded-lg px-3 py-2 text-sm font-medium text-primary hover:bg-accent"
      >
        <RotateCw className="size-4" aria-hidden /> {t('error.reload')}
      </button>
    </div>
  )
}
