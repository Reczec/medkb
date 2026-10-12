import type { Lang } from '@/i18n/lang'
import { translate } from '@/i18n/translate'
import type { SectionKey, Sections } from '@/lib/types'

/** Same order as app/content.py. */
export const SECTION_ORDER: SectionKey[] = [
  'definition',
  'symptoms',
  'causes',
  'diagnostics',
  'therapy',
  'red_flags',
]

/** Matches the server composition (labels of `lang`); used when converting sections to free text. */
export function composeContent(sections: Sections, lang: Lang): string {
  return SECTION_ORDER.flatMap((key) => {
    const text = sections[key]?.trim()
    return text ? [`${translate(lang, `section.${key}`)}\n${text}`] : []
  }).join('\n\n')
}

/** Blank values and absent keys mean the same thing to the API. */
export function cleanSections(sections: Sections): Sections {
  return Object.fromEntries(SECTION_ORDER.flatMap((key) => {
    const text = sections[key]?.trim()
    return text ? [[key, text]] : []
  }))
}
