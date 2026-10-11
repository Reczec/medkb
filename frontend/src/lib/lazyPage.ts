import { type ComponentType, lazy } from 'react'

/** Time (ms) of the last reload after a missing chunk, in sessionStorage. */
export const RELOAD_FLAG = 'medkb:chunk-reload'
/** A second failure within this window means reloading does not help: show the error. */
const RELOAD_WINDOW_MS = 60_000

function lastReload(): number | null {
  try {
    const value = Number(sessionStorage.getItem(RELOAD_FLAG))
    return value > 0 ? value : null
  } catch {
    return Date.now() // storage blocked: no loop protection, so never reload
  }
}

function remember(value: number | null) {
  try {
    if (value === null) sessionStorage.removeItem(RELOAD_FLAG)
    else sessionStorage.setItem(RELOAD_FLAG, String(value))
  } catch {
    // ignore: see lastReload
  }
}

/**
 * Load a page module and hand its named export to React.lazy. After a deploy, an open tab may
 * ask for a chunk that no longer exists: reload once to get the new index. If that did not help
 * (another failure within a minute), let the route's error page show the problem. A reload
 * longer ago belongs to an earlier deploy and does not block this one.
 */
export async function loadPage<K extends string, M extends Record<K, ComponentType>>(
  load: () => Promise<M>,
  name: K,
  reload: () => void = () => window.location.reload(),
): Promise<{ default: M[K] }> {
  try {
    const module = await load()
    return { default: module[name] }
  } catch (error) {
    const last = lastReload()
    if (last === null || Date.now() - last > RELOAD_WINDOW_MS) {
      remember(Date.now())
      reload()
      return new Promise(() => {}) // the page is reloading
    }
    remember(null)
    throw error
  }
}

export function lazyPage<K extends string, M extends Record<K, ComponentType>>(
  load: () => Promise<M>,
  name: K,
) {
  return lazy(() => loadPage(load, name))
}
