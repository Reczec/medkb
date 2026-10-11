import { FileQuestion } from 'lucide-react'
import { Link } from 'react-router'
import { EmptyState } from '@/components/feedback/EmptyState'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'

export function NotFoundPage() {
  const { t } = useI18n()
  return (
    <EmptyState
      icon={FileQuestion}
      title={t('notFound.title')}
      text={t('notFound.text')}
      action={
        <Button asChild variant="outline">
          <Link to="/">{t('notFound.action')}</Link>
        </Button>
      }
    />
  )
}
