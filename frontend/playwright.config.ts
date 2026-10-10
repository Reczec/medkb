import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { defineConfig, devices } from '@playwright/test'

const PORT = 8765
const python = process.env.PYTHON ?? 'python'
const scratch = path.join(os.tmpdir(), `medkb-e2e-${Date.now()}`)
fs.mkdirSync(scratch, { recursive: true })

/**
 * Smoke tests against the real stack: FastAPI serves the built frontend (run `npm run build` first)
 * in demo mode with a fresh SQLite database seeded with the example entries.
 */
export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['github'], ['list']] : 'list',
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: `"${python}" -m uvicorn app.main:app --host 127.0.0.1 --port ${PORT}`,
    cwd: path.resolve(import.meta.dirname, '..'),
    url: `http://127.0.0.1:${PORT}/api/health`,
    reuseExistingServer: false,
    timeout: 60_000,
    env: {
      DATABASE_URL: `sqlite:///${path.join(scratch, 'e2e.db').replaceAll('\\', '/')}`,
      ARCHIVE_DIR: path.join(scratch, 'archives'),
      DEMO_MODE: 'true',
      JWT_SECRET: 'e2e-secret-that-is-at-least-32-characters',
    },
  },
})
