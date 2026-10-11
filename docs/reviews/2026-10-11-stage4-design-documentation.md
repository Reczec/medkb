# Stage 4 design documentation

Date: 2026-10-11. Scope: ordinary extension of the existing MedKB visual system.

## Authority and evidence

Compared `PRODUCT.md`, the normative tokens and visual rules in `DESIGN.md`, the schema-v2 extensions in `.impeccable/design.json`, and the stage 4 direction contract in `.impeccable/surfaces/frontend-src-app-tsx.md` with the implemented code. The Impeccable document reference informed this documentation pass. A generic isolated documenter substituted for the unavailable named documenter; this is a code comparison and evidence record, not a regenerated design system.

Implementation evidence: `frontend/src/index.css`, shared `components/ui/button.tsx`, `components/layout/Sidebar.tsx`, `features/documents/DocumentPage.tsx`, `features/editor/EditorPage.tsx`, and the AI presentation components `AssistantPage`, `AIResponse`, `AIUsage`, `DocumentAI`, `EditorAI`, and `StudyAI` under `frontend/src/features/ai`.

All sixteen expected screenshot files were present in `.impeccable/review`: `ai-{assistant,patient,staff,editor}-{desktop,phone}-{light,dark}.png`. This documenter directly inspected `ai-assistant-phone-dark.png` and `ai-editor-desktop-light.png`; the other files were inventoried, not individually visually reviewed in this pass. The finish review's supplied disposition is **ship**. Screenshot existence and this documentation do not independently certify all states or behaviors.

## Extension consistent with the system

- AI surfaces reuse the semantic card, foreground, muted, border, primary, and destructive colors. Their light paper and dark slate appearance comes from existing CSS theme tokens; no new palette, font, image asset, or visual world is introduced.
- The assistant uses one reading sheet beneath a single 30px page title. Its 16px/24px form layout stacks on phones and becomes horizontal at the existing small breakpoint. Panels retain the established 16px corners, hairline borders, sheet shadow, and 20px padding, increasing to 24px where appropriate.
- Shared primary and outline buttons preserve teal actions, existing focus treatment, disabled states, and rounded control shapes. Editor apply controls allow wrapped labels to fit the narrow aside. AI result text and citation titles explicitly allow long content to wrap.
- Global Inter Variable and its alternate glyph settings continue to apply. Section headings use the existing 16px semibold tier; secondary information uses muted UI text. Usage totals and AI confidence use tabular figures.
- Document AI joins the existing reading-sheet/aside composition. Professional summary occupies the source-tab system; patient explanation uses a separate panel. The specialty filing-tab signature and the existing classification presentation remain in place.
- Editor AI is separated from the rule-based scores by a hairline and its own heading. The incumbent classifier retains its explicit “Regelbasiert” explanation, while AI results carry “KI-generiert”. Draft metadata is visibly reviewable before applying it, and the copy distinguishes applying fields from saving an entry.
- Assistant navigation reuses the petrol rail and its existing active indicator. Prototype notices remain visible in the reviewed assistant and editor captures. AI copy also distinguishes provisional generation, cached results, retryable errors, and cited entries.

## Differences and existing drift

The original surface brief still describes nine specialties in its inherited direction text. Its stage 4 scope already identifies this as pre-existing drift; `DESIGN.md` and the implemented editor show sixteen. It is recorded here without changing the authoritative files.

The extension has local density choices rather than new global tokens: AI result text is 16px with relaxed leading and a 68-character maximum width, while the canonical document-reading text is documented as 17px. The assistant stacks sections with 24px gaps rather than the general 32px page rhythm, and its question action is 44px tall to align with the field rather than the ordinary 32px button. These are observed surface variations; they do not redefine the shared hierarchy or control primitives.

`DESIGN.md` and `.impeccable/design.json` are preserved. No redesign, concept exploration, asset production, or token refresh was performed.

## Verification boundary

This report documents visual-system continuity using code and the two named captures. It does not certify live provider availability, medical quality, streaming correctness, role enforcement, keyboard interaction, contrast measurements, or the full automated suite. Those belong to the implementation checks and stage 4 completion report. The supplied finish-review **ship** disposition is a visual handoff, not proof of a live AI smoke test.

Final code recheck: inspected the subsequent diff in `AIResponse.tsx`, `useAI.ts`, and `AssistantPage.tsx`. Retry now returns its result and can use an assistant-specific handler so a successful retry enters conversation history; successful requests clear the question only when it still matches the submitted text. The diff changes callbacks and state handling, with no CSS classes, layout, typography, tokens, or visible labels changed. The visual-system documentation remains applicable. This recheck did not recapture screenshots or certify retry behavior through execution.
