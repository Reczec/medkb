# RAG design documentation

Date: 2026-10-12. Scope: ordinary extension of the existing AI assistant and shared AI response presentation.

## Authority and evidence checked

Compared `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json`, the incumbent direction contract in `.impeccable/surfaces/frontend-src-app-tsx.md`, and the Impeccable `reference/document.md` guidance against `frontend/src/features/ai/AssistantPage.tsx`, `AIResponse.tsx`, `AIText.tsx`, `client.ts`, and both i18n dictionaries. The stage 4 design documentation supplied the incumbent surface comparison. A fresh generic documenter performs the named documenter role; this report records the extension, without regenerating the design system.

Opened and visually inspected all eight final captures individually:

| Language | Desktop, light | Desktop, dark | Phone, light | Phone, dark |
| --- | --- | --- | --- | --- |
| English | `.impeccable/review/rag-en-desktop-light.png` | `.impeccable/review/rag-en-desktop-dark.png` | `.impeccable/review/rag-en-phone-light.png` | `.impeccable/review/rag-en-phone-dark.png` |
| German | `.impeccable/review/rag-de-desktop-light.png` | `.impeccable/review/rag-de-desktop-dark.png` | `.impeccable/review/rag-de-phone-light.png` | `.impeccable/review/rag-de-phone-dark.png` |

Each shows the assistant at the document top, its question and completed answer, hybrid retrieval label, linked source, expanded source excerpt with visible focus treatment, and prototype notice. The phone captures show the full vertically stacked surface; text stays within the sheet. The files contain rendered content rather than blank, black, loading, or wrong-route evidence. English captures use the patient demo and German captures the doctor demo; this is not an exhaustive role matrix.

The supplied finish-review verdict is **ship** after its sole material fix, German hint alignment, was scored resolved. The supplied detector result was `[]` from one run on `AIResponse.tsx` and `client.ts`. Those are handoff evidence, not commands rerun by this documenter. The verdict pass supports resolution of that listed fix; it does not constitute a new whole-application review.

## Extension conformance

- Retrieval mode and fallback reason join the existing muted metadata hierarchy beneath the explicit AI-generated marker. Both dictionaries define hybrid and keyword labels and disabled, incomplete-index, and embedding-unavailable explanations. The screenshot matrix demonstrates hybrid mode; fallback presentation is checked in code only.
- Each citation retains the existing internal entry link and teal link treatment. Optional excerpts use native `details` and `summary`, keeping source text discoverable without another route, modal, or visual subsystem. Section names resolve through the existing localized section keys, with a content fallback. Titles and excerpts render as React text; excerpts preserve whitespace and allow long text to wrap.
- Sources sit below the answer in the same record sheet. Disclosure summaries use existing muted/foreground colors and the shared ring token for visible keyboard focus. Excerpts use relaxed 14px body text and a 68-character maximum width. No palette, typography family, token, shipping raster, or motion is introduced.
- The assistant retains its single page title, petrol desktop rail, existing mobile shell, hairline response divider, paper/slate panel, sheet shadow, and teal question action. The field and action stack on phones and align horizontally at the incumbent small breakpoint.
- English and German hints both explain that answers use excerpts from up to five entries and that sources can be inspected. Both retain the restriction on personal health data and emergency notice. German now matches the retrieval behavior rather than describing the previous entry-only context. Prototype notices remain visible in every checked capture.
- The classifier and its explanation are not redesigned by this extension. AI retains its separate AI-generated identity; retrieval metadata does not claim classifier output or external medical verification.

## Incumbent differences and drift

The existing surface brief describes nine specialties and proportional tab widths, whereas `DESIGN.md` specifies sixteen specialties and a separate proportional share bar. These inherited discrepancies remain unchanged. `PRODUCT.md` still describes a German-only interface, while the current application defaults to English and provides a German switch. This report records that stale product wording without editing it.

The existing `AppShell.tsx` footer is a German literal in both language captures, alongside the localized assistant notice. This predates the RAG presentation and remains outside this extension. The incumbent assistant also uses 24px section gaps, a 44px question action, and 16px AI answer text rather than the general 32px page rhythm, 32px button, and 17px document-reading tier. These established surface choices are not new normative tokens.

`DESIGN.md` and `.impeccable/design.json` are preserved. This ordinary extension requires no new world or approved system change, so no token regeneration or unsolicited drift repair was performed.

## Verification bounds

This is a code and screenshot comparison, not a medical-quality assessment, retrieval relevance evaluation, live-provider test, automated-suite run, measured contrast audit, screen-reader audit, or runtime keyboard test. The captures demonstrate one completed hybrid answer with one expanded source in each language/theme/viewport combination. They do not demonstrate lexical fallback, pending/error/cache states, multiple long sources, all roles, or every caller of the shared response component. Native disclosure semantics and focus styling are present in code and focused captures; their full runtime behavior belongs to implementation verification. No deployment or commit was performed by this documenter.
