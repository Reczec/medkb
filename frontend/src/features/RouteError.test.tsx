import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { RouteError } from '@/features/RouteError'
import { I18nProvider } from '@/i18n/I18nProvider'

function Boom(): never {
  throw new Error('kaputt')
}

it('shows a friendly error instead of a stack trace', async () => {
  vi.spyOn(console, 'error').mockImplementation(() => {})
  const router = createMemoryRouter([{ path: '/', element: <Boom />, errorElement: <RouteError /> }])
  render(
    <I18nProvider lang="de">
      <RouterProvider router={router} />
    </I18nProvider>,
  )
  expect(await screen.findByText('Diese Ansicht ist abgestürzt')).toBeInTheDocument()
  expect(screen.getByText('kaputt')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Neu laden/ })).toBeInTheDocument()
})
