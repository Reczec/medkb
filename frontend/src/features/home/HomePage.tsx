import { useAuth } from '@/features/auth/context'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { PatientHome } from '@/features/home/PatientHome'

/** "/" : patients get a search-first start page, staff the dashboard. */
export function HomePage() {
  const { user } = useAuth()
  return user?.role === 'patient' ? <PatientHome /> : <DashboardPage />
}
