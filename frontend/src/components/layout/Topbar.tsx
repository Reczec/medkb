import { Menu, Plus, Search } from 'lucide-react'
import { Link } from 'react-router'
import { openCommandPalette } from '@/components/layout/CommandPalette'
import { Button } from '@/components/ui/button'

export function Topbar({ onOpenMenu }: { onOpenMenu: () => void }) {
  const isMac = typeof navigator !== 'undefined' && /Mac/i.test(navigator.platform)
  return (
    <header className="sticky top-0 z-30 border-b bg-background/85 backdrop-blur-md supports-[backdrop-filter]:bg-background/70">
      <div className="mx-auto flex h-16 max-w-[1320px] items-center gap-3 px-4 sm:px-6 lg:px-10">
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={onOpenMenu}
          aria-label="Menü öffnen"
        >
          <Menu />
        </Button>

        <button
          type="button"
          onClick={openCommandPalette}
          className="group flex h-10 w-full max-w-md items-center gap-2.5 rounded-lg border bg-card px-3 text-sm text-muted-foreground shadow-sheet transition-[border-color,box-shadow] duration-200 hover:border-primary/40 hover:shadow-lift focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none"
        >
          <Search className="size-4 shrink-0" aria-hidden />
          <span className="truncate">Einträge, Symptome, Diagnosen suchen…</span>
          <kbd className="ml-auto hidden shrink-0 rounded border bg-muted px-1.5 py-0.5 font-sans text-[11px] text-muted-foreground sm:inline">
            {isMac ? '⌘' : 'Strg'} K
          </kbd>
        </button>

        <Button asChild className="ml-auto shrink-0">
          <Link to="/wissen/neu">
            <Plus aria-hidden />
            <span className="hidden sm:inline">Neuer Eintrag</span>
            <span className="sr-only sm:hidden">Neuer Eintrag</span>
          </Link>
        </Button>
      </div>
    </header>
  )
}
