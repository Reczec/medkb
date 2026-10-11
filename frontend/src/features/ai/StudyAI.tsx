import { Button } from '@/components/ui/button'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'

export function StudyAI({ pmid }: { pmid: string }) {
  const ai = useAI()
  return <div className="mb-3">
    <Button type="button" variant="outline" disabled={ai.pending} onClick={() => void ai.run('/studies/summarize', { pmid }, false)}>Abstract mit KI zusammenfassen</Button>
    <AIResponse ai={ai} />
  </div>
}
