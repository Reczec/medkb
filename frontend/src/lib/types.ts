/** Mirrors app/schemas.py. Datetimes are ISO strings in UTC. */

export interface Document {
  id: number
  title: string
  content: string
  category: string
  doc_type: string
  keywords: string[]
  source: string | null
  auto_classified: boolean
  created_at: string
  updated_at: string
}

export interface DocumentList {
  items: Document[]
  total: number
  limit: number
  offset: number
}

export interface DocumentCreate {
  title: string
  content: string
  doc_type: string
  category?: string
  keywords?: string[]
  source?: string | null
}

export interface DocumentUpdate {
  title?: string
  content?: string
  doc_type?: string
  category?: string
  keywords?: string[]
  source?: string | null
  reclassify?: boolean
}

export interface ClassifyResponse {
  category: string
  confidence: number
  fallback: boolean
  scores: Record<string, number>
  matched_terms: string[]
  keywords: string[]
}

export interface Meta {
  categories: string[]
  doc_types: string[]
  default_category: string
}

export interface CountItem {
  name: string
  count: number
}

export interface RecentItem {
  id: number
  title: string
  category: string
  updated_at: string
}

export interface DayCount {
  date: string
  count: number
}

export interface Stats {
  total: number
  auto_classified: number
  categories: CountItem[]
  doc_types: CountItem[]
  recent: RecentItem[]
  activity: DayCount[]
}

export interface AuditEntry {
  id: number
  timestamp: string
  action: string
  document_id: number | null
  detail: string
}

export interface ArchiveInfo {
  name: string
  created_at: string
  size_bytes: number
  document_count: number
}

export interface RestoreResult {
  restored: number
  backup: ArchiveInfo
}
