import { screen } from '@testing-library/react'
import { LanguageSwitch } from '@/i18n/LanguageSwitch'
import { renderWithProviders } from '@/test/utils'

it.each(['en', 'de'] as const)('keeps the visible code inside the accessible name (%s)', (lang) => {
  renderWithProviders(<LanguageSwitch tone="surface" />, { lang })
  for (const code of ['EN', 'DE']) {
    const button = screen.getByText(code).closest('button')!
    expect(button.getAttribute('aria-label')).toContain(code)
    expect(button).not.toHaveAttribute('lang')
  }
})
