import {
  Archive,
  FilePlus2,
  FilePen,
  History,
  RotateCcw,
  Trash2,
  type LucideIcon,
} from 'lucide-react'
import type { TranslationKey } from '@/i18n/translate'

interface AuditAction {
  /** Message key of the label; null for actions this client does not know. */
  key: TranslationKey | null
  /** The backend's raw action name, shown when there is no translation. */
  raw: string
  icon: LucideIcon
  className: string
}

const MUTED = 'bg-muted text-foreground/85'

type KnownAction = Omit<AuditAction, 'raw'>

/** Message keys, icons and colours of change-log actions (keys are the backend's action names). */
export const AUDIT_ACTIONS: Record<string, KnownAction> = {
  create: { key: 'audit.create', icon: FilePlus2, className: MUTED },
  update: { key: 'audit.update', icon: FilePen, className: MUTED },
  delete: { key: 'audit.delete', icon: Trash2, className: 'bg-destructive/10 text-destructive' },
  archive_create: { key: 'audit.archive_create', icon: Archive, className: MUTED },
  archive_restore: { key: 'audit.archive_restore', icon: History, className: MUTED },
  demo_reset: { key: 'audit.demo_reset', icon: RotateCcw, className: MUTED },
}

export const auditAction = (action: string): AuditAction => ({
  ...(AUDIT_ACTIONS[action] ?? { key: null, icon: FilePen, className: MUTED }),
  raw: action,
})
