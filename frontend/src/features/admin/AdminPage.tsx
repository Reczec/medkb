import { Archive, ListChecks, Users } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ArchivesPanel } from '@/features/admin/ArchivesPanel'
import { AuditTable } from '@/features/admin/AuditTable'
import { UsersPanel } from '@/features/admin/UsersPanel'
import { useI18n } from '@/i18n/context'

export function AdminPage() {
  const { t } = useI18n()
  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-1">
        <h1 className="text-3xl font-semibold tracking-tight">{t('admin.title')}</h1>
        <p className="text-muted-foreground">{t('admin.subtitle')}</p>
      </header>

      <Tabs defaultValue="archives" className="gap-5">
        <TabsList className="h-10! max-w-full justify-start overflow-x-auto">
          <TabsTrigger value="archives" className="px-3">
            <Archive aria-hidden /> {t('admin.tab.archives')}
          </TabsTrigger>
          <TabsTrigger value="audit" className="px-3">
            <ListChecks aria-hidden /> {t('admin.tab.audit')}
          </TabsTrigger>
          <TabsTrigger value="users" className="px-3">
            <Users aria-hidden /> {t('admin.tab.users')}
          </TabsTrigger>
        </TabsList>
        <TabsContent value="archives">
          <ArchivesPanel />
        </TabsContent>
        <TabsContent value="audit">
          <AuditTable />
        </TabsContent>
        <TabsContent value="users">
          <UsersPanel />
        </TabsContent>
      </Tabs>
    </div>
  )
}
