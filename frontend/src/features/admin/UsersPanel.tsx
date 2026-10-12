import { ErrorState } from '@/components/feedback/ErrorState'
import { Skeleton } from '@/components/ui/skeleton'
import { useI18n } from '@/i18n/context'
import { formatDate } from '@/lib/format'
import { useUsers } from '@/lib/queries'

export function UsersPanel() {
  const users = useUsers()
  const { t, lang } = useI18n()

  if (users.error) return <ErrorState error={users.error} onRetry={() => users.refetch()} />
  if (users.isPending) return <Skeleton className="h-40 rounded-xl" />

  return (
    <div className="flex flex-col gap-3">
      <p className="max-w-2xl text-sm text-muted-foreground">
        {t('users.noteBefore')} <code className="text-xs">ADMIN_PASSWORD</code>.
      </p>
      <div className="overflow-x-auto rounded-xl border bg-card shadow-sheet">
        <table aria-label={t('users.table')} className="w-full min-w-[480px] text-sm">
          <thead>
            <tr className="border-b text-left text-xs text-muted-foreground">
              <th className="px-5 py-3 font-medium">{t('users.username')}</th>
              <th className="px-3 py-3 font-medium">{t('users.name')}</th>
              <th className="px-3 py-3 font-medium">{t('users.role')}</th>
              <th className="px-5 py-3 font-medium">{t('users.created')}</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {users.data.map((user) => (
              <tr key={user.id}>
                <td className="px-5 py-3 font-mono text-xs">{user.username}</td>
                <td className="px-3 py-3">{user.display_name}</td>
                <td className="px-3 py-3">{t(`role.${user.role}`)}</td>
                <td className="tabular px-5 py-3 text-muted-foreground">
                  {formatDate(user.created_at, lang)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
