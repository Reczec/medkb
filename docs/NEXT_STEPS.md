# Next steps after stage 3

Updated 2026-10-11. Stages 1–3 are implemented and integrated into `main`. The stage 3 implementation and local integration record were pushed to `origin/main` through `309e3b9`.

## Next: stage 4 — AI features

Write `docs/superpowers/plans/<date>-etappe-4-ki.md` before implementing, following the existing plans: file map, shared interfaces, failing tests first, full checks and one commit per task. Work on a feature branch; coordinate file ownership if Claude and Codex work concurrently.

The authoritative requirements are [v2 spec §5](superpowers/specs/2026-10-10-medkb-v2-design.md). Suggested task order:

1. **Resolve provider and input contracts.** Verify the currently available model, endpoint, limits and terms against official provider documentation. The spec proposes an OpenAI-compatible provider with `AI_BASE_URL`, `AI_API_KEY`, `AI_MODEL`; credentials remain in local/server configuration. Without a key, return `503 ai_not_configured` and show a clear UI hint. Tests use a fake provider.
2. **Build the shared backend foundation.** Provider completion/streaming, `ai_cache`, `ai_usage`, content-aware cache keys, atomic quota accounting, per-client 30 uncached calls/day and configurable global limit (spec default 500). Cached responses must not consume quota; failures must not create successful cache entries. Specify SSE error/cancellation behavior and trusted client-IP handling before deployment.
3. **Add document explanations and summaries.** Explain in B1 language, warning signs and professional summary, with role checks, explicit AI labeling and the existing prototype notice. Keep the rule-based classifier separate and explainable.
4. **Add study summaries and grounded questions.** PubMed currently returns metadata, not abstracts: add an abstract-fetching contract and tests before promising abstract summaries. The assistant uses the existing search's top five entries, cites `[n]`, handles no matching context honestly, uses role-appropriate language and accepts at most six history messages. Treat entry content and conversation text as untrusted input. `ask` is not cached.
5. **Add admin drafts and classification second opinions.** Validate generated structured fields; let the admin review a draft before saving. Preserve `ai_generated` and clearly distinguish the AI suggestion from the existing rule result.
6. **Integrate the UI and finish.** SSE rendering, retry/not-configured/rate-limit states, role-based controls, dashboard usage, seed-cache prewarming CLI, fake-provider backend tests, mocked browser flows, documentation and independent final review.

## Parallel follow-up from stage 3

WHO ICD-11 seed-code mapping remains unconfirmed without credentials. Once configured, run `scripts/check_seed_sources.py` and correct mismatches. This does not prevent AI implementation, but should be resolved before presenting the live source mapping as verified.

## Before stage 5 — public deployment

Prioritize the correctness and auth issues in [BACKLOG.md](BACKLOG.md), especially old-token 401 handling, required JWT claims, demo-reset consistency and archive restore double-submit protection. Stage 4 quota/client identity must work correctly behind the deployment proxy.

Then follow stage 5: deployment configuration for Render and Neon, production configuration/secrets, PostgreSQL verification, CI container smoke checks, README live link and fresh screenshots/demo GIF. Recheck hosting limits and deployment behavior against current official documentation at that time.

Stage 4 implementation has not started; this file records sequencing and planning requirements rather than replacing its task plan.
