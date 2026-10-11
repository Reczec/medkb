import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { Toaster } from 'sonner'
import { EditorPage } from '@/features/editor/EditorPage'
import { LanguageSwitch } from '@/i18n/LanguageSwitch'
import type { Lang } from '@/i18n/lang'
import { mockFetch, PLAIN_FIELDS, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const meta = {
  categories: ['Kardiologie', 'HNO'],
  doc_types: ['Symptom', 'Diagnose'],
  default_category: 'Allgemeinmedizin',
}
const classification = {
  category: 'Kardiologie',
  confidence: 0.83,
  fallback: false,
  scores: { Kardiologie: 10, HNO: 2 },
  matched_terms: ['herz'],
  keywords: ['Herzrasen'],
}
const saved = {
  id: 9,
  title: 'Herzrasen',
  content: 'Herzrasen und Brustschmerzen bei Belastung.',
  category: 'Kardiologie',
  doc_type: 'Symptom',
  keywords: ['Herzrasen'],
  source: null,
  auto_classified: true,
  ...PLAIN_FIELDS,
  created_at: '2026-10-01T10:00:00Z',
  updated_at: '2026-10-01T10:00:00Z',
}
const translated = {
  ...saved,
  title_en: 'Palpitations',
  content_en: 'Palpitations and chest pain on exertion.',
  keywords_en: ['Palpitations'],
}

type Call = [string, RequestInit | undefined]
const bodies = (fetchMock: ReturnType<typeof mockFetch>, method: string) =>
  (fetchMock.mock.calls as unknown as Call[])
    .filter(([, init]) => init?.method === method)
    .map(([url, init]) => ({ url, body: JSON.parse(String(init?.body)) }))

function renderEditor(path = '/wissen/neu', lang: Lang = 'en') {
  return renderWithProviders(
    <>
      <LanguageSwitch tone="surface" />
      <EditorPage />
      <Toaster />
    </>,
    {
      lang,
      path,
      route: path === '/wissen/neu' ? '/wissen/neu' : '/wissen/:id/bearbeiten',
      routes: [{ path: '/wissen/:id', element: <p>Detail page</p> }],
    },
  )
}

async function fillNewEntry() {
  fireEvent.change(await screen.findByLabelText('Title'), { target: { value: 'Herzrasen' } })
  fireEvent.change(screen.getByLabelText('Content'), {
    target: { value: 'Herzrasen und Brustschmerzen bei Belastung.' },
  })
}

it('labels the editor in English and explains the German canonical text', async () => {
  mockFetch({ '/api/meta': meta, '/api/classify': classification })
  renderEditor()
  expect(await screen.findByRole('heading', { level: 1, name: 'New entry' })).toBeInTheDocument()
  expect(await screen.findByLabelText('Title')).toBeInTheDocument()
  expect(screen.getByLabelText('Source (optional)')).toBeInTheDocument()
  expect(screen.getByLabelText('English term')).toBeInTheDocument()
  expect(screen.getByLabelText('ICD-11 code')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Free text' })).toHaveAttribute('aria-pressed', 'true')
  expect(screen.getByText(/Entries are written in German/)).toBeInTheDocument()
  expect(screen.getByRole('radio', { name: /Automatic/ })).toBeChecked()
  expect(screen.getByRole('button', { name: 'Save' })).toBeDisabled()
  expect(screen.getByRole('complementary', { name: 'Live classification' })).toBeInTheDocument()
})

it('sends no English fields when the English version stays empty', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents': saved })
  const { router } = renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('button', { name: 'Save' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  const create = bodies(fetchMock, 'POST').find((c) => c.url === '/api/documents')!
  expect(create.body).not.toHaveProperty('title_en')
  expect(create.body).not.toHaveProperty('content_en')
  expect(create.body).not.toHaveProperty('sections_en')
  expect(create.body).not.toHaveProperty('keywords_en')
})

it('sends the English version entered in the collapsible section', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents': saved })
  const { router } = renderEditor()
  await fillNewEntry()
  expect(screen.queryByLabelText('Title (English)')).not.toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: /English version/ }))
  fireEvent.change(screen.getByLabelText('Title (English)'), { target: { value: 'Palpitations' } })
  fireEvent.change(screen.getByLabelText('Content (English)'), {
    target: { value: 'Palpitations and chest pain on exertion.' },
  })
  const keywords = screen.getByRole('textbox', { name: 'Add English keyword' })
  fireEvent.change(keywords, { target: { value: 'Palpitations' } })
  fireEvent.keyDown(keywords, { key: 'Enter' })
  fireEvent.click(screen.getByRole('button', { name: 'Save' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  const create = bodies(fetchMock, 'POST').find((c) => c.url === '/api/documents')!
  expect(create.body).toMatchObject({
    title: 'Herzrasen',
    title_en: 'Palpitations',
    content_en: 'Palpitations and chest pain on exertion.',
    keywords_en: ['Palpitations'],
  })
})

it('sends English sections in section mode', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents': saved })
  const { router } = renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('button', { name: 'Sections' }))
  fireEvent.click(screen.getByRole('button', { name: /English version/ }))
  fireEvent.change(screen.getByLabelText('Definition (English)'), { target: { value: 'A heart rhythm symptom.' } })
  fireEvent.click(screen.getByRole('button', { name: 'Save' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  const create = bodies(fetchMock, 'POST').find((c) => c.url === '/api/documents')!
  expect(create.body.sections_en).toEqual({ definition: 'A heart rhythm symptom.' })
  expect(create.body).not.toHaveProperty('content_en')
})

it('opens the English version of a translated entry and clears a field with null', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents/9': translated })
  const { router } = renderEditor('/wissen/9/bearbeiten')
  const title = await screen.findByLabelText('Title (English)')
  expect(title).toHaveValue('Palpitations')
  expect(screen.getByLabelText('Content (English)')).toHaveValue('Palpitations and chest pain on exertion.')
  fireEvent.change(title, { target: { value: '' } })
  fireEvent.click(screen.getByRole('button', { name: 'Save' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  expect(bodies(fetchMock, 'PATCH')[0].body).toEqual({ title_en: null })
})

it('keeps typed values and the editor mounted when the language changes', async () => {
  mockFetch({ '/api/meta': meta, '/api/classify': classification })
  renderEditor()
  const title = await screen.findByLabelText('Title')
  fireEvent.change(title, { target: { value: 'Herzrasen' } })
  fireEvent.click(screen.getByRole('button', { name: /English version/ }))
  fireEvent.change(screen.getByLabelText('Title (English)'), { target: { value: 'Palpitations' } })
  fireEvent.click(screen.getByRole('button', { name: /German/ }))
  const germanTitle = await screen.findByLabelText('Titel')
  expect(germanTitle).toBe(title)
  expect(germanTitle).toHaveValue('Herzrasen')
  expect(screen.getByLabelText('Titel (englisch)')).toHaveValue('Palpitations')
  expect(screen.getByRole('button', { name: 'Speichern' })).toBeInTheDocument()
})

it('notes that the AI draft is written in German', async () => {
  mockFetch({ '/api/meta': meta })
  renderEditor()
  const panel = await screen.findByRole('region', { name: 'AI assistance' })
  expect(within(panel).getByRole('button', { name: 'Create AI draft' })).toBeInTheDocument()
  expect(within(panel).getByText('Draft is written in German.')).toBeInTheDocument()
  expect(within(panel).getByRole('button', { name: 'Request AI second opinion' })).toBeInTheDocument()
})
