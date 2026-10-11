import { Button } from '@/components/ui/button'
import { useAuth } from '@/features/auth/context'
import { useI18n } from '@/i18n/context'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'

export function DocumentAI({ documentId, summaryOnly = false }: { documentId: number; summaryOnly?: boolean }) {
  const ai = useAI()
  const { user } = useAuth()
  const { t } = useI18n()
  if (summaryOnly && user?.role === 'patient') return null
  const generate = (feature: string) => void ai.run(`/documents/${documentId}/${feature}`, undefined, feature !== 'red-flags')
  return <section aria-label={t('ai.help')} className="min-w-0">
    <p className="mb-3 text-sm text-muted-foreground">{summaryOnly ? t('ai.summaryHint') : t('ai.explainHint')}</p>
    <div className="flex flex-wrap gap-2">
      {summaryOnly ? <Button type="button" variant="outline" disabled={ai.pending} onClick={() => generate('summary')}>{t('ai.summary')}</Button> : <>
        <Button type="button" variant="outline" disabled={ai.pending} onClick={() => generate('explain')}>{t('ai.explain')}</Button>
        <Button type="button" variant="outline" disabled={ai.pending} onClick={() => generate('red-flags')}>{t('ai.redFlags')}</Button>
      </>}
    </div>
    <AIResponse ai={ai} />
  </section>
}
