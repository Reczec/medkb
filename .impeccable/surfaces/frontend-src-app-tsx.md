---
version: 1
slug: "frontend-src-app-tsx"
primary_target: "frontend/src/App.tsx"
related_targets: []
---

# Surface brief: MedKB app (all routes in frontend/src)

Mode: Operate. Audience and job: see PRODUCT.md. Direction pinned by the user in brainstorming (spec section 2/8); no concept roll.

## Direction contract

THESIS: A credible clinical reference tool whose specialties are always legible at a glance. Refuses the generic dark admin template with grey cards and one accent.

OWN-WORLD: Colour-coded medical record filing. Deep petrol rail (sidebar) beside a cool off-white work area; white sheets with soft offset shadows; nine specialty colours (oklch, equal lightness) used as filing tabs, chart series and dots; Inter with tabular numerals; teal primary for actions. Dark theme: blue-slate, same tab colours.

STORY: The visitor sees the size and spread of the knowledge base, filters by specialty like pulling a drawer tab, opens an entry and sees exactly why it was classified where it is.

FIRST VIEWPORT (dashboard, 1440): petrol rail left (brand, nav, theme). Work area: page title + one-line summary sentence with inline counted numbers; below, the specialty filing strip (tabs with counts, proportional widths) spanning full width; then a two-column row: activity chart as daily bars (30 days, wide) and document-type bars; then recent entries as tabbed sheets. Primary action "Neuer Eintrag" top right.

FORM: No concept roll was run (concept-seed skipped; no seed key). The user pinned the visual direction in brainstorming: "klinisch-modern", light default off-white with a teal/petrol accent, a colour per specialty, dark mode, Inter, motion everywhere with reduced motion respected, credible clinical tool before showpiece. The filing-tab signature is the implementer's choice inside that pinned direction, not a user quote. Signature move: specialty filing tabs, a coloured tab protruding above each entry sheet and a proportional tab strip as the category filter; selecting a tab slides the list into its new order (layout animation).

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Stage 4 extension scope

AI assistance extends this same Operate world: assistant question/result sheet; document explanation and staff summary; editor review/apply controls. Teal actions, existing panels, Inter, safe text, explicit KI-generiert, prototype notice. Desktop assistant has one max-width reading sheet below the title; phone stacks labelled field/action/result with sources below. New editor AI controls join the existing aside, separated from rule scores. No world replacement, comp or new asset. Existing nine-specialty wording above is pre-existing drift; code and DESIGN have sixteen.
