import { render, screen } from '@testing-library/react'
import { Suspense } from 'react'
import { loadPage, RELOAD_FLAG } from '@/lib/lazyPage'

afterEach(() => {
  sessionStorage.clear()
  vi.restoreAllMocks()
})

it('resolves the named export of a page module', async () => {
  const Page = () => <p>Seite</p>
  const { default: Component } = await loadPage(async () => ({ Page }), 'Page')
  render(
    <Suspense fallback={null}>
      <Component />
    </Suspense>,
  )
  expect(screen.getByText('Seite')).toBeInTheDocument()
})

it('reloads once when a chunk is gone after a new deploy', async () => {
  const reload = vi.fn()
  const pending = loadPage(() => Promise.reject(new TypeError('Failed to fetch module')), 'Page', reload)
  await Promise.race([pending, new Promise((resolve) => setTimeout(resolve, 20))])
  expect(reload).toHaveBeenCalledTimes(1)
  expect(sessionStorage.getItem(RELOAD_FLAG)).toBe('1')
})

it('shows the error instead of reloading again', async () => {
  sessionStorage.setItem(RELOAD_FLAG, '1')
  const reload = vi.fn()
  await expect(
    loadPage(() => Promise.reject(new TypeError('Failed to fetch module')), 'Page', reload),
  ).rejects.toThrow('Failed to fetch module')
  expect(reload).not.toHaveBeenCalled()
  expect(sessionStorage.getItem(RELOAD_FLAG)).toBeNull()
})
