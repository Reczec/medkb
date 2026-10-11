# Next steps after the public launch

Updated 2026-10-12. All five stages are done; the demo runs at https://medkb.onrender.com. See the [stage 5 record](reviews/2026-10-12-stage5-deployment.md).

## Still to verify live

1. **Cold start:** open the demo after 15+ minutes without visitors and time the first page (Render: about a minute).
2. **Visitor IP header:** confirm Render's edge overwrites a client-sent `True-Client-IP`. Test: send 30 uncached AI questions with one spoofed value, then one with another spoofed value; the last must answer 429. This uses up the tester's own 30-call AI quota until UTC midnight. If it answers 200, the header is spoofable: switch `CLIENT_IP_HEADER` to a header Render does overwrite, or leave it empty (all visitors then share one quota).

## Optional improvements

- The minors in [BACKLOG](BACKLOG.md) (stable entry IDs across resets, deploy only after CI via `checksPass`, smaller demo media).
- Rotate the Gemini key and the Neon password, since both were shared in a chat during setup; update them in the Render dashboard.
- Pre-warm the AI cache on the live service (`python -m app.ai.prewarm` with the production `DATABASE_URL`), so first visitors get instant answers.
