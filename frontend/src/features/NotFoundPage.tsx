import { FileQuestion } from 'lucide-react'
import { Link } from 'react-router'
import { EmptyState } from '@/components/feedback/EmptyState'
import { Button } from '@/components/ui/button'

export function NotFoundPage() {
  return (
    <EmptyState
      icon={FileQuestion}
      title="Seite nicht gefunden"
      text="Diese Adresse gibt es in MedKB nicht. Vielleicht hilft die Suche weiter."
      action={
        <Button asChild variant="outline">
          <Link to="/">Zum Dashboard</Link>
        </Button>
      }
    />
  )
}
