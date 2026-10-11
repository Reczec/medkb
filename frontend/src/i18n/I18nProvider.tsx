import { type ReactNode, useCallback, useLayoutEffect, useMemo, useState } from 'react'
import { I18nContext, type I18nValue } from '@/i18n/context'
import { type Lang, LOCALES, readLang, setApiLanguage, writeLang } from '@/i18n/lang'
import { hasMessage, translate } from '@/i18n/translate'

interface I18nProviderProps {
  /** Start language that is not read from or written to storage (tests). */
  lang?: Lang
  children: ReactNode
}

/**
 * Holds the interface language. A change re-renders the tree but never remounts it, so open
 * forms keep their input. The API client and <html lang> follow in a layout effect, which runs
 * before any child fetches data.
 */
export function I18nProvider({ lang: fixed, children }: I18nProviderProps) {
  const [lang, setLangState] = useState<Lang>(() => fixed ?? readLang())

  useLayoutEffect(() => {
    setApiLanguage(lang)
    document.documentElement.lang = lang
  }, [lang])

  const setLang = useCallback(
    (next: Lang) => {
      setLangState(next)
      if (fixed === undefined) writeLang(next)
    },
    [fixed],
  )

  const value = useMemo<I18nValue>(() => {
    const label = (prefix: string) => (name: string) => {
      const key = `${prefix}.${name}`
      return hasMessage(key) ? translate(lang, key) : name
    }
    return {
      lang,
      setLang,
      locale: LOCALES[lang],
      t: (key, params) => translate(lang, key, params),
      categoryLabel: label('category'),
      docTypeLabel: label('docType'),
    }
  }, [lang, setLang])

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}
