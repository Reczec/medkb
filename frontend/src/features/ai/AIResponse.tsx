import { Link } from 'react-router'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'
import { AIText } from './AIText'
import type { useAI } from './useAI'

export function AIResponse({ ai, structured = false, onRetry }: { ai: ReturnType<typeof useAI>; structured?: boolean; onRetry?: () => void }) {
  const { t } = useI18n()
  if (!ai.pending && !ai.result && !ai.error) return null
  return <div className="mt-4 min-w-0 border-t pt-4">
    {ai.error ? <div role="alert" className="text-sm">
      <p className="text-destructive">{ai.error}</p>
      <Button type="button" variant="outline" className="mt-3" onClick={onRetry ?? ai.retry}>{t('action.retry')}</Button>
    </div> : <>
      <p className="mb-3 flex flex-wrap gap-2 text-xs font-medium text-muted-foreground">
        <span>{t('doc.aiGenerated')}</span>{ai.result?.cached && <span>· {t('ai.cached')}</span>}
        {ai.pending && <span role="status">· {t('ai.creating')}</span>}
      </p>
      {ai.pending && <p className="mb-3 text-xs text-muted-foreground">{t('ai.provisional')}</p>}
      <AIText text={ai.result?.text ?? (structured ? t('ai.preparing') : ai.partial)} />
      {!!ai.result?.citations.length && <nav aria-label={t('ai.sources')} className="mt-4 flex flex-wrap gap-3 text-sm">
        {ai.result.citations.map(ref => <Link key={ref.index} to={`/wissen/${ref.id}`} className="text-primary underline underline-offset-4 [overflow-wrap:anywhere]">[{ref.index}] {ref.title}</Link>)}
      </nav>}
    </>}
  </div>
}
