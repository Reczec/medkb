import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { useState } from 'react'
import { useI18n } from '@/i18n/context'
import { I18nProvider } from '@/i18n/I18nProvider'
import { getApiLanguage } from '@/i18n/lang'
import { LanguageSwitch } from '@/i18n/LanguageSwitch'

function Probe() {
  const { lang, t, categoryLabel, docTypeLabel } = useI18n()
  return (
    <p data-testid="probe">
      {lang}|{t('notice.prototype')}|{categoryLabel('Kardiologie')}|{docTypeLabel('Diagnose')}|
      {categoryLabel('Unbekannt')}
    </p>
  )
}

beforeEach(() => {
  localStorage.clear()
  document.documentElement.lang = ''
})

it('starts in English', () => {
  render(
    <I18nProvider>
      <Probe />
    </I18nProvider>,
  )
  expect(screen.getByTestId('probe').textContent).toBe(
    'en|Prototype with example data – not medical advice.|Cardiology|Diagnosis|Unbekannt',
  )
  expect(document.documentElement.lang).toBe('en')
  expect(getApiLanguage()).toBe('en')
})

it('keeps the browser tab title in the interface language', () => {
  render(
    <I18nProvider lang="en">
      <Probe />
    </I18nProvider>,
  )
  expect(document.title).toBe('MedKB – Medical knowledge base')
  cleanup()
  render(
    <I18nProvider lang="de">
      <Probe />
    </I18nProvider>,
  )
  expect(document.title).toBe('MedKB – Medizinische Wissensdatenbank')
})

it('reads the stored choice', () => {
  localStorage.setItem('medkb:lang', 'de')
  render(
    <I18nProvider>
      <Probe />
    </I18nProvider>,
  )
  expect(screen.getByTestId('probe').textContent).toContain('de|Prototyp mit Beispieldaten')
  expect(document.documentElement.lang).toBe('de')
})

it('ignores a stored value it does not know', () => {
  localStorage.setItem('medkb:lang', 'fr')
  render(
    <I18nProvider>
      <Probe />
    </I18nProvider>,
  )
  expect(screen.getByTestId('probe').textContent).toContain('en|')
})

it('stores the choice, updates <html lang> and the API language', () => {
  render(
    <I18nProvider>
      <LanguageSwitch />
      <Probe />
    </I18nProvider>,
  )
  fireEvent.click(screen.getByRole('button', { name: /German/ }))
  expect(localStorage.getItem('medkb:lang')).toBe('de')
  expect(document.documentElement.lang).toBe('de')
  expect(getApiLanguage()).toBe('de')
  expect(screen.getByTestId('probe').textContent).toContain('de|Prototyp')
})

it('works when storage is blocked', () => {
  const blocked = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    throw new Error('blocked')
  })
  render(
    <I18nProvider>
      <LanguageSwitch />
      <Probe />
    </I18nProvider>,
  )
  act(() => {
    fireEvent.click(screen.getByRole('button', { name: /German/ }))
  })
  expect(screen.getByTestId('probe').textContent).toContain('de|')
  blocked.mockRestore()
})

it('a prop fixes the language without touching storage (tests)', () => {
  render(
    <I18nProvider lang="de">
      <Probe />
    </I18nProvider>,
  )
  expect(screen.getByTestId('probe').textContent).toContain('de|')
  expect(localStorage.getItem('medkb:lang')).toBeNull()
})

it('keeps the state of the page when the language changes', () => {
  function Form() {
    const [value, setValue] = useState('')
    return <input aria-label="draft" value={value} onChange={(e) => setValue(e.target.value)} />
  }
  render(
    <I18nProvider>
      <LanguageSwitch />
      <Form />
    </I18nProvider>,
  )
  fireEvent.change(screen.getByLabelText('draft'), { target: { value: 'unsaved text' } })
  fireEvent.click(screen.getByRole('button', { name: /German/ }))
  expect(screen.getByLabelText('draft')).toHaveValue('unsaved text')
})

it('marks the active language with aria-pressed', () => {
  render(
    <I18nProvider>
      <LanguageSwitch />
    </I18nProvider>,
  )
  expect(screen.getByRole('button', { name: /English/ })).toHaveAttribute('aria-pressed', 'true')
  expect(screen.getByRole('button', { name: /German/ })).toHaveAttribute('aria-pressed', 'false')
  expect(screen.getByRole('group', { name: 'Language' })).toBeInTheDocument()
})
