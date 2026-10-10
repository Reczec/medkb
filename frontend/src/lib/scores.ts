export interface ScoreBar {
  name: string
  score: number
  /** Score relative to the best category (0–1). */
  share: number
}

/** Classifier scores → bars for display: best first, zeros dropped, at most `max`. */
export function toScoreBars(scores: Record<string, number>, max = 5): ScoreBar[] {
  const ranked = Object.entries(scores)
    .filter(([, score]) => score > 0)
    .sort(([, a], [, b]) => b - a)
    .slice(0, max)
  const best = ranked[0]?.[1] ?? 0
  return ranked.map(([name, score]) => ({ name, score, share: score / best }))
}
