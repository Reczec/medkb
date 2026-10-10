import { expect, test, type Page } from '@playwright/test'

type Role = 'admin' | 'doctor' | 'patient'

/** Demo login through the API; the token is put into sessionStorage before any page script runs. */
async function loginAs(page: Page, role: Role): Promise<string> {
  const response = await page.request.post('/api/auth/demo', { data: { role } })
  expect(response.ok()).toBe(true)
  const { access_token: token } = await response.json()
  await page.addInitScript((value) => sessionStorage.setItem('token', value), token)
  return token
}

test.describe('as admin', () => {
  let token = ''
  test.beforeEach(async ({ page }) => {
    token = await loginAs(page, 'admin')
  })

test('dashboard summarises the seeded knowledge base', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Überblick' })).toBeVisible()
  const summary = page.getByTestId('summary')
  await expect(summary).toContainText('16')
  await expect(page.getByRole('navigation', { name: 'Fachgebiete' }).getByRole('link')).toHaveCount(9)
})

test('every filing tab shows its full name and the drawer edge shows the share', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/')
  const strip = page.getByRole('navigation', { name: 'Fachgebiete' })
  const truncated = await strip.locator('[data-tab-label]').evaluateAll((labels) =>
    labels.filter((label) => label.scrollWidth > label.clientWidth + 1).map((l) => l.textContent),
  )
  expect(truncated).toEqual([])
  await expect(strip.locator('[data-tab-label]')).toHaveCount(9)
  const tops = await strip.getByRole('link').evaluateAll((links) =>
    links.map((link) => Math.round(link.getBoundingClientRect().top)),
  )
  expect(new Set(tops).size).toBe(1) // one drawer edge, no second row
  const share = (name: string) =>
    strip.locator(`[data-share="${name}"]`).evaluate((el) => el.getBoundingClientRect().width)
  const neuro = await share('Neurologie') // 3 entries
  const hno = await share('HNO') // 2
  const derma = await share('Dermatologie') // 1
  expect(neuro).toBeGreaterThan(hno)
  expect(hno).toBeGreaterThan(derma)
  expect(neuro / derma).toBeCloseTo(3, 0)
  // The share bar is its own labelled element, not the edge the tabs stand on.
  const tabsBottom = await strip.getByRole('list').evaluate((el) => el.getBoundingClientRect().bottom)
  const barTop = await strip.locator('[data-share]').first().evaluate((el) => el.getBoundingClientRect().top)
  expect(barTop - tabsBottom).toBeGreaterThanOrEqual(8)
  await expect(strip.getByText('Anteil der Einträge')).toBeVisible()
})

test('dimmed filing tabs keep readable labels', async ({ page }) => {
  await page.goto('/wissen?category=Neurologie')
  const strip = page.getByRole('navigation', { name: 'Fachgebiete' })
  const other = strip.getByRole('button', { name: /HNO/ })
  const opacity = await other.evaluate((el) => {
    let node: Element | null = el
    let value = 1
    while (node) {
      value *= Number(getComputedStyle(node).opacity)
      node = node.parentElement
    }
    return value
  })
  expect(opacity).toBe(1)
})

test('activity is drawn as daily bars, not a smoothed curve', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('.recharts-bar-rectangle').first()).toBeVisible()
  await expect(page.locator('.recharts-area')).toHaveCount(0)
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

  test('specialty names stay readable on a phone', async ({ page }) => {
    await page.goto('/')
    const labels = page.getByRole('navigation', { name: 'Fachgebiete' }).locator('[data-tab-label]')
    await expect(labels.first()).toHaveText('Neurologie')
    const truncated = await labels.evaluateAll((all) =>
      all.filter((label) => label.scrollWidth > label.clientWidth + 1).length,
    )
    expect(truncated).toBe(0)
  })

  test('long titles, URLs and keywords do not widen the page', async ({ page }) => {
    const created = await page.request.post('/api/documents', {
      headers: { Authorization: `Bearer ${token}` },
      data: {
        title: 'Kopfschmerz/Migräne/Spannungskopfschmerz/Clusterkopfschmerz/Medikamentenübergebrauch',
        content:
          'Siehe https://register.awmf.org/de/leitlinien/detail/030-057-sehr-lange-adresse-ohne-leerzeichen ' +
          'für Details. Donaudampfschifffahrtsgesellschaftskapitänskajütenschlüsselanhänger.',
        doc_type: 'Leitlinie',
        keywords: Array.from({ length: 20 }, (_, i) => `Schlagwort${i}MitSehrLangemNamenOhneLücke`),
      },
    })
    expect(created.ok()).toBe(true)
    const { id } = await created.json()
    for (const path of ['/wissen?q=Clusterkopfschmerz', `/wissen/${id}`, `/wissen/${id}/bearbeiten`]) {
      await page.goto(path)
      await page.waitForLoadState('networkidle')
      const width = await page.evaluate(() => document.documentElement.scrollWidth)
      expect(width, path).toBeLessThanOrEqual(375)
    }
  })

  for (const path of ['/', '/wissen', '/wissen/1', '/wissen/neu', '/admin']) {
    test(`no horizontal scrolling on ${path}`, async ({ page }) => {
      await page.goto(path)
      await page.waitForLoadState('networkidle')
      const width = await page.evaluate(() => document.documentElement.scrollWidth)
      expect(width).toBeLessThanOrEqual(375)
    })
  }
})
})

test.describe('login and roles', () => {
  test('visitors without a login land on the login page and can enter as a role', async ({ page }) => {
    await page.goto('/wissen')
    await expect(page).toHaveURL(/\/login\?next=%2Fwissen$/)
    await page.getByRole('button', { name: /Ärztin \/ Arzt/ }).click()
    await expect(page).toHaveURL(/\/wissen$/)
    await expect(page.getByRole('heading', { level: 1, name: 'Wissensdatenbank' })).toBeVisible()
  })

  test('patients get the search-first home and no edit or admin access', async ({ page }) => {
    await loginAs(page, 'patient')
    await page.goto('/')
    await expect(page.getByRole('heading', { level: 1, name: 'Wonach suchst du?' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Neuer Eintrag' })).toHaveCount(0)
    await page.goto('/wissen/1')
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    await expect(page.getByRole('link', { name: /Bearbeiten/ })).toHaveCount(0)
    await expect(page.getByRole('region', { name: 'Klassifikation' })).toHaveCount(0)
    await page.goto('/admin')
    await expect(page.getByText('Keine Berechtigung')).toBeVisible()
  })

  test('doctors see the classification but cannot edit', async ({ page }) => {
    await loginAs(page, 'doctor')
    await page.goto('/wissen/1')
    await expect(page.getByRole('region', { name: 'Klassifikation' })).toBeVisible()
    await expect(page.getByRole('link', { name: /Bearbeiten/ })).toHaveCount(0)
  })

  test('logging out returns to the login page', async ({ page }) => {
    await loginAs(page, 'doctor')
    await page.goto('/')
    await page.getByRole('button', { name: 'Abmelden' }).click()
    await expect(page).toHaveURL(/\/login/)
    await expect(page.getByRole('heading', { level: 1, name: 'Anmelden' })).toBeVisible()
  })

  test('the API refuses a patient write with 403', async ({ page }) => {
    const token = await loginAs(page, 'patient')
    const response = await page.request.delete('/api/documents/1', {
      headers: { Authorization: `Bearer ${token}` },
    })
    expect(response.status()).toBe(403)
  })

  test('the login page fits a phone', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await page.goto('/login')
    await page.waitForLoadState('networkidle')
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(375)
  })
})
