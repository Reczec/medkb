---
name: MedKB
description: A medical knowledge base organised like a colour-coded record filing system.
colors:
  primary: "oklch(0.53 0.1 196)"
  primary-foreground: "oklch(0.99 0.005 196)"
  teal-wash: "oklch(0.945 0.025 190)"
  teal-wash-foreground: "oklch(0.3 0.06 200)"
  cool-paper: "oklch(0.984 0.004 197)"
  sheet-white: "oklch(1 0 0)"
  slate-ink: "oklch(0.24 0.025 230)"
  muted-wash: "oklch(0.958 0.007 210)"
  muted-ink: "oklch(0.5 0.022 230)"
  hairline: "oklch(0.91 0.01 215)"
  destructive: "oklch(0.58 0.2 25)"
  petrol-rail: "oklch(0.285 0.047 214)"
  rail-foreground: "oklch(0.97 0.01 200)"
  rail-muted: "oklch(0.76 0.03 205)"
  rail-active: "oklch(0.36 0.055 205)"
  rail-well: "oklch(0.23 0.04 216)"
  rail-accent: "oklch(0.8 0.11 188)"
  specialty-allgemeinmedizin: "oklch(0.62 0.1 202)"
  specialty-innere-medizin: "oklch(0.62 0.12 135)"
  specialty-kardiologie: "oklch(0.62 0.17 22)"
  specialty-neurologie: "oklch(0.62 0.15 292)"
  specialty-hno: "oklch(0.62 0.13 248)"
  specialty-dermatologie: "oklch(0.62 0.13 45)"
  specialty-orthopaedie: "oklch(0.62 0.12 90)"
  specialty-paediatrie: "oklch(0.62 0.14 338)"
  specialty-psychiatrie: "oklch(0.62 0.09 270)"
  specialty-augenheilkunde: "oklch(0.62 0.12 225)"
  specialty-pneumologie: "oklch(0.62 0.11 158)"
  specialty-gastroenterologie: "oklch(0.62 0.12 112)"
  specialty-endokrinologie: "oklch(0.62 0.13 68)"
  specialty-urologie: "oklch(0.62 0.12 315)"
  specialty-gynaekologie: "oklch(0.62 0.13 0)"
  specialty-infektiologie: "oklch(0.62 0.1 180)"
  specialty-fallback: "oklch(0.6 0.02 230)"
typography:
  display:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.025em"
    fontFeature: "\"cv11\", \"ss01\""
  headline:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.625
    fontFeature: "\"cv11\", \"ss01\""
  title:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1.5
    fontFeature: "\"cv11\", \"ss01\""
  body-reading:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.625
    fontFeature: "\"cv11\", \"ss01\""
  body:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.43
    fontFeature: "\"cv11\", \"ss01\""
  label:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
    lineHeight: 1.33
    fontFeature: "\"cv11\", \"ss01\""
  numeral:
    fontFamily: "Inter Variable, ui-sans-serif, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    fontFeature: "\"tnum\""
rounded:
  sm: "8px"
  md: "10px"
  lg: "12px"
  xl: "16px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "20px"
  xl: "24px"
  2xl: "32px"
  gutter-sm: "16px"
  gutter-md: "24px"
  gutter-lg: "40px"
  container: "1320px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.lg}"
    padding: "0 10px"
    height: "32px"
  button-primary-hover:
    backgroundColor: "oklch(0.53 0.1 196 / 0.8)"
  button-outline:
    backgroundColor: "{colors.cool-paper}"
    textColor: "{colors.slate-ink}"
    rounded: "{rounded.lg}"
    padding: "0 10px"
    height: "32px"
  button-outline-hover:
    backgroundColor: "{colors.muted-wash}"
  record-sheet:
    backgroundColor: "{colors.sheet-white}"
    textColor: "{colors.slate-ink}"
    rounded: "{rounded.xl}"
    padding: "20px"
  file-tab:
    textColor: "{colors.slate-ink}"
    typography: "{typography.label}"
    rounded: "12px 12px 0 0"
    padding: "0 10px"
    height: "28px"
  file-tab-md:
    textColor: "{colors.slate-ink}"
    rounded: "12px 12px 0 0"
    padding: "0 14px"
    height: "36px"
  specialty-strip-tab:
    backgroundColor: "{colors.sheet-white}"
    textColor: "{colors.slate-ink}"
    rounded: "12px 12px 0 0"
    padding: "2px 12px 0"
    height: "40px"
  specialty-strip-tab-selected:
    height: "48px"
  search-trigger:
    backgroundColor: "{colors.sheet-white}"
    textColor: "{colors.muted-ink}"
    rounded: "{rounded.lg}"
    padding: "0 12px"
    height: "40px"
  input:
    backgroundColor: "{colors.sheet-white}"
    textColor: "{colors.slate-ink}"
    rounded: "{rounded.lg}"
    height: "44px"
  keyword-chip:
    backgroundColor: "{colors.muted-wash}"
    textColor: "{colors.slate-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "2px 8px"
  nav-item:
    textColor: "{colors.rail-muted}"
    rounded: "{rounded.lg}"
    padding: "0 12px"
    height: "40px"
  nav-item-active:
    backgroundColor: "{colors.rail-active}"
    textColor: "{colors.rail-foreground}"
  data-bar:
    backgroundColor: "{colors.muted-wash}"
    rounded: "{rounded.full}"
    height: "8px"
