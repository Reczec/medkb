import { categoryStyle, KNOWN_CATEGORIES } from '@/lib/categories'

const SPECIALTIES = [
  'HNO', 'Augenheilkunde', 'Neurologie', 'Kardiologie', 'Pneumologie', 'Gastroenterologie',
  'Endokrinologie', 'Urologie', 'Gynäkologie', 'Dermatologie', 'Orthopädie', 'Pädiatrie',
  'Psychiatrie', 'Infektiologie', 'Innere Medizin', 'Allgemeinmedizin',
]

/** oklch(L C H) -> [L, C, H] */
function parse(color: string): [number, number, number] {
  const match = /oklch\(([\d.]+) ([\d.]+) ([\d.]+)\)/.exec(color)
  if (!match) throw new Error(`not an oklch colour: ${color}`)
  return [Number(match[1]), Number(match[2]), Number(match[3])]
}

it('knows the 16 specialties in the backend tie order', () => {
  expect(KNOWN_CATEGORIES).toEqual(SPECIALTIES)
})

it('gives every specialty the same lightness (Equal Weight)', () => {
  for (const name of SPECIALTIES) expect(parse(categoryStyle(name).color)[0]).toBe(0.62)
})

it('keeps neighbouring hues at least 20° apart', () => {
  const hues = SPECIALTIES.map((name) => parse(categoryStyle(name).color)[2]).sort((a, b) => a - b)
  expect(new Set(hues).size).toBe(16)
  const gaps = hues.map((hue, i) => (i === 0 ? hue + 360 - hues.at(-1)! : hue - hues[i - 1]))
  expect(Math.min(...gaps)).toBeGreaterThanOrEqual(20)
})
