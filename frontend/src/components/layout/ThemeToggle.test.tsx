import { fireEvent, render, screen } from '@testing-library/react'
import { ThemeToggle } from '@/components/layout/ThemeToggle'

it('switches to dark and remembers the choice', () => {
  render(<ThemeToggle />)
  fireEvent.click(screen.getByRole('radio', { name: 'Dunkel' }))
  expect(document.documentElement.classList.contains('dark')).toBe(true)
  expect(localStorage.getItem('theme')).toBe('dark')
  expect(screen.getByRole('radio', { name: 'Dunkel' })).toHaveAttribute('aria-checked', 'true')
})

it('switches back to light', () => {
  localStorage.setItem('theme', 'dark')
  render(<ThemeToggle />)
  fireEvent.click(screen.getByRole('radio', { name: 'Hell' }))
  expect(document.documentElement.classList.contains('dark')).toBe(false)
})
