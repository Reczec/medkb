import { Button } from '@/components/ui/button'
import { useAuth } from '@/features/auth/context'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'

export function DocumentAI({ documentId, summaryOnly = false }: { documentId: number; summaryOnly?: boolean }) {
  const ai = useAI()
  const { user } = useAuth()
  if (summaryOnly && user?.role === 'patient') return null
  const generate = (feature: string) => void ai.run(`/documents/${documentId}/${feature}`, undefined, feature !== 'red-flags')
  return <section aria-label="KI-Hilfe" className="min-w-0">
    <p className="mb-3 text-sm text-muted-foreground">{summaryOnly ? 'Fachliche Kurzfassung zum Prüfen.' : 'Den Eintrag mit KI verständlicher machen.'}</p>
    <div className="flex flex-wrap gap-2">
      {summaryOnly ? <Button type="button" variant="outline" disabled={ai.pending} onClick={() => generate('summary')}>KI-Zusammenfassung</Button> : <>
        <Button type="button" variant="outline" disabled={ai.pending} onClick={() => generate('explain')}>Einfach erklären</Button>
        <Button type="button" variant="outline" disabled={ai.pending} onClick={() => generate('red-flags')}>Warnzeichen erklären</Button>
      </>}
    </div>
    <AIResponse ai={ai} />
  </section>
}
