import { screen } from '@testing-library/react'
import { CountUp } from '@/components/motion/CountUp'
import { renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

it('shows the final value immediately with reduced motion', () => {
  renderWithProviders(<CountUp value={42} />)
  expect(screen.getByText('42')).toBeInTheDocument()
})

it('formats with the given suffix', () => {
  renderWithProviders(<CountUp value={75} suffix=" %" />)
  expect(screen.getByText('75 %')).toBeInTheDocument()
})
