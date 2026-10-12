import { Link } from 'react-router'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'
import { AIText } from './AIText'
import { SECTION_ORDER } from '@/lib/sections'
import type { SectionKey } from '@/lib/types'
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
      {ai.result?.retrieval && <div className="mb-4 text-xs text-muted-foreground">
        <p>{t(ai.result.retrieval.mode === 'hybrid' ? 'rag.hybrid' : 'rag.lexical')}</p>
        {ai.result.retrieval.reason && <p className="mt-1">{t(`rag.reason.${ai.result.retrieval.reason}`)}</p>}
      </div>}
      <AIText text={ai.result?.text ?? (structured ? t('ai.preparing') : ai.partial)} />
      {!!ai.result?.citations.length && <nav aria-label={t('ai.sources')} className="mt-5 flex flex-col gap-4 text-sm">
        {ai.result.citations.map(ref => <div key={ref.index} className="min-w-0">
          <Link to={`/wissen/${ref.id}`} className="text-primary underline underline-offset-4 [overflow-wrap:anywhere]">[{ref.index}] {ref.title}</Link>
          {ref.excerpt && <details className="mt-2 max-w-[68ch]">
            <summary className="cursor-pointer rounded-sm text-muted-foreground outline-none hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring">
              {t('rag.excerpt')}{ref.section && <> · {SECTION_ORDER.includes(ref.section as SectionKey) ? t(`section.${ref.section as SectionKey}`) : t('editor.content')}</>}
            </summary>
            <p className="mt-3 whitespace-pre-wrap text-sm leading-relaxed [overflow-wrap:anywhere]">{ref.excerpt}</p>
          </details>}
        </div>)}
      </nav>}
    </>}
  </div>
}
