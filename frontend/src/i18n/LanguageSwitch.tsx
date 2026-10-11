import { useI18n } from '@/i18n/context'
import { LANGS } from '@/i18n/lang'
import { cn } from '@/lib/utils'

/** `rail` sits on the petrol navigation rail; `surface` on the normal work area. */
export function LanguageSwitch({
  className,
  tone = 'rail',
}: {
  className?: string
  tone?: 'rail' | 'surface'
}) {
  const { lang, setLang, t } = useI18n()
  const surface = tone === 'surface'
  return (
    <div
      role="group"
      aria-label={t('lang.switch')}
      className={cn('flex rounded-lg p-0.5', surface ? 'border bg-muted' : 'bg-rail-well', className)}
    >
      {LANGS.map((code) => {
        const active = lang === code
        return (
          <button
            key={code}
            type="button"
            lang={code}
            aria-pressed={active}
            aria-label={t(`lang.${code}`)}
            title={t(`lang.${code}`)}
            onClick={() => setLang(code)}
            className={cn(
              'flex h-7 flex-1 items-center justify-center rounded-md px-2 text-xs font-semibold tracking-wide transition-colors duration-200',
              'focus-visible:ring-2 focus-visible:outline-none',
              surface
                ? cn(
                    'focus-visible:ring-ring',
                    active ? 'bg-card text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground',
                  )
                : cn(
                    'focus-visible:ring-rail-ring',
                    active
                      ? 'bg-rail-active text-rail-foreground shadow-sm'
                      : 'text-rail-muted hover:text-rail-foreground',
                  ),
            )}
          >
            {code.toUpperCase()}
          </button>
        )
      })}
    </div>
  )
}
