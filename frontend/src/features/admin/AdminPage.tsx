import { Archive, ListChecks, LogOut } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { AdminTokenGate } from '@/features/admin/AdminTokenGate'
import { ArchivesPanel } from '@/features/admin/ArchivesPanel'
import { AuditTable } from '@/features/admin/AuditTable'

export function AdminPage() {
  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-1">
        <h1 className="text-3xl font-semibold tracking-tight">Administration</h1>
        <p className="text-muted-foreground">Archive verwalten und Änderungen nachvollziehen.</p>
      </header>

      <AdminTokenGate>
        {(logout) => (
          <Tabs defaultValue="archives" className="gap-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <TabsList className="h-10!">
                <TabsTrigger value="archives" className="px-3">
                  <Archive aria-hidden /> Archive
                </TabsTrigger>
                <TabsTrigger value="audit" className="px-3">
                  <ListChecks aria-hidden /> Änderungsprotokoll
                </TabsTrigger>
              </TabsList>
              <Button variant="ghost" onClick={logout}>
                <LogOut aria-hidden /> Abmelden
              </Button>
            </div>
            <TabsContent value="archives">
              <ArchivesPanel />
            </TabsContent>
            <TabsContent value="audit">
              <AuditTable />
            </TabsContent>
          </Tabs>
        )}
      </AdminTokenGate>
    </div>
  )
}
