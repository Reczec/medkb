import { toScoreBars } from '@/lib/scores'

it('sorts, normalises and drops zero scores', () => {
  expect(toScoreBars({ HNO: 2, Kardiologie: 8, Neurologie: 0, Dermatologie: 4 })).toEqual([
    { name: 'Kardiologie', score: 8, share: 1 },
    { name: 'Dermatologie', score: 4, share: 0.5 },
    { name: 'HNO', score: 2, share: 0.25 },
  ])
})

it('returns an empty list when every score is 0', () => {
  expect(toScoreBars({ HNO: 0 })).toEqual([])
})

it('keeps at most max entries', () => {
  const scores = { A: 6, B: 5, C: 4, D: 3, E: 2, F: 1 }
  expect(toScoreBars(scores).map((b) => b.name)).toEqual(['A', 'B', 'C', 'D', 'E'])
  expect(toScoreBars(scores, 2)).toHaveLength(2)
})
