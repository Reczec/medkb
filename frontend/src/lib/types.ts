/** Mirrors app/schemas.py. Datetimes are ISO strings in UTC. */

export type SectionKey = 'definition' | 'symptoms' | 'causes' | 'diagnostics' | 'therapy' | 'red_flags'

/** Structured content; the API composes `content` from it. */
export type Sections = Partial<Record<SectionKey, string | null>>

export interface FurtherReadingLink {
  label: string
  /** English label; the German one is shown when it is missing. */
  label_en?: string | null
  url: string
}

export interface Document {
  id: number
  title: string
  content: string
  category: string
  doc_type: string
  keywords: string[]
  source: string | null
  auto_classified: boolean
  term_en: string | null
  icd11_code: string | null
  medications: string[]
  sections: Sections | null
  further_reading: FurtherReadingLink[]
  ai_generated: boolean
  /** Optional English version; German above is canonical. */
  title_en: string | null
  content_en: string | null
  sections_en: Sections | null
  keywords_en: string[]
  created_at: string
  updated_at: string
}

export interface DocumentList {
  items: Document[]
  total: number
  limit: number
  offset: number
}

/** Send `content` for free text or `sections` for a structured entry. */
export interface DocumentCreate {
  ai_generated?: boolean
  title: string
  content?: string
  sections?: Sections
  doc_type: string
  category?: string
  keywords?: string[]
  source?: string | null
  term_en?: string | null
  icd11_code?: string | null
  medications?: string[]
  title_en?: string | null
  content_en?: string | null
  sections_en?: Sections
  keywords_en?: string[]
}

export interface DocumentUpdate {
  title?: string
  /** Sent without `sections`, it turns the entry into free text. */
  content?: string
  sections?: Sections
  doc_type?: string
  category?: string
  keywords?: string[]
  source?: string | null
  term_en?: string | null
  icd11_code?: string | null
  medications?: string[]
  title_en?: string | null
  content_en?: string | null
  sections_en?: Sections
  keywords_en?: string[] | null
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
  title_en?: string | null
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
  actor: string | null
  document_id: number | null
  detail: string
}

export interface UserInfo {
  id: number
  username: string
  display_name: string
  role: 'admin' | 'doctor' | 'patient'
  created_at: string
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

/** Answer of an external source; problems are reported in `status`, never as an error. */
export interface SourceResult<T> {
  status: 'ok' | 'empty' | 'unavailable' | 'not_configured'
  fetched_at: string | null
  data: T | null
}

export interface Study {
  pmid: string
  title: string
  journal: string | null
  year: number | null
  /** The first three authors; `more_authors` means "et al.". */
  authors: string[]
  more_authors: boolean
  url: string
}

export interface LatestStudies {
  category: string
  studies: Study[]
}

export interface Icd11Entry {
  code: string
  title: string
  definition: string | null
  url: string
  release: string
  /** The language WHO answered in; German is a prerelease. */
  language: string
}

export interface MedicationLabel {
  ingredient: string
  brand_names: string[]
  indications: string | null
  warnings: string | null
  adverse_reactions: string | null
  url: string
}

export interface MedicationsOut {
  found: MedicationLabel[]
  missing: string[]
}
