import { createContext, useContext } from 'react'
import type { Lang } from '@/i18n/lang'
import type { Params, TranslationKey } from '@/i18n/translate'

export interface I18nValue {
  lang: Lang
  setLang: (lang: Lang) => void
  /** BCP 47 locale for Intl formatting, e.g. "en-GB". */
  locale: string
  t: (key: TranslationKey, params?: Params) => string
  /** Translated specialty name; unknown names come back unchanged. */
  categoryLabel: (name: string) => string
  /** Translated document type; unknown names come back unchanged. */
  docTypeLabel: (name: string) => string
}

export const I18nContext = createContext<I18nValue | null>(null)

export function useI18n(): I18nValue {
  const value = useContext(I18nContext)
  if (!value) throw new Error('useI18n must be used inside <I18nProvider>')
  return value
}
