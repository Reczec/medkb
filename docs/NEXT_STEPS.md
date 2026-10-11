# Next steps after stage 4

Updated 2026-10-11. Stages 1–4 are integrated into main; stage 4 implementation ends at c65c0f1. See [stage 4 record](reviews/2026-10-11-stage4-completion.md) for checks and integration status.

## Configure and smoke-test AI

1. Put a provider key in local/server configuration, never Git. Defaults and official references are in [README](../README.md#configuration-ai-assistance).
2. Restart the backend. Try one explanation, a staff summary, a grounded question and one reviewed draft; inspect provider output and rate limits. No real provider key was supplied during implementation, so only deterministic fake transport tests were run.
3. Optionally warm one entry with `python -m app.ai.prewarm --limit 1`, then warm all after checking the account's limits. Full seed warmup may need 376 uncached calls; the global budget still applies. Run `scripts/check_seed_sources.py` with WHO credentials before claiming code mappings verified.

## Next: stage 5 — public deployment

Write a plan next to the stage 4 plan, with a file map, failing tests first and full checks per task. The user shares this checkout; coordinate edits and inspect changes before committing.

1. Resolve the relevant auth/reset/archive correctness follow-ups in [BACKLOG](BACKLOG.md).
2. Verify current Render/Neon hosting behavior and limits from official documentation; prepare deployment configuration, persistent PostgreSQL/archives and environment secrets.
3. Test the AI quota transaction on PostgreSQL with concurrent requests. Configure proxy trust narrowly and verify actual client identity; otherwise every request may share the reverse proxy's IP budget. Set a stable JWT_SECRET.
4. Run deployment container health/UI smoke checks, then verify external PubMed/WHO/openFDA and AI with real credentials. Provider prompts and source-index validation do not certify medical claims.
5. Refresh README live link, screenshots and demo GIF. Current README raster screenshots are older than the stage 4 interface; current verification captures are in ignored .impeccable/review/.

Stage 5 requires its implementation and configuration work before deployment.
