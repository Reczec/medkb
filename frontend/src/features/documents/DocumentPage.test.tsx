import { fireEvent, screen, waitFor, within } from '@testing-library/react'
import { DocumentPage } from '@/features/documents/DocumentPage'
import { mockFetch, PLAIN_FIELDS, renderWithProviders } from '@/test/utils'

vi.mock('motion/react', async (importOriginal) => ({
  ...(await importOriginal<typeof import('motion/react')>()),
  useReducedMotion: () => true,
}))

afterEach(() => vi.unstubAllGlobals())

const document5 = {
  id: 5, title: 'Herzinsuffizienz', content: 'Absatz eins.\n\nAbsatz zwei mit Atemnot.',
  category: 'Kardiologie', doc_type: 'Diagnose', keywords: ['Herz', 'Atemnot'],
  source: 'Lehrbuch', auto_classified: true, ...PLAIN_FIELDS,
  created_at: '2026-10-01T10:00:00Z', updated_at: '2026-10-02T10:00:00Z',
}
const classification = {
  category: 'Kardiologie', confidence: 0.83, fallback: false,
  scores: { Kardiologie: 10, 'Innere Medizin': 2, HNO: 0 },
  matched_terms: ['herz', 'atemnot'], keywords: ['Herz'],
}

const render = () =>
  renderWithProviders(<DocumentPage />, {
    path: '/wissen/5',
    route: '/wissen/:id',
    routes: [{ path: '/wissen', element: <p>Liste</p> }],
  })

it('shows the entry with its specialty and paragraphs', async () => {
  mockFetch({ '/api/documents/5': document5, '/api/classify': classification })
  render()
  expect(await screen.findByRole('heading', { level: 1, name: 'Herzinsuffizienz' })).toBeInTheDocument()
  expect(screen.getAllByText('Kardiologie').length).toBeGreaterThan(0)
  expect(screen.getByText('Absatz zwei mit Atemnot.')).toBeInTheDocument()
})

it('explains the classification with score bars and matched terms', async () => {
  mockFetch({ '/api/documents/5': document5, '/api/classify': classification })
  render()
  const explainer = await screen.findByRole('region', { name: 'Klassifikation' })
  expect(await within(explainer).findByText('Innere Medizin')).toBeInTheDocument()
  expect(within(explainer).getByText('Kardiologie')).toBeInTheDocument()
  expect(within(explainer).queryByText('HNO')).not.toBeInTheDocument()
  expect(within(explainer).getByText('atemnot')).toBeInTheDocument()
})

it('says when the entry does not exist', async () => {
  mockFetch({ '/api/documents/5': new Response(JSON.stringify({ detail: 'Document not found.' }), { status: 404 }) })
  render()
  expect(await screen.findByText('Eintrag nicht gefunden')).toBeInTheDocument()
})

it('deletes after confirmation and returns to the list', async () => {
  const fetchMock = mockFetch({ '/api/documents/5': document5, '/api/classify': classification })
  const { router } = render()
  fireEvent.click(await screen.findByRole('button', { name: /Löschen/ }))
  const dialog = await screen.findByRole('alertdialog')
  expect(within(dialog).getByText('Eintrag endgültig löschen?')).toBeInTheDocument()
  fetchMock.mockImplementationOnce(async () => new Response(null, { status: 204 }))
  fireEvent.click(within(dialog).getByRole('button', { name: 'Endgültig löschen' }))
  await waitFor(() => expect(router.state.location.pathname).toBe('/wissen'))
  const calls = fetchMock.mock.calls as unknown as [string, RequestInit | undefined][]
  expect(calls.some(([url, init]) => url === '/api/documents/5' && init?.method === 'DELETE')).toBe(true)
})

it('treats a non-numeric id as not found instead of loading forever', async () => {
  mockFetch({})
  renderWithProviders(<DocumentPage />, { path: '/wissen/abc', route: '/wissen/:id' })
  expect(await screen.findByText('Eintrag nicht gefunden')).toBeInTheDocument()
})

const structured = {
  ...document5,
  term_en: 'Heart failure',
  icd11_code: 'BD10',
  sections: { definition: 'Das Herz pumpt zu wenig.', symptoms: 'Atemnot.', therapy: 'Medikamente.' },
  further_reading: [{ label: 'MedlinePlus (NIH, englisch): Heart Failure', url: 'https://medlineplus.gov/heartfailure.html' }],
}

it('shows a structured entry by its sections', async () => {
  mockFetch({ '/api/documents/5': structured, '/api/classify': classification })
  render()
  expect(await screen.findByRole('heading', { level: 2, name: 'Symptome' })).toBeInTheDocument()
  expect(screen.getByRole('heading', { level: 2, name: 'Therapie' })).toBeInTheDocument()
  expect(screen.queryByText('Absatz eins.')).not.toBeInTheDocument()
})

it('lists the English term and the ICD-11 code in the details', async () => {
  mockFetch({ '/api/documents/5': structured, '/api/classify': classification })
  render()
  const details = await screen.findByRole('region', { name: 'Details' })
  expect(within(details).getByText('Heart failure')).toBeInTheDocument()
  expect(within(details).getByText('BD10')).toBeInTheDocument()
})

it('opens further reading in a new tab and names the site', async () => {
  mockFetch({ '/api/documents/5': structured, '/api/classify': classification })
  render()
  const reading = await screen.findByRole('region', { name: 'Weiterlesen' })
  const link = within(reading).getByRole('link', { name: /Heart Failure/ })
  expect(link).toHaveAttribute('href', 'https://medlineplus.gov/heartfailure.html')
  expect(link).toHaveAttribute('target', '_blank')
  expect(link).toHaveAttribute('rel', 'noreferrer noopener')
  expect(within(reading).getByText('medlineplus.gov')).toBeInTheDocument()
})
