import {
  Archive,
  FilePlus2,
  FilePen,
  History,
  RotateCcw,
  Trash2,
  type LucideIcon,
} from 'lucide-react'

interface AuditAction {
  label: string
  icon: LucideIcon
  className: string
}

const MUTED = 'bg-muted text-foreground/85'

/** Labels and icons for change-log actions (keys are the backend's action names). */
export const AUDIT_ACTIONS: Record<string, AuditAction> = {
  create: { label: 'Angelegt', icon: FilePlus2, className: MUTED },
  update: { label: 'Bearbeitet', icon: FilePen, className: MUTED },
  delete: { label: 'Gelöscht', icon: Trash2, className: 'bg-destructive/10 text-destructive' },
  archive_create: { label: 'Archiviert', icon: Archive, className: MUTED },
  archive_restore: { label: 'Wiederhergestellt', icon: History, className: MUTED },
  demo_reset: { label: 'Demo zurückgesetzt', icon: RotateCcw, className: MUTED },
}

export const auditAction = (action: string): AuditAction =>
  AUDIT_ACTIONS[action] ?? { label: action, icon: FilePen, className: MUTED }
