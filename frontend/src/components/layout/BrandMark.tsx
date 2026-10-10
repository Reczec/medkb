import { categoryStyle } from '@/lib/categories'

/** Three staggered filing tabs: the specialty colour system in miniature. */
export function BrandMark({ className }: { className?: string }) {
  const tabs = ['Kardiologie', 'Allgemeinmedizin', 'Neurologie'].map((c) => categoryStyle(c).color)
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden>
      <rect x="4" y="4" width="8" height="7" rx="2" fill={tabs[0]} />
      <rect x="12.5" y="2" width="8" height="9" rx="2" fill={tabs[1]} />
      <rect x="21" y="5" width="7" height="6" rx="2" fill={tabs[2]} />
      <rect x="3" y="9" width="26" height="20" rx="4" fill="currentColor" opacity="0.9" />
      <path
        d="M16 13.5v11M10.5 19h11"
        stroke="var(--rail)"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  )
}
