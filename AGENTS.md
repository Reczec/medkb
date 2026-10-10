# MedKB – agent guide

MedKB is a medical knowledge base (FastAPI + React) being grown from a diploma-thesis prototype into a public CV demo. Read before working:

- **Product truth** (users, roles, principles): [PRODUCT.md](PRODUCT.md)
- **Visual system** (tokens, filing-tab signature, rules): [DESIGN.md](DESIGN.md). Read it before any UI change.
- **v2 spec** (the whole target, 5 stages): [docs/superpowers/specs/2026-10-10-medkb-v2-design.md](docs/superpowers/specs/2026-10-10-medkb-v2-design.md)
- **Open follow-ups** from the stage 1 reviews: [docs/BACKLOG.md](docs/BACKLOG.md)

## Status

| Stage (spec §12) | State |
|---|---|
| 1 React frontend, redesign, dashboard | done, merged into `main` ([plan](docs/superpowers/plans/2026-10-10-etappe-1-frontend-redesign.md)) |
| 2 Roles and auth (admin / doctor / patient, demo login, demo reset) | done ([plan](docs/superpowers/plans/2026-10-10-etappe-2-rollen-auth.md)) |
| 3 Data model, ~45 realistic entries, PubMed / WHO ICD-11 / openFDA | next |
| 4 AI features (free OpenAI-compatible provider, cache, rate limit) | open |
| 5 Deployment (Render + Neon), README, demo GIF | open |

Continue a stage by writing its plan next to the stage 1 plan (same structure: file map, tasks with failing test first, commit per task), then implement it task by task.

## Working rules

- UI text German, code and API English.
- Test first: a failing test, then the change, then the whole suite. Every task ends green on `pytest`, `ruff check . && ruff format --check .`, and in `frontend/`: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run e2e`.
- One commit per task.
- The rule-based classifier is the thesis core: keep it, keep it explainable. Its UI marker is "regelbasiert"; AI features (stage 4) get their own clearly separate marker.
- Every view keeps the notice "Prototyp mit Beispieldaten – keine medizinische Beratung." There is no patient data, ever.

## Gotchas (not visible from config)

- **e2e** needs a fresh `npm run build`, and `PYTHON` pointing at the venv's Python (Windows: `PYTHON=../.venv/Scripts/python.exe npm run e2e`). Playwright starts its own uvicorn on port 8765 with a throwaway seeded SQLite DB.
- **shadcn CLI** via `npx shadcn` fails under npm 12 (allow-scripts error). Run `./node_modules/.bin/shadcn add <component>` from `frontend/`. Generated components import `cn` from the `cn` package. `src/index.css` must keep `@import "shadcn/tailwind.css"`, which supplies the `data-open` and `data-horizontal` variants.
- Stack versions are newer than most training data: Vite 8, TypeScript 6 (no `baseUrl`, only `paths`), React Router 8 (`react-router`, `createBrowserRouter`), Tailwind v4 (tokens in `src/index.css`, no config file), `motion` (`motion/react`), oxlint instead of ESLint. Check the installed package's types before assuming an API.
- **Frontend test helpers** live in `src/test/utils.tsx`: `renderWithProviders` (memory router + QueryClient) and `mockFetch`, which answers by the *longest* matching URL substring. Give specific routes keys that are longer than the generic ones.
- **Backend reload.** A uvicorn started before a backend change keeps serving old code; restart it. FastAPI serves `frontend/dist` (see `app/spa.py`), so after `npm run build` the whole app runs on :8000.
- **Auth in tests.** Backend: fixtures `client` (admin), `doctor_client`, `patient_client`, `anon_client` in `tests/conftest.py`; bcrypt runs with 4 rounds there. Frontend unit tests: `renderWithProviders(..., { user: TEST_USERS.patient })` (default admin; `withAuth: true` for the real provider). e2e: `loginAs(page, role)` in `e2e/smoke.spec.ts`.
- **New columns** on existing tables need an entry in `ADDED_COLUMNS` (`app/database.py`): `create_all` never alters tables.
- **Keyword search** matches the JSON text of the keyword column. Terms containing `"`, `[`, `]`, `,` or `\` skip that column (`JSON_SYNTAX` in `app/services.py`).
- **Line endings.** `.gitattributes` forces LF.
- **Local Python** is 3.11 in `.venv`, while the project targets 3.12+ (CI runs 3.12 and 3.13).
