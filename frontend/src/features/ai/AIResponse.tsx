import { Link } from 'react-router'
import { Button } from '@/components/ui/button'
import type { useAI } from './useAI'

export function AIResponse({ ai, structured = false, onRetry }: { ai: ReturnType<typeof useAI>; structured?: boolean; onRetry?: () => void }) {
  if (!ai.pending && !ai.result && !ai.error) return null
  return <div className="mt-4 min-w-0 border-t pt-4">
    {ai.error ? <div role="alert" className="text-sm">
      <p className="text-destructive">{ai.error}</p>
      <Button type="button" variant="outline" className="mt-3" onClick={onRetry ?? ai.retry}>Erneut versuchen</Button>
    </div> : <>
      <p className="mb-3 flex flex-wrap gap-2 text-xs font-medium text-muted-foreground">
        <span>KI-generiert</span>{ai.result?.cached && <span>· Bereits erstellt</span>}
        {ai.pending && <span role="status">· Antwort wird erstellt …</span>}
      </p>
      {ai.pending && <p className="mb-3 text-xs text-muted-foreground">Vorläufige Antwort – noch nicht geprüft.</p>}
      <p className="max-w-[68ch] whitespace-pre-wrap text-base leading-relaxed [overflow-wrap:anywhere]">
        {ai.result?.text ?? (structured ? 'Entwurf wird vorbereitet …' : ai.partial)}
      </p>
      {!!ai.result?.citations.length && <nav aria-label="Quellen der KI-Antwort" className="mt-4 flex flex-wrap gap-3 text-sm">
        {ai.result.citations.map(ref => <Link key={ref.index} to={`/wissen/${ref.id}`} className="text-primary underline underline-offset-4 [overflow-wrap:anywhere]">[{ref.index}] {ref.title}</Link>)}
      </nav>}
    </>}
  </div>
}
