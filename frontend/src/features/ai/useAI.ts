import { useEffect, useRef, useState } from 'react'
import { requestAI, type AIResult } from './client'

export function useAI() {
  const controller = useRef<AbortController | null>(null)
  const last = useRef<{ path: string; body?: unknown; stream: boolean } | null>(null)
  const [state, setState] = useState<{ pending: boolean; result?: AIResult; partial: string; error?: string }>({ pending: false, partial: '' })
  useEffect(() => () => controller.current?.abort(), [])
  const run = async (path: string, body?: unknown, stream = true) => {
    controller.current?.abort()
    const current = new AbortController(); controller.current = current
    last.current = { path, body, stream }
    setState({ pending: true, partial: '' })
    try {
      const result = await requestAI(path, body, { stream, signal: current.signal,
        onToken: text => { if (!current.signal.aborted) setState(prev => ({ ...prev, partial: prev.partial + text })) },
      })
      if (!current.signal.aborted) setState({ pending: false, result, partial: '' })
      return current.signal.aborted ? undefined : result
    } catch (error) {
      if (!current.signal.aborted) setState({ pending: false, partial: '', error: (error as Error).message })
    }
  }
  const retry = () => { if (last.current) void run(last.current.path, last.current.body, last.current.stream) }
  const clear = () => { controller.current?.abort(); setState({ pending: false, partial: '' }) }
  return { ...state, run, retry, clear }
}
