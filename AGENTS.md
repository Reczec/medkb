# MedKB – agent guide

MedKB is a medical knowledge base (FastAPI + React) being grown from a diploma-thesis prototype into a public CV demo. Read before working:

- **Product truth** (users, roles, principles): [PRODUCT.md](PRODUCT.md)
- **Visual system** (tokens, filing-tab signature, rules): [DESIGN.md](DESIGN.md). Read it before any UI change.
- **v2 spec** (the whole target, 5 stages): [docs/superpowers/specs/2026-10-10-medkb-v2-design.md](docs/superpowers/specs/2026-10-10-medkb-v2-design.md)
- **Open follow-ups** from the stage 1 reviews: [docs/BACKLOG.md](docs/BACKLOG.md)
- **Stage 3 completion and handoff** (commits, reviews, decisions and remaining verification): [docs/reviews/2026-10-11-stage3-completion.md](docs/reviews/2026-10-11-stage3-completion.md)
- **Stage 4 completion** (AI contracts, decisions, tests and verification boundaries): [docs/reviews/2026-10-11-stage4-completion.md](docs/reviews/2026-10-11-stage4-completion.md)
- **Stage 5 deployment record** (live checks, decisions): [docs/reviews/2026-10-12-stage5-deployment.md](docs/reviews/2026-10-12-stage5-deployment.md)
- **Bilingual release** (English default, German switch; live checks, open warmup): [docs/reviews/2026-10-12-mehrsprachigkeit.md](docs/reviews/2026-10-12-mehrsprachigkeit.md)
- **Next steps** (after the public launch): [docs/NEXT_STEPS.md](docs/NEXT_STEPS.md)
- **RAG extension** (index, evaluation, release boundaries): [docs/reviews/2026-10-12-rag-chatbot.md](docs/reviews/2026-10-12-rag-chatbot.md), [evaluation commands](evaluation/rag/README.md).

## Status

| Stage (spec §12) | State |
|---|---|
| 1 React frontend, redesign, dashboard | done, merged into `main` ([plan](docs/superpowers/plans/2026-10-10-etappe-1-frontend-redesign.md)) |
| 2 Roles and auth (admin / doctor / patient, demo login, demo reset) | done ([plan](docs/superpowers/plans/2026-10-10-etappe-2-rollen-auth.md)) |
| 3 Data model, 47 realistic entries, PubMed / WHO ICD-11 / openFDA | done, merged into `main` and pushed ([plan](docs/superpowers/plans/2026-10-11-etappe-3-inhalte-quellen.md)) |
| 4 AI features (free OpenAI-compatible provider, cache, rate limit) | done; live-checked with Gemini 2026-10-12 ([plan](docs/superpowers/plans/2026-10-11-etappe-4-ki.md)) |
| 5 Deployment (Render + Neon), README, demo GIF | done, live at https://medkb.onrender.com ([plan](docs/superpowers/plans/2026-10-12-etappe-5-deployment.md), [record](docs/reviews/2026-10-12-stage5-deployment.md)) |

Continue a stage by writing its plan next to the stage 1 plan (same structure: file map, tasks with failing test first, commit per task), then implement it task by task.

## Working rules

