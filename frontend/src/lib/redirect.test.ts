import { safeNext } from '@/lib/redirect'

it.each([
  ['/wissen', '/wissen'],
  ['/wissen?category=HNO#top', '/wissen?category=HNO#top'],
  [null, '/'],
  ['', '/'],
  ['https://evil.example', '/'],
  ['//evil.example', '/'],
  ['/\\evil.example', '/'],
  ['/%5Cevil.example', '/%5Cevil.example'],
  ['/\t/evil.example', '/'],
  ['javascript:alert(1)', '/'],
])('safeNext(%j) → %j', (input, expected) => {
  expect(safeNext(input)).toBe(expected)
})
