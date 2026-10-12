import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'
import type { DocumentCreate } from '@/lib/types'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'

export function EditorAI({ title, content, canDraft, onDraft, onCategory }: {
  title: string; content: string; canDraft: boolean
  onDraft: (draft: DocumentCreate) => void; onCategory: (category: string) => void
}) {
  const draft = useAI(); const opinion = useAI()
  const { t, categoryLabel } = useI18n()
  const [draftFor, setDraftFor] = useState('')
  const [opinionFor, setOpinionFor] = useState('')
  const input = JSON.stringify([title, content])
  return <section aria-label={t('ai.support')} className="mt-5 border-t pt-5">
    <h2 className="text-base font-semibold">{t('ai.support')}</h2>
    <p className="mt-1 mb-3 text-sm text-muted-foreground">{t('ai.supportHint')}</p>
    {canDraft && <>
      <Button type="button" variant="outline" disabled={title.trim().length < 3 || draft.pending} onClick={() => { setDraftFor(input); void draft.run('/draft', { title: title.trim() }) }}>{t('ai.draft')}</Button>
      <p className="mt-1.5 text-xs text-muted-foreground">{t('ai.draftNote')}</p>
      {draftFor === input && <><AIResponse ai={draft} structured />
        {draft.result?.draft && <div className="mt-3 flex flex-col gap-3">
          <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm">
            <dt>{t('doc.termEn')}</dt><dd className="[overflow-wrap:anywhere]">{draft.result.draft.term_en || '—'}</dd>
            <dt>{t('doc.icd11')}</dt><dd>{draft.result.draft.icd11_code || '—'}</dd>
            <dt>{t('ai.ingredients')}</dt><dd className="[overflow-wrap:anywhere]">{draft.result.draft.medications?.join(', ') || '—'}</dd>
          </dl>
          <p className="text-xs text-muted-foreground">{t('ai.draftCheck')}</p>
          <Button type="button" className="h-auto min-h-8 whitespace-normal" onClick={() => { onDraft(draft.result!.draft!); draft.clear() }}>{t('ai.draftApply')}</Button>
        </div>}
      </>}
    </>}
    <div className="mt-4">
      <Button type="button" variant="outline" className="h-auto min-h-8 whitespace-normal" disabled={title.trim().length < 3 || content.trim().length < 10 || opinion.pending} onClick={() => { setOpinionFor(input); void opinion.run('/classify', { title, content }, false) }}>{t('ai.opinion')}</Button>
      {opinionFor === input && <><AIResponse ai={opinion} />
        {opinion.result?.classification && <div className="mt-3 text-sm">
          <p>{categoryLabel(opinion.result.classification.category)} · {t('ai.confidence')} <span className="tabular">{Math.round(opinion.result.classification.confidence * 100)} %</span></p>
          <Button type="button" variant="outline" className="mt-2 h-auto min-h-8 whitespace-normal" onClick={() => onCategory(opinion.result!.classification!.category)}>{t('ai.applyCategory', { category: categoryLabel(opinion.result.classification.category) })}</Button>
        </div>}
      </>}
    </div>
  </section>
}
