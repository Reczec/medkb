import type { SectionKey } from '@/lib/types'

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
