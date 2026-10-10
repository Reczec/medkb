import { act, renderHook } from '@testing-library/react'
import { useDebounced } from '@/hooks/useDebounced'

it('only updates after the delay', () => {
  vi.useFakeTimers()
  const { result, rerender } = renderHook(({ value }) => useDebounced(value, 300), {
    initialProps: { value: 'a' },
  })
  rerender({ value: 'ab' })
  expect(result.current).toBe('a')
  act(() => vi.advanceTimersByTime(300))
  expect(result.current).toBe('ab')
  vi.useRealTimers()
})
