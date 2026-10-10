import { CornerDownLeft, FilePlus2, LayoutDashboard, Library, SunMoon } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command'
import { useAuth } from '@/features/auth/context'
import { useDebounced } from '@/hooks/useDebounced'
import { categoryStyle } from '@/lib/categories'
import { useDocuments } from '@/lib/queries'
import { storeTheme } from '@/lib/theme'

const OPEN_EVENT = 'medkb:command-palette'

/** Opens the palette from anywhere (e.g. the search field in the top bar). */
export function openCommandPalette() {
  window.dispatchEvent(new Event(OPEN_EVENT))
}

export function CommandPalette() {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const debounced = useDebounced(query, 200)
  const navigate = useNavigate()
  const { user } = useAuth()
  const { data, isFetching } = useDocuments({ q: debounced, limit: 8 }, open)

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key.toLowerCase() === 'k' && (event.ctrlKey || event.metaKey)) {
        event.preventDefault()
        setOpen((value) => !value)
      }
    }
    const onOpen = () => setOpen(true)
    window.addEventListener('keydown', onKey)
    window.addEventListener(OPEN_EVENT, onOpen)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener(OPEN_EVENT, onOpen)
    }
  }, [])

  const close = () => {
    setOpen(false)
    setQuery('')
  }

  const go = (path: string) => {
    close()
    navigate(path)
  }

  const toggleTheme = () => {
    storeTheme(document.documentElement.classList.contains('dark') ? 'light' : 'dark')
    close()
  }

  return (
    <CommandDialog
      open={open}
      onOpenChange={(next) => (next ? setOpen(true) : close())}
      title="Befehlspalette"
      description="Einträge suchen und Aktionen ausführen"
    >
      <Command shouldFilter={false}>
        <CommandInput placeholder="Einträge durchsuchen…" value={query} onValueChange={setQuery} />
        <CommandList>
          <CommandEmpty>{isFetching ? 'Suche läuft…' : 'Keine Einträge gefunden.'}</CommandEmpty>
          {data && data.items.length > 0 && (
            <CommandGroup heading={debounced.trim() ? 'Treffer' : 'Zuletzt geändert'}>
              {data.items.map((doc) => (
                <CommandItem
                  key={doc.id}
                  value={`doc-${doc.id}`}
                  onSelect={() => go(`/wissen/${doc.id}`)}
                >
                  <span
                    className="size-2 shrink-0 rounded-full"
                    style={{ background: categoryStyle(doc.category).color }}
                    aria-hidden
                  />
                  <span className="truncate">{doc.title}</span>
                  <span className="ml-auto shrink-0 text-xs text-muted-foreground">
                    {doc.category}
                  </span>
                </CommandItem>
              ))}
            </CommandGroup>
          )}
          <CommandSeparator />
          <CommandGroup heading="Aktionen">
            {user?.role === 'admin' && (
              <CommandItem value="action-new" onSelect={() => go('/wissen/neu')}>
                <FilePlus2 /> Neuer Eintrag
              </CommandItem>
            )}
            <CommandItem value="action-list" onSelect={() => go('/wissen')}>
              <Library /> Wissensdatenbank öffnen
            </CommandItem>
            <CommandItem value="action-dashboard" onSelect={() => go('/')}>
              <LayoutDashboard /> Zum Dashboard
            </CommandItem>
            <CommandItem value="action-theme" onSelect={toggleTheme}>
              <SunMoon /> Hell / Dunkel wechseln
            </CommandItem>
          </CommandGroup>
        </CommandList>
        <div className="flex items-center gap-3 border-t px-3 py-2 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1">
            <CornerDownLeft className="size-3" aria-hidden /> öffnen
          </span>
          <span>Esc schließen</span>
        </div>
      </Command>
    </CommandDialog>
  )
}
