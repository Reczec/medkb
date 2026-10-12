import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'

export function StudyAI({ pmid }: { pmid: string }) {
  const ai = useAI()
  const { t } = useI18n()
  return <div className="mb-3">
    <Button type="button" variant="outline" disabled={ai.pending} onClick={() => void ai.run('/studies/summarize', { pmid }, false)}>{t('ai.studySummary')}</Button>
    <AIResponse ai={ai} />
  </div>
}
