# Public RAG activation — 2026-10-12

The user requested the same RAG experience in https://medkb.onrender.com as in the local preview.
The frontend was already deployed at `3ba00fe`; semantic retrieval had deliberately remained off.

## Index and configuration

- Read Render's existing Neon connection without committing any credentials. The local `.env`
  remains unchanged. Temporary operator connection material is removed after verification.
- Compared every current production chunk key with the validated local evaluation database.
  All 47 documents matched exactly across both languages and the embedding/chunk signature.
- Imported only those matching, normalized vectors with PostgreSQL upserts in one transaction;
  rechecked the corpus before commit and required complete coverage in both languages.
  Result: 542 imported, 271 German ready, 271 English ready, zero provider calls.
  Production global usage at that point was 3 for the UTC day.
- Set `RAG_ENABLED=true` in Render and saved/deployed the existing build. The first attempt
  through a masked field retained `false`; live verification caught this. Revealed only that
  nonsensitive flag, changed it visibly to `true`, and repeated save/deploy.
- Updated `render.yaml` to retain the enabled flag and explicit development-selected threshold
  `RAG_MIN_SIMILARITY=0.60` on subsequent Blueprint synchronization. Local defaults remain off.

No new model, paid tier, startup indexing, provider key or public indexing endpoint was introduced.
The earlier frozen evaluation and human-review limitations remain in the [implementation record](2026-10-12-rag-chatbot.md).

## Verification

Render configuration deployment `dep-db6kcrom7kps73b97s6g` became Live at code commit `3ba00fe`.
At 20:44:27 UTC (22:44 Vienna), patient-demo checks returned:

| Request | HTTP | Retrieval | Indexed chunks | Cited excerpts |
|---|---|---|---|---|
| German migraine symptoms, JSON | 200 | hybrid | 271 | 2: symptoms, definition |
| English migraine symptoms, SSE terminal `done` | 200 | hybrid | 271 | 2: symptoms, definition |

Both assertions required nonempty server-owned section/excerpt fields. This verifies production
query embeddings and completions with Render's existing configured provider. These are deliberate
operator smoke checks, outside the automated tests. Automated provider tests remain mocked.
Render startup restores the demo entries (`app.main`); complete semantic coverage after this
restart confirms index persistence across the real PostgreSQL demo reset without regeneration.
No extra manual reset or production-content edit was needed.

The public patient UI generated an English migraine answer, displayed `Semantic + keyword search`
and two sources, and expanded the Symptoms disclosure to show the matching entry excerpt.
Local proof capture: `.impeccable/review/rag-public-live.png` (ignored, not committed).
The screenshot shows a real public response, unlike the earlier mocked UI-test capture.

A second Neon coverage check after restart imported zero rows: all 542 valid vectors were reused,
with 271 ready per language. Global usage was then 11. Temporary connection material was deleted.

Local checks: full backend suite (827 passed, one existing skip), Ruff check/format (99 files),
frontend lint/typecheck/build passed. The first concurrent frontend unit run missed the login
button once (226/227); the bounded one-worker rerun passed all 227. The first browser run under
concurrent unit-test load failed the CPU-throttled draft navigation and two dashboard checks
(35/38). The failed draft left a disposable entry (48 instead of 47), causing the summary failure;
the filing-tab check also sampled equal animated bar widths. A fresh serial browser run passed
all 38 tests (52.4 s); a further normal `npm test` run passed all 227. No frontend code or test
expectations were changed. Final local suite: 827 backend, 227 frontend, 38 browser tests green.

## Operations

Unchanged example-data resets reuse the persisted content-addressed vectors. Editing content
can make a language index incomplete: the assistant then declares keyword fallback until an
operator rebuilds with `python -m app.rag.index_cli --pause 15` against the production database.
Rollback is `RAG_ENABLED=false` followed by save/deploy; persisted vectors can remain in Neon.
