import type { SectionKey, Sections } from '@/lib/types'

/** Same order and labels as app/content.py. */
export const SECTION_ORDER: SectionKey[] = [
  'definition',
  'symptoms',
  'causes',
  'diagnostics',
  'therapy',
  'red_flags',
]

export const SECTION_LABELS: Record<SectionKey, string> = {
  definition: 'Definition',
  symptoms: 'Symptome',
  causes: 'Ursachen',
  diagnostics: 'Diagnostik',
  therapy: 'Therapie',
  red_flags: 'Warnzeichen',
}

/** Matches the server composition; used when converting sections to editable free text. */
export function composeContent(sections: Sections): string {
  return SECTION_ORDER.flatMap((key) => {
    const text = sections[key]?.trim()
    return text ? [`${SECTION_LABELS[key]}\n${text}`] : []
  }).join('\n\n')
}

/** Blank values and absent keys mean the same thing to the API. */
export function cleanSections(sections: Sections): Sections {
  return Object.fromEntries(SECTION_ORDER.flatMap((key) => {
    const text = sections[key]?.trim()
    return text ? [[key, text]] : []
  }))
}