---

# Design System: MedKB

## Overview

**Creative North Star: "The Colour-Coded Record Room"**

MedKB looks like a well-kept clinical filing room. A deep petrol rail runs down the left edge like the cabinet it belongs to. Beside it is a cool off-white work surface, and on that surface lie white record sheets. Each sheet carries a small coloured tab naming its specialty, so the specialty is the first thing you read on any entry, list or chart. Filtering works like pulling a drawer tab: the tab grows, its colour stripe thickens, and the other tabs fade.

The system is calm and dense, and it reads like a reference tool rather than a showcase. Colour has a narrow job. The sixteen specialty hues identify where something is filed. Teal means action or a neutral measurement. Everything else stays in quiet blue-greys. Depth comes from paper: sheets rest on a soft, low shadow and lift a little when you can act on them. Motion uses one fast-settling curve and is always reduced to plain fades when the user asks for reduced motion.

The dark theme keeps the same world in blue-slate. The rail turns darker than the work area, the sheets become slate panels, and the specialty colours do not change.

**Key Characteristics:**
- A petrol navigation rail beside a cool off-white work area
- White record sheets with a soft resting shadow and a hover lift
- Sixteen specialty colours at equal lightness, used as tab stripes, washes, icons, dots and bar fills
- Inter Variable with cv11/ss01 alternates and tabular numerals for every count
- Teal primary for actions, focus and specialty-neutral data
- One easing curve (expo-out) for motion, with reduced motion respected everywhere

## Colors

A cool, low-chroma blue-grey field. Colour appears only where it carries filing information (specialties) or marks something you can act on (teal).

### Primary
- **Clinical Teal** (primary): The colour of action. Used for the "Neuer Eintrag" button, links such as "Alle Einträge", the focus ring (one step lighter), the text caret, text selection at 22% alpha, and data bars that do not belong to a specialty (document-type bars, the 30-day activity chart).
- **Teal Wash** (teal-wash / teal-wash-foreground): A pale teal for selected chips, hover on strip tabs, and icon wells in admin panels.

### Secondary
- **Specialty Hues** (specialty-*): Sixteen colours that all sit at oklch lightness 0.62, with chroma between 0.09 and 0.17. These are Allgemeinmedizin, Innere Medizin, Kardiologie, Neurologie, HNO, Dermatologie, Orthopädie, Pädiatrie, Psychiatrie, Augenheilkunde, Pneumologie, Gastroenterologie, Endokrinologie, Urologie, Gynäkologie and Infektiologie. Unknown specialties use a grey fallback (specialty-fallback). The hues stay the same in light and dark themes.

### Neutral
- **Cool Paper** (cool-paper): The work-area background, a near-white with a faint cyan cast.
- **Sheet White** (sheet-white): Record sheets, panels, the search trigger and inputs.
- **Slate Ink** (slate-ink): Body text and headings. Blue-slate, not black.
- **Muted Wash / Muted Ink** (muted-wash, muted-ink): Keyword chips, bar tracks and info wells / secondary text, axis ticks and counts.
- **Hairline** (hairline): All 1px borders and the drawer edge under the specialty strip.
- **Petrol Rail family** (petrol-rail, rail-foreground, rail-muted, rail-active, rail-well, rail-accent): Used only in the sidebar. rail-active is the moving pill behind the current nav item. rail-accent is the 2px marker on that pill's left edge. rail-well sits behind the theme toggle.
- **Destructive** (destructive): Used as a 10% tint behind red text for delete actions and errors, never as a solid button.

### Named Rules
**The Filing Colour Rule.** A specialty colour is only ever a 3px top stripe, a 14–16% wash mixed into the surface, a 35% border mix, an icon, a dot or a bar fill. It is never the colour of text. Tab labels stay in Slate Ink.

**The Equal Weight Rule.** All specialty hues share lightness 0.62, so no specialty looks more important than another. A new specialty gets a new hue at L 0.62 and C 0.09–0.17.

**The Petrol Rail Rule.** The saturated dark petrol belongs only to the navigation rail. The work area never uses it as a background.

