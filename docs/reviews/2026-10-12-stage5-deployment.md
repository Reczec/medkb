# Stage 5 — public deployment record (2026-10-12)

Live: **https://medkb.onrender.com** (Render free Docker web service, Frankfurt; Neon Postgres free, Frankfurt, direct endpoint). Plan: [etappe-5-deployment](../superpowers/plans/2026-10-12-etappe-5-deployment.md). Branch `feat/v2-stage5` merged by fast-forward into `main` (PR Reczec/medkb#1, CI green on all five jobs including the container smoke test and PostgreSQL).

## Commits

| Commit | Task |
|---|---|
| 093ca99 | 1 atomic demo reset, tokens require exp/sub, late 401 keeps a new login |
| fe4d5bc | 2 AI client identity from a configured proxy header |
| b9e0e38 | 3 caching and security headers, HEAD /, 404 for missing assets |
| fe0f4c5 | 4 lazy routes: main chunk 1,168 kB → 341 kB |
| bf7965b | 5 render.yaml, PORT-aware image with --no-proxy-headers, container smoke test in CI |
| 1f5ad5b | extra: Urologie stems only at word start (found in the screenshots) |
| 0ee2814 | 6 README with GIF and screenshots from real services |
| 62cdb93 | final review fixes: Postgres pool pre-ping/recycle (Neon idle suspend), CLIENT_IP_HEADER warning and deploy step |

Before stage 5, on `main`: 43fe489 (blank page after saving — exit animation never finished on slow CPUs; CI had been red since stage 4), 09ff56b (AI Markdown rendering, focused warning signs, plain-language explain), WHO ICD verification of all 44 codes.

## Live acceptance (2026-10-12, warm service)

| Check | Result |
|---|---|
| `/api/health`, `/` | 200 in ~0.15 s |
| Shell `Cache-Control` | `no-cache`; hashed asset `public, max-age=31536000, immutable`; missing asset 404 |
| Security headers | nosniff, strict-origin-when-cross-origin, X-Frame-Options DENY |
| Demo login | admin, doctor, patient |
| Content | 47 entries, 16 specialties; Migräne → Neurologie, ICD 8A80 |
| PubMed / WHO ICD-11 / openFDA | ok in 0.9 / 0.7 / 1.7 s (ICD in German); dashboard latest studies ok |
| Patient on sources | 403 |
| AI (Gemini) | explain, red-flags, summary, ask with citation: 200 in 1–2 s; usage counted |
| Login page in the browser | renders |

Spoof test (2026-10-12): 19 uncached questions with `True-Client-IP: 198.51.100.10` counted against the same visitor bucket as this network's earlier header-less requests (429 at call 20, not 31); a fresh fake value `203.0.113.99` then also got 429. So a client-sent value is not used as is. Four calls got 503 `ai_unavailable` because the burst (~40/min) exceeded Gemini's free per-minute limit; the reservations still counted, as designed.

Second network (user's phone on mobile data, same day): AI answered while the home network was at its limit, so Render writes the visitor's real IP into `True-Client-IP` and visitors get separate quotas. That phone test also showed the assistant answering "keine passenden Einträge" for "Was hilft bei Erkältung?": fixed in the following commit (everyday question words, partial-match fallback weighted by term rarity and title hits).

Open live check: cold start time after 15 min idle.

## Rulings

- Task 1: Ruling: reset flushes before clearing the audit log — SessionLocal has autoflush=False, so the seed's own audit rows would otherwise survive — cost if wrong: none.
- Task 5: Ruling: --no-proxy-headers in the image + CLIENT_IP_HEADER (Task 2) instead of uvicorn proxy trust — Render's default FORWARDED_ALLOW_IPS=* would trust spoofable X-Forwarded-For — cost if wrong: until CLIENT_IP_HEADER is set, all visitors share one AI client budget (global limit still applies).
- Task 5: Ruling: autoDeployTrigger (current Render field) instead of the deprecated autoDeploy named in the plan; region frankfurt (near the user, Neon has eu-central-1) — cost if wrong: none.
- Task 6: Ruling: README stays English (existing README, code/docs English, international recruiters) instead of German with English summary — cost if wrong: one translation.
- Task 6: Ruling: demo media use the real local services (Gemini, PubMed, WHO, openFDA) instead of mocks — authentic output for a CV demo — cost if wrong: re-recording gives slightly different text.
- Task 6: Ruling: recording script lives in frontend/scripts (needs frontend's Playwright) instead of scripts/ — cost if wrong: none.
- Final: Ruling: True-Client-IP spoof resistance is undocumented by Render — verify live in Task 7 before relying on it — cost if wrong: one visitor could reset their own 30-call AI quota (global 500 still caps).
- Final: Ruling: Neon pooled endpoint + psycopg prepared statements left to the live check; README advises the connection string Neon shows — cost if wrong: errors on first queries, fixed by the direct URL.

## Deferred minors

- client_ip takes the leftmost value; a misconfigured X-Forwarded-For would be spoofable (README now forbids it)
- two overlapping resets (deploy + loop) can duplicate entries until the next reset; PostgreSQL table lock would prevent it
- entry IDs change on every cold start, so shared entry links break after sleep (fixed IDs or RESTART IDENTITY)
- explicit /index.html request lacks no-cache
- chunk-reload flag can stay set when the reload lands on a non-lazy route
- render autoDeployTrigger: commit deploys without waiting for CI (checksPass)
- 7.7 MB README GIF loads slowly

Also recorded in [BACKLOG](../BACKLOG.md).
