import { render, screen, within } from '@testing-library/react'
import { SectionedContent } from '@/features/documents/SectionedContent'

it('renders the sections in their fixed order and skips empty ones', () => {
  render(
    <SectionedContent
      sections={{ therapy: 'Ruhe.', definition: 'Kopfschmerz.', causes: '  ', symptoms: null }}
    />,
  )
  const headings = screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent)
  expect(headings).toEqual(['Definition', 'Therapie'])
  expect(screen.getByText('Kopfschmerz.')).toBeInTheDocument()
})

it('sets the warning signs apart and points to the emergency number', () => {
  render(
    <SectionedContent
      sections={{ definition: 'Text.', red_flags: 'Lähmungen: sofort Notruf 144.' }}
    />,
  )
  const warning = screen.getByRole('region', { name: 'Warnzeichen' })
  expect(within(warning).getByText('Lähmungen: sofort Notruf 144.')).toBeInTheDocument()
  expect(within(warning).getByText('Im Notfall: 144')).toBeInTheDocument()
})

it('leaves out the emergency line when the warning signs do not mention 144', () => {
  render(<SectionedContent sections={{ red_flags: 'Rasch zum Arzt.' }} />)
  const warning = screen.getByRole('region', { name: 'Warnzeichen' })
  expect(within(warning).queryByText('Im Notfall: 144')).not.toBeInTheDocument()
})
