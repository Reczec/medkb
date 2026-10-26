import { expect, test, type Page } from '@playwright/test'
import path from 'node:path'

type Role = 'admin' | 'doctor' | 'patient'

/** Optional captures of the real built stack for the stage finish review. */
async function captureReview(page: Page, surface: string) {
  if (process.env.MEDKB_CAPTURE_REVIEW !== '1') return
  for (const theme of ['light', 'dark']) {
    await page.evaluate((value) => localStorage.setItem('theme', value), theme)
    for (const [device, width, height] of [['desktop', 1440, 900], ['phone', 375, 812]] as const) {
      await page.setViewportSize({ width, height })
      await page.reload()
      await page.waitForLoadState('networkidle')
      await page.evaluate(() => document.fonts.ready)
      await page.screenshot({ path: path.resolve(import.meta.dirname, '../../.impeccable/review', `${surface}-${device}-${theme}.png`), fullPage: true })
    }
  }
}

const study = {
  pmid: '123456', title: 'Demo study on migraine', journal: 'Demo Journal', year: 2026,
  authors: ['A Example'], more_authors: false, url: 'https://pubmed.ncbi.nlm.nih.gov/123456/',
}

// Keep browser tests independent of upstream APIs, credentials and rate limits. The interface
// defaults to English; these flows run in German (i18n.spec.ts covers the default and the switch).
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('medkb:lang', 'de'))
  await page.route('**/api/sources/**', async (route) => {
    const path = new URL(route.request().url()).pathname
    const result = path.endsWith('/latest-studies')
      ? { status: 'ok', data: [{ category: 'Neurologie', studies: [study] }, { category: 'Kardiologie', studies: [study] }] }
      : path.endsWith('/studies')
        ? { status: 'ok', data: [study] }
        : path.endsWith('/icd11')
          ? { status: 'not_configured', data: null }
          : { status: 'empty', data: null }
    await route.fulfill({ json: { ...result, fetched_at: '2026-10-11T10:00:00Z' } })
  })
})

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
  await expect(summary).toContainText('103')
  await expect(page.getByRole('navigation', { name: 'Fachgebiete' }).getByRole('link')).toHaveCount(16)
  await captureReview(page, 'dashboard')
})

test('every filing tab shows its full name and the drawer edge shows the share', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/')
  const strip = page.getByRole('navigation', { name: 'Fachgebiete' })
  const truncated = await strip.locator('[data-tab-label]').evaluateAll((labels) =>
    labels.filter((label) => label.scrollWidth > label.clientWidth + 1).map((l) => l.textContent),
  )
  expect(truncated).toEqual([])
  await expect(strip.locator('[data-tab-label]')).toHaveCount(16)
  const tops = await strip.getByRole('link').evaluateAll((links) =>
    links.map((link) => Math.round(link.getBoundingClientRect().top)),
  )
  expect(new Set(tops).size).toBe(1) // one drawer edge, no second row
  const share = (name: string) =>
    strip.locator(`[data-share="${name}"]`).evaluate((el) => el.getBoundingClientRect().width)
  const neuro = await share('Neurologie') // 8 entries
  const hno = await share('HNO') // 6
  const eyes = await share('Augenheilkunde') // 6
  const gynecology = await share('Gynäkologie') // 5
  expect(hno).toBeCloseTo(eyes, 0)
  expect(neuro).toBeGreaterThan(hno)
  expect(neuro / gynecology).toBeCloseTo(1.6, 1)
  // The share bar is its own labelled element, not the edge the tabs stand on.
  const tabsBottom = await strip.getByRole('list').evaluate((el) => el.getBoundingClientRect().bottom)
  const barTop = await strip.locator('[data-share]').first().evaluate((el) => el.getBoundingClientRect().top)
  expect(barTop - tabsBottom).toBeGreaterThanOrEqual(8)
  await expect(strip.getByText('Anteil der Einträge')).toBeVisible()
})

