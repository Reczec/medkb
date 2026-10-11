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

it('reviews and explicitly applies a draft, then saves its AI provenance', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification,
    '/api/ai/draft': { text: 'Allgemeiner Entwurf.', cached: false, citations: [], draft: {
      title: 'Herzrasen', content: 'Allgemeiner Entwurf zu Herzrasen.', doc_type: 'Diagnose',
      term_en: 'Palpitations', icd11_code: 'BC81', medications: [], ai_generated: true,
    } }, '/api/documents': saved,
  })
  renderEditor()
  fireEvent.change(await screen.findByLabelText('Titel'), { target: { value: 'Herzrasen' } })
  fireEvent.click(screen.getByRole('button', { name: 'KI-Entwurf erstellen' }))
  expect(await screen.findByText('Allgemeiner Entwurf.')).toBeInTheDocument()
  expect(screen.getByLabelText('Inhalt')).toHaveValue('')
  fireEvent.click(screen.getByRole('button', { name: 'Geprüften Entwurf übernehmen' }))
  expect(screen.getByLabelText('Inhalt')).toHaveValue('Allgemeiner Entwurf zu Herzrasen.')
  expect(screen.getByLabelText('Fachbegriff (en)')).toHaveValue('Palpitations')
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await screen.findByText('Detailseite')
  expect(bodies(fetchMock, 'POST').find(call => call.url === '/api/documents')?.body.ai_generated).toBe(true)
})

it('shows an AI category opinion separately and applies it only on request', async () => {
  mockFetch({ '/api/meta': meta, '/api/classify': classification,
    '/api/ai/classify': { text: 'Separate Meinung.', cached: false, citations: [], classification: { category: 'HNO', confidence: 0.6, reasoning: 'Separate Meinung.' } },
  })
  renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('button', { name: 'KI-Zweitmeinung anfordern' }))
  expect(await screen.findByText('Separate Meinung.')).toBeInTheDocument()
  expect(screen.getByRole('radio', { name: /Automatisch/ })).toBeChecked()
  fireEvent.click(screen.getByRole('button', { name: 'Fachgebiet HNO übernehmen' }))
  expect(screen.getByRole('radio', { name: 'HNO' })).toBeChecked()
})
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
    term_en: null,
    icd11_code: null,
    medications: [],
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

const structured = {
  ...saved, term_en: 'Migraine', icd11_code: '8A80', medications: ['ibuprofen'],
  sections: { definition: 'Migräne mit Kopfschmerzen.', symptoms: 'Lichtempfindlichkeit.', red_flags: 'Bei Lähmungen sofort 144.' },
  further_reading: [{ label: 'WHO', url: 'https://www.who.int/' }], ai_generated: true,
}

it('creates and previews sections without sending free text', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents': saved })
  const { router } = renderEditor()
  await fillNewEntry()
  fireEvent.click(screen.getByRole('button', { name: 'Abschnitte' }))
  expect(screen.getByLabelText('Definition')).toHaveValue('Herzrasen und Brustschmerzen bei Belastung.')
  fireEvent.change(screen.getByLabelText('Symptome'), { target: { value: 'Brustschmerz.' } })
  await waitFor(() => expect(bodies(fetchMock, 'POST').some((call) => call.url === '/api/classify' && call.body.sections?.symptoms === 'Brustschmerz.')).toBe(true))
  const preview = bodies(fetchMock, 'POST').findLast((call) => call.url === '/api/classify')!
  expect(preview.body).not.toHaveProperty('content')
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  const create = bodies(fetchMock, 'POST').find((call) => call.url === '/api/documents')!
  expect(create.body.sections).toMatchObject({ definition: 'Herzrasen und Brustschmerzen bei Belastung.', symptoms: 'Brustschmerz.' })
  expect(create.body).not.toHaveProperty('content')
})

