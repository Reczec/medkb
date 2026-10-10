import { fireEvent, screen, waitFor } from '@testing-library/react'
import { Toaster } from 'sonner'
import { EditorPage } from '@/features/editor/EditorPage'
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
  keywords: ['Herzrasen', 'Brustschmerz'],
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

type Call = [string, RequestInit | undefined]
const bodies = (fetchMock: ReturnType<typeof mockFetch>, method: string) =>
  (fetchMock.mock.calls as unknown as Call[])
    .filter(([, init]) => init?.method === method)
    .map(([url, init]) => ({ url, body: JSON.parse(String(init?.body)) }))

function renderEditor(path = '/wissen/neu') {
  return renderWithProviders(
    <>
      <EditorPage />
      <Toaster />
    </>,
    {
      path,
      route: path === '/wissen/neu' ? '/wissen/neu' : '/wissen/:id/bearbeiten',
      routes: [{ path: '/wissen/:id', element: <p>Detailseite</p> }],
    },
  )
}

async function fillNewEntry() {
  fireEvent.change(await screen.findByLabelText('Titel'), { target: { value: 'Herzrasen' } })
  fireEvent.change(screen.getByLabelText('Inhalt'), {
    target: { value: 'Herzrasen und Brustschmerzen bei Belastung.' },
  })
}

it('classifies live while typing', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification })
  renderEditor()
  await fillNewEntry()
  expect(await screen.findByText(/Vorschlag: Kardiologie/)).toBeInTheDocument()
  expect(bodies(fetchMock, 'POST').some((c) => c.url === '/api/classify')).toBe(true)
  expect(screen.getByRole('radio', { name: /Automatisch/ })).toHaveTextContent('Kardiologie')
})

it('creates an entry without a category when automatic is kept', async () => {
  const fetchMock = mockFetch({
    '/api/meta': meta,
    '/api/classify': classification,
    '/api/documents': saved,
  })
  const { router } = renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  const create = bodies(fetchMock, 'POST').find((c) => c.url === '/api/documents')!
  expect(create.body).toEqual({
    title: 'Herzrasen',
    content: 'Herzrasen und Brustschmerzen bei Belastung.',
    doc_type: 'Symptom',
  })
})

it('sends a manual category when one is chosen', async () => {
  const fetchMock = mockFetch({
    '/api/meta': meta,
    '/api/classify': classification,
    '/api/documents': saved,
  })
  renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('radio', { name: 'HNO' }))
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() =>
    expect(bodies(fetchMock, 'POST').some((c) => c.url === '/api/documents')).toBe(true),
  )
  const create = bodies(fetchMock, 'POST').find((c) => c.url === '/api/documents')!
  expect(create.body.category).toBe('HNO')
})

it('asks the classifier again when switching back to automatic and keeps the keywords', async () => {
  const manual = { ...saved, category: 'HNO', auto_classified: false, keywords: ['MeinSchlagwort'] }
  const fetchMock = mockFetch({
    '/api/meta': meta,
    '/api/classify': classification,
    '/api/documents/9': manual,
  })
  const { router } = renderEditor('/wissen/9/bearbeiten')
  fireEvent.click(await screen.findByRole('radio', { name: /Automatisch/ }))
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  expect(bodies(fetchMock, 'PATCH')[0].body).toEqual({
    reclassify: true,
    keywords: ['MeinSchlagwort'],
  })
})

it('reclassifies an automatic entry when its text changes', async () => {
  const fetchMock = mockFetch({
    '/api/meta': meta,
    '/api/classify': classification,
    '/api/documents/9': saved,
  })
  renderEditor('/wissen/9/bearbeiten')
  fireEvent.change(await screen.findByLabelText('Inhalt'), {
    target: { value: 'Ohrenschmerzen und Schwindel seit gestern.' },
  })
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(bodies(fetchMock, 'PATCH')).toHaveLength(1))
  expect(bodies(fetchMock, 'PATCH')[0].body).toEqual({
    content: 'Ohrenschmerzen und Schwindel seit gestern.',
    reclassify: true,
    keywords: ['Herzrasen'],
  })
})

it('only sends changed fields when editing', async () => {
  const fetchMock = mockFetch({
    '/api/meta': meta,
    '/api/classify': classification,
    '/api/documents/9': saved,
  })
  renderEditor('/wissen/9/bearbeiten')
  fireEvent.change(await screen.findByLabelText('Quelle (optional)'), {
    target: { value: 'Leitlinie Herzrhythmus' },
  })
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(bodies(fetchMock, 'PATCH')).toHaveLength(1))
  expect(bodies(fetchMock, 'PATCH')[0].body).toEqual({ source: 'Leitlinie Herzrhythmus' })
})

it('shows validation errors from the server', async () => {
  const error = new Response(
    JSON.stringify({
      detail: [{ loc: ['body', 'title'], msg: 'String should have at least 3 characters' }],
    }),
    { status: 422 },
  )
  mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents': error })
  renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  expect(
    await screen.findByText(/title: String should have at least 3 characters/),
  ).toBeInTheDocument()
})

it('says so when the id in the address is not a number', async () => {
  mockFetch({ '/api/meta': meta })
  renderEditor('/wissen/abc/bearbeiten')
  expect(await screen.findByText('Eintrag nicht gefunden')).toBeInTheDocument()
})
