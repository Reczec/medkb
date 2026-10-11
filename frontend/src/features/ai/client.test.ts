import { requestAI } from './client'

afterEach(() => vi.unstubAllGlobals())

const result = { text: 'Migräne erklärt.', cached: false, citations: [] }

function response(parts: Uint8Array[]) {
  return new Response(new ReadableStream({ start(controller) {
    parts.forEach(part => controller.enqueue(part)); controller.close()
  } }), { headers: { 'Content-Type': 'text/event-stream' } })
}

it('decodes split UTF-8 and SSE frames and returns only validated done', async () => {
  const bytes = new TextEncoder().encode(`event: token\ndata: {"text":"Migräne"}\n\nevent: done\ndata: ${JSON.stringify(result)}\n\n`)
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response(Array.from(bytes, byte => new Uint8Array([byte])))))
  const token = vi.fn()
  expect(await requestAI('/ask', {}, { stream: true, onToken: token })).toEqual(result)
  expect(token).toHaveBeenCalledWith('Migräne')
})

it.each(['event: token\ndata: {"text":"partial"}\n\n', 'event: error\ndata: {"message":"Retry"}\n\n', 'event: done\ndata: {broken}\n\n'])('rejects unfinished or invalid stream %s', async (text) => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response([new TextEncoder().encode(text)])))
  await expect(requestAI('/ask', {}, { stream: true })).rejects.toThrow()
})

it('maps missing configuration and quota to actionable German copy', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'ai_not_configured' }), { status: 503 })))
  await expect(requestAI('/ask', {})).rejects.toThrow('noch nicht eingerichtet')
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'limit' }), { status: 429, headers: { 'Retry-After': '60' } })))
  await expect(requestAI('/ask', {})).rejects.toThrow('Tageslimit')
})

it('passes cancellation through', async () => {
  const controller = new AbortController(); controller.abort()
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new DOMException('Aborted', 'AbortError')))
  await expect(requestAI('/ask', {}, { signal: controller.signal })).rejects.toMatchObject({ name: 'AbortError' })
})

it('handles CRLF separators split across chunks', async () => {
  const bytes = new TextEncoder().encode(`event: done\r\ndata: ${JSON.stringify(result)}\r\n\r\n`)
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response(Array.from(bytes, byte => new Uint8Array([byte])))))
  expect(await requestAI('/ask', {}, { stream: true })).toEqual(result)
})
