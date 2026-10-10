import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { RouteError } from '@/features/RouteError'

function Boom(): never {
  throw new Error('kaputt')
}

it('shows a friendly error instead of a stack trace', async () => {
  vi.spyOn(console, 'error').mockImplementation(() => {})
  const router = createMemoryRouter([{ path: '/', element: <Boom />, errorElement: <RouteError /> }])
  render(<RouterProvider router={router} />)
  expect(await screen.findByText('Diese Ansicht ist abgestürzt')).toBeInTheDocument()
  expect(screen.getByText('kaputt')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /Neu laden/ })).toBeInTheDocument()
})
