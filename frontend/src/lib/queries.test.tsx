import { fireEvent, screen, waitFor } from '@testing-library/react'
import {
  useCreateDocument,
  useDeleteDocument,
  useIcd11,
  useLatestStudies,
  useMedications,
  useRestoreArchive,
  useStudies,
  useUpdateDocument,
} from '@/lib/queries'
import { makeQueryClient, mockFetch, renderWithProviders } from '@/test/utils'

afterEach(() => vi.unstubAllGlobals())

function SourcesAndActions() {
  const studies = useStudies(5, true)
  const icd = useIcd11(5, true)
  const medications = useMedications(5, true)
  const latest = useLatestStudies()
  const create = useCreateDocument()
  const update = useUpdateDocument(5)
  const remove = useDeleteDocument()
  const restore = useRestoreArchive()
  return (
    <>
      {[studies, icd, medications, latest].map((query, i) => (
        <output key={i}>{query.data?.fetched_at}</output>
      ))}
      <button onClick={() => create.mutate({ title: 'Migräne', content: 'Kopfschmerzen mit Übelkeit.', doc_type: 'Diagnose' })}>Create</button>
      <button onClick={() => update.mutate({ term_en: 'Migraine', icd11_code: '8A80', medications: ['sumatriptan'] })}>Update</button>
      <button onClick={() => remove.mutate(5)}>Delete</button>
      <button onClick={() => restore.mutate('example.json')}>Restore</button>
    </>
  )
}

it.each(['Create', 'Update', 'Delete', 'Restore'])('refreshes previously cached sources after %s', async (action) => {
  const client = makeQueryClient()
  const oldTime = '2026-10-10T10:00:00Z'
  const newTime = '2026-10-11T10:00:00Z'
  for (const source of ['studies', 'icd11', 'medications']) {
    client.setQueryData(['source', source, 5], { status: 'empty', data: null, fetched_at: oldTime })
  }
  client.setQueryData(['source', 'latest-studies'], { status: 'empty', data: null, fetched_at: oldTime })
  const fetchMock = mockFetch({
    '/api/sources/': { status: 'empty', data: null, fetched_at: newTime },
    '/api/documents': {},
    '/api/archives': {},
  })
  renderWithProviders(<SourcesAndActions />, { client })
  expect(screen.getAllByText(oldTime)).toHaveLength(4)
  fireEvent.click(screen.getByRole('button', { name: action }))
  await waitFor(() => expect(screen.getAllByText(newTime)).toHaveLength(4))
  expect(fetchMock.mock.calls.filter(([input]) => String(input).includes('/api/sources/'))).toHaveLength(4)
})
