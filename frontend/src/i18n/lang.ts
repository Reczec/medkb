export type Lang = 'en' | 'de'

export const LANGS: Lang[] = ['en', 'de']
export const DEFAULT_LANG: Lang = 'en'
/** localStorage key of the chosen language. */
export const LANG_KEY = 'medkb:lang'

export const LOCALES: Record<Lang, string> = { en: 'en-GB', de: 'de-AT' }

export function isLang(value: unknown): value is Lang {
  return value === 'en' || value === 'de'
}

/** The stored choice, English when nothing valid is stored or storage is blocked. */
export function readLang(): Lang {
  try {
    const stored = localStorage.getItem(LANG_KEY)
    return isLang(stored) ? stored : DEFAULT_LANG
  } catch {
    return DEFAULT_LANG
  }
}

export function writeLang(lang: Lang): void {
  try {
    localStorage.setItem(LANG_KEY, lang)
  } catch {
    // storage blocked: the choice lasts until the next reload
  }
}

// The API client reads the language here, so it needs no React context.
let apiLanguage: Lang = DEFAULT_LANG

export const getApiLanguage = (): Lang => apiLanguage

export function setApiLanguage(lang: Lang): void {
  apiLanguage = lang
}
