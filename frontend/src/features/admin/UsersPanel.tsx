import { ErrorState } from '@/components/feedback/ErrorState'
import { Skeleton } from '@/components/ui/skeleton'
import { ROLE_LABELS } from '@/lib/auth'
import { formatDate } from '@/lib/format'
import { useUsers } from '@/lib/queries'

export function UsersPanel() {
  const users = useUsers()

  if (users.error) return <ErrorState error={users.error} onRetry={() => users.refetch()} />
  if (users.isPending) return <Skeleton className="h-40 rounded-xl" />

  return (
    <div className="flex flex-col gap-3">
      <p className="max-w-2xl text-sm text-muted-foreground">
        Demo-Zugänge haben zufällige Passwörter und sind nur über die Demo-Karten erreichbar. Ein
        eigener Admin-Zugang entsteht über <code className="text-xs">ADMIN_PASSWORD</code>.
      </p>
      <div className="overflow-x-auto rounded-xl border bg-card shadow-sheet">
        <table aria-label="Nutzer" className="w-full min-w-[480px] text-sm">
          <thead>
            <tr className="border-b text-left text-xs text-muted-foreground">
              <th className="px-5 py-3 font-medium">Benutzer</th>
              <th className="px-3 py-3 font-medium">Name</th>
              <th className="px-3 py-3 font-medium">Rolle</th>
              <th className="px-5 py-3 font-medium">Angelegt</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {users.data.map((user) => (
              <tr key={user.id}>
                <td className="px-5 py-3 font-mono text-xs">{user.username}</td>
                <td className="px-3 py-3">{user.display_name}</td>
                <td className="px-3 py-3">{ROLE_LABELS[user.role]}</td>
                <td className="tabular px-5 py-3 text-muted-foreground">
                  {formatDate(user.created_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
