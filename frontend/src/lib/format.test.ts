import { formatDate, formatRelative } from '@/lib/format'

it('formats dates for Austria', () => {
  expect(formatDate('2026-03-05T14:07:00Z')).toMatch(/05\.03\.2026|5\. März 2026|05\. März 2026/)
})

it('formats relative times in German', () => {
  const now = new Date('2026-10-10T12:00:00Z')
  expect(formatRelative('2026-10-10T11:57:00Z', now)).toBe('vor 3 Minuten')
  expect(formatRelative('2026-10-08T12:00:00Z', now)).toBe('vorgestern')
  expect(formatRelative('2026-10-10T11:59:59Z', now)).toBe('gerade eben')
})
