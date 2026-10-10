import { useReducedMotion } from 'motion/react'
import { useId } from 'react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { formatDay } from '@/lib/format'
import type { DayCount } from '@/lib/types'

interface TooltipPayload {
  active?: boolean
  payload?: { payload: DayCount }[]
}

function ChartTooltip({ active, payload }: TooltipPayload) {
  if (!active || !payload?.length) return null
  const day = payload[0].payload
  return (
    <div className="rounded-lg border bg-popover px-3 py-2 text-sm shadow-lift">
      <div className="text-xs text-muted-foreground">{formatDay(day.date)}</div>
      <div className="tabular font-semibold">
        {day.count} {day.count === 1 ? 'Änderung' : 'Änderungen'}
      </div>
    </div>
  )
}

export function ActivityChart({ activity }: { activity: DayCount[] }) {
  const reduced = useReducedMotion()
  const gradientId = useId()
  const total = activity.reduce((sum, day) => sum + day.count, 0)
  const today = activity.at(-1)?.count ?? 0

  return (
    <section className="flex flex-col rounded-xl border bg-card p-5 shadow-sheet">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-base font-semibold">Änderungen der letzten 30 Tage</h2>
        <p className="text-sm text-muted-foreground">
          <span className="tabular font-medium text-foreground">{total}</span> gesamt ·{' '}
          <span className="tabular font-medium text-foreground">{today}</span> heute
        </p>
      </div>
      <div className="mt-4 h-52 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={activity} margin={{ top: 8, right: 4, bottom: 0, left: -24 }}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--primary)" stopOpacity={0.32} />
                <stop offset="100%" stopColor="var(--primary)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} stroke="var(--border)" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDay}
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
            <Tooltip
              content={<ChartTooltip />}
              cursor={{ stroke: 'var(--primary)', strokeOpacity: 0.35, strokeDasharray: '3 3' }}
            />
            <Area
              type="monotone"
              dataKey="count"
              stroke="var(--primary)"
              strokeWidth={2}
              fill={`url(#${gradientId})`}
              isAnimationActive={!reduced}
              animationDuration={900}
              animationEasing="ease-out"
              activeDot={{ r: 4, strokeWidth: 2, stroke: 'var(--card)' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
