import { expect, test, type Page } from '@playwright/test'
import path from 'node:path'

const answer = { text: 'Eine Mittelohrentzündung betrifft den Raum hinter dem Trommelfell. Diese Erklärung ersetzt keine ärztliche Beratung.\n\nPrototyp mit Beispieldaten – keine medizinische Beratung.', cached: false, citations: [] }
const draft = { title: 'KI-Testentwurf', content: 'Dies ist ein allgemeiner, zu prüfender Beispielentwurf über Migräne.', doc_type: 'Diagnose', term_en: 'Migraine', icd11_code: '8A80', medications: ['sumatriptan'], ai_generated: true }

async function login(page: Page, role: string) {
  const response = await page.request.post('/api/auth/demo', { data: { role } })
  const { access_token } = await response.json()
  await page.addInitScript(token => sessionStorage.setItem('token', token), access_token)
  return access_token as string
}

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('medkb:lang', 'de'))
  await page.route('**/api/sources/**', route => route.fulfill({ json: { status: 'empty', data: null } }))
  await page.route('**/api/ai/**', async route => {
    const url = new URL(route.request().url())
    if (url.pathname.endsWith('/usage')) return route.fulfill({ json: { today: 7, limit: 500 } })
    const result = url.pathname.endsWith('/draft') ? { ...answer, text: draft.content, draft }
      : url.pathname.endsWith('/ask') ? { ...answer, text: 'Allgemeine Erklärung zur Mittelohrentzündung [1].\n\nPrototyp mit Beispieldaten – keine medizinische Beratung.', citations: [{ index: 1, id: 1, title: 'Akute Mittelohrentzündung (Otitis media)' }] }
      : answer
    if (url.searchParams.get('stream') === 'true') return route.fulfill({ contentType: 'text/event-stream', body: `event: token\ndata: {"text":"Migräne"}\n\nevent: done\ndata: ${JSON.stringify(result)}\n\n` })
    return route.fulfill({ json: result })
  })
})

async function capture(page: Page, surface: string, setup: () => Promise<void>) {
  if (process.env.MEDKB_CAPTURE_AI !== '1') return
  for (const theme of ['light', 'dark']) {
    for (const [device, width, height] of [['desktop', 1440, 900], ['phone', 375, 812]] as const) {
      await page.setViewportSize({ width, height })
      await page.evaluate(value => localStorage.setItem('theme', value), theme)
      await page.reload()
      await setup()
      await page.waitForLoadState('networkidle')
      await page.evaluate(() => document.fonts.ready)
      await page.evaluate(() => window.scrollTo(0, 0))
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
      await page.screenshot({ path: path.resolve(import.meta.dirname, '../../.impeccable/review', `ai-${surface}-${device}-${theme}.png`), fullPage: true, animations: 'disabled' })
    }
  }
}

test('patient explains an entry without staff summaries', async ({ page }) => {
  await login(page, 'patient'); await page.goto('/wissen/1')
  const setup = async () => {
    await expect(page.getByRole('tab', { name: 'KI-Zusammenfassung' })).toHaveCount(0)
    await page.getByRole('button', { name: 'Einfach erklären' }).click()
    await expect(page.getByText('KI-generiert', { exact: true })).toBeVisible()
  }
  await setup(); await capture(page, 'patient', setup)
})

test('assistant streams an answer and links its knowledge source', async ({ page }) => {
  await login(page, 'patient'); await page.goto('/assistent')
  const setup = async () => {
    await page.getByLabel('Deine Frage').fill('Mittelohrentzündung')
    await page.getByRole('button', { name: 'Frage stellen' }).click()
    await expect(page.getByRole('link', { name: '[1] Akute Mittelohrentzündung (Otitis media)' })).toHaveAttribute('href', '/wissen/1')
  }
  await setup(); await capture(page, 'assistant', setup)
})

test('admin reviews, applies and saves a draft with its AI marker', async ({ page }) => {
  const token = await login(page, 'admin'); await page.goto('/wissen/neu')
  // A slow CPU, like the CI runner: the route change after saving once left the page blank
  // because the page transition waited for an exit animation that never finished.
  const cdp = await page.context().newCDPSession(page)
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 8 })
  const setup = async () => {
    await page.getByLabel('Titel', { exact: true }).fill('KI-Testentwurf')
    await page.getByRole('button', { name: 'KI-Entwurf erstellen' }).click()
    await expect(page.getByRole('button', { name: 'Geprüften Entwurf übernehmen' })).toBeVisible()
    await expect(page.getByLabel('Inhalt', { exact: true })).toHaveValue('')
  }
  await setup(); await capture(page, 'editor', setup)
  await page.getByRole('button', { name: 'Geprüften Entwurf übernehmen' }).click()
  await expect(page.getByLabel('Inhalt', { exact: true })).toHaveValue(draft.content)
  await page.getByRole('button', { name: 'Speichern', exact: true }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'KI-Testentwurf' })).toBeVisible()
  await expect(page.getByRole('heading', { level: 1, name: 'Neuer Eintrag' })).toHaveCount(0)
  await expect(page.getByText('KI-generiert', { exact: true })).toBeVisible()
  const id = new URL(page.url()).pathname.split('/').at(-1)
  expect((await page.request.delete(`/api/documents/${id}`, { headers: { Authorization: `Bearer ${token}` } })).ok()).toBe(true)
})

test('staff summary stays separate from entry content', async ({ page }) => {
  await login(page, 'doctor'); await page.goto('/wissen/1?tab=ki')
  const setup = async () => {
    await page.getByRole('button', { name: 'KI-Zusammenfassung' }).click()
    await expect(page.getByText('KI-generiert', { exact: true })).toBeVisible()
  }
  await setup(); await capture(page, 'staff', setup)
})

test('unconfigured AI shows recovery and fits a phone', async ({ page }) => {
  await login(page, 'patient')
  await page.route('**/api/ai/**', route => route.fulfill({ status: 503, json: { detail: 'ai_not_configured' } }))
  await page.setViewportSize({ width: 375, height: 812 }); await page.goto('/wissen/1')
  await page.getByRole('button', { name: 'Einfach erklären' }).click()
  await expect(page.getByRole('alert')).toContainText('noch nicht eingerichtet')
  await expect(page.getByRole('button', { name: 'Erneut versuchen' })).toBeVisible()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})
