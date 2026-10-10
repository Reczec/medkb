/** Labels and badge colours for change-log actions (keys are the backend's action names). */
export const AUDIT_ACTIONS: Record<string, { label: string; className: string }> = {
  create: { label: 'Angelegt', className: 'bg-emerald-500/12 text-emerald-700 dark:text-emerald-300' },
  update: { label: 'Bearbeitet', className: 'bg-sky-500/12 text-sky-700 dark:text-sky-300' },
  delete: { label: 'Gelöscht', className: 'bg-red-500/12 text-red-700 dark:text-red-300' },
  archive_create: { label: 'Archiviert', className: 'bg-violet-500/12 text-violet-700 dark:text-violet-300' },
  archive_restore: {
    label: 'Wiederhergestellt',
    className: 'bg-violet-500/12 text-violet-700 dark:text-violet-300',
  },
  demo_reset: {
    label: 'Demo zurückgesetzt',
    className: 'bg-amber-500/14 text-amber-800 dark:text-amber-300',
  },
}

export const auditAction = (action: string) =>
  AUDIT_ACTIONS[action] ?? { label: action, className: 'bg-muted text-foreground' }
