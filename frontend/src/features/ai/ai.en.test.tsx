import { act, fireEvent, screen, waitFor } from '@testing-library/react'
import { requestAI } from '@/features/ai/client'
import { LanguageSwitch } from '@/i18n/LanguageSwitch'
import { setApiLanguage } from '@/i18n/lang'
import { mockFetch, renderWithProviders, TEST_USERS } from '@/test/utils'
import { AssistantPage } from './AssistantPage'
import { DocumentAI } from './DocumentAI'

afterEach(() => {
  vi.unstubAllGlobals()
  setApiLanguage('en')
})

const en = { lang: 'en' as const }

it('labels the document panel and answer in English', async () => {
  mockFetch({ '/api/ai/documents/5/explain': { text: 'General explanation.', cached: true, citations: [] } })
  renderWithProviders(<DocumentAI documentId={5} />, { ...en, user: TEST_USERS.patient })
  expect(screen.getByRole('region', { name: 'AI help' })).toBeInTheDocument()
  expect(screen.getByText('Make the entry easier to understand with AI.')).toBeInTheDocument()
  fireEvent.click(screen.getByRole('button', { name: 'Explain simply' }))
  expect(await screen.findByText('General explanation.')).toBeInTheDocument()
  expect(screen.getByText('AI-generated')).toBeInTheDocument()
  expect(screen.getByText('· Already generated')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Explain warning signs' })).toBeInTheDocument()
})

it('names the staff summary button in English', () => {
  mockFetch({})
  renderWithProviders(<DocumentAI documentId={5} summaryOnly />, en)
  expect(screen.getByRole('button', { name: 'AI summary' })).toBeInTheDocument()
  expect(screen.getByText('Professional summary to review.')).toBeInTheDocument()
})

it('explains a missing AI configuration in English with a retry button', async () => {
  mockFetch({ '/api/ai': new Response(JSON.stringify({ detail: 'ai_not_configured' }), { status: 503 }) })
  renderWithProviders(<DocumentAI documentId={5} summaryOnly />, en)
  fireEvent.click(screen.getByRole('button', { name: 'AI summary' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('The AI is not set up yet.')
  expect(screen.getByRole('button', { name: 'Try again' })).toBeInTheDocument()
})

it('explains the daily limit in English', async () => {
  mockFetch({ '/api/ai/ask': new Response(JSON.stringify({ detail: 'limit' }), { status: 429 }) })
  renderWithProviders(<AssistantPage />, en)
  fireEvent.change(screen.getByLabelText('Your question'), { target: { value: 'migraine' } })
  fireEvent.click(screen.getByRole('button', { name: 'Ask' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Daily AI limit reached.')
})

it('translates client errors by the API language', async () => {
  setApiLanguage('en')
  vi.stubGlobal('fetch', vi.fn().mockImplementation(async () => new Response(JSON.stringify({ detail: 'ai_not_configured' }), { status: 503 })))
  await expect(requestAI('/ask', {})).rejects.toThrow('not set up yet')
  setApiLanguage('de')
  await expect(requestAI('/ask', {})).rejects.toThrow('noch nicht eingerichtet')
})

it('drops a running request and its text when the language changes', async () => {
  let signal: AbortSignal | undefined
  const encoder = new TextEncoder()
  vi.stubGlobal('fetch', vi.fn(async (_url: string, init?: RequestInit) => {
    signal = init?.signal as AbortSignal
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(encoder.encode('event: token\ndata: {"text":"Partial english"}\n\n'))
        signal?.addEventListener('abort', () => controller.error(new DOMException('Aborted', 'AbortError')))
      },
    })
    return new Response(stream, { headers: { 'Content-Type': 'text/event-stream' } })
  }))
  renderWithProviders(
    <>
      <LanguageSwitch tone="surface" />
      <DocumentAI documentId={5} />
    </>,
    { ...en, user: TEST_USERS.patient },
  )
  fireEvent.click(screen.getByRole('button', { name: 'Explain simply' }))
  expect(await screen.findByText('Partial english')).toBeInTheDocument()
  await act(async () => {
    fireEvent.click(screen.getByRole('button', { name: /German/ }))
  })
  await waitFor(() => expect(signal?.aborted).toBe(true))
  expect(screen.queryByText('Partial english')).not.toBeInTheDocument()
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Einfach erklären' })).toBeEnabled()
})
