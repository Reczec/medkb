import { cn } from '@/lib/utils'

it('joins class names and drops falsy values', () => {
  expect(cn('a', false, null, undefined, 'c')).toBe('a c')
})

it('lets later tailwind classes win', () => {
  expect(cn('px-2', 'px-4')).toBe('px-4')
})
