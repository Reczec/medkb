# Next steps after the public launch

Updated 2026-10-12. All five stages are done; the demo runs at https://medkb.onrender.com. See the [stage 5 record](reviews/2026-10-12-stage5-deployment.md).

## Still to verify live

1. **Cold start:** open the demo after 15+ minutes without visitors and time the first page (Render: about a minute).
2. **Visitor IP header:** a spoofed `True-Client-IP` is not honoured (tested 2026-10-12, see the record). Still open: ask one AI question from a second network (phone on mobile data) while the first network is at its daily limit; an answer confirms per-visitor buckets.

## Optional improvements

- The minors in [BACKLOG](BACKLOG.md) (stable entry IDs across resets, deploy only after CI via `checksPass`, smaller demo media).
- Rotate the Gemini key and the Neon password, since both were shared in a chat during setup; update them in the Render dashboard.
- Pre-warm the AI cache on the live service (`python -m app.ai.prewarm` with the production `DATABASE_URL`), so first visitors get instant answers.
