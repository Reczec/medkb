import { ApiError, api, errorMessage } from '@/lib/api'

describe('errorMessage', () => {
  it('reads a string detail', async () => {
    const res = new Response(JSON.stringify({ detail: 'Document not found.' }), { status: 404 })
    expect(await errorMessage(res)).toBe('Document not found.')
  })

  it('joins pydantic error details', async () => {
    const body = {
      detail: [
        { loc: ['body', 'title'], msg: 'too short' },
        { loc: ['body', 'content'], msg: 'missing' },
      ],
    }
    expect(await errorMessage(new Response(JSON.stringify(body), { status: 422 }))).toBe(
      'title: too short; content: missing',
    )
  })

  it('falls back to the status for non-JSON bodies', async () => {
    expect(await errorMessage(new Response('<html>', { status: 502 }))).toBe('Fehler 502')
  })
})

describe('api', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    sessionStorage.clear()
  })

  it('throws ApiError with the status and sends the admin token', async () => {
    sessionStorage.setItem('adminToken', 'secret')
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: 'Invalid or missing admin token.' }), { status: 401 }),
    )
    vi.stubGlobal('fetch', fetchMock)

    const error = await api('/api/audit', { admin: true }).catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBe(401)
    expect((error as ApiError).message).toBe('Invalid or missing admin token.')
    const init = fetchMock.mock.calls[0][1] as RequestInit
    expect(new Headers(init.headers).get('X-Admin-Token')).toBe('secret')
  })

  it('sends JSON bodies and parses JSON responses', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: 1 }), { status: 201 }))
    vi.stubGlobal('fetch', fetchMock)

    const result = await api<{ id: number }>('/api/documents', { method: 'POST', body: { title: 'x' } })

    expect(result).toEqual({ id: 1 })
    const init = fetchMock.mock.calls[0][1] as RequestInit
    expect(init.method).toBe('POST')
    expect(init.body).toBe('{"title":"x"}')
    expect(new Headers(init.headers).get('Content-Type')).toBe('application/json')
  })

  it('returns undefined for 204', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(null, { status: 204 })))
    expect(await api('/api/documents/1', { method: 'DELETE' })).toBeUndefined()
  })

  it('returns the raw response when asked to', async () => {
    const response = new Response('{"a":1}', { status: 200 })
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response))
    expect(await api('/api/archives/x.json', { raw: true })).toBe(response)
  })

  it('wraps network failures in an ApiError with status 0', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    const error = await api('/api/stats').catch((e: unknown) => e)
    expect(error).toBeInstanceOf(ApiError)
    expect((error as ApiError).status).toBe(0)
    expect((error as ApiError).message).toBe('Server nicht erreichbar')
  })
})

describe('documentsPath', () => {
  it('encodes special characters and skips empty filters', async () => {
    const { documentsPath } = await import('@/lib/queries')
    const path = documentsPath({ q: ' 100% "Ohr_" ', category: '', offset: 10, limit: 10 })
    const url = new URL(path, 'http://x')
    expect(url.searchParams.get('q')).toBe('100% "Ohr_"')
    expect(url.searchParams.has('category')).toBe(false)
    expect(url.searchParams.get('offset')).toBe('10')
  })
})
