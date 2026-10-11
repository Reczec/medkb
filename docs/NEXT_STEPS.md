# Next steps after stage 4

Updated 2026-10-11. Stages 1–4 are integrated into main; stage 4 implementation ends at c65c0f1. See [stage 4 record](reviews/2026-10-11-stage4-completion.md) for checks and integration status.

## AI live check (done 2026-10-12)

A real Gemini key (local `.env` only) answered all seven features through the app with demo roles: explain, red-flags, summary, ask with citation, draft, classify, PubMed study summary; second explain came from the cache; usage counted. Two findings were fixed in `09ff56b`: raw Markdown in the UI (now a safe Markdown subset renderer) and an unfocused red-flags answer. Seed warmup was not run.

WHO ICD-11 (done 2026-10-12): with local WHO keys, `scripts/check_seed_sources.py` resolved all 44 bundled codes (release 2026-01, German titles) and each WHO title matches its entry; 69/69 further-reading links answered 200.

## Next: stage 5 — public deployment

Plan: [etappe-5-deployment](superpowers/plans/2026-10-12-etappe-5-deployment.md). The user shares this checkout with Claude and Codex; inspect changes before committing.

1. Resolve the relevant auth/reset/archive correctness follow-ups in [BACKLOG](BACKLOG.md).
2. Verify current Render/Neon hosting behavior and limits from official documentation; prepare deployment configuration, persistent PostgreSQL/archives and environment secrets.
3. Test the AI quota transaction on PostgreSQL with concurrent requests. Configure proxy trust narrowly and verify actual client identity; otherwise every request may share the reverse proxy's IP budget. Set a stable JWT_SECRET.
4. Run deployment container health/UI smoke checks, then verify external PubMed/WHO/openFDA and AI with real credentials. Provider prompts and source-index validation do not certify medical claims.
5. Refresh README live link, screenshots and demo GIF. Current README raster screenshots are older than the stage 4 interface; current verification captures are in ignored .impeccable/review/.

Stage 5 requires its implementation and configuration work before deployment.
