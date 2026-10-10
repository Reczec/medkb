import {
  Baby,
  Bone,
  Brain,
  Ear,
  HeartPulse,
  type LucideIcon,
  Smile,
  Sparkles,
  Stethoscope,
  Activity,
} from 'lucide-react'

export interface CategoryStyle {
  /** Solid colour for dots, chart segments and text accents. */
  color: string
  /** Translucent background for badges. */
  soft: string
  icon: LucideIcon
}

const styles: Record<string, { hue: number; chroma: number; icon: LucideIcon }> = {
  Allgemeinmedizin: { hue: 196, chroma: 0.1, icon: Stethoscope },
  'Innere Medizin': { hue: 150, chroma: 0.12, icon: Activity },
  Kardiologie: { hue: 18, chroma: 0.17, icon: HeartPulse },
  Neurologie: { hue: 285, chroma: 0.15, icon: Brain },
  HNO: { hue: 235, chroma: 0.13, icon: Ear },
  Dermatologie: { hue: 55, chroma: 0.13, icon: Sparkles },
  Orthopädie: { hue: 85, chroma: 0.12, icon: Bone },
  Pädiatrie: { hue: 340, chroma: 0.14, icon: Baby },
  Psychiatrie: { hue: 265, chroma: 0.09, icon: Smile },
}

export const KNOWN_CATEGORIES = Object.keys(styles)

const fallback: CategoryStyle = {
  color: 'oklch(0.6 0.02 230)',
  soft: 'oklch(0.6 0.02 230 / 0.14)',
  icon: Stethoscope,
}

export function categoryStyle(name: string): CategoryStyle {
  const style = styles[name]
  if (!style) return fallback
  return {
    color: `oklch(0.62 ${style.chroma} ${style.hue})`,
    soft: `oklch(0.62 ${style.chroma} ${style.hue} / 0.14)`,
    icon: style.icon,
  }
}
