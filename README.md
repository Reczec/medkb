# MedKB – Digital Medical Knowledge Base

A medical knowledge base organised like a colour-coded record room: 47 structured textbook
entries in 16 specialties, an explainable rule-based classifier, live data from PubMed, the WHO
ICD-11 API and openFDA, and AI assistance that stays grounded in the entries. Three roles
(admin, doctor, patient) see the same knowledge at different depths.

**Live demo: [medkb.onrender.com](https://medkb.onrender.com)** · one click per role, no sign-up.
The free hosting sleeps after 15 minutes without visitors; the first request then takes about
20–30 seconds (measured: 22 s), everything after that is instant.

> **Prototype with example data only – not a medical product and not medical advice.**
> The bundled entries are short, generic textbook-style texts. There is no patient data.

![Demo: doctor dashboard, entry with PubMed studies and ICD-11, AI summary; patient warning signs; AI assistant](docs/media/demo.gif)

FastAPI + SQLAlchemy (SQLite or PostgreSQL), React 19 + TypeScript (Vite, Tailwind CSS,
shadcn/ui, Motion, Recharts, TanStack Query). The UI is in English with a one-click switch to German (EN | DE), code and API in English.

## Background

This project re-implements my part of my diploma thesis at TGM Wien (HTL, Wirtschaftsingenieurwesen –
Betriebsinformatik, 2026). The thesis was a team project on AI-assisted systems in medicine; my chapter
covered a digital knowledge base with search, automatic classification and archiving. This
repository is a clean rebuild from the written specification of that chapter (requirements,
architecture, classification logic, archive function), with added tests, PostgreSQL support and
a CI setup. Built with AI assistance (Claude).

## Features

- **English and German**: the whole interface, all 47 entries, server messages, ICD-11 and AI
  answers follow the chosen language (English by default, remembered per browser). The rule-based
  classifier works on the German text, so German stays the canonical language of an entry; the
  English version is optional per entry and falls back field by field with a visible note
- **Structured entries**: sections (definition, symptoms, causes, diagnostics, therapy, warning
  signs), English term, ICD-11 code, active ingredients and checked further-reading links
  (gesundheit.gv.at, WHO, MedlinePlus); 47 example entries across 16 specialties
- **Live sources for staff**: newest PubMed articles per entry and per specialty, WHO ICD-11 title
  and definition, openFDA drug labels. Cached for 24 h; an unavailable source shows a retry, never
  an error page
- **Search**: multi-term keyword search over title, content and keywords in both languages
  (all terms must match), case-insensitive including umlauts, ranked by relevance (title > keywords > content),
  filters for category and document type, pagination
- **Automatic classification**: a transparent, rule-based scoring of German medical vocabulary
  suggests a category (e.g. HNO, Neurologie, Kardiologie) and keywords. The user always keeps
  control: a manually chosen category is never overwritten.
- **Archive**: admin-only export of all entries to a JSON file, list of archives, download,
  restore (an automatic "pre-restore" backup is created first)
- **Roles and login**: admin (everything), doctor (reads in professional depth, sees why an
  entry was classified), patient (reads, search-first start page, no internal data). JWT login;
  in demo mode one click per role on the login page, and the example data resets every 24 h
- **Traceability**: change log of create / update / delete / archive actions with who did it
  (admin-only)
- **Dashboard** with a 30-day activity chart, document types and the specialties as colour-coded
  filing tabs; command palette (Ctrl+K), animated transitions, light/dark theme, responsive down
  to phone width, `prefers-reduced-motion` respected
- **AI assistance**: simple explanations and warning signs for every role, professional entry
  and PubMed abstract summaries for staff, grounded questions with entry links, and admin-only
  drafts and category second opinions. Drafts require explicit review/apply/save. The thesis
  rule classifier remains separate. Persistent content-aware cache and atomic daily quotas.

| Dashboard (doctor) | Entry with classification | PubMed studies (dark) | Patient start (phone) |
|---|---|---|---|
| ![](docs/media/dashboard-light.png) | ![](docs/media/entry-light.png) | ![](docs/media/studies-dark.png) | ![](docs/media/patient-phone.png) |

## Architecture

```mermaid
flowchart LR
    UI["React UI<br/>TypeScript / Vite"] -- "REST /api (JSON, SSE)" --> API["FastAPI app<br/>roles via JWT"]
    API --> SVC["services: CRUD, search, stats, audit"]
    API --> CLS["classifier: rules + scoring"]
    API --> ARC["archive: JSON export / restore"]
    API --> SRC["sources: PubMed, WHO ICD-11, openFDA"]
    API --> AI["AI: grounded prompts, cache, quotas"]
    SRC -- "24 h cache" --> DB
    AI -- "cache + daily quotas" --> DB
    SVC --> DB[("PostgreSQL (Neon) or SQLite<br/>SQLAlchemy 2")]
    AI --> LLM["OpenAI-compatible model<br/>(default: Gemini)"]
    ARC --> FS[("archives/*.json")]
```

Hosting: one Docker web service on Render (free) serves the API and the built UI; the database is
Neon Postgres (free). See [Deployment](#deployment).

```
app/
  main.py          FastAPI app, startup
  spa.py           serves the built frontend with a fallback to index.html
  auth.py, users.py  password hashing, JWT, role checks; demo and admin accounts
  demo.py          periodic reset of the example data in demo mode
  routers/         auth.py (login), documents.py, admin.py (archives, audit), users.py
  services.py      CRUD, search with relevance ranking, statistics, audit log
  classifier.py    rule-based classification and keyword extraction
  archive.py       JSON export / list / restore
  models.py, schemas.py, database.py, config.py, content.py (sections → full text)
  seed.py, seed_data/     example entries, one module per specialty
  sources/         PubMed, WHO ICD-11, openFDA clients and their cache
  ai/              compatible provider, prompts, cache/quotas, validated execution, prewarm CLI
frontend/
  src/features/    dashboard, documents (list, detail, source panels), editor, ai, admin, auth
  src/components/  layout (shell, command palette), specialty (filing tabs, score bars), ui (shadcn)
  src/lib/         API client, query hooks, types, helpers
  e2e/             Playwright smoke tests
tests/             pytest suite (classifier, document API, admin API, SPA serving)
```

## Quick start

Requires Python 3.12+ and Node.js 22+.

**Backend** (Windows PowerShell; on macOS/Linux use `source .venv/bin/activate` and `cp`)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload
```

**Frontend**, in a second terminal
```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173> (Vite forwards `/api` to the backend). Interactive API docs are at
<http://localhost:8000/docs>. For a production-like run, `npm run build` once; FastAPI then serves
the built UI itself at <http://localhost:8000>.
With the default `.env` (demo mode), the login page offers one-click access as admin, doctor or
patient, and the example entries are restored on every start. Set `ADMIN_PASSWORD` for a real
`admin` login.

> **Demo mode deletes all entries and the change log on every start** (and every
> `DEMO_RESET_HOURS`). Keep `DEMO_MODE=false` for data you want to keep; Docker Compose defaults to
> `false`.

### Docker (PostgreSQL)

```bash
cp .env.example .env      # set JWT_SECRET
docker compose up --build
```

## Configuration: external sources

The doctor and admin views show PubMed studies, WHO ICD-11 and openFDA drug labels. PubMed
and openFDA work without credentials. An optional `NCBI_API_KEY` increases PubMed's request
limit. Patients see the entry content and warning signs without requesting these sources.

For ICD-11, register at [WHO ICD API](https://icd.who.int/icdapi), open **View API access key(s)**
and put `ICD_CLIENT_ID` and `ICD_CLIENT_SECRET` in `.env`. Without them the tab reports that
ICD-11 is not configured. ICD-11 follows the interface language (`Accept-Language`); the
German response is marked as a WHO prerelease. `ICD_LANGUAGE` (default `de`) is only the
fallback for clients that send no language, and `ICD_RELEASE` defaults to `2026-01`.

`SOURCES_TIMEOUT=8` sets the upstream request timeout in seconds; `SOURCE_CACHE_HOURS=24`
sets the database cache lifetime. The panels show their source and retrieval time, and offer
a retry if a source is unavailable. FDA labels are English US product information and are
explicitly marked as unsuitable for dosage decisions.

Run `python scripts/check_seed_sources.py` to check the bundled further-reading links and,
with WHO credentials configured, the ICD codes. Last run (2026-10-12): all 69 links answer and
all 44 codes resolve to the matching WHO title. See [.env.example](.env.example) for all source
variables.

## Configuration: AI assistance

Set `AI_API_KEY` in your local/server environment and restart the backend. The default is
`AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/` and
`AI_MODEL=gemini-3.5-flash-lite`. The endpoint follows Google's
[OpenAI compatibility documentation](https://ai.google.dev/gemini-api/docs/openai).
The model is configurable; the older 2.5 Flash is restricted for new projects according to
its [model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash).
The [pricing page](https://ai.google.dev/gemini-api/docs/pricing) lists a free tier for the
default model, subject to availability and provider quotas. Free-tier content may be used
to improve Google's products. Send example data only. The tests never call a real model; all
seven features were checked live against Gemini on 2026-10-12.

Other compatible providers can replace the base URL/key/model, for example
[Groq's compatibility endpoint](https://console.groq.com/docs/openai). Choose a model that
the account currently supports. Without a key, requests return `503 ai_not_configured` and
the UI explains that setup is pending. There are no fabricated offline AI responses.

`AI_TIMEOUT=30` is the upstream timeout in seconds (maximum 120).
`AI_DAILY_LIMIT=500` and `AI_CLIENT_DAILY_LIMIT=30` limit uncached calls per UTC day.
A begun failed call still consumes its reservation. Cache hits are free of these quotas;
429 includes `Retry-After` until UTC midnight. An HMAC of the client IP is stored, salted
with `JWT_SECRET`; set a stable secret. Behind a reverse proxy set `CLIENT_IP_HEADER` to the
header the proxy itself writes (for example `True-Client-IP`); the Docker image ignores
`X-Forwarded-For`, which visitors could fake.

Cached successful document results bind to content, role, provider, model and prompt version,
and survive unchanged demo resets, including PostgreSQL ID changes. Seed identity uses canonical source/title plus semantic content; snapshots exclude IDs and timestamps. Questions and admin opinions/drafts are uncached.
Prompt changes require bumping `PROMPT_VERSION` in `app/ai/store.py`. Errors and interrupted
streams are never successful cache entries. Streamed tokens are provisional; only `done`
contains the validated final result. `ask` uses the existing keyword search's top five
entries, validates source indices, and accepts six bounded previous messages. German question words are removed; generic follow-ups reuse the previous user topic. Try short
topics such as “Migräne”; this is keyword retrieval, not semantic search. Source-index
validation and prompts do not certify factual correctness or clinical safety.

Optional explicit cache warmup (never automatic on startup):

```powershell
.venv/Scripts/python.exe -m app.ai.prewarm --limit 1
# Omit --limit for all entries: 47 × 8 role/feature variants = 376 potential calls.
.venv/Scripts/python.exe -m app.ai.prewarm --lang en --pause 4   # the English answers (376 more)
```

The AI answers in the interface language (English default); German and English answers are cached
separately, and drafts are always written in German because the classifier works on German text.
The trusted operator job uses the global budget, while public clients keep their separate
30-call limit. Repeated warmup reuses cached results; failures are counted in its summary.
Without a key it exits without requests. Run after example seeding; respect provider rate limits.

## Deployment

The repository contains a Render Blueprint ([render.yaml](render.yaml)): one free Docker web
service in Frankfurt, health check `/api/health`, demo mode with a reset every 3 hours.

1. **Database:** create a free project on [Neon](https://neon.com) (region Frankfurt) and copy
   its connection string.
2. **Service:** in [Render](https://render.com) choose *New → Blueprint* and connect this
   repository. Render asks for the secrets once: `DATABASE_URL` (the Neon string), `AI_API_KEY`
   and optionally `ICD_CLIENT_ID`, `ICD_CLIENT_SECRET`, `NCBI_API_KEY`. `JWT_SECRET` is generated.
   Enter `True-Client-IP` for `CLIENT_IP_HEADER`, then confirm on the live service that a
   client-sent value is overwritten: repeated AI requests with `-H 'True-Client-IP: 1.2.3.4'`
   must keep counting against your own visitor quota. Left empty, all visitors share one AI
   quota (the server logs a warning). Never use `X-Forwarded-For`: its first entry is
   client-controlled.
3. Every push to `main` deploys again.

Free-tier behaviour: the service sleeps after 15 minutes without requests and needs about 20–30
seconds to wake (measured 22 s on 2026-10-12, including the demo reset); Neon pauses after 5 minutes and wakes in seconds. The filesystem is not
persistent, so archives live only until the next restart. Hashed assets are cached for a year,
the HTML shell never; every response carries basic security headers.

## API overview

| Method | Path | Who | Description |
|---|---|---|---|
| POST | `/api/auth/login` | everyone | Username + password → JWT |
| POST | `/api/auth/demo` | everyone (demo mode) | `{role}` → JWT for the demo account of that role |
| GET | `/api/auth/me`, `/api/auth/options` | logged in / everyone | Current user; whether demo mode is on |
| GET | `/api/documents` | logged in | Search/list: `q`, `category`, `doc_type`, `limit`, `offset` |
| GET | `/api/documents/{id}`, `/api/stats`, `/api/meta` | logged in | Entry; dashboard numbers; categories and types |
| POST | `/api/classify` | doctor, admin | Preview category and keywords without saving |
| POST | `/api/documents` | admin | Create (category/keywords are suggested automatically if omitted) |
| PATCH / DELETE | `/api/documents/{id}` | admin | Partial update (`reclassify: true` re-runs the classifier), delete |
| POST / GET | `/api/archives` | admin | Create an archive / list archives |
| GET | `/api/archives/{name}` | admin | Download an archive |
| POST | `/api/archives/{name}/restore` | admin | Replace all entries with an archive |
| GET | `/api/audit`, `/api/users` | admin | Change log; login accounts |
| POST | `/api/ai/documents/{id}/explain`, `/red-flags` | logged in | Simple explanation / general warning signs |
| POST | `/api/ai/documents/{id}/summary` | doctor, admin | Professional summary |
| POST | `/api/ai/studies/summarize` | doctor, admin | `{pmid}` → summary of the actual NCBI abstract |
| POST | `/api/ai/ask` | logged in | `{question, history?}` → grounded answer and entry references |
| POST | `/api/ai/draft`, `/api/ai/classify` | admin | Validated draft / separate category opinion, no save |
| GET | `/api/ai/usage` | doctor, admin | Global UTC-day reservations and configured limit |

AI results contain `{text, cached, citations, draft?, classification?}`. Explain, summary,
ask and draft accept `?stream=true`: SSE `token` carries `{text}`, `done` carries the complete
result, and `error` carries `{code,message}`. Red flags, classification and studies return JSON.

Send the token as `Authorization: Bearer <token>`. Missing or expired token → 401, wrong role → 403.

## How the classification works

1. Each category has a vocabulary of word stems with a weight (1 = general, 2 = specific).
   Stems are matched inside words, so compounds like *Rückenschmerzen* are found; a leading
   `^` restricts a stem to the start of a word (avoids "Drachen" → *rachen*).
2. Score per category = Σ weight × hits. Hits are the occurrences in the content (capped at 3,
   so repetition cannot dominate) plus a bonus if the stem appears in the title.
3. The highest score wins; ties go to the more specific category. Below a minimum score the
   entry falls back to *Allgemeinmedizin*.
4. Keywords are the actual words from the text that triggered a rule, topped up with frequent nouns.

`POST /api/classify` returns the scores and matched terms, so every suggestion is explainable.

## Tests

```bash
pytest                      # in-memory SQLite
TEST_DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/medkb_test pytest   # PostgreSQL
ruff check . && ruff format --check .

cd frontend
npm run lint && npm run typecheck && npm test          # oxlint, TypeScript, Vitest
npm run build && npx playwright install chromium
PYTHON=../.venv/bin/python npm run e2e                 # Playwright against the real stack
```

The backend tests cover the classifier, CRUD and validation, search (AND semantics, umlauts, ranking,
wildcard escaping, pagination), statistics, admin authentication, archive export/restore
(including corrupt files and path traversal), the audit log, the activity series and serving the
frontend. The suite passes on SQLite and on PostgreSQL 16. Frontend unit tests (Vitest + Testing
Library) cover the API client, helpers and every page; Playwright smoke tests run search, editing
with live classification, archiving and phone-width layout against FastAPI with a seeded database.
Source clients are tested against recorded responses (no network in tests), AI features with a
fake provider. The workflow in `.github/workflows/ci.yml` runs all of it, builds the Docker image,
starts it like Render does and checks health, UI and demo login.

The README media come from a scripted tour against a running instance with real sources and AI:
`cd frontend && node scripts/record-demo.mjs` (needs ffmpeg; writes `docs/media/`).

## Limitations and possible next steps

- **The classifier is rule-based, not machine learning.** It does not understand context or
  negation ("kein Fieber"). The example entries were written together with the vocabulary, so
  their 47/47 result is a regression test, not an accuracy measurement. A real evaluation would
  need a labelled, independent test set.
- **Search is substring matching**, not PostgreSQL full-text or semantic search. That is fine
  for a prototype; for large data sets use full-text indexes (`tsvector`) or embeddings.
- **Simple accounts.** Roles are enforced on every endpoint, but there is no registration,
  password reset or rate limiting on login; demo accounts exist for the public demo.
- **Existing databases are upgraded by a small built-in step** (`upgrade_schema`), not Alembic.
- **Tables are created with `create_all`**; production use would add migrations (Alembic).
- **Restoring an archive replaces all entries and assigns new ids.**
- No patient data should ever be entered: the app has no encryption at rest, no access
  control for entries and no data-protection (GDPR) measures beyond what is listed here.

Ideas: full-text/semantic search, a trained classifier evaluated on labelled data,
user roles, versioning of single entries, import of archives into an empty database via CLI.

## License

MIT – see [LICENSE](LICENSE).
