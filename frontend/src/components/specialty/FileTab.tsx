import { categoryStyle } from '@/lib/categories'
import { cn } from '@/lib/utils'

interface FileTabProps {
  name: string
  className?: string
  size?: 'sm' | 'md'
}

/** The labelled filing tab that sits on top of a record sheet and names its specialty. */
export function FileTab({ name, className, size = 'sm' }: FileTabProps) {
  const style = categoryStyle(name)
  const Icon = style.icon
  return (
    <span
      data-testid="file-tab"
      className={cn(
        'relative inline-flex max-w-full items-center gap-1.5 overflow-hidden rounded-t-lg border border-b-0 font-semibold text-foreground',
        size === 'sm' ? 'h-7 px-2.5 text-xs' : 'h-9 px-3.5 text-sm',
        className,
      )}
      style={{
        background: `color-mix(in oklab, ${style.color} 16%, var(--card))`,
        borderColor: `color-mix(in oklab, ${style.color} 35%, var(--border))`,
      }}
    >
      <span className="absolute inset-x-0 top-0 h-[3px]" style={{ background: style.color }} aria-hidden />
      <Icon className={cn('shrink-0', size === 'sm' ? 'size-3.5' : 'size-4')} style={{ color: style.color }} aria-hidden />
      <span className="truncate">{name}</span>
    </span>
  )
}
