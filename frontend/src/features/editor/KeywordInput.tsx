import { X } from 'lucide-react'
import { useState } from 'react'
import { cn } from '@/lib/utils'

export const MAX_KEYWORDS = 20
export const MAX_KEYWORD_LENGTH = 50

interface KeywordInputProps {
  value: string[]
  onChange: (value: string[]) => void
  id?: string
  className?: string
}

/** Adds keywords not yet in `list` (case-insensitive), stopping at MAX_KEYWORDS. */
export function mergeKeywords(list: string[], additions: string[]): string[] {
  const result = [...list]
  const seen = new Set(list.map((k) => k.toLowerCase()))
  for (const raw of additions) {
    const word = raw.trim().slice(0, MAX_KEYWORD_LENGTH)
    if (!word || seen.has(word.toLowerCase()) || result.length >= MAX_KEYWORDS) continue
    seen.add(word.toLowerCase())
    result.push(word)
  }
  return result
}

export function KeywordInput({ value, onChange, id, className }: KeywordInputProps) {
  const [draft, setDraft] = useState('')
  const full = value.length >= MAX_KEYWORDS

  const commit = (words: string[]) => {
    const next = mergeKeywords(value, words)
    if (next.length !== value.length) onChange(next)
  }

  const handleChange = (text: string) => {
    if (!text.includes(',')) {
      setDraft(text)
      return
    }
    const parts = text.split(',')
    commit(parts.slice(0, -1))
    setDraft(parts.at(-1)?.trimStart() ?? '')
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      commit([draft])
      if (!full) setDraft('')
    } else if (event.key === 'Backspace' && draft === '' && value.length > 0) {
      onChange(value.slice(0, -1))
    }
  }

  return (
    <div className={className}>
      <div
        className={cn(
          'flex min-h-11 flex-wrap items-center gap-1.5 rounded-lg border bg-card px-2 py-1.5 shadow-xs transition-[border-color,box-shadow]',
          'focus-within:border-ring focus-within:ring-3 focus-within:ring-ring/30',
        )}
      >
        {value.length > 0 && (
          <ul className="contents">
            {value.map((keyword) => (
              <li
                key={keyword}
                className="inline-flex h-7 max-w-full items-center gap-1 rounded-md bg-muted pr-1 pl-2 text-sm"
              >
                <span className="truncate">{keyword}</span>
                <button
                  type="button"
                  onClick={() => onChange(value.filter((k) => k !== keyword))}
                  aria-label={`${keyword} entfernen`}
                  className="flex size-5 items-center justify-center rounded text-muted-foreground hover:bg-background hover:text-foreground"
                >
                  <X className="size-3.5" aria-hidden />
                  <span className="sr-only">entfernen</span>
                </button>
              </li>
            ))}
          </ul>
        )}
        <input
          id={id}
          type="text"
          value={draft}
          onChange={(event) => handleChange(event.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => {
            if (draft.trim()) {
              commit([draft])
              setDraft('')
            }
          }}
          aria-label="Schlagwort hinzufügen"
          placeholder={value.length === 0 ? 'Enter oder Komma fügt hinzu' : ''}
          maxLength={MAX_KEYWORD_LENGTH}
          className="h-7 min-w-32 flex-1 bg-transparent px-1 text-sm outline-none placeholder:text-muted-foreground"
        />
      </div>
      <p className="mt-1.5 text-xs text-muted-foreground">
        {full
          ? `Maximal ${MAX_KEYWORDS} Schlagwörter erreicht.`
          : 'Leer lassen, dann werden Schlagwörter automatisch erzeugt.'}
      </p>
    </div>
  )
}