## Typography

**Display Font:** Inter Variable (with ui-sans-serif, system-ui)
**Body Font:** Inter Variable
**Label/Mono Font:** the system monospace stack, used only for machine strings (detected classifier terms, archive filenames)

**Character:** A single neutral grotesque used throughout, made a little more precise with the cv11 and ss01 alternates. Hierarchy comes from weight and size, not from switching typefaces.

### Hierarchy
- **Display** (600, 30px, tight tracking -0.025em; 36px on large screens for document titles): One page title per route ("Überblick", "Wissensdatenbank", the entry title). Balanced wrapping.
- **Headline** (400, 18px, line-height 1.625, Muted Ink): The one-sentence page summary under the title. Counted numbers inside it are semibold Slate Ink. Max width about 48rem.
- **Title** (600, 16px): Section and panel headings ("Zuletzt bearbeitet", "Klassifikation"). Record-sheet titles in lists go up to 18px with snug leading and are clamped to two lines.
- **Body** (400, 14px): UI text, card excerpts (relaxed leading, clamped to three lines), table cells.
- **Body Reading** (400, 17px, line-height 1.625, max 68ch): The text of an entry on its detail sheet.
- **Label** (500, 12px, Muted Ink): Sub-headings inside panels ("Erkannte Begriffe", "Schlagwörter"), metadata lines, chips, axis ticks. Sentence case, no tracking, never uppercase.
- **Numeral** (600, 13px, tabular): Counts on strip tabs, scores and statistics.

### Named Rules
**The Tabular Count Rule.** Every number that can be compared (counts, scores, dates in tables) uses tabular figures.

**The One Title Rule.** Each page has a single 30px title. Below it everything steps down to 16px titles, so there is no intermediate display tier.

## Layout

The shell is a flex row. The rail is sticky and full viewport height: 248px wide, or 72px when collapsed, with its width animated over 300ms. Below 768px it becomes a 272px left drawer opened from a menu button. The work column has a sticky 64px top bar (translucent Cool Paper with backdrop blur) holding the search trigger and the primary action. Below that is a centred container, max 1320px, with gutters of 16px, 24px from 640px, and 40px from 1024px.

Pages stack sections with 32px gaps, and grids use 24px gaps. From 1024px the content grids use three columns: a two-column main sheet plus a one-column aside (dashboard chart + doc-type panel, entry + classification, editor + live classification). Record-sheet grids are one column, then two from 1024px (knowledge base), or one / two from 640px / three from 1280px (recent list), with 20px row gaps to leave room for the tabs. Panels use 20px internal padding (24px for the reading sheet and editor on larger screens). The specialty strip scrolls horizontally on narrow screens instead of wrapping.

## Elevation & Depth

The system is a hybrid of tonal surfaces and paper shadows. Sheets, panels, the search trigger and filter inputs rest on a two-layer soft shadow tinted with slate. A sheet you can act on lifts to a deeper, more diffuse shadow on hover or focus. In the dark theme both shadows switch to black at higher opacity. Nothing else casts a shadow, apart from the selected strip tab, which casts a short upward shadow so it reads as standing in front of the drawer edge.

### Shadow Vocabulary
- **Sheet** (`box-shadow: 0 1px 2px oklch(0.3 0.03 220 / 0.06), 0 4px 14px -4px oklch(0.3 0.03 220 / 0.1)`): The resting state of every white sheet and panel.
- **Lift** (`box-shadow: 0 2px 4px oklch(0.3 0.03 220 / 0.06), 0 14px 32px -10px oklch(0.3 0.04 220 / 0.2)`): Hover and focus on clickable sheets and the search trigger, plus floating tooltips.

### Named Rules
**The Paper Lift Rule.** Sheets rest on the Sheet shadow. Only something you can act on lifts to the Lift shadow, and only in response to hover or focus.

## Shapes

Corners are gently rounded, using a 12px base radius. Sheets and panels use 16px. Buttons, inputs, nav pills and strip tabs use 12px. Chips use 10px. Bars and the share strip are fully rounded. Filing tabs round only their top corners, have no bottom border, and overlap the sheet or drawer edge by 1–2px so they look joined to it. Borders are always 1px hairlines. The drawer edge under the specialty strip is the only 2px line.

## Components

### Buttons
Small and businesslike, with a teal fill for the one primary action per view.
- **Shape:** 12px radius, 32px tall (36px large), 14px medium label with a 16px leading icon.
- **Primary:** Clinical Teal fill with near-white text. Hover drops to 80% opacity. Active nudges down 1px.
- **Outline:** Cool Paper with a hairline border, Muted Wash on hover. Used for secondary actions such as "Bearbeiten".
- **Destructive:** Red text on a 10% red tint. It never uses a solid red fill.
- **Focus:** A 3px ring in the Ring colour at 50% plus a ring-coloured border. Global fallback: 2px solid outline, 2px offset.

