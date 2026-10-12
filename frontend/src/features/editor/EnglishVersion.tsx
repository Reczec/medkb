import { ChevronRight } from 'lucide-react'
import { useId, useState } from 'react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Field } from '@/features/editor/Field'
import { KeywordInput } from '@/features/editor/KeywordInput'
import { SectionFields } from '@/features/editor/SectionFields'
import { useI18n } from '@/i18n/context'
import type { Sections } from '@/lib/types'
import { cn } from '@/lib/utils'

export interface EnglishFields {
  titleEn: string
  contentEn: string
  sectionsEn: Sections
  keywordsEn: string[]
}

interface EnglishVersionProps {
  value: EnglishFields
  /** Follows the German text: sections or free text. */
  mode: 'text' | 'sections'
  onChange: (patch: Partial<EnglishFields>) => void
  defaultOpen: boolean
}

/**
 * Optional English text of an entry. The classifier never reads it; the fields start collapsed
 * unless the entry already has an English version.
 */
export function EnglishVersion({ value, mode, onChange, defaultOpen }: EnglishVersionProps) {
  const { t } = useI18n()
  const [open, setOpen] = useState(defaultOpen)
  const panelId = useId()

  return (
    <section className="flex flex-col gap-4 rounded-lg border bg-muted/30 p-4">
      <h2 className="text-sm font-medium">
        <button
          type="button"
          aria-expanded={open}
          aria-controls={open ? panelId : undefined}
          onClick={() => setOpen((current) => !current)}
          className="flex w-full items-center gap-1.5 rounded-md text-left focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none"
        >
          <ChevronRight className={cn('size-4 transition-transform', open && 'rotate-90')} aria-hidden />
          {t('editor.en.toggle')}
        </button>
      </h2>
      {open && (
        <div id={panelId} className="flex flex-col gap-5">
          <p className="text-sm text-muted-foreground">{t('editor.en.hint')}</p>
          <Field id="title-en" label={t('editor.en.title')}>
            <Input
              id="title-en"
              value={value.titleEn}
              onChange={(event) => onChange({ titleEn: event.target.value })}
              maxLength={200}
              className="h-11 text-base"
            />
          </Field>
          {mode === 'sections' ? (
            <SectionFields
              value={value.sectionsEn}
              onChange={(sectionsEn) => onChange({ sectionsEn })}
              idPrefix="section-en"
              labelSuffix={t('editor.en.sectionSuffix')}
            />
          ) : (
            <Field id="content-en" label={t('editor.en.content')}>
              <Textarea
                id="content-en"
                value={value.contentEn}
                onChange={(event) => onChange({ contentEn: event.target.value })}
                maxLength={50_000}
                className="min-h-40 w-full min-w-0 text-base leading-relaxed [field-sizing:content] [overflow-wrap:anywhere]"
              />
            </Field>
          )}
          <Field id="keywords-en" label={t('editor.en.keywords')}>
            <KeywordInput
              id="keywords-en"
              value={value.keywordsEn}
              onChange={(keywordsEn) => onChange({ keywordsEn })}
              addLabel={t('editor.en.addKeyword')}
              emptyHint={t('editor.en.keywordsHint')}
            />
          </Field>
        </div>
      )}
    </section>
  )
}
