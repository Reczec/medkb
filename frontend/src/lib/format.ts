import { type Lang, LOCALES } from '@/i18n/lang'

const dateFormats = {} as Record<Lang, Intl.DateTimeFormat>
const dayFormats = {} as Record<Lang, Intl.DateTimeFormat>
const relativeFormats = {} as Record<Lang, Intl.RelativeTimeFormat>
const numberFormats = {} as Record<Lang, Intl.NumberFormat>

// Intl objects are costly to build; one per language and kind.
const dateFormat = (lang: Lang) =>
  (dateFormats[lang] ??= new Intl.DateTimeFormat(LOCALES[lang], {
    dateStyle: 'medium',
    timeStyle: 'short',
  }))
const dayFormat = (lang: Lang) =>
  (dayFormats[lang] ??= new Intl.DateTimeFormat(LOCALES[lang], { day: 'numeric', month: 'short' }))
const relativeFormat = (lang: Lang) =>
  (relativeFormats[lang] ??= new Intl.RelativeTimeFormat(LOCALES[lang], { numeric: 'auto' }))
const numberFormat = (lang: Lang) => (numberFormats[lang] ??= new Intl.NumberFormat(LOCALES[lang]))

export const formatDate = (iso: string, lang: Lang = 'de') => dateFormat(lang).format(new Date(iso))
export const formatDay = (iso: string, lang: Lang = 'de') => dayFormat(lang).format(new Date(iso))
export const formatNumber = (value: number, lang: Lang = 'de') => numberFormat(lang).format(value)

const UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ['year', 365 * 24 * 3600],
  ['month', 30 * 24 * 3600],
  ['week', 7 * 24 * 3600],
  ['day', 24 * 3600],
  ['hour', 3600],
  ['minute', 60],
]

const JUST_NOW: Record<Lang, string> = { de: 'gerade eben', en: 'just now' }

/** "3 minutes ago" / "vor 3 Minuten", "yesterday" / "gestern", …; under a minute → "just now". */
export function formatRelative(iso: string, lang: Lang = 'de', now: Date = new Date()): string {
  const seconds = (new Date(iso).getTime() - now.getTime()) / 1000
  for (const [unit, size] of UNITS) {
    if (Math.abs(seconds) >= size) {
      return relativeFormat(lang).format(Math.round(seconds / size), unit)
    }
  }
  return JUST_NOW[lang]
}
