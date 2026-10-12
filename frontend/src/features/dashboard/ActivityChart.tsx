import { useReducedMotion } from 'motion/react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useI18n } from '@/i18n/context'
import { formatDay } from '@/lib/format'
import type { DayCount } from '@/lib/types'

interface TooltipPayload {
  active?: boolean
  payload?: { payload: DayCount }[]
}

function ChartTooltip({ active, payload }: TooltipPayload) {
  const { t, lang } = useI18n()
  if (!active || !payload?.length) return null
  const day = payload[0].payload
  return (
    <div className="rounded-lg border bg-popover px-3 py-2 text-sm shadow-lift">
      <div className="text-xs text-muted-foreground">{formatDay(day.date, lang)}</div>
      <div className="tabular font-semibold">
        {t('activity.change', { count: day.count })}
      </div>
    </div>
  )
}

/** One bar per day: days without changes stay at zero instead of being smoothed over. */
export function ActivityChart({ activity }: { activity: DayCount[] }) {
  const reduced = useReducedMotion()
  const { t, lang } = useI18n()
  const total = activity.reduce((sum, day) => sum + day.count, 0)
  const today = activity.at(-1)?.count ?? 0

  return (
    <section className="flex flex-col rounded-xl border bg-card p-5 shadow-sheet">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-base font-semibold">{t('activity.title')}</h2>
        <p className="text-sm text-muted-foreground">
          <span className="tabular font-medium text-foreground">{total}</span> {t('activity.total')} ·{' '}
          <span className="tabular font-medium text-foreground">{today}</span> {t('activity.today')}
        </p>
      </div>
      <div className="mt-4 h-52 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={activity} margin={{ top: 8, right: 4, bottom: 0, left: -24 }}>
            <CartesianGrid vertical={false} stroke="var(--border)" />
            <XAxis
              dataKey="date"
              tickFormatter={(value: string) => formatDay(value, lang)}
              tickLine={false}
              axisLine={false}
              minTickGap={32}
              tick={{ fill: 'var(--muted-foreground)', fontSize: 12 }}
            />
            <YAxis
              allowDecimals={false}
              tickLine={false}
              axisLine={false}
              width={44}
              tick={{ fill: 'var(--muted-foreground)', fontSize: 12 }}
            />
            <Tooltip content={<ChartTooltip />} cursor={{ fill: 'var(--muted)', opacity: 0.6 }} />
            <Bar
              dataKey="count"
              fill="var(--primary)"
              radius={[3, 3, 0, 0]}
              maxBarSize={18}
              minPointSize={0}
              isAnimationActive={!reduced}
              animationDuration={700}
              animationEasing="ease-out"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
