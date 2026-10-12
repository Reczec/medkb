import { linkLabel, localized } from '@/i18n/localized'
import type { Document } from '@/lib/types'

const base: Document = {
  id: 1,
  title: 'Erkältung',
  content: 'Deutscher Text.',
  category: 'Allgemeinmedizin',
  doc_type: 'Beschreibung',
  keywords: ['Schnupfen'],
  source: null,
  auto_classified: true,
  term_en: null,
  icd11_code: null,
  medications: [],
  sections: { definition: 'Deutsch.' },
  further_reading: [],
  ai_generated: false,
  title_en: null,
  content_en: null,
  sections_en: null,
  keywords_en: [],
  created_at: '2026-10-01T10:00:00Z',
  updated_at: '2026-10-01T10:00:00Z',
}

it('uses the English version field by field', () => {
  const doc = {
    ...base,
    title_en: 'Common cold',
    content_en: 'English text.',
    sections_en: { definition: 'English.' },
    keywords_en: ['Runny nose'],
  }
  expect(localized(doc, 'en')).toEqual({
    title: 'Common cold',
    content: 'English text.',
    sections: { definition: 'English.' },
    keywords: ['Runny nose'],
    fallback: false,
  })
})

it('falls back to German per field without flagging a partly translated entry', () => {
  const doc = { ...base, title_en: 'Common cold' }
  const result = localized(doc, 'en')
  expect(result.title).toBe('Common cold')
  expect(result.content).toBe('Deutscher Text.')
  expect(result.keywords).toEqual(['Schnupfen'])
  expect(result.fallback).toBe(false)
})

it('keeps German sections that have no English text, such as the warning signs', () => {
  const doc = {
    ...base,
    sections: { definition: 'Deutsch.', red_flags: 'Sofort Notruf 144.' },
    sections_en: { definition: 'English.' },
  }
  expect(localized(doc, 'en').sections).toEqual({
    definition: 'English.',
    red_flags: 'Sofort Notruf 144.',
  })
  expect(localized(doc, 'de').sections).toEqual(doc.sections)
})

it('flags an entry that has no English version at all', () => {
  const result = localized(base, 'en')
  expect(result.title).toBe('Erkältung')
  expect(result.fallback).toBe(true)
})

it('always shows German in German', () => {
  const doc = { ...base, title_en: 'Common cold' }
  expect(localized(doc, 'de')).toMatchObject({ title: 'Erkältung', fallback: false })
})

it('picks the English link label when there is one', () => {
  const link = { label: 'Deutsch', label_en: 'English', url: 'https://www.who.int/x' }
  expect(linkLabel(link, 'en')).toBe('English')
  expect(linkLabel(link, 'de')).toBe('Deutsch')
  expect(linkLabel({ label: 'Nur Deutsch', url: 'https://www.who.int/x' }, 'en')).toBe('Nur Deutsch')
})
