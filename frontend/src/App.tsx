import { createBrowserRouter, RouterProvider } from 'react-router'
import { AppShell } from '@/components/layout/AppShell'
import { AdminPage } from '@/features/admin/AdminPage'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { DocumentPage } from '@/features/documents/DocumentPage'
import { KnowledgeBasePage } from '@/features/documents/KnowledgeBasePage'
import { EditorPage } from '@/features/editor/EditorPage'
import { NotFoundPage } from '@/features/NotFoundPage'
import { RouteError } from '@/features/RouteError'

const router = createBrowserRouter([
  {
    element: <AppShell />,
    errorElement: <RouteError />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'wissen', element: <KnowledgeBasePage /> },
      { path: 'wissen/neu', element: <EditorPage /> },
      { path: 'wissen/:id', element: <DocumentPage /> },
      { path: 'wissen/:id/bearbeiten', element: <EditorPage /> },
      { path: 'admin', element: <AdminPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