### Chips
- **Keyword chip:** Muted Wash, 12px Slate Ink at 80%, 10px radius, truncated at 12rem. Lists show five and then a "+N" count.
- **Detected-term chip:** Dashed hairline border with a 12px mono label, for raw classifier tokens.
- **Category picker chip:** 36px tall with a 12px radius and an 8px specialty dot. When selected, the border takes the specialty colour and the fill takes its 14% wash.
- **Active filter pill:** Fully rounded, hairline border. Hover turns it destructive red to show that clicking removes it.

### Cards / Containers (Record Sheets)
- **Corner Style:** 16px.
- **Background:** Sheet White in light, slate panel in dark.
- **Shadow Strategy:** Sheet at rest, Lift on hover/focus (see Elevation).
- **Border:** 1px hairline.
- **Internal Padding:** 20px. 24px horizontal and 28px bottom on the reading sheet.

### Inputs / Fields
- **Style:** Sheet White, hairline border, 12px radius. Search and filter fields are 44px tall with 16px text and the Sheet shadow.
- **Focus:** The border becomes the ring colour, with a 3px ring at 50%. The caret is teal.
- **Error / Disabled:** Destructive border with a 20% destructive ring / 50% opacity.

### Navigation
- **Rail:** On petrol. Nav items are 40px tall, 14px medium, Rail Muted text, with an 18px icon. The current item has a Rail Active pill that slides between items on a spring (stiffness 480, damping 40) and carries a 2px Rail Accent marker on its left edge. Brand mark and name sit at the top, and a small disclaimer and the theme toggle (a segmented well with a sliding pill) sit at the bottom.
- **Top bar:** The search trigger looks like a 40px sheet with a keyboard hint ("Strg K") and opens the command palette. The primary action is on the right.

### Filing Tab (signature)
The tab that names a sheet's specialty. Top-rounded, no bottom border, a 3px specialty stripe along the top, a 16% specialty wash fill and a 35% specialty-mixed border, with a specialty-coloured icon and a 12px semibold Slate Ink label. It sits 16–20px in from the sheet's left edge and overlaps the sheet by 1px. On hover over the card it rises 4px.

### Specialty Strip (signature)
The specialty filter, and the dashboard's summary of the collection. It is a row of tabs standing on a 2px hairline drawer edge, sorted by count. Each tab is 40px tall on Sheet White with a 3px top stripe, a 13px medium name and a tabular count. Hovering grows a tab to 44px with a teal wash. The selected tab grows to 48px, takes its 14% specialty wash, thickens its stripe to 5px and casts the upward shadow, while the other tabs fade their stripes to 35%. Below it, a separate 8px share bar labelled "Anteil der Einträge" splits proportionally by specialty. This keeps the tabs readable without making their widths proportional. Tabs enter with a 40ms stagger, and the share bar grows in from the left.

### Score Bars (signature)
The classifier's scores, one 8px rounded bar per specialty in that specialty's colour on a Muted Wash track. The winner's name is semibold and every other bar drops to 45% opacity. Widths animate with the expo-out curve, and the list reorders on a spring (stiffness 380, damping 34).

## Do's and Don'ts

### Do:
- **Do** show a specialty through the Filing Tab or a stripe, dot, icon or bar in its colour, at L 0.62, the same in both themes.
- **Do** keep labels on coloured surfaces in Slate Ink. A specialty colour only tints the surface (14–16% mix) or marks it (3px stripe).
- **Do** put every content block on a white record sheet with a 16px radius, a 1px hairline and the Sheet shadow, and lift to the Lift shadow only on interactive hover/focus.
- **Do** use Clinical Teal for the single primary action per view, for links and focus, and for data that does not belong to a specialty.
- **Do** use the expo-out curve `cubic-bezier(0.16, 1, 0.3, 1)` for entrances and state changes (200ms state, 280ms route, 350–600ms entrance), and reduce to opacity-only when reduced motion is requested.
- **Do** set every comparable number in tabular figures.

### Don't:
- **Don't** colour text with a specialty hue, or fill a large area with a solid specialty colour.
- **Don't** use the petrol rail colour anywhere outside the navigation rail.
- **Don't** introduce shadows beyond Sheet and Lift, or use hard offset shadows.
- **Don't** use solid red fills for destructive actions. Use red text on a 10% tint.
- **Don't** add uppercase tracked labels above headings. Sub-labels are 12px sentence case in Muted Ink.
- **Don't** make strip tabs proportional in width. Proportion lives in the separate share bar so names stay readable.