test('filing tab washes keep their specialty hue', async ({ page }) => {
  await page.goto('/')
  const tab = page.getByTestId('file-tab').filter({ hasText: 'Allgemeinmedizin' }).first()
  const [r, g, b] = await tab.evaluate((el) => {
    const canvas = document.createElement('canvas')
    canvas.width = canvas.height = 1
    const ctx = canvas.getContext('2d')!
    ctx.fillStyle = getComputedStyle(el).backgroundColor
    ctx.fillRect(0, 0, 1, 1)
    return Array.from(ctx.getImageData(0, 0, 1, 1).data)
  })
  // Allgemeinmedizin is teal: green and blue above red, never a mauve-pink wash.
  expect(g).toBeGreaterThan(r)
  expect(b).toBeGreaterThan(r)
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

test('the section editor creates an entry with source metadata and warning signs', async ({ page }) => {
  await page.goto('/wissen/neu')
  await page.getByLabel('Titel', { exact: true }).fill('Migräne – strukturiertes Beispiel')
  await page.getByLabel('Fachbegriff (en)').fill('Migraine')
  await page.getByLabel('ICD-11-Code').fill('8A80')
  await page.getByLabel('Wirkstoff hinzufügen').fill('sumatriptan')
  await page.getByLabel('Wirkstoff hinzufügen').press('Enter')
  await page.getByRole('button', { name: 'Abschnitte', exact: true }).click()
  await page.getByLabel('Definition', { exact: true }).fill('Migräne verursacht wiederkehrende Kopfschmerzen.')
  await page.getByLabel('Symptome', { exact: true }).fill('Kopfschmerzen mit Übelkeit und Lichtempfindlichkeit.')
  await page.getByLabel('Warnzeichen', { exact: true }).fill('Bei plötzlich stärkstem Kopfschmerz: 144 anrufen.')
  await expect(page.getByRole('complementary', { name: 'Live-Klassifikation' })).toContainText('Vorschlag: Neurologie')
  await page.getByRole('button', { name: 'Speichern', exact: true }).click()
  await expect(page).toHaveURL(/\/wissen\/\d+$/)
  await expect(page.getByRole('heading', { name: 'Migräne – strukturiertes Beispiel', level: 1 })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Symptome', exact: true })).toBeVisible()
  await expect(page.getByRole('region', { name: 'Warnzeichen', exact: true })).toContainText('144 anrufen')
  await expect(page.getByText('Im Notfall: 144', { exact: true })).toBeVisible()
  await expect(page.getByRole('tab', { name: 'Medikamente' })).toBeVisible()
  await expect(page.getByText('Migraine', { exact: true })).toBeVisible()
  await expect(page.getByText('8A80', { exact: true })).toBeVisible()
  if (process.env.MEDKB_CAPTURE_REVIEW === '1') {
    await page.goto(page.url() + '/bearbeiten')
    await captureReview(page, 'editor')
  }
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
    await expect(labels).toHaveCount(16)
    await expect(labels.filter({ hasText: /^HNO$/ })).toBeVisible()
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
  test('a doctor opens studies with PubMed provenance and a persistent tab', async ({ page }) => {
    await loginAs(page, 'doctor')
    await page.goto('/wissen/1')
    await page.getByRole('tab', { name: 'Studien', exact: true }).click()
    await expect(page.getByRole('link', { name: study.title })).toHaveAttribute('href', study.url)
    await expect(page.getByText('PubMed · NCBI', { exact: true })).toBeVisible()
    await page.reload()
    await expect(page.getByRole('tab', { name: 'Studien', exact: true })).toHaveAttribute('aria-selected', 'true')
    await expect(page.getByRole('link', { name: study.title })).toBeVisible()
    await captureReview(page, 'studies')
  })

  test('a patient sees seed warning signs without source tabs or requests', async ({ page }) => {
    await loginAs(page, 'patient')
    const sourceRequests: string[] = []
    page.on('request', (request) => {
      if (new URL(request.url()).pathname.startsWith('/api/sources/')) sourceRequests.push(request.url())
    })
    await page.goto('/wissen/1')
    await expect(page.getByRole('region', { name: 'Warnzeichen', exact: true })).toBeVisible()
    await expect(page.getByRole('tablist')).toHaveCount(0)
    await expect(page.getByRole('contentinfo')).toContainText('Prototyp mit Beispieldaten – keine medizinische Beratung.')
    await captureReview(page, 'patient-detail')
    expect(sourceRequests).toEqual([])
  })
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
    await expect(page.getByText('Prototyp mit Beispieldaten – keine medizinische Beratung.').filter({ visible: true })).toBeVisible()
    await expect(page.getByRole('radiogroup', { name: 'Farbschema' }).filter({ visible: true })).toBeVisible()
    await expect(page.getByText(/Diplomarbeit an der TGM Wien/)).toBeVisible()
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(375)
  })
})
