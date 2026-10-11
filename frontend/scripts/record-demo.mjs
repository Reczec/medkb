// Records the README demo tour against a running MedKB (real sources and AI) and writes
// docs/media/demo.gif plus screenshots. Usage, from frontend/ with the app on :8000:
//   node scripts/record-demo.mjs            (BASE_URL=http://127.0.0.1:8000 by default)
// Needs ffmpeg on PATH for the GIF. Demo mode must be on (one-click roles).
import { execFileSync } from 'node:child_process'
import { mkdirSync, readdirSync, renameSync, rmSync } from 'node:fs'
import path from 'node:path'
import { chromium } from '@playwright/test'

const BASE_URL = process.env.BASE_URL ?? 'http://127.0.0.1:8000'
const MEDIA = path.resolve(import.meta.dirname, '../../docs/media')
const VIDEO_DIR = path.join(MEDIA, '.video')
const SIZE = { width: 1280, height: 800 }
const pause = (page, ms = 1200) => page.waitForTimeout(ms)

mkdirSync(MEDIA, { recursive: true })
rmSync(VIDEO_DIR, { recursive: true, force: true })

async function shot(page, name) {
  await page.mouse.move(0, 0) // no hover tooltips in the stills
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: path.join(MEDIA, `${name}.png`) })
}

async function loginAs(page, label) {
  await page.goto(`${BASE_URL}/login`)
  await page.getByRole('button', { name: `Als ${label} öffnen` }).click()
  await page.waitForURL((url) => !url.pathname.startsWith('/login'), { waitUntil: 'commit' })
}

async function logout(page) {
  await page.getByRole('button', { name: 'Abmelden' }).click()
  await page.waitForURL((url) => url.pathname === '/login', { waitUntil: 'commit' })
}

const browser = await chromium.launch()

// 1) The tour, recorded as video.
const tour = await browser.newContext({
  viewport: SIZE,
  colorScheme: 'light',
  recordVideo: { dir: VIDEO_DIR, size: SIZE },
})
const page = await tour.newPage()
await page.goto(`${BASE_URL}/login`)
await pause(page, 1500)
await loginAs(page, 'Ärztin / Arzt')
await page.getByRole('heading', { name: 'Überblick' }).waitFor()
await pause(page, 2500)

await page.goto(`${BASE_URL}/wissen`)
await page.getByRole('searchbox').pressSequentially('Migräne', { delay: 90 })
await pause(page, 1200)
await page.getByRole('link', { name: 'Migräne', exact: true }).first().click()
await page.getByRole('heading', { level: 1, name: 'Migräne' }).waitFor()
await pause(page, 1800)

for (const tab of ['Studien', 'ICD-11']) {
  const trigger = page.getByRole('tab', { name: tab })
  await trigger.click()
  await page.waitForLoadState('networkidle')
  await pause(page, 2200)
}
await page.getByRole('tab', { name: 'KI-Zusammenfassung' }).click()
await page.getByRole('button', { name: 'KI-Zusammenfassung' }).click()
await page.getByText('KI-generiert').first().waitFor()
await page.waitForFunction(() => !document.body.innerText.includes('Antwort wird erstellt'), null, {
  timeout: 60_000,
})
await pause(page, 2500)

await logout(page)
await loginAs(page, 'Patient:in')
await pause(page, 1500)
await page.goto(`${BASE_URL}/wissen?q=Migr%C3%A4ne`)
await page.getByRole('link', { name: 'Migräne', exact: true }).first().click()
await page.getByRole('button', { name: 'Warnzeichen erklären' }).click()
await page.getByText('Sofort Notruf 144').first().waitFor({ timeout: 60_000 })
await page.getByText('Sofort Notruf 144').first().scrollIntoViewIfNeeded()
await pause(page, 3000)

await page.goto(`${BASE_URL}/assistent`)
await page.getByLabel('Deine Frage').pressSequentially('Was hilft bei Migräne?', { delay: 60 })
await page.getByRole('button', { name: 'Frage stellen' }).click()
await page.getByRole('link', { name: /^\[1\]/ }).first().waitFor({ timeout: 60_000 })
await pause(page, 3000)
await tour.close()

// 2) Still screenshots: light and dark desktop, one phone view.
for (const scheme of ['light', 'dark']) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: scheme })
  const shots = await context.newPage()
  await loginAs(shots, 'Ärztin / Arzt')
  await shots.getByRole('heading', { name: 'Überblick' }).waitFor()
  await pause(shots, 1500)
  await shot(shots, `dashboard-${scheme}`)
  await shots.goto(`${BASE_URL}/wissen?q=Migr%C3%A4ne`)
  await shots.getByRole('link', { name: 'Migräne', exact: true }).first().click()
  await shots.getByRole('heading', { level: 1, name: 'Migräne' }).waitFor()
  await pause(shots, 800)
  await shot(shots, `entry-${scheme}`)
  await shots.getByRole('tab', { name: 'Studien' }).click()
  await pause(shots, 1500)
  await shot(shots, `studies-${scheme}`)
  await context.close()
}
const phone = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, colorScheme: 'light' })
const phonePage = await phone.newPage()
await loginAs(phonePage, 'Patient:in')
await pause(phonePage, 1500)
await shot(phonePage, 'patient-phone')
await phone.close()
await browser.close()

// 3) Video -> GIF (palette for clean colours, 8 fps, 880 px wide; stays under 8 MB).
const video = readdirSync(VIDEO_DIR).find((file) => file.endsWith('.webm'))
const webm = path.join(MEDIA, 'demo.webm')
renameSync(path.join(VIDEO_DIR, video), webm)
rmSync(VIDEO_DIR, { recursive: true, force: true })
execFileSync('ffmpeg', [
  '-y', '-loglevel', 'error', '-i', webm,
  '-vf', 'fps=8,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4',
  path.join(MEDIA, 'demo.gif'),
])
rmSync(webm)
console.log('Wrote', MEDIA)
