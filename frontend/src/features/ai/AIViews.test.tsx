import { fireEvent, screen } from '@testing-library/react'
import { DocumentAI } from './DocumentAI'
import { AssistantPage } from './AssistantPage'
import { mockFetch, renderWithProviders, TEST_USERS } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

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
