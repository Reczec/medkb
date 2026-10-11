import type { Lang } from '@/i18n/lang'
import type { Document, FurtherReadingLink, Sections } from '@/lib/types'

export interface LocalizedDocument {
  title: string
  content: string
  sections: Sections | null
  keywords: string[]
  /** English was asked for, but the entry has no English version at all (German is shown). */
  fallback: boolean
}

/**
 * The text of an entry in the chosen language. German is canonical; English is used field by
 * field when it exists, so a half-translated entry still reads sensibly.
 */
export function localized(document: Document, lang: Lang): LocalizedDocument {
  if (lang !== 'en') {
    return {
      title: document.title,
      content: document.content,
      sections: document.sections,
      keywords: document.keywords,
      fallback: false,
    }
  }
  const hasEnglish = Boolean(document.title_en || document.content_en || document.sections_en)
  return {
    title: document.title_en || document.title,
    content: document.content_en || document.content,
    sections: document.sections_en || document.sections,
    keywords: document.keywords_en.length > 0 ? document.keywords_en : document.keywords,
    fallback: !hasEnglish,
  }
}

export function linkLabel(link: FurtherReadingLink, lang: Lang): string {
  return lang === 'en' && link.label_en ? link.label_en : link.label
}
