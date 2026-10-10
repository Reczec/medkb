/**
 * Where to go after login. Only same-origin paths are allowed; browsers read "\" as "/" and drop
 * tabs, so "/\evil.com" would otherwise become "//evil.com".
 */
export function safeNext(value: string | null): string {
  // oxlint-disable-next-line no-control-regex -- control characters are exactly what we reject
  if (!value || !value.startsWith('/') || /[\\\u0000-\u001f]/.test(value)) return '/'
  try {
    const url = new URL(value, window.location.origin)
    if (url.origin !== window.location.origin) return '/'
    return url.pathname + url.search + url.hash
  } catch {
    return '/'
  }
}
