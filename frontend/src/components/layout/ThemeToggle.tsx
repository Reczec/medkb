import { Monitor, Moon, Sun } from 'lucide-react'
import { motion } from 'motion/react'
import { useTheme, type Theme } from '@/lib/theme'
import { cn } from '@/lib/utils'

const options: { value: Theme; label: string; icon: typeof Sun }[] = [
  { value: 'light', label: 'Hell', icon: Sun },
  { value: 'dark', label: 'Dunkel', icon: Moon },
  { value: 'system', label: 'System', icon: Monitor },
]

export function ThemeToggle({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme()
  return (
    <div
      role="radiogroup"
      aria-label="Farbschema"
      className={cn('relative flex rounded-lg bg-rail-well p-0.5', className)}
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
              'focus-visible:ring-2 focus-visible:ring-rail-ring focus-visible:outline-none',
              active ? 'text-rail-foreground' : 'text-rail-muted hover:text-rail-foreground',
            )}
          >
            {active && (
              <motion.span
                layoutId="theme-pill"
                className="absolute inset-0 -z-10 rounded-md bg-rail-active shadow-sm"
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
