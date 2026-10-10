const dateFormat = new Intl.DateTimeFormat('de-AT', { dateStyle: 'medium', timeStyle: 'short' })
const dayFormat = new Intl.DateTimeFormat('de-AT', { day: 'numeric', month: 'short' })
const relativeFormat = new Intl.RelativeTimeFormat('de-AT', { numeric: 'auto' })
const numberFormat = new Intl.NumberFormat('de-AT')

export const formatDate = (iso: string) => dateFormat.format(new Date(iso))
export const formatDay = (iso: string) => dayFormat.format(new Date(iso))
export const formatNumber = (value: number) => numberFormat.format(value)

const UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ['year', 365 * 24 * 3600],
  ['month', 30 * 24 * 3600],
  ['week', 7 * 24 * 3600],
  ['day', 24 * 3600],
  ['hour', 3600],
  ['minute', 60],
]

/** "vor 3 Minuten", "gestern", … ; under a minute → "gerade eben". */
export function formatRelative(iso: string, now: Date = new Date()): string {
  const seconds = (new Date(iso).getTime() - now.getTime()) / 1000
  for (const [unit, size] of UNITS) {
    if (Math.abs(seconds) >= size) return relativeFormat.format(Math.round(seconds / size), unit)
  }
  return 'gerade eben'
}