- UI text English by default with a German switch; code and API English. New texts go into **both** dictionaries (`frontend/src/i18n/messages.de.ts`, `messages.en.ts`; the German file defines the key set), never as literals in components. Entries stay German-canonical (classifier), the English version is optional.
- Test first: a failing test, then the change, then the whole suite. Every task ends green on `pytest`, `ruff check . && ruff format --check .`, and in `frontend/`: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run e2e`.
- One commit per task.
- The rule-based classifier is the thesis core: keep it, keep it explainable. Its UI marker is "regelbasiert"; AI features (stage 4) get their own clearly separate marker.
- Every view keeps the notice "Prototyp mit Beispieldaten – keine medizinische Beratung." There is no patient data, ever.

## Gotchas (not visible from config)

- **Deployment.** `main` auto-deploys to Render (Blueprint `render.yaml`); every deploy restarts the service and resets the demo data. Secrets live only in the Render dashboard. Neon uses the direct (non-pooler) endpoint. `node frontend/scripts/record-demo.mjs` re-records the README media against a running instance.

- **AI tests/setup.** No key means HTTP503 `ai_not_configured`; override `get_provider` with a fake or intercept `/api/ai/**` in browser tests. Never call a paid/live model in tests. SSE partial text is provisional until `done`. Bump `app.ai.store.PROMPT_VERSION` after prompt changes. Quotas and cache survive demo reset; successful semantic content snapshots exclude IDs/reset timestamps; canonical source/title seed identity also survives PostgreSQL resets. Explicit CLI: `python -m app.ai.prewarm --limit 1`; trusted warmup still respects the global budget.
- **RAG.** Default off until an operator-built current index and real evaluation pass. `python -m app.rag.index_cli --pause 4` resumes content-addressed bilingual vectors; it never runs on page load. `python -m app.rag.evaluate --split dev --sweep --output PATH` tunes only on dev; freeze before the held-out test run. Native Gemini model001 currently requires top-level REST `taskType`/`outputDimensionality` to return768; `embedContentConfig` was accepted but ignored for dimensions in the live probe. Reject wrong-sized vectors. Ask prompt version is separate (`ASK_PROMPT_VERSION`); other warmed document caches retain their version. Edited content makes index coverage incomplete and visibly falls back to keywords; rebuilding is explicit. Never use fake vectors as semantic-quality evidence.

- **e2e** needs a fresh `npm run build`, and `PYTHON` pointing at the venv's Python. From `frontend/` in PowerShell: `$env:PYTHON = (Resolve-Path ../.venv/Scripts/python.exe).Path; npm run e2e`. Use an absolute path: Playwright launches from the repository root. It starts its own uvicorn on port 8765 with a throwaway seeded SQLite DB.
- **Sources in tests.** The autouse respx fixture `network` blocks real outbound HTTP in backend tests; register mock responses there. Browser tests intercept every `/api/sources/**` request with `page.route`, including dashboard studies. Keep these mocks when adding tests.
- **ICD-11** needs `ICD_CLIENT_ID` and `ICD_CLIENT_SECRET`. The WHO OAuth token is cached in process (`app/sources/icd11.py`); the test fixture resets it. Source responses are cached separately in the database for `SOURCE_CACHE_HOURS`.
- **Seed content** lives in `app/seed_data/<specialty>.py`, assembled in `app/seed_data/__init__.py`. `scripts/check_seed_sources.py` checks further-reading links and, when WHO credentials exist, ICD codes. All 44 bundled ICD codes were live-verified on 2026-10-12.
- **shadcn CLI** via `npx shadcn` fails under npm 12 (allow-scripts error). Run `./node_modules/.bin/shadcn add <component>` from `frontend/`. Generated components import `cn` from the `cn` package. `src/index.css` must keep `@import "shadcn/tailwind.css"`, which supplies the `data-open` and `data-horizontal` variants.
- Stack versions are newer than most training data: Vite 8, TypeScript 6 (no `baseUrl`, only `paths`), React Router 8 (`react-router`, `createBrowserRouter`), Tailwind v4 (tokens in `src/index.css`, no config file), `motion` (`motion/react`), oxlint instead of ESLint. Check the installed package's types before assuming an API.
- **Frontend test helpers** live in `src/test/utils.tsx`: `renderWithProviders` (memory router + QueryClient) and `mockFetch`, which answers by the *longest* matching URL substring. Give specific routes keys that are longer than the generic ones.
- **Language.** The frontend sends `Accept-Language`; the backend answers messages, ICD-11, search and AI in that language (`app/i18n.py`, English default). `renderWithProviders` defaults to `lang="de"` so older tests keep German strings; pass `lang: 'en'` to test English. e2e specs set `localStorage['medkb:lang']='de'` in an init script (`e2e/i18n.spec.ts` covers the English default). German AI cache keys are unchanged; English adds the language to the key. Drafts stay German.
- **Backend reload.** A uvicorn started before a backend change keeps serving old code; restart it. FastAPI serves `frontend/dist` (see `app/spa.py`), so after `npm run build` the whole app runs on :8000.
- **Auth in tests.** Backend: fixtures `client` (admin), `doctor_client`, `patient_client`, `anon_client` in `tests/conftest.py`; bcrypt runs with 4 rounds there. Frontend unit tests: `renderWithProviders(..., { user: TEST_USERS.patient })` (default admin; `withAuth: true` for the real provider). e2e: `loginAs(page, role)` in `e2e/smoke.spec.ts`.
- **New columns** on existing tables need an entry in `ADDED_COLUMNS` (`app/database.py`): `create_all` never alters tables.
- **Keyword search** matches the JSON text of the keyword column. Terms containing `"`, `[`, `]`, `,` or `\` skip that column (`JSON_SYNTAX` in `app/services.py`).
- **Line endings.** `.gitattributes` forces LF.
- **Local Python** is 3.11 in `.venv`, while the project targets 3.12+ (CI runs 3.12 and 3.13).
