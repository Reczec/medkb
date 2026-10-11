import { type Lang, LOCALES } from '@/i18n/lang'
import { de, type MessageKey } from '@/i18n/messages.de'
import { en } from '@/i18n/messages.en'

type PluralBase<K> = K extends `${infer Base}_one` ? Base : never

/** A message key, or the base of a `_one`/`_other` pair (picked by `params.count`). */
export type TranslationKey = MessageKey | PluralBase<MessageKey>

export type Params = Record<string, string | number>
type Dictionaries = Record<Lang, Record<string, string>>

const DEFAULTS: Dictionaries = { de, en }

/**
 * Looks up `key`, picks the plural form when `params.count` is a number, and fills `{name}`
 * placeholders. Unknown keys come back unchanged, so a missing text is visible, not a crash.
 */
export function translate(
  lang: Lang,
  key: string,
  params?: Params,
  dictionaries: Dictionaries = DEFAULTS,
): string {
  const dict = dictionaries[lang]
  let template = dict[key]
  if (template === undefined && typeof params?.count === 'number') {
    const rule = new Intl.PluralRules(LOCALES[lang]).select(params.count)
    template = dict[`${key}_${rule === 'one' ? 'one' : 'other'}`]
  }
  if (template === undefined) return key
  return template.replace(/\{(\w+)\}/g, (match, name: string) =>
    params && name in params ? String(params[name]) : match,
  )
}

/** Whether `key` exists as a plain message (used for optional labels such as categories). */
export function hasMessage(key: string): boolean {
  return key in de
}
