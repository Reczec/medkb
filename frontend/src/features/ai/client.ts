import { api, ApiError } from '@/lib/api'
import type { DocumentCreate } from '@/lib/types'

export interface AIResult {
  text: string
  cached: boolean
  citations: { index: number; id: number; title: string }[]
  draft?: DocumentCreate
  classification?: { category: string; confidence: number; reasoning: string }
}
export interface AIOptions {
  signal?: AbortSignal
  stream?: boolean
  onToken?: (text: string) => void
}

function result(value: unknown): AIResult {
  const data = value as AIResult
  if (!data || typeof data.text !== 'string' || typeof data.cached !== 'boolean' || !Array.isArray(data.citations)) {
    throw new Error('Die KI-Antwort ist ungültig. Bitte erneut versuchen.')
  }
  return data
}

export async function requestAI(path: string, body?: unknown, options: AIOptions = {}): Promise<AIResult> {
  try {
    const response = await api(`/api/ai${path}${options.stream ? '?stream=true' : ''}`, {
      method: 'POST', body, raw: true, signal: options.signal,
    })
    if (!response.headers.get('content-type')?.includes('text/event-stream')) return result(await response.json())
    if (!response.body) throw new Error('KI-Antwort konnte nicht geladen werden.')
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8', { fatal: true })
    let buffer = ''
    let size = 0
    try {
      while (true) {
        const { done, value } = await reader.read()
        if (options.signal?.aborted) throw new DOMException('Aborted', 'AbortError')
        buffer = (buffer + decoder.decode(value, { stream: !done })).replace(/\r\n/g, '\n')
        size += value?.length ?? 0
        if (size > 200_000) throw new Error('Die KI-Antwort ist zu lang.')
        let boundary: number
        while ((boundary = buffer.indexOf('\n\n')) >= 0) {
          const frame = buffer.slice(0, boundary); buffer = buffer.slice(boundary + 2)
          const lines = frame.split('\n')
          const event = lines.find(line => line.startsWith('event:'))?.slice(6).trim()
          const data = lines.filter(line => line.startsWith('data:')).map(line => line.slice(5).trimStart()).join('\n')
          if (!data) continue
          const parsed = JSON.parse(data)
          if (event === 'error') throw new Error(parsed.message || 'KI-Antwort abgebrochen. Bitte erneut versuchen.')
          if (event === 'done') return result(parsed)
          if (event === 'token') {
            if (typeof parsed.text !== 'string') throw new Error('Ungültiger KI-Stream.')
            options.onToken?.(parsed.text)
          }
        }
        if (done) throw new Error('KI-Antwort wurde unterbrochen. Bitte erneut versuchen.')
      }
    } finally { await reader.cancel(); reader.releaseLock() }
  } catch (error) {
    if (error instanceof ApiError) {
      if (error.status === 429) throw new Error('KI-Tageslimit erreicht. Bitte morgen erneut versuchen.')
      if (error.message === 'ai_not_configured') throw new Error('Die KI ist noch nicht eingerichtet. Bitte später erneut versuchen.')
      if (error.status === 503) throw new Error('KI momentan nicht verfügbar. Bitte später erneut versuchen.')
    }
    throw error
  }
}
