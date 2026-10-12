# Bilingual release (English default, German switch) – record

Spec: [2026-10-12-mehrsprachigkeit-design.md](../superpowers/specs/2026-10-12-mehrsprachigkeit-design.md) ·
Plan: [2026-10-12-mehrsprachigkeit.md](../superpowers/plans/2026-10-12-mehrsprachigkeit.md) · PR #3.

## What shipped

- Interface in English by default with an EN | DE switch (remembered in `localStorage`, sent as
  `Accept-Language`). The editor and open forms are never remounted by a switch.
- All 47 entries have an English version; German stays canonical because the rule-based classifier
  works on German text. Missing English parts fall back field by field, with a visible note when
  an entry has no English version at all.
- Search matches both languages. Server messages, ICD-11 and AI answers follow the request
  language. German AI cache keys are unchanged (pinned test), English adds the language to the key,
  drafts stay German.
- Editor: collapsible "English version"; a cleared field is sent as `null`.

## Verification

| Check | Result |
|---|---|
| pytest, ruff | green |
| vitest / oxlint / tsc / build | 224 passed, clean |
| Playwright | 35 passed (existing flows pinned to German, `i18n.spec.ts` covers the default) |
| CI on the PR | docker, frontend, postgres, sqlite 3.12 and 3.13 green |

Fresh-context whole-branch review: five findings were fixed with a failing test first (partly
translated entries lost German warning signs in English, palette titles, AI draft dropped typed
English text, German-only server texts, tab title). Deferred minors: no client-side length checks
for the English editor fields, no `lang="de"` on German fallback text, label-in-name of the
language switch, `title_en` without a title bonus in AI retrieval, silent `lang="de"` defaults in
backend helpers.

## Live acceptance (2026-10-12, after the Render deploy)

- `<title>` is English; the schema upgrade added the new columns on Neon without data loss.
- Search `cold` and `Erkältung` find the same entries in both languages (5 and 1 hits).
- ICD-11 for entry 1: "Acute otitis media" (`en`) and "Akute Otitis media" (`de`).
- AI explain for entry 1: English answer generated live (`cached: false`), German answer served
  from the warmed cache (`cached: true`) – the existing cache survived.
- `/api/auth/me` without a token answers in the request language.

## Still open

- English AI cache warmup: `python -m app.ai.prewarm --lang en --pause 4` against the Neon
  database (376 calls). The shared 500/day budget is partly used on the release day, so run it
  after the next UTC midnight.
- README GIF and screenshots still show the German interface; re-record with
  `node frontend/scripts/record-demo.mjs` (now English) after the warmup.
