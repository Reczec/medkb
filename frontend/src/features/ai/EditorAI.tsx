import { useState } from 'react'
import { Button } from '@/components/ui/button'
import type { DocumentCreate } from '@/lib/types'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'

export function EditorAI({ title, content, canDraft, onDraft, onCategory }: {
  title: string; content: string; canDraft: boolean
  onDraft: (draft: DocumentCreate) => void; onCategory: (category: string) => void
}) {
  const draft = useAI(); const opinion = useAI()
  const [draftFor, setDraftFor] = useState('')
  const [opinionFor, setOpinionFor] = useState('')
  const input = JSON.stringify([title, content])
  return <section aria-label="KI-Unterstützung" className="mt-5 border-t pt-5">
    <h2 className="text-base font-semibold">KI-Unterstützung</h2>
    <p className="mt-1 mb-3 text-sm text-muted-foreground">Vorschläge prüfen. Übernehmen ändert nur die Formularfelder; gespeichert wird mit „Speichern“.</p>
    {canDraft && <>
      <Button type="button" variant="outline" disabled={title.trim().length < 3 || draft.pending} onClick={() => { setDraftFor(input); void draft.run('/draft', { title: title.trim() }) }}>KI-Entwurf erstellen</Button>
      {draftFor === input && <><AIResponse ai={draft} structured />
        {draft.result?.draft && <div className="mt-3 flex flex-col gap-3">
          <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm">
            <dt>Fachbegriff (en)</dt><dd className="[overflow-wrap:anywhere]">{draft.result.draft.term_en || '—'}</dd>
            <dt>ICD-11</dt><dd>{draft.result.draft.icd11_code || '—'}</dd>
            <dt>Wirkstoffe</dt><dd className="[overflow-wrap:anywhere]">{draft.result.draft.medications?.join(', ') || '—'}</dd>
          </dl>
          <p className="text-xs text-muted-foreground">Auch Fachbegriff, Code und Wirkstoffe prüfen. Übernahme ersetzt Inhalt und diese Metadaten.</p>
          <Button type="button" className="h-auto min-h-8 whitespace-normal" onClick={() => { onDraft(draft.result!.draft!); draft.clear() }}>Geprüften Entwurf übernehmen</Button>
        </div>}
      </>}
    </>}
    <div className="mt-4">
      <Button type="button" variant="outline" className="h-auto min-h-8 whitespace-normal" disabled={title.trim().length < 3 || content.trim().length < 10 || opinion.pending} onClick={() => { setOpinionFor(input); void opinion.run('/classify', { title, content }, false) }}>KI-Zweitmeinung anfordern</Button>
      {opinionFor === input && <><AIResponse ai={opinion} />
        {opinion.result?.classification && <div className="mt-3 text-sm">
          <p>{opinion.result.classification.category} · Konfidenz <span className="tabular">{Math.round(opinion.result.classification.confidence * 100)} %</span></p>
          <Button type="button" variant="outline" className="mt-2 h-auto min-h-8 whitespace-normal" onClick={() => onCategory(opinion.result!.classification!.category)}>Fachgebiet {opinion.result.classification.category} übernehmen</Button>
        </div>}
      </>}
    </div>
  </section>
}
