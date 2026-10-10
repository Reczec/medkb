import { useEffect, useState } from 'react'
import { useLocation } from 'react-router'
import { CommandPalette } from '@/components/layout/CommandPalette'
import { PageTransition } from '@/components/layout/PageTransition'
import { Sidebar } from '@/components/layout/Sidebar'
import { Topbar } from '@/components/layout/Topbar'
import { Sheet, SheetContent, SheetDescription, SheetTitle } from '@/components/ui/sheet'
import { cn } from '@/lib/utils'

const COLLAPSE_KEY = 'sidebar'

function readCollapsed() {
  try {
    return localStorage.getItem(COLLAPSE_KEY) === 'collapsed'
  } catch {
    return false
  }
}

export function AppShell() {
  const [collapsed, setCollapsed] = useState(readCollapsed)
  const [menuOpen, setMenuOpen] = useState(false)
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo({ top: 0 })
  }, [pathname])

  const toggleCollapsed = () => {
    setCollapsed((value) => {
      try {
        localStorage.setItem(COLLAPSE_KEY, value ? 'expanded' : 'collapsed')
      } catch {
        // ignore
      }
      return !value
    })
  }

  return (
    <div className="flex min-h-dvh">
      <aside
        className={cn(
          'sticky top-0 hidden h-dvh shrink-0 transition-[width] duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] md:block',
          collapsed ? 'w-[72px]' : 'w-[248px]',
        )}
      >
        <Sidebar collapsed={collapsed} onToggleCollapsed={toggleCollapsed} />
      </aside>

      <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
        <SheetContent side="left" className="w-[272px] border-0 p-0" showCloseButton={false}>
          <SheetTitle className="sr-only">Navigation</SheetTitle>
          <SheetDescription className="sr-only">Hauptnavigation von MedKB</SheetDescription>
          <Sidebar layoutScope="drawer" onNavigate={() => setMenuOpen(false)} />
        </SheetContent>
      </Sheet>

      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar onOpenMenu={() => setMenuOpen(true)} />
        <main className="mx-auto w-full max-w-[1320px] flex-1 px-4 py-6 sm:px-6 sm:py-8 lg:px-10">
          <PageTransition />
        </main>
        <footer className="mx-auto w-full max-w-[1320px] px-4 pb-6 text-xs text-muted-foreground sm:px-6 lg:px-10">
          Prototyp mit Beispieldaten – keine medizinische Beratung. Inhalte auf Lehrbuchniveau, keine
          Patientendaten.
        </footer>
      </div>

      <CommandPalette />
    </div>
  )
}
