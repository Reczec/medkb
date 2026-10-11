import { type ComponentType, lazy } from 'react'

/** Set while the one reload after a missing chunk is under way. */
export const RELOAD_FLAG = 'medkb:chunk-reload'

function flag(action: 'get' | 'set' | 'clear'): boolean {
  try {
    if (action === 'get') return sessionStorage.getItem(RELOAD_FLAG) === '1'
    if (action === 'set') sessionStorage.setItem(RELOAD_FLAG, '1')
    else sessionStorage.removeItem(RELOAD_FLAG)
  } catch {
    // Storage blocked: no reload loop protection, so never reload.
    return action === 'get'
  }
  return false
}

/**
 * Load a page module and hand its named export to React.lazy. After a deploy, an open tab may
 * ask for a chunk that no longer exists: reload once to get the new index, and if that does not
 * help, let the route's error page show the problem.
 */
export async function loadPage<K extends string, M extends Record<K, ComponentType>>(
  load: () => Promise<M>,
  name: K,
  reload: () => void = () => window.location.reload(),
): Promise<{ default: M[K] }> {
  try {
    const module = await load()
    flag('clear')
    return { default: module[name] }
  } catch (error) {
    if (!flag('get')) {
      flag('set')
      reload()
      return new Promise(() => {}) // the page is reloading
    }
    flag('clear')
    throw error
  }
}

export function lazyPage<K extends string, M extends Record<K, ComponentType>>(
  load: () => Promise<M>,
  name: K,
) {
  return lazy(() => loadPage(load, name))
}
