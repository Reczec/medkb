import type { ReactNode } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router'
import { AppShell } from '@/components/layout/AppShell'
import { LoginPage } from '@/features/auth/LoginPage'
import { RequireAuth, RequireRole } from '@/features/auth/guards'
import { NotFoundPage } from '@/features/NotFoundPage'
import { RouteError } from '@/features/RouteError'
import { lazyPage } from '@/lib/lazyPage'

// Pages load on demand, so the first visit only downloads the shell and its page.
const HomePage = lazyPage(() => import('@/features/home/HomePage'), 'HomePage')
const KnowledgeBasePage = lazyPage(
  () => import('@/features/documents/KnowledgeBasePage'),
  'KnowledgeBasePage',
)
const DocumentPage = lazyPage(() => import('@/features/documents/DocumentPage'), 'DocumentPage')
const EditorPage = lazyPage(() => import('@/features/editor/EditorPage'), 'EditorPage')
const AssistantPage = lazyPage(() => import('@/features/ai/AssistantPage'), 'AssistantPage')
const AdminPage = lazyPage(() => import('@/features/admin/AdminPage'), 'AdminPage')

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
      { path: 'assistent', element: <AssistantPage /> },
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
