import { useQuery } from '@tanstack/react-query'
import { useI18n } from '@/i18n/context'
import { api } from '@/lib/api'

export function AIUsage() {
  const { t } = useI18n()
  const query = useQuery({
    queryKey: ['ai-usage'],
    queryFn: () => api<{ today: number; limit: number }>('/api/ai/usage'),
    staleTime: 30_000,
  })
  return (
    <p className="text-sm text-muted-foreground">
      {t('usage.label')}{' '}
      {query.data ? (
        <span className="tabular font-medium text-foreground">
          {query.data.today} / {query.data.limit}
        </span>
      ) : query.error ? (
        t('usage.unavailable')
      ) : (
        t('usage.loading')
      )}{' '}
      <span className="text-xs">{t('usage.note')}</span>
    </p>
  )
}
