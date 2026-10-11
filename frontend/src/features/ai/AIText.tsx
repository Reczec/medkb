import type { ReactNode } from 'react'

/**
 * Model answers in the small Markdown subset the prompts ask for (app/ai/prompts.py):
 * paragraphs, **bold**, *emphasis*, "- " lists, "1. " lists and "### " subheadings.
 * Everything becomes React text, so model output can never inject HTML.
 */

type Block =
  | { kind: 'heading' | 'paragraph'; text: string }
  | { kind: 'bullets' | 'numbers'; items: string[] }

const HEADING = /^#{1,6}\s+/
const BULLET = /^\s*[-*•]\s+/
const NUMBER = /^\s*\d+[.)]\s+/
const RULE = /^\s*([-*_])\1{2,}\s*$/

function parse(text: string): Block[] {
  const blocks: Block[] = []
  let paragraph: string[] = []
  const flush = () => {
    if (paragraph.length) blocks.push({ kind: 'paragraph', text: paragraph.join(' ') })
    paragraph = []
  }
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim()
    if (!line || RULE.test(line)) {
      flush()
      continue
    }
    const listKind = BULLET.test(line) ? 'bullets' : NUMBER.test(line) ? 'numbers' : null
    if (HEADING.test(line)) {
      flush()
      blocks.push({ kind: 'heading', text: line.replace(HEADING, '') })
    } else if (listKind) {
      flush()
      const item = line.replace(listKind === 'bullets' ? BULLET : NUMBER, '')
      const last = blocks.at(-1)
      if (last && last.kind === listKind) last.items.push(item)
      else blocks.push({ kind: listKind, items: [item] })
    } else {
      paragraph.push(line)
    }
  }
  flush()
  return blocks
}

/** **bold** and *emphasis*; a marker still open while streaming is simply hidden. */
function inline(text: string): ReactNode[] {
  return text
    .split(/(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)/g)
    .filter(Boolean)
    .map((part, index) => {
      if (/^\*\*[^*]+\*\*$/.test(part)) {
        return (
          <strong key={index} className="font-semibold">
            {part.slice(2, -2)}
          </strong>
        )
      }
      if (/^\*[^*\s][^*]*\*$/.test(part)) return <em key={index}>{part.slice(1, -1)}</em>
      return part.replace(/\*+/g, '')
    })
}

export function AIText({ text }: { text: string }) {
  return (
    <div className="flex max-w-[68ch] flex-col gap-3 text-base leading-relaxed [overflow-wrap:anywhere]">
      {parse(text).map((block, index) => {
        if (!('items' in block)) {
          return (
            <p key={index} className={block.kind === 'heading' ? 'mt-1 font-semibold' : undefined}>
              {inline(block.text)}
            </p>
          )
        }
        const List = block.kind === 'bullets' ? 'ul' : 'ol'
        return (
          <List
            key={index}
            className={`flex flex-col gap-1 pl-5 ${block.kind === 'bullets' ? 'list-disc' : 'list-decimal'} marker:text-muted-foreground`}
          >
            {block.items.map((item, i) => (
              <li key={i}>{inline(item)}</li>
            ))}
          </List>
        )
      })}
    </div>
  )
}
