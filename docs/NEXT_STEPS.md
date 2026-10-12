# Next steps after the public launch

Updated 2026-10-12. All five stages are done; the demo runs at https://medkb.onrender.com. See the [stage 5 record](reviews/2026-10-12-stage5-deployment.md).

## Still to do for the bilingual release

- English AI cache warmup after the next UTC midnight (`python -m app.ai.prewarm --lang en --pause 4` against Neon), then re-record the README GIF and screenshots. See the [record](reviews/2026-10-12-mehrsprachigkeit.md).

## RAG extension

Implementation and evaluation are recorded in [the RAG handoff](reviews/2026-10-12-rag-chatbot.md).
Before public semantic enablement: build the current index on Neon using the explicit operator
CLI, verify coverage in both languages, then set `RAG_ENABLED=true` and the development-selected
threshold in Render. Code deployment keeps RAG disabled. Index rows survive demo resets and
unchanged seeds reuse their vectors; edited/restored content requires a resumable rebuild.
Complete the saved human answer-support rubric; mechanical source indices alone do not prove
answer quality. The bilingual document-cache warmup remains separate from query embeddings.

## Still to verify live

1. ~~Cold start~~: measured 22 s after 18 idle minutes (2026-10-12).
2. ~~Visitor IP header~~: confirmed 2026-10-12 (spoof test plus a second network).

## Done after the launch (2026-10-12)

- Assistant retrieval for everyday questions (d79e862), found by the phone test.
- Review minors (0e07044): example entries keep ids 1..47 across resets, PostgreSQL resets are serialized with a table lock, Render deploys only after green CI (`checksPass`), `/index.html` never cached, proxy IP taken from the appended value, chunk reload works again after a later deploy.
- Live AI cache warmed (`python -m app.ai.prewarm --pause 4` against the Neon database): 376/376 role/feature variants, 0 failed; live answers then come from the cache in < 0.1 s, also for visitors at their daily limit. Re-run after prompt or content changes (`PROMPT_VERSION`).
- Stable ids confirmed live: `/wissen/7` is Migräne after the redeploy (ids 1..47).

## Optional improvements

- Rotate the Gemini key, the Neon password and the WHO credentials (all shared in a chat during setup); update them in the Render dashboard (Environment), which redeploys.
- Remaining [BACKLOG](BACKLOG.md) items (accessibility details, design ideas, a smaller demo video).
