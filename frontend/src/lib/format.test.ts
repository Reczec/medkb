import { formatDate, formatDay, formatNumber, formatRelative } from '@/lib/format'

it('formats dates for Austria in German', () => {
  expect(formatDate('2026-03-05T14:07:00Z', 'de')).toMatch(/05\.03\.2026|5\. März 2026|05\. März 2026/)
})

it('formats dates in English', () => {
  expect(formatDate('2026-03-05T14:07:00Z', 'en')).toMatch(/5 Mar 2026/)
})

it('formats days and numbers per language', () => {
  expect(formatDay('2026-10-12', 'en')).toMatch(/12 Oct/)
  expect(formatDay('2026-10-12', 'de')).toMatch(/12\. Okt/)
  expect(formatNumber(1234567, 'en')).toBe('1,234,567')
  expect(formatNumber(1234567, 'de')).toMatch(/1\s?234\s?567/)
})

it('formats relative times in German', () => {
  const now = new Date('2026-10-10T12:00:00Z')
  expect(formatRelative('2026-10-10T11:57:00Z', 'de', now)).toBe('vor 3 Minuten')
  expect(formatRelative('2026-10-08T12:00:00Z', 'de', now)).toBe('vorgestern')
  expect(formatRelative('2026-10-10T11:59:59Z', 'de', now)).toBe('gerade eben')
})

it('formats relative times in English', () => {
  const now = new Date('2026-10-10T12:00:00Z')
  expect(formatRelative('2026-10-10T11:57:00Z', 'en', now)).toBe('3 minutes ago')
  expect(formatRelative('2026-10-09T12:00:00Z', 'en', now)).toBe('yesterday')
  expect(formatRelative('2026-10-10T11:59:59Z', 'en', now)).toBe('just now')
})
