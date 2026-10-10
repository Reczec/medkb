import { fireEvent, screen, waitFor } from '@testing-library/react'
import { Icd11Panel } from '@/features/documents/sources/Icd11Panel'
import { MedicationsPanel } from '@/features/documents/sources/MedicationsPanel'
import { StudiesPanel } from '@/features/documents/sources/StudiesPanel'
import { mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

const FETCHED = new Date(Date.now() - 5 * 60 * 1000).toISOString()
const ok = <T,>(data: T) => ({ status: 'ok', fetched_at: FETCHED, data })
const bare = (status: string) => ({ status, fetched_at: null, data: null })

const STUDIES_URL = '/api/sources/documents/5/studies'
const ICD_URL = '/api/sources/documents/5/icd11'
const MEDS_URL = '/api/sources/documents/5/medications'

const studies = [
  {
    pmid: '41000002', title: 'Triptans in acute migraine', journal: 'Cephalalgia', year: 2026,
    authors: ['Müller A', 'Smith B', 'Rossi C'], more_authors: true,
    url: 'https://pubmed.ncbi.nlm.nih.gov/41000002/',
  },
]

const calls = (fetchMock: ReturnType<typeof mockFetch>, url: string) =>
  fetchMock.mock.calls.filter(([input]) => String(input).includes(url)).length

describe('StudiesPanel', () => {
  it('lists studies with journal, year, authors and provenance', async () => {
    mockFetch({ [STUDIES_URL]: ok(studies) })
    renderWithProviders(<StudiesPanel documentId={5} termEn="Migraine" enabled />)
    const link = await screen.findByRole('link', { name: /Triptans in acute migraine/ })
    expect(link).toHaveAttribute('href', 'https://pubmed.ncbi.nlm.nih.gov/41000002/')
    expect(link).toHaveAttribute('target', '_blank')
    expect(screen.getByText('Cephalalgia')).toBeInTheDocument()
    expect(screen.getByText('2026')).toBeInTheDocument()
    expect(screen.getByText('Müller A, Smith B, Rossi C et al.')).toBeInTheDocument()
    expect(screen.getByText('PubMed · NCBI')).toBeInTheDocument()
    expect(screen.getByText(/abgerufen vor 5 Minuten/)).toBeInTheDocument()
    expect(screen.getByText(/„Migraine“/)).toBeInTheDocument()
  })

  it('says when there are no studies', async () => {
    mockFetch({ [STUDIES_URL]: bare('empty') })
    renderWithProviders(<StudiesPanel documentId={5} termEn="Migraine" enabled />)
    expect(await screen.findByText(/Keine Studien gefunden/)).toBeInTheDocument()
  })

  it('offers a retry when PubMed is unavailable', async () => {
    const fetchMock = mockFetch({ [STUDIES_URL]: bare('unavailable') })
    renderWithProviders(<StudiesPanel documentId={5} termEn="Migraine" enabled />)
    expect(await screen.findByText('PubMed ist gerade nicht erreichbar.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Erneut versuchen/ }))
    await waitFor(() => expect(calls(fetchMock, STUDIES_URL)).toBe(2))
  })

  it('does not fetch while disabled', () => {
    const fetchMock = mockFetch({ [STUDIES_URL]: ok(studies) })
    renderWithProviders(<StudiesPanel documentId={5} termEn="Migraine" enabled={false} />)
    expect(calls(fetchMock, STUDIES_URL)).toBe(0)
  })
})

describe('Icd11Panel', () => {
  const entry = {
    code: '8A80', title: 'Migräne', definition: 'Eine wiederkehrende Kopfschmerzerkrankung.',
    url: 'https://icd.who.int/browse/2026-01/mms/de#1260284546', release: '2026-01', language: 'de',
  }

  it('shows code, title, definition and a link to the WHO browser', async () => {
    mockFetch({ [ICD_URL]: ok(entry) })
    renderWithProviders(<Icd11Panel documentId={5} enabled />)
    expect(await screen.findByText('8A80')).toBeInTheDocument()
    expect(screen.getByText('Migräne')).toBeInTheDocument()
    expect(screen.getByText('Eine wiederkehrende Kopfschmerzerkrankung.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Im ICD-11-Browser öffnen/ })).toHaveAttribute('href', entry.url)
    expect(screen.getByText(/Deutsche Fassung: WHO-Prerelease/)).toBeInTheDocument()
    expect(screen.getByText('WHO ICD-11')).toBeInTheDocument()
  })

  it('omits the prerelease note for English answers', async () => {
    mockFetch({ [ICD_URL]: ok({ ...entry, language: 'en', title: 'Migraine' }) })
    renderWithProviders(<Icd11Panel documentId={5} enabled />)
    expect(await screen.findByText('Migraine')).toBeInTheDocument()
    expect(screen.queryByText(/WHO-Prerelease/)).not.toBeInTheDocument()
  })

  it('explains when the server has no WHO API access', async () => {
    mockFetch({ [ICD_URL]: bare('not_configured') })
    renderWithProviders(<Icd11Panel documentId={5} enabled />)
    expect(
      await screen.findByText('ICD-11 ist auf diesem Server nicht eingerichtet (WHO-API-Zugang fehlt).'),
    ).toBeInTheDocument()
  })
})

describe('MedicationsPanel', () => {
  const meds = {
    found: [
      {
        ingredient: 'metformin', brand_names: ['Glucophage'],
        indications: 'Adjunct to diet and exercise.', warnings: 'WARNING: LACTIC ACIDOSIS',
        adverse_reactions: 'Diarrhea, nausea.', url: 'https://open.fda.gov/apis/drug/label/',
      },
    ],
    missing: ['empagliflozin'],
  }

  it('marks the data as US FDA information and lists each ingredient', async () => {
    mockFetch({ [MEDS_URL]: ok(meds) })
    renderWithProviders(<MedicationsPanel documentId={5} enabled />)
    expect(await screen.findByText('metformin')).toBeInTheDocument()
    expect(screen.getByText(/US-FDA-Produktinformation, englisch/)).toBeInTheDocument()
    expect(screen.getByText('WARNING: LACTIC ACIDOSIS')).toBeInTheDocument()
    expect(screen.getByText(/Kein FDA-Label gefunden für: empagliflozin/)).toBeInTheDocument()
    expect(screen.getByText(/openFDA/)).toBeInTheDocument()
  })
})
