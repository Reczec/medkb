import { createBrowserRouter, RouterProvider } from 'react-router'
import { AppShell } from '@/components/layout/AppShell'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { KnowledgeBasePage } from '@/features/documents/KnowledgeBasePage'
import { NotFoundPage } from '@/features/NotFoundPage'
import { RouteError } from '@/features/RouteError'

const router = createBrowserRouter([
  {
    element: <AppShell />,
    errorElement: <RouteError />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'wissen', element: <KnowledgeBasePage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
