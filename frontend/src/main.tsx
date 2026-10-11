import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { MotionConfig } from 'motion/react'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Toaster } from 'sonner'
import { TooltipProvider } from '@/components/ui/tooltip'
import { AuthProvider } from '@/features/auth/AuthProvider'
import { I18nProvider } from '@/i18n/I18nProvider'
import { applyTheme, readTheme } from '@/lib/theme'
import App from './App.tsx'
import './index.css'

applyTheme(readTheme())

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
      retry: (count, error) => {
        const status = (error as { status?: number }).status ?? 0
        return status !== 0 && status < 500 ? false : count < 2
      },
    },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <I18nProvider>
        <MotionConfig reducedMotion="user">
          <TooltipProvider delayDuration={300}>
            <AuthProvider>
              <App />
            </AuthProvider>
            <Toaster position="bottom-right" richColors closeButton />
          </TooltipProvider>
        </MotionConfig>
      </I18nProvider>
    </QueryClientProvider>
  </StrictMode>,
)
