import type { Lang } from '@/i18n/lang'
import { SECTION_ORDER } from '@/lib/sections'
import type { Document, FurtherReadingLink, Sections } from '@/lib/types'

export interface LocalizedDocument {
  title: string
  content: string
  sections: Sections | null
  keywords: string[]
  /** Language each field is really in; differs from the interface language on a German fallback. */
  titleLang: Lang
  contentLang: Lang
  keywordsLang: Lang
  /** English was asked for, but the entry has no English version at all (German is shown). */
  fallback: boolean
}

/** Section by section: English where it exists, so untranslated warning signs stay visible. */
function mergeSections(german: Sections | null, english: Sections | null): Sections | null {
  const merged: Sections = {}
  for (const key of SECTION_ORDER) {
    const text = english?.[key] || german?.[key]
    if (text) merged[key] = text
  }
  return Object.keys(merged).length > 0 ? merged : null
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
      titleLang: 'de',
      contentLang: 'de',
      keywordsLang: 'de',
      fallback: false,
    }
  }
  const hasEnglish = Boolean(document.title_en || document.content_en || document.sections_en)
  return {
    title: document.title_en || document.title,
    content: document.content_en || document.content,
    sections: mergeSections(document.sections, document.sections_en),
    keywords: document.keywords_en.length > 0 ? document.keywords_en : document.keywords,
    titleLang: document.title_en ? 'en' : 'de',
    contentLang: document.content_en || document.sections_en ? 'en' : 'de',
    keywordsLang: document.keywords_en.length > 0 ? 'en' : 'de',
    fallback: !hasEnglish,
  }
}

/** The `lang` attribute for text that is not in the interface language (screen readers switch voice). */
export const langAttr = (fieldLang: Lang, interfaceLang: Lang): Lang | undefined =>
  fieldLang === interfaceLang ? undefined : fieldLang

export function linkLabel(link: FurtherReadingLink, lang: Lang): string {
  return lang === 'en' && link.label_en ? link.label_en : link.label
}
