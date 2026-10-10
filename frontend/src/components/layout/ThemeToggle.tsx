import { Monitor, Moon, Sun } from 'lucide-react'
import { motion } from 'motion/react'
import { useTheme, type Theme } from '@/lib/theme'
import { cn } from '@/lib/utils'

const options: { value: Theme; label: string; icon: typeof Sun }[] = [
  { value: 'light', label: 'Hell', icon: Sun },
  { value: 'dark', label: 'Dunkel', icon: Moon },
  { value: 'system', label: 'System', icon: Monitor },
]

/** `rail` sits on the petrol navigation rail; `surface` on the normal work area. */
export function ThemeToggle({
  className,
  tone = 'rail',
}: {
  className?: string
  tone?: 'rail' | 'surface'
}) {
  const { theme, setTheme } = useTheme()
  const surface = tone === 'surface'
  return (
    <div
      role="radiogroup"
      aria-label="Farbschema"
      className={cn('relative flex rounded-lg p-0.5', surface ? 'border bg-muted' : 'bg-rail-well', className)}
    >
      {options.map(({ value, label, icon: Icon }) => {
        const active = theme === value
        return (
          <button
            key={value}
            type="button"
            role="radio"
            aria-checked={active}
            aria-label={label}
            title={label}
            onClick={() => setTheme(value)}
            className={cn(
              'relative z-10 flex h-7 flex-1 items-center justify-center rounded-md transition-colors duration-200',
              'focus-visible:ring-2 focus-visible:outline-none',
              surface
                ? cn('focus-visible:ring-ring', active ? 'text-foreground' : 'text-muted-foreground hover:text-foreground')
                : cn('focus-visible:ring-rail-ring', active ? 'text-rail-foreground' : 'text-rail-muted hover:text-rail-foreground'),
            )}
          >
            {active && (
              <motion.span
                layoutId="theme-pill"
                className={cn('absolute inset-0 -z-10 rounded-md shadow-sm', surface ? 'bg-card' : 'bg-rail-active')}
                transition={{ type: 'spring', stiffness: 520, damping: 40 }}
              />
            )}
            <Icon className="size-3.5" aria-hidden />
          </button>
        )
      })}
    </div>
  )
}
