import { expect, test, type Page } from '@playwright/test'

type Role = 'admin' | 'doctor' | 'patient'

// Browser tests stay independent of upstream APIs; the interface language is NOT preset here.
test.beforeEach(async ({ page }) => {
  await page.route('**/api/sources/**', (route) =>
    route.fulfill({ json: { status: 'empty', data: null, fetched_at: '2026-10-11T10:00:00Z' } }),
  )
  await page.route('**/api/ai/usage', (route) => route.fulfill({ json: { today: 0, limit: 500 } }))
})

async function loginAs(page: Page, role: Role): Promise<string> {
  const response = await page.request.post('/api/auth/demo', { data: { role } })
  expect(response.ok()).toBe(true)
  const { access_token: token } = await response.json()
  await page.addInitScript((value) => sessionStorage.setItem('token', value), token)
  return token
}

const switchTo = (page: Page, name: 'English' | 'German' | 'Englisch' | 'Deutsch') =>
  page.getByRole('button', { name: new RegExp(name) }).filter({ visible: true }).first().click()

test('the login page is English by default and the demo opens in English', async ({ page }) => {
  await page.goto('/login')
  await expect(page.getByRole('heading', { level: 1, name: 'Sign in' })).toBeVisible()
  await expect(page.locator('html')).toHaveAttribute('lang', 'en')
  await page.getByRole('button', { name: /Open as doctor/ }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Overview' })).toBeVisible()
})

test('the chosen language survives a reload and applies to entries', async ({ page }) => {
  await loginAs(page, 'doctor')
  await page.goto('/wissen')
  await expect(page.getByRole('heading', { level: 1, name: 'Knowledge base' })).toBeVisible()
  await switchTo(page, 'German')
  await expect(page.getByRole('heading', { level: 1, name: 'Wissensdatenbank' })).toBeVisible()
  await expect(page.locator('html')).toHaveAttribute('lang', 'de')
  await page.reload()
  await expect(page.getByRole('heading', { level: 1, name: 'Wissensdatenbank' })).toBeVisible()
  expect(await page.evaluate(() => localStorage.getItem('medkb:lang'))).toBe('de')

  await page.getByRole('searchbox', { name: 'Suchbegriffe' }).fill('Migräne')
  const german = page.getByRole('link', { name: 'Migräne', exact: true }).first()
  await expect(german).toBeVisible()
  await german.click()
  await expect(page.getByRole('heading', { level: 1, name: 'Migräne' })).toBeVisible()
  await expect(page.getByRole('heading', { level: 2, name: 'Symptome' })).toBeVisible()

  await switchTo(page, 'Englisch')
  await expect(page.getByRole('heading', { level: 1, name: 'Migraine' })).toBeVisible()
  await expect(page.getByRole('heading', { level: 2, name: 'Symptoms' })).toBeVisible()
  await expect(page.getByText('Only available in German')).toHaveCount(0)
})

test('the English term finds an entry that is stored in German', async ({ page }) => {
  await loginAs(page, 'doctor')
  await page.goto('/wissen')
  await page.getByRole('searchbox', { name: 'Search terms' }).fill('migraine')
  await expect(page.getByRole('link', { name: 'Migraine', exact: true }).first()).toBeVisible()
})

test('an entry without an English version shows the German text with a note', async ({ page }) => {
  const token = await loginAs(page, 'admin')
  const created = await page.request.post('/api/documents', {
    headers: { Authorization: `Bearer ${token}` },
    data: {
      title: 'Nur deutscher Testeintrag',
      content: 'Ein Text ohne englische Fassung, der nur auf Deutsch existiert.',
      doc_type: 'Symptom',
    },
  })
  expect(created.ok()).toBe(true)
  const { id } = await created.json()
  try {
    await page.goto(`/wissen/${id}`)
    await expect(page.getByRole('heading', { level: 1, name: 'Nur deutscher Testeintrag' })).toBeVisible()
    await expect(page.getByRole('status').filter({ hasText: 'Only available in German' })).toBeVisible()
  } finally {
    // The other specs count the seeded entries.
    await page.request.delete(`/api/documents/${id}`, { headers: { Authorization: `Bearer ${token}` } })
  }
})

test('the language switch fits the phone login without overflow', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 })
  await page.goto('/login')
  await page.waitForLoadState('networkidle')
  const group = page.getByRole('group', { name: 'Language' }).filter({ visible: true })
  await expect(group).toBeVisible()
  await group.getByRole('button', { name: /German/ }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Anmelden' })).toBeVisible()
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(375)
})
