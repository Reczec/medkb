import { Archive, ListChecks, Users } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ArchivesPanel } from '@/features/admin/ArchivesPanel'
import { AuditTable } from '@/features/admin/AuditTable'
import { UsersPanel } from '@/features/admin/UsersPanel'

export function AdminPage() {
  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-1">
        <h1 className="text-3xl font-semibold tracking-tight">Administration</h1>
        <p className="text-muted-foreground">Archive verwalten, Änderungen nachvollziehen, Zugänge einsehen.</p>
      </header>

      <Tabs defaultValue="archives" className="gap-5">
        <TabsList className="h-10!">
          <TabsTrigger value="archives" className="px-3">
            <Archive aria-hidden /> Archive
          </TabsTrigger>
          <TabsTrigger value="audit" className="px-3">
            <ListChecks aria-hidden /> Änderungsprotokoll
          </TabsTrigger>
          <TabsTrigger value="users" className="px-3">
            <Users aria-hidden /> Nutzer
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
