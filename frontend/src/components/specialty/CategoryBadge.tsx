import { categoryStyle } from '@/lib/categories'
import { cn } from '@/lib/utils'

export function CategoryBadge({ name, className }: { name: string; className?: string }) {
  const style = categoryStyle(name)
  return (
    <span
      className={cn(
        'inline-flex h-6 shrink-0 items-center gap-1.5 rounded-md px-2 text-xs font-medium',
        className,
      )}
      style={{ background: style.soft, color: `color-mix(in oklch, ${style.color} 70%, var(--foreground))` }}
    >
      <span className="size-1.5 rounded-full" style={{ background: style.color }} aria-hidden />
      {name}
    </span>
  )
}
