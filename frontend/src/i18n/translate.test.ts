import { translate } from '@/i18n/translate'

const dicts = {
  de: {
    hello: 'Hallo {name}',
    changes_one: '{count} Änderung',
    changes_other: '{count} Änderungen',
    plain: 'Text',
  },
  en: {
    hello: 'Hello {name}',
    changes_one: '{count} change',
    changes_other: '{count} changes',
    plain: 'Text',
  },
}

it('fills placeholders', () => {
  expect(translate('en', 'hello', { name: 'Ada' }, dicts)).toBe('Hello Ada')
  expect(translate('de', 'hello', { name: 'Ada' }, dicts)).toBe('Hallo Ada')
})

it('picks the plural form by count', () => {
  expect(translate('en', 'changes', { count: 1 }, dicts)).toBe('1 change')
  expect(translate('en', 'changes', { count: 3 }, dicts)).toBe('3 changes')
  expect(translate('de', 'changes', { count: 0 }, dicts)).toBe('0 Änderungen')
  expect(translate('de', 'changes', { count: 1 }, dicts)).toBe('1 Änderung')
})

it('keeps an unknown placeholder visible and returns unknown keys unchanged', () => {
  expect(translate('en', 'hello', {}, dicts)).toBe('Hello {name}')
  expect(translate('en', 'no.such.key', undefined, dicts)).toBe('no.such.key')
})

it('uses a non-plural text even when a count is given', () => {
  expect(translate('en', 'plain', { count: 5 }, dicts)).toBe('Text')
})
