import { expect, test } from '@playwright/test'

test('dashboard summarises the seeded knowledge base', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Überblick' })).toBeVisible()
  const summary = page.getByTestId('summary')
  await expect(summary).toContainText('16')
  await expect(page.getByRole('navigation', { name: 'Fachgebiete' }).getByRole('link')).toHaveCount(9)
})

test('search leads to an entry with its classification', async ({ page }) => {
  await page.goto('/wissen')
  await page.getByRole('searchbox').fill('kopfschmerz')
  await page.getByRole('link', { name: /Anamnese bei Kopfschmerzen/ }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Anamnese bei Kopfschmerzen' })).toBeVisible()
  await expect(page.getByRole('region', { name: 'Klassifikation' })).toContainText('Neurologie')
})

test('a new entry is classified live and saved', async ({ page }) => {
  await page.goto('/wissen/neu')
  await page.getByLabel('Titel').fill('Herzrasen bei Belastung')
  await page
    .getByLabel('Inhalt')
    .fill('Patient klagt über Brustschmerzen, Herzrasen und Atemnot bei Belastung.')
  const live = page.getByRole('complementary', { name: 'Live-Klassifikation' })
  await expect(live.getByText(/Vorschlag: Kardiologie/)).toBeVisible()
  await page.getByRole('button', { name: 'Speichern' }).click()
  await expect(page.getByRole('heading', { level: 1, name: 'Herzrasen bei Belastung' })).toBeVisible()
  await expect(page).toHaveURL(/\/wissen\/\d+$/)
})

test('admin creates an archive', async ({ page }) => {
  await page.goto('/admin')
  await page.getByLabel('Admin-Token').fill('e2e-token')
  await page.getByRole('button', { name: 'Anmelden' }).click()
  await page.getByRole('button', { name: 'Archiv erstellen' }).click()
  await expect(page.getByRole('button', { name: /herunterladen/ }).first()).toBeVisible()
})

test('deep links survive a reload', async ({ page }) => {
  await page.goto('/wissen/1')
  await page.reload()
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
  const response = await page.request.get('/api/nope')
  expect(response.status()).toBe(404)
  expect(await response.json()).toEqual({ detail: 'Not Found' })
})

test.describe('phone width', () => {
  test.use({ viewport: { width: 375, height: 812 } })

  for (const path of ['/', '/wissen', '/wissen/1', '/wissen/neu', '/admin']) {
    test(`no horizontal scrolling on ${path}`, async ({ page }) => {
      await page.goto(path)
      await page.waitForLoadState('networkidle')
      const width = await page.evaluate(() => document.documentElement.scrollWidth)
      expect(width).toBeLessThanOrEqual(375)
    })
  }
})