it('prefills sections and only patches the changed structured content', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents/9': structured })
  renderEditor('/wissen/9/bearbeiten')
  expect(await screen.findByLabelText('Definition')).toHaveValue('Migräne mit Kopfschmerzen.')
  expect(screen.getByLabelText('Fachbegriff (en)')).toHaveValue('Migraine')
  expect(screen.getByLabelText('ICD-11-Code')).toHaveValue('8A80')
  expect(screen.getByRole('button', { name: 'Abschnitte' })).toHaveAttribute('aria-pressed', 'true')
  fireEvent.change(screen.getByLabelText('Therapie'), { target: { value: 'Bewegung und Ruhe.' } })
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(bodies(fetchMock, 'PATCH')).toHaveLength(1))
  const patch = bodies(fetchMock, 'PATCH')[0].body
  expect(patch.sections.therapy).toBe('Bewegung und Ruhe.')
  expect(patch.reclassify).toBe(true)
  expect(patch).not.toHaveProperty('content')
  expect(patch).not.toHaveProperty('further_reading')
  expect(patch).not.toHaveProperty('ai_generated')
})

it('sends content without sections when converting an entry to free text', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents/9': structured })
  renderEditor('/wissen/9/bearbeiten')
  await screen.findByLabelText('Definition')
  fireEvent.click(screen.getByRole('button', { name: 'Freitext' }))
  expect(screen.getByLabelText('Inhalt')).toHaveValue('Definition\nMigräne mit Kopfschmerzen.\n\nSymptome\nLichtempfindlichkeit.\n\nWarnzeichen\nBei Lähmungen sofort 144.')
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(bodies(fetchMock, 'PATCH')).toHaveLength(1))
  expect(bodies(fetchMock, 'PATCH')[0].body.content).toContain('Symptome\nLichtempfindlichkeit.')
  expect(bodies(fetchMock, 'PATCH')[0].body).not.toHaveProperty('sections')
})

it('adds and removes active ingredients and clears optional fields', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents/9': structured })
  renderEditor('/wissen/9/bearbeiten')
  fireEvent.click(await screen.findByRole('button', { name: 'ibuprofen entfernen' }))
  fireEvent.change(screen.getByRole('textbox', { name: 'Wirkstoff hinzufügen' }), { target: { value: 'metformin' } })
  fireEvent.keyDown(screen.getByRole('textbox', { name: 'Wirkstoff hinzufügen' }), { key: 'Enter' })
  fireEvent.change(screen.getByLabelText('Fachbegriff (en)'), { target: { value: '' } })
  fireEvent.change(screen.getByLabelText('ICD-11-Code'), { target: { value: '' } })
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(bodies(fetchMock, 'PATCH')).toHaveLength(1))
  expect(bodies(fetchMock, 'PATCH')[0].body).toEqual({ medications: ['metformin'], term_en: null, icd11_code: null })
})

it('keeps the form and shows the ICD field error from a 422 response', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents': new Response(JSON.stringify({ detail: [{ loc: ['body', 'icd11_code'], msg: 'Not an ICD-11 stem code.' }] }), { status: 422 }) })
  const { router } = renderEditor()
  await fillNewEntry()
  fireEvent.change(screen.getByLabelText('ICD-11-Code'), { target: { value: '8A80.123' } })
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  expect(await screen.findByText('icd11_code: Not an ICD-11 stem code.')).toBeInTheDocument()
  expect(screen.getByLabelText('ICD-11-Code')).toHaveValue('8A80.123')
  expect(router.state.location.pathname).toBe('/wissen/neu')
  expect(bodies(fetchMock, 'POST').find((call) => call.url === '/api/documents')!.body.icd11_code).toBe('8A80.123')
})

it('does not patch an untouched structured entry', async () => {
  const fetchMock = mockFetch({ '/api/meta': meta, '/api/classify': classification, '/api/documents/9': structured })
  const { router } = renderEditor('/wissen/9/bearbeiten')
  await screen.findByLabelText('Definition')
  fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen/9'))
  expect(bodies(fetchMock, 'PATCH')).toHaveLength(0)
})

it('blocks leaving a new form when only an optional field changed', async () => {
  mockFetch({ '/api/meta': meta })
  renderEditor()
  fireEvent.change(await screen.findByLabelText('Fachbegriff (en)'), { target: { value: 'Migraine' } })
  fireEvent.click(screen.getByRole('link', { name: 'Abbrechen' }))
  expect(await screen.findByRole('alertdialog')).toHaveTextContent('Änderungen verwerfen?')
})
