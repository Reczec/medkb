import { fireEvent, render, screen } from '@testing-library/react'
import { useState } from 'react'
import { KeywordInput } from '@/features/editor/KeywordInput'

function Harness({ initial = [] as string[] }) {
  const [value, setValue] = useState(initial)
  return <KeywordInput value={value} onChange={setValue} />
}

const input = () => screen.getByRole('textbox', { name: 'Schlagwort hinzufügen' })
const chips = () =>
  screen.queryAllByRole('listitem').map((li) => li.textContent?.replace('entfernen', '').trim())

it('adds keywords on comma and Enter and ignores duplicates', () => {
  render(<Harness />)
  fireEvent.change(input(), { target: { value: 'Fieber, fieber, Husten' } })
  fireEvent.keyDown(input(), { key: 'Enter' })
  expect(chips()).toEqual(['Fieber', 'Husten'])
  expect(input()).toHaveValue('')
})

it('removes the last keyword with Backspace in an empty field', () => {
  render(<Harness initial={['A', 'B']} />)
  fireEvent.keyDown(input(), { key: 'Backspace' })
  expect(chips()).toEqual(['A'])
})

it('stops at 20 keywords', () => {
  render(<Harness initial={Array.from({ length: 20 }, (_, i) => `W${i}`)} />)
  fireEvent.change(input(), { target: { value: 'Neu' } })
  fireEvent.keyDown(input(), { key: 'Enter' })
  expect(chips()).toHaveLength(20)
  expect(screen.getByText(/Maximal 20 Schlagwörter/)).toBeInTheDocument()
})

it('removes a keyword with its button', () => {
  render(<Harness initial={['A', 'B']} />)
  fireEvent.click(screen.getByRole('button', { name: 'A entfernen' }))
  expect(chips()).toEqual(['B'])
})
