import { de } from '@/i18n/messages.de'
import { en } from '@/i18n/messages.en'

const placeholders = (text: string) => [...text.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort()

it('has the same keys in both languages', () => {
  expect(Object.keys(en).sort()).toEqual(Object.keys(de).sort())
})

it('uses the same placeholders in both languages', () => {
  for (const key of Object.keys(de) as (keyof typeof de)[]) {
    expect(placeholders(en[key]), key).toEqual(placeholders(de[key]))
  }
})

it('has no empty text', () => {
  for (const [dict, name] of [[de, 'de'], [en, 'en']] as const) {
    for (const [key, text] of Object.entries(dict)) expect(text.trim(), `${name}:${key}`).not.toBe('')
  }
})

it('keeps plural forms in pairs', () => {
  for (const dict of [de, en]) {
    const keys = Object.keys(dict)
    for (const key of keys.filter((k) => k.endsWith('_one'))) {
      expect(keys, key).toContain(key.replace(/_one$/, '_other'))
    }
    for (const key of keys.filter((k) => k.endsWith('_other'))) {
      expect(keys, key).toContain(key.replace(/_other$/, '_one'))
    }
  }
})

it('names every specialty and document type', async () => {
  const { KNOWN_CATEGORIES } = await import('@/lib/categories')
  for (const name of KNOWN_CATEGORIES) expect(de).toHaveProperty(`category.${name}`)
  for (const name of ['Symptom', 'Diagnose', 'Beschreibung', 'Anamnese', 'Befund', 'Leitlinie']) {
    expect(de).toHaveProperty(`docType.${name}`)
  }
})
