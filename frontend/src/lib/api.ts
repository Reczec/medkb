/** Thin fetch wrapper for the MedKB REST API. */

export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

interface ValidationIssue {
  loc?: (string | number)[]
  msg: string
}

/** Turns an error response into a readable message (FastAPI `detail`, string or list). */
export async function errorMessage(res: Response): Promise<string> {
  try {
    const data: unknown = await res.json()
    const detail = (data as { detail?: unknown })?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
      return (detail as ValidationIssue[])
        .map((issue) => `${(issue.loc ?? []).slice(1).join('.')}: ${issue.msg}`)
        .join('; ')
    }
  } catch {
    // not JSON
  }
  return `Fehler ${res.status}`
}

export interface ApiOptions {
  method?: string
  body?: unknown
  /** Send the admin token from sessionStorage. */
  admin?: boolean
  /** Return the Response instead of parsed JSON (downloads). */
  raw?: boolean
  signal?: AbortSignal
}

export const ADMIN_TOKEN_KEY = 'adminToken'

export async function api(path: string, opts: ApiOptions & { raw: true }): Promise<Response>
export async function api<T = unknown>(path: string, opts?: ApiOptions): Promise<T>
export async function api<T = unknown>(path: string, opts: ApiOptions = {}): Promise<T | Response> {
  const headers = new Headers()
  if (opts.body !== undefined) headers.set('Content-Type', 'application/json')
  if (opts.admin) headers.set('X-Admin-Token', sessionStorage.getItem(ADMIN_TOKEN_KEY) ?? '')

  let res: Response
  try {
    res = await fetch(path, {
      method: opts.method ?? 'GET',
      headers,
      body: opts.body === undefined ? undefined : JSON.stringify(opts.body),
      signal: opts.signal,
    })
  } catch (error) {
    if ((error as Error)?.name === 'AbortError') throw error
    throw new ApiError(0, 'Server nicht erreichbar')
  }

  if (!res.ok) throw new ApiError(res.status, await errorMessage(res))
  if (opts.raw) return res
  if (res.status === 204) return undefined as T
  return (await res.json()) as T
}
