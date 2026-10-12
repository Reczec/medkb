import { Menu, Plus, Search } from 'lucide-react'
import { Link } from 'react-router'
import { openCommandPalette } from '@/components/layout/CommandPalette'
import { useAuth } from '@/features/auth/context'
import { useI18n } from '@/i18n/context'
import { Button } from '@/components/ui/button'

export function Topbar({ onOpenMenu }: { onOpenMenu: () => void }) {
  const { user } = useAuth()
  const { t } = useI18n()
  const isMac = typeof navigator !== 'undefined' && /Mac/i.test(navigator.platform)
  return (
    <header className="sticky top-0 z-30 border-b bg-background/85 backdrop-blur-md supports-[backdrop-filter]:bg-background/70">
      <div className="mx-auto flex h-16 max-w-[1320px] items-center gap-3 px-4 sm:px-6 lg:px-10">
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={onOpenMenu}
          aria-label={t('nav.openMenu')}
        >
          <Menu />
        </Button>

        <button
          type="button"
          onClick={openCommandPalette}
          className="group flex h-10 w-full max-w-md min-w-0 items-center gap-2.5 rounded-lg border bg-card px-3 text-sm text-muted-foreground shadow-sheet transition-[border-color,box-shadow] duration-200 hover:border-primary/40 hover:shadow-lift focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none"
        >
          <Search className="size-4 shrink-0" aria-hidden />
          <span className="truncate">{t('search.placeholder')}</span>
          <kbd className="ml-auto hidden shrink-0 rounded border bg-muted px-1.5 py-0.5 font-sans text-[11px] text-muted-foreground sm:inline">
            {isMac ? '⌘' : t('shortcut.ctrl')} K
          </kbd>
        </button>

        {user?.role === 'admin' && (
        <Button asChild className="ml-auto shrink-0">
          <Link to="/wissen/neu">
            <Plus aria-hidden />
            <span className="hidden sm:inline">{t('action.newEntry')}</span>
            <span className="sr-only sm:hidden">{t('action.newEntry')}</span>
          </Link>
        </Button>
        )}
      </div>
    </header>
  )
}
