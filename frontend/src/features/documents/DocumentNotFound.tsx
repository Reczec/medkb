import { FileQuestion } from 'lucide-react'
import { Link } from 'react-router'
import { EmptyState } from '@/components/feedback/EmptyState'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'

export function DocumentNotFound() {
  const { t } = useI18n()
  return (
    <EmptyState
      icon={FileQuestion}
      title={t('docNotFound.title')}
      text={t('docNotFound.text')}
      action={
        <Button asChild variant="outline">
          <Link to="/wissen">{t('docNotFound.action')}</Link>
        </Button>
      }
    />
  )
}
