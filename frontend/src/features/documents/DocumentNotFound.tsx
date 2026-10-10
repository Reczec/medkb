import { FileQuestion } from 'lucide-react'
import { Link } from 'react-router'
import { EmptyState } from '@/components/feedback/EmptyState'
import { Button } from '@/components/ui/button'

export function DocumentNotFound() {
  return (
    <EmptyState
      icon={FileQuestion}
      title="Eintrag nicht gefunden"
      text="Der Eintrag wurde gelöscht oder hat nie existiert."
      action={
        <Button asChild variant="outline">
          <Link to="/wissen">Zur Wissensdatenbank</Link>
        </Button>
      }
    />
  )
}
