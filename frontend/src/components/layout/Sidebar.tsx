import { LayoutDashboard, Library, PanelLeftClose, PanelLeftOpen, ShieldCheck } from 'lucide-react'
import { motion } from 'motion/react'
import { NavLink, useLocation } from 'react-router'
import { BrandMark } from '@/components/layout/BrandMark'
import { ThemeToggle } from '@/components/layout/ThemeToggle'
import { cn } from '@/lib/utils'

const NAV = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/wissen', label: 'Wissensdatenbank', icon: Library, end: false },
  { to: '/admin', label: 'Admin', icon: ShieldCheck, end: false },
]

interface SidebarProps {
  collapsed?: boolean
  onToggleCollapsed?: () => void
  onNavigate?: () => void
  /** Separate layout ids so the desktop rail and the mobile drawer never share an animation. */
  layoutScope?: string
}

export function Sidebar({ collapsed = false, onToggleCollapsed, onNavigate, layoutScope = 'rail' }: SidebarProps) {
  const { pathname } = useLocation()

  return (
    <div className="flex h-full flex-col bg-rail text-rail-foreground">
      <div className={cn('flex h-16 items-center gap-3 px-4', collapsed && 'justify-center px-0')}>
        <BrandMark className="size-8 shrink-0 text-rail-foreground" />
        {!collapsed && (
          <div className="min-w-0 leading-tight">
            <div className="text-[15px] font-semibold tracking-tight">MedKB</div>
            <div className="truncate text-xs text-rail-muted">Medizinische Wissensdatenbank</div>
          </div>
        )}
      </div>

      <nav aria-label="Hauptnavigation" className="mt-4 flex flex-col gap-1 px-3">
        {NAV.map(({ to, label, icon: Icon, end }) => {
          const active = end ? pathname === to : pathname.startsWith(to)
          return (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={onNavigate}
              title={collapsed ? label : undefined}
              className={cn(
                'relative flex h-10 items-center gap-3 rounded-lg px-3 text-sm font-medium transition-colors duration-200',
                'focus-visible:ring-2 focus-visible:ring-rail-ring focus-visible:outline-none',
                active ? 'text-rail-foreground' : 'text-rail-muted hover:text-rail-foreground',
                collapsed && 'justify-center px-0',
              )}
            >
              {active && (
                <motion.span
                  layoutId={`${layoutScope}-nav-active`}
                  className="absolute inset-0 rounded-lg bg-rail-active"
                  transition={{ type: 'spring', stiffness: 480, damping: 40 }}
                >
                  <span className="absolute top-2 bottom-2 left-0 w-0.5 rounded-full bg-rail-accent" />
                </motion.span>
              )}
              <Icon className="relative size-[18px] shrink-0" aria-hidden />
              {!collapsed && <span className="relative truncate">{label}</span>}
            </NavLink>
          )
        })}
      </nav>

      <div className="mt-auto flex flex-col gap-3 border-t border-rail-border p-3">
        {!collapsed && (
          <p className="px-1 text-[11px] leading-snug text-rail-muted">
            Prototyp mit Beispieldaten – keine medizinische Beratung.
          </p>
        )}
        <div className={cn('flex items-center gap-2', collapsed && 'flex-col')}>
          <ThemeToggle className={cn(collapsed ? 'w-full flex-col' : 'flex-1')} />
          {onToggleCollapsed && (
            <button
              type="button"
              onClick={onToggleCollapsed}
              aria-label={collapsed ? 'Seitenleiste ausklappen' : 'Seitenleiste einklappen'}
              title={collapsed ? 'Ausklappen' : 'Einklappen'}
              className="flex size-8 shrink-0 items-center justify-center rounded-lg text-rail-muted transition-colors hover:bg-rail-active hover:text-rail-foreground focus-visible:ring-2 focus-visible:ring-rail-ring focus-visible:outline-none"
            >
              {collapsed ? <PanelLeftOpen className="size-4" /> : <PanelLeftClose className="size-4" />}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
