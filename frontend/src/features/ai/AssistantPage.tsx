import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { AIResponse } from './AIResponse'
import { useAI } from './useAI'
import type { AIResult } from './client'

export function AssistantPage() {
  const [question, setQuestion] = useState('')
  const [history, setHistory] = useState<{ role: 'user' | 'assistant'; content: string }[]>([])
  const [asked, setAsked] = useState('')
  const ai = useAI()
  const remember = (text: string, result: AIResult) => {
    setHistory(prev => [...prev, { role: 'user' as const, content: text }, { role: 'assistant' as const, content: result.text.slice(0, 4000) }].slice(-6))
    setQuestion(current => current.trim() === text ? '' : current)
  }
  const submit = async (event: React.FormEvent) => {
    event.preventDefault()
    const text = question.trim()
    if (!text || ai.pending) return
    setAsked(text)
    const result = await ai.run('/ask', { question: text, history })
    if (result) {
      remember(text, result)
    }
  }
  return <div className="flex max-w-4xl flex-col gap-6">
    <header><h1 className="text-3xl font-semibold tracking-tight">KI-Assistent</h1>
      <p className="mt-2 max-w-[68ch] text-lg leading-relaxed text-muted-foreground">Fragen zu den Einträgen – mit Quellen zum Weiterlesen.</p></header>
    <section className="min-w-0 rounded-xl border bg-card p-5 shadow-sheet sm:p-6">
      <p className="mb-5 text-sm text-muted-foreground">Nutze kurze Themen oder Suchbegriffe, etwa „Migräne“. Die Suche berücksichtigt bis zu fünf passende Einträge. Keine persönlichen Gesundheitsdaten eingeben. Bei akuter Gefahr: Notruf 144.</p>
      <form onSubmit={submit} className="flex flex-col gap-2">
        <label htmlFor="ai-question" className="text-sm font-medium">Deine Frage</label>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Input id="ai-question" value={question} onChange={event => setQuestion(event.target.value)} maxLength={200} placeholder="Was möchtest du verstehen?" className="h-11 min-w-0 flex-1 text-base" />
          <Button type="submit" disabled={!question.trim() || ai.pending} className="h-11">Frage stellen</Button>
        </div>
      </form>
      {asked && <h2 className="mt-6 text-base font-semibold [overflow-wrap:anywhere]">{asked}</h2>}
      <AIResponse ai={ai} onRetry={() => { void ai.retry().then(result => { if (result) remember(asked, result) }) }} />
      {history.length > 0 && <Button type="button" variant="ghost" className="mt-4" disabled={ai.pending} onClick={() => { setHistory([]); setAsked(''); ai.clear() }}>Gespräch zurücksetzen</Button>}
    </section>
    <p className="text-xs text-muted-foreground">Prototyp mit Beispieldaten – keine medizinische Beratung.</p>
  </div>
}
