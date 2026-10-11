import { render, screen } from '@testing-library/react'
import { AIText } from '@/features/ai/AIText'

it('renders headings, bold terms and lists instead of raw markdown', () => {
  const { container } = render(
    <AIText
      text={'Migräne ist ein **anfallsartiger** Kopfschmerz.\n\n### Sofort Notruf 144\n- Lähmungen\n* Sprachstörung\n\nZweiter Absatz.'}
    />,
  )
  expect(screen.getByText('anfallsartiger').tagName).toBe('STRONG')
  expect(screen.getByText('Sofort Notruf 144').tagName).toBe('P')
  expect(screen.getAllByRole('listitem').map((li) => li.textContent)).toEqual(['Lähmungen', 'Sprachstörung'])
  expect(screen.getByText('Zweiter Absatz.')).toBeInTheDocument()
  expect(container.textContent).not.toMatch(/\*\*|###/)
})

it('never turns model output into HTML', () => {
  const { container } = render(<AIText text={'<img src=x onerror=alert(1)> **<b>fett</b>**'} />)
  expect(container.querySelector('img')).toBeNull()
  expect(container.querySelector('b')).toBeNull()
  expect(container.textContent).toContain('<img src=x onerror=alert(1)>')
})

it('drops separator lines and keeps citation markers', () => {
  const { container } = render(<AIText text={'Ruhe hilft [1].\n\n---\n\nEnde.'} />)
  expect(container.textContent).not.toContain('---')
  expect(screen.getByText('Ruhe hilft [1].')).toBeInTheDocument()
})

it('keeps an unfinished bold marker readable while streaming', () => {
  const { container } = render(<AIText text={'Das ist **halb'} />)
  expect(container.textContent).toBe('Das ist halb')
})
