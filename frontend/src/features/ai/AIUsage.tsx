import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function AIUsage() {
  const query = useQuery({ queryKey: ['ai-usage'], queryFn: () => api<{ today: number; limit: number }>('/api/ai/usage'), staleTime: 30_000 })
  return <p className="text-sm text-muted-foreground">KI-Anfragen heute: {query.data ? <span className="tabular font-medium text-foreground">{query.data.today} / {query.data.limit}</span> : query.error ? 'nicht verfügbar' : 'wird geladen …'} <span className="text-xs">(UTC, gesamte Demo)</span></p>
}
