import { screen } from '@testing-library/react'
import { DocumentCard } from '@/features/documents/DocumentCard'
import { renderWithProviders } from '@/test/utils'

it('names the card link after the entry title', () => {
  renderWithProviders(
    <DocumentCard
      document={{
        id: 3,
        title: 'Migräne',
        content: 'Anfallsartige Kopfschmerzen.',
        category: 'Neurologie',
        doc_type: 'Symptom',
        keywords: [],
        source: null,
        auto_classified: true,
        created_at: '2026-10-01T10:00:00Z',
        updated_at: '2026-10-01T10:00:00Z',
      }}
    />,
  )
  expect(screen.getByRole('link', { name: 'Migräne' })).toHaveAttribute('href', '/wissen/3')
})
