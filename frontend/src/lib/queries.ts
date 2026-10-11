import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
  type QueryClient,
} from '@tanstack/react-query'
import { api } from '@/lib/api'
import type {
  ArchiveInfo,
  AuditEntry,
  ClassifyResponse,
  Document,
  DocumentCreate,
  DocumentList,
  DocumentUpdate,
  Icd11Entry,
  LatestStudies,
  MedicationsOut,
  Meta,
  RestoreResult,
  Sections,
  SourceResult,
  Stats,
  Study,
  UserInfo,
} from '@/lib/types'

export interface DocumentQuery {
  q?: string
  category?: string
  docType?: string
  offset?: number
  limit?: number
}

export function documentsPath({ q, category, docType, offset = 0, limit = 10 }: DocumentQuery) {
  const params = new URLSearchParams()
  if (q?.trim()) params.set('q', q.trim())
  if (category) params.set('category', category)
  if (docType) params.set('doc_type', docType)
  params.set('limit', String(limit))
  params.set('offset', String(offset))
  return `/api/documents?${params}`
}

/** Everything that shows document data must refresh after a change. */
function invalidateAfterChange(client: QueryClient) {
  return Promise.all(
    ['documents', 'document', 'stats', 'audit'].map((key) =>
      client.invalidateQueries({ queryKey: [key] }),
    ),
  )
}

export const useMeta = () =>
  useQuery({ queryKey: ['meta'], queryFn: () => api<Meta>('/api/meta'), staleTime: Infinity })

export const useStats = () => useQuery({ queryKey: ['stats'], queryFn: () => api<Stats>('/api/stats') })

export const useDocuments = (query: DocumentQuery, enabled = true) =>
  useQuery({
    queryKey: ['documents', query],
    queryFn: ({ signal }) => api<DocumentList>(documentsPath(query), { signal }),
    placeholderData: keepPreviousData,
    enabled,
  })

export const useDocument = (id: number) =>
  useQuery({
    queryKey: ['document', id],
    queryFn: () => api<Document>(`/api/documents/${id}`),
    enabled: Number.isInteger(id) && id > 0,
    retry: (count, error) => (error as { status?: number }).status !== 404 && count < 2,
  })

type ClassifyInput = { content: string } | { sections: Sections }

export function useClassify(title: string, input: string | ClassifyInput) {
  const body = typeof input === 'string' ? { content: input } : input
  const enabled = 'content' in body
    ? body.content.trim().length >= 10
    : Object.values(body.sections).some((text) => Boolean(text?.trim()))
  return useQuery({
    queryKey: ['classify', title, body],
    queryFn: ({ signal }) =>
      api<ClassifyResponse>('/api/classify', { method: 'POST', body: { title, ...body }, signal }),
    enabled: title.trim().length >= 1 && enabled,
    placeholderData: keepPreviousData,
    staleTime: Infinity,
  })
}

export function useCreateDocument() {
  const client = useQueryClient()
  return useMutation({
    mutationFn: (data: DocumentCreate) =>
      api<Document>('/api/documents', { method: 'POST', body: data }),
    onSuccess: () => invalidateAfterChange(client),
  })
}

export function useUpdateDocument(id: number) {
  const client = useQueryClient()
  return useMutation({
    mutationFn: (data: DocumentUpdate) =>
      api<Document>(`/api/documents/${id}`, { method: 'PATCH', body: data }),
    onSuccess: () => invalidateAfterChange(client),
  })
}

export function useDeleteDocument() {
  const client = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api<void>(`/api/documents/${id}`, { method: 'DELETE' }),
    onSuccess: () => invalidateAfterChange(client),
  })
}

export const useArchives = (enabled = true) =>
  useQuery({
    queryKey: ['archives'],
    queryFn: () => api<ArchiveInfo[]>('/api/archives'),
    enabled,
  })

export function useCreateArchive() {
  const client = useQueryClient()
  return useMutation({
    mutationFn: () => api<ArchiveInfo>('/api/archives', { method: 'POST' }),
    onSuccess: () =>
      Promise.all([
        client.invalidateQueries({ queryKey: ['archives'] }),
        client.invalidateQueries({ queryKey: ['audit'] }),
      ]),
  })
}

export function useRestoreArchive() {
  const client = useQueryClient()
  return useMutation({
    mutationFn: (name: string) =>
      api<RestoreResult>(`/api/archives/${encodeURIComponent(name)}/restore`, {
        method: 'POST',
      }),
    onSuccess: () =>
      Promise.all([
        invalidateAfterChange(client),
        client.invalidateQueries({ queryKey: ['archives'] }),
      ]),
  })
}

export const useUsers = () =>
  useQuery({ queryKey: ['users'], queryFn: () => api<UserInfo[]>('/api/users') })

export const useAudit = (limit = 50, enabled = true) =>
  useQuery({
    queryKey: ['audit', limit],
    queryFn: () => api<AuditEntry[]>(`/api/audit?limit=${limit}`),
    enabled,
  })

const SOURCE_STALE_MS = 10 * 60 * 1000

/** A document's live data from an external source; fetched only while `enabled`. */
function useDocumentSource<T>(source: string, id: number, enabled: boolean) {
  return useQuery({
    queryKey: ['source', source, id],
    queryFn: ({ signal }) =>
      api<SourceResult<T>>(`/api/sources/documents/${id}/${source}`, { signal }),
    enabled: enabled && Number.isInteger(id) && id > 0,
    staleTime: SOURCE_STALE_MS,
    gcTime: SOURCE_STALE_MS, // survives closing the tab, so reopening it does not refetch
  })
}

export const useStudies = (id: number, enabled: boolean) =>
  useDocumentSource<Study[]>('studies', id, enabled)

export const useIcd11 = (id: number, enabled: boolean) =>
  useDocumentSource<Icd11Entry>('icd11', id, enabled)

export const useMedications = (id: number, enabled: boolean) =>
  useDocumentSource<MedicationsOut>('medications', id, enabled)

export const useLatestStudies = (enabled = true) =>
  useQuery({
    queryKey: ['source', 'latest-studies'],
    queryFn: ({ signal }) =>
      api<SourceResult<LatestStudies[]>>('/api/sources/latest-studies', { signal }),
    enabled,
    staleTime: SOURCE_STALE_MS,
    gcTime: SOURCE_STALE_MS, // survives closing the tab, so reopening it does not refetch
  })
