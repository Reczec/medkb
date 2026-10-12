import { expect, test } from '@playwright/test'
import path from 'node:path'

test.beforeEach(async ({ page }) => {
  await page.route('**/api/sources/**', route => route.fulfill({ json: { status: 'empty', data: null } }))
})

for (const [lang, role] of [['en', 'patient'], ['de', 'doctor']] as const) {
  test(`RAG ${lang} source evidence is accessible and fits a phone`, async ({ page }) => {
    const response = await page.request.post('/api/auth/demo', { data: { role } })
    const { access_token } = await response.json()
    await page.addInitScript(({ token, language }) => {
      sessionStorage.setItem('token', token)
      localStorage.setItem('medkb:lang', language)
    }, { token: access_token, language: lang })
    const title = lang === 'en' ? 'Migraine' : 'Migräne'
    const excerpt = lang === 'en' ? 'Nausea and sensitivity to light and sound can accompany an attack.' : 'Begleitend treten oft Übelkeit sowie Licht- und Lärmempfindlichkeit auf.'
    const result = { text: `${title} [1].`, cached: false,
      retrieval: { mode: 'hybrid', indexed_chunks: 250 },
      citations: [{ index: 1, id: 7, title, section: 'symptoms', excerpt }] }
    await page.route('**/api/ai/ask*', route => route.fulfill({ contentType: 'text/event-stream',
      body: `event: token\ndata: {"text":"${title}"}\n\nevent: done\ndata: ${JSON.stringify(result)}\n\n` }))
    const sizes = process.env.MEDKB_CAPTURE_RAG === '1'
      ? [['desktop', 1440, 900], ['phone', 375, 812]] as const : [['phone', 375, 812]] as const
    const themes = process.env.MEDKB_CAPTURE_RAG === '1' ? ['light', 'dark'] : ['light']
    for (const theme of themes) for (const [device, width, height] of sizes) {
      await page.setViewportSize({ width, height })
      await page.addInitScript(value => localStorage.setItem('theme', value), theme)
      await page.goto('/assistent')
      await page.getByLabel(lang === 'en' ? 'Your question' : 'Deine Frage').fill(lang === 'en' ? 'What causes a pounding head?' : 'Was bedeutet Pochen im Kopf?')
      await page.getByRole('button', { name: lang === 'en' ? 'Ask' : 'Frage stellen', exact: true }).click()
      await expect(page.getByText(lang === 'en' ? 'Semantic + keyword search' : 'Semantische + Stichwortsuche', { exact: true })).toBeVisible()
      const disclosure = page.locator('summary').filter({ hasText: lang === 'en' ? 'Source excerpt' : 'Quellenauszug' })
      await disclosure.focus(); await page.keyboard.press('Enter')
      await expect(page.getByText(excerpt, { exact: true })).toBeVisible()
      await expect(page.getByRole('link', { name: `[1] ${title}` })).toHaveAttribute('href', '/wissen/7')
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
      if (process.env.MEDKB_CAPTURE_RAG === '1') {
        await page.evaluate(() => document.fonts.ready)
        await page.evaluate(() => window.scrollTo(0, 0))
        await page.screenshot({ path: path.resolve(import.meta.dirname, '../../.impeccable/review', `rag-${lang}-${device}-${theme}.png`), fullPage: true, animations: 'disabled' })
      }
    }
  })
}

test('RAG fallback and no-context answer remain honest in English', async ({ page }) => {
  const response = await page.request.post('/api/auth/demo', { data: { role: 'patient' } })
  const { access_token } = await response.json()
  await page.addInitScript(token => sessionStorage.setItem('token', token), access_token)
  await page.route('**/api/ai/ask*', route => route.fulfill({ json: {
    text: 'There are no matching entries in the knowledge base.', cached: false, citations: [],
    retrieval: { mode: 'lexical', reason: 'index_incomplete', indexed_chunks: 0 },
  } }))
  await page.goto('/assistent')
  await page.getByLabel('Your question').fill('How do I repair a bicycle?')
  await page.getByRole('button', { name: 'Ask', exact: true }).click()
  await expect(page.getByText('Keyword search', { exact: true })).toBeVisible()
  await expect(page.getByText('The semantic index is not ready.')).toBeVisible()
  await expect(page.getByText('There are no matching entries in the knowledge base.')).toBeVisible()
  await expect(page.locator('summary')).toHaveCount(0)
})
