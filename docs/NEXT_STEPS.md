# Next steps after the public launch

Updated 2026-10-12. All five stages are done; the demo runs at https://medkb.onrender.com. See the [stage 5 record](reviews/2026-10-12-stage5-deployment.md).

## Still to verify live

1. **Cold start:** open the demo after 15+ minutes without visitors and time the first page (Render: about a minute).
2. ~~Visitor IP header~~: confirmed 2026-10-12 (spoof test plus a second network).

## Done after the launch (2026-10-12)

- Assistant retrieval for everyday questions (d79e862), found by the phone test.
- Review minors (0e07044): example entries keep ids 1..47 across resets, PostgreSQL resets are serialized with a table lock, Render deploys only after green CI (`checksPass`), `/index.html` never cached, proxy IP taken from the appended value, chunk reload works again after a later deploy.
- Live AI cache warmed (`python -m app.ai.prewarm --pause 4` against the Neon database): 376/376 role/feature variants, 0 failed; live answers then come from the cache in < 0.1 s, also for visitors at their daily limit. Re-run after prompt or content changes (`PROMPT_VERSION`).
- Stable ids confirmed live: `/wissen/7` is Migräne after the redeploy (ids 1..47).

## Optional improvements

- Rotate the Gemini key, the Neon password and the WHO credentials (all shared in a chat during setup); update them in the Render dashboard (Environment), which redeploys.
- Remaining [BACKLOG](BACKLOG.md) items (accessibility details, design ideas, a smaller demo video).
