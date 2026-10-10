import type { ReactNode } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router'
import { AppShell } from '@/components/layout/AppShell'
import { AdminPage } from '@/features/admin/AdminPage'
import { LoginPage } from '@/features/auth/LoginPage'
import { RequireAuth, RequireRole } from '@/features/auth/guards'
import { HomePage } from '@/features/home/HomePage'
import { DocumentPage } from '@/features/documents/DocumentPage'
import { KnowledgeBasePage } from '@/features/documents/KnowledgeBasePage'
import { EditorPage } from '@/features/editor/EditorPage'
import { NotFoundPage } from '@/features/NotFoundPage'
import { RouteError } from '@/features/RouteError'

const adminOnly = (element: ReactNode) => <RequireRole roles={['admin']}>{element}</RequireRole>

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage />, errorElement: <RouteError /> },
  {
    element: (
      <RequireAuth>
        <AppShell />
      </RequireAuth>
    ),
    errorElement: <RouteError />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'wissen', element: <KnowledgeBasePage /> },
      { path: 'wissen/neu', element: adminOnly(<EditorPage />) },
      { path: 'wissen/:id', element: <DocumentPage /> },
      { path: 'wissen/:id/bearbeiten', element: adminOnly(<EditorPage />) },
      { path: 'admin', element: adminOnly(<AdminPage />) },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
