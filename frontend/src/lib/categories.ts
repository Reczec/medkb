import {
  Activity,
  Baby,
  Bone,
  Brain,
  Droplets,
  Ear,
  Eye,
  FlaskConical,
  HeartPulse,
  type LucideIcon,
  Microscope,
  Smile,
  Soup,
  Sparkles,
  Stethoscope,
  Venus,
  Wind,
} from 'lucide-react'

export interface CategoryStyle {
  /** Solid colour for dots, chart segments and text accents. */
  color: string
  /** Translucent background for badges. */
  soft: string
  icon: LucideIcon
}

/**
 * 16 hues spaced evenly (22.5°) around the wheel, all at the same lightness (Equal Weight).
 * Key order = the backend's tie order (app/classifier.py CATEGORIES).
 */
const styles: Record<string, { hue: number; chroma: number; icon: LucideIcon }> = {
  HNO: { hue: 248, chroma: 0.13, icon: Ear },
  Augenheilkunde: { hue: 225, chroma: 0.12, icon: Eye },
  Neurologie: { hue: 292, chroma: 0.15, icon: Brain },
  Kardiologie: { hue: 22, chroma: 0.17, icon: HeartPulse },
  Pneumologie: { hue: 158, chroma: 0.11, icon: Wind },
  Gastroenterologie: { hue: 112, chroma: 0.12, icon: Soup },
  Endokrinologie: { hue: 68, chroma: 0.13, icon: FlaskConical },
  Urologie: { hue: 315, chroma: 0.12, icon: Droplets },
  Gynäkologie: { hue: 0, chroma: 0.13, icon: Venus },
  Dermatologie: { hue: 45, chroma: 0.13, icon: Sparkles },
  Orthopädie: { hue: 90, chroma: 0.12, icon: Bone },
  Pädiatrie: { hue: 338, chroma: 0.14, icon: Baby },
  Psychiatrie: { hue: 270, chroma: 0.09, icon: Smile },
  Infektiologie: { hue: 180, chroma: 0.1, icon: Microscope },
  'Innere Medizin': { hue: 135, chroma: 0.12, icon: Activity },
  Allgemeinmedizin: { hue: 202, chroma: 0.1, icon: Stethoscope },
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
