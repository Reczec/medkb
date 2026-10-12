import { fireEvent, screen } from '@testing-library/react'
import { DocumentAI } from './DocumentAI'
import { AssistantPage } from './AssistantPage'
import { mockFetch, renderWithProviders, TEST_USERS } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

it.each([
  ['en', 'Your question', 'Ask', 'Semantic + keyword search', 'Source excerpt'],
  ['de', 'Deine Frage', 'Frage stellen', 'Semantische + Stichwortsuche', 'Quellenauszug'],
] as const)('shows retrieval and source evidence in %s', async (lang, label, action, mode, disclosure) => {
  mockFetch({ '/api/ai/ask': { text: 'Evidence [1].', cached: false,
    retrieval: { mode: 'hybrid', indexed_chunks: 12 },
    citations: [{ index: 1, id: 5, title: 'Migräne', section: 'symptoms', excerpt: '<script>untrusted</script>' }] } })
  renderWithProviders(<AssistantPage />, { lang })
  fireEvent.change(screen.getByLabelText(label), { target: { value: 'Pounding head?' } })
  fireEvent.click(screen.getByRole('button', { name: action }))
  expect(await screen.findByText(mode)).toBeInTheDocument()
  const toggle = screen.getByText(disclosure, { exact: false })
  expect(toggle.tagName).toBe('SUMMARY')
  expect(screen.getByText('<script>untrusted</script>')).toBeInTheDocument()
  expect(document.querySelector('script')).toBeNull()
})

it('explains keyword fallback without implying semantic success', async () => {
  mockFetch({ '/api/ai/ask': { text: 'No sources.', cached: false, citations: [],
    retrieval: { mode: 'lexical', reason: 'index_incomplete', indexed_chunks: 0 } } })
  renderWithProviders(<AssistantPage />, { lang: 'en' })
  fireEvent.change(screen.getByLabelText('Your question'), { target: { value: 'Example?' } })
  fireEvent.click(screen.getByRole('button', { name: 'Ask' }))
  expect(await screen.findByText('Keyword search')).toBeInTheDocument()
  expect(screen.getByText('The semantic index is not ready.')).toBeInTheDocument()
})

it('offers patient explanations and warning signs, with a labelled result', async () => {
  mockFetch({ '/api/ai/documents/5/explain': { text: 'Allgemeine Erklärung.', cached: true, citations: [] } })
  renderWithProviders(<DocumentAI documentId={5} />, { user: TEST_USERS.patient })
  expect(screen.queryByRole('button', { name: 'KI-Zusammenfassung' })).not.toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: 'Einfach erklären' }))
  expect(await screen.findByText('Allgemeine Erklärung.')).toBeInTheDocument()
  expect(screen.getByText('KI-generiert')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Warnzeichen erklären' })).toBeInTheDocument()
})

it('offers staff summaries and retry after configuration errors', async () => {
  mockFetch({ '/api/ai': new Response(JSON.stringify({ detail: 'ai_not_configured' }), { status: 503 }) })
  renderWithProviders(<DocumentAI documentId={5} summaryOnly />)
  fireEvent.click(screen.getByRole('button', { name: 'KI-Zusammenfassung' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('noch nicht eingerichtet')
  expect(screen.getByRole('button', { name: 'Erneut versuchen' })).toBeInTheDocument()
})

it('answers a question with links to the actual knowledge entries', async () => {
  mockFetch({ '/api/ai/ask': { text: 'Erklärung [1].', cached: false, citations: [{ index: 1, id: 5, title: 'Migräne' }] } })
  renderWithProviders(<AssistantPage />)
  fireEvent.change(screen.getByLabelText('Deine Frage'), { target: { value: 'Migräne' } })
  fireEvent.click(screen.getByRole('button', { name: 'Frage stellen' }))
  expect(await screen.findByRole('link', { name: '[1] Migräne' })).toHaveAttribute('href', '/wissen/5')
})

it('records a successfully retried exchange before a followup request', async () => {
  const result = { text: 'Erklärung [1].', cached: false, citations: [{ index: 1, id: 5, title: 'Migräne' }] }
  const fetchMock = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ detail: 'ai_unavailable' }), { status: 503 }))
    .mockImplementation(async () => new Response(JSON.stringify(result)))
  vi.stubGlobal('fetch', fetchMock)
  renderWithProviders(<AssistantPage />)
  fireEvent.change(screen.getByLabelText('Deine Frage'), { target: { value: 'Was ist Migräne?' } })
  fireEvent.click(screen.getByRole('button', { name: 'Frage stellen' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Erneut versuchen' }))
  await screen.findByRole('link', { name: '[1] Migräne' })
  expect(screen.getByRole('button', { name: 'Gespräch zurücksetzen' })).toBeInTheDocument()
  expect(screen.getByLabelText('Deine Frage')).toHaveValue('')
  fireEvent.change(screen.getByLabelText('Deine Frage'), { target: { value: 'Wie wird das behandelt?' } })
  fireEvent.click(screen.getByRole('button', { name: 'Frage stellen' }))
  const options = fetchMock.mock.calls.at(-1)![1] as RequestInit
  expect(JSON.parse(String(options.body)).history).toEqual([
    { role: 'user', content: 'Was ist Migräne?' }, { role: 'assistant', content: 'Erklärung [1].' },
  ])
})
