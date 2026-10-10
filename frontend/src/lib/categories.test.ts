import { Stethoscope } from 'lucide-react'
import { KNOWN_CATEGORIES, categoryStyle } from '@/lib/categories'

it('has a distinct colour for every known category', () => {
  expect(KNOWN_CATEGORIES).toHaveLength(9)
  const colours = KNOWN_CATEGORIES.map((name) => categoryStyle(name).color)
  expect(new Set(colours).size).toBe(9)
})

it('falls back for unknown categories', () => {
  const style = categoryStyle('Xyz')
  expect(style.icon).toBe(Stethoscope)
  expect(style.color).toBe(categoryStyle('Auch unbekannt').color)
})
