# MedKB – Digital Medical Knowledge Base

A small web application for storing, classifying, searching and archiving medical knowledge
entries (symptoms, diagnoses, descriptions, …). Python/FastAPI backend, SQLite or PostgreSQL,
React + TypeScript frontend (Vite, Tailwind CSS, shadcn/ui, Motion, Recharts). The UI is in German,
the code and API are in English.

> **Prototype with example data only – not a medical product and not medical advice.**
> The bundled entries are short, generic textbook-style texts. There is no patient data.

![Search and dashboard](docs/screenshots/search.png)

## Background

This project re-implements my part of my diploma thesis at TGM Wien (HTL, Wirtschaftsingenieurwesen –
Betriebsinformatik, 2026). The thesis was a team project on AI-assisted systems in medicine; my chapter
covered a digital knowledge base with search, automatic classification and archiving. This
repository is a clean rebuild from the written specification of that chapter (requirements,
architecture, classification logic, archive function), with added tests, PostgreSQL support and
a CI setup. Built with AI assistance (Claude).

## Features

- **Structured entries**: title, content, category, document type, keywords, source, timestamps
- **Search**: multi-term keyword search over title, content and keywords (all terms must match),
  case-insensitive including umlauts, ranked by relevance (title > keywords > content),
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

| Search & dashboard | Classification suggestion | Admin: archives & change log |
|---|---|---|
| ![](docs/screenshots/search.png) | ![](docs/screenshots/editor-classification.png) | ![](docs/screenshots/admin-archive.png) |

## Architecture

```mermaid
flowchart LR
    UI["React UI<br/>TypeScript / Vite"] -- "REST /api (JSON)" --> API["FastAPI app"]
    API --> SVC["services: CRUD, search, stats, audit"]
    API --> CLS["classifier: rules + scoring"]
    API --> ARC["archive: JSON export / restore"]
    SVC --> DB[("SQLite or PostgreSQL<br/>SQLAlchemy 2")]
    ARC --> DB
    ARC --> FS[("archives/*.json")]
```

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
  models.py, schemas.py, database.py, config.py, security.py
  seed.py, seed_data.py   example entries
frontend/
  src/features/    dashboard, documents (list, detail), editor, admin
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
ICD-11 is not configured. The defaults are `ICD_RELEASE=2026-01` and `ICD_LANGUAGE=de`;
the German response is marked as a WHO prerelease. Use `en` for English.

`SOURCES_TIMEOUT=8` sets the upstream request timeout in seconds; `SOURCE_CACHE_HOURS=24`
sets the database cache lifetime. The panels show their source and retrieval time, and offer
a retry if a source is unavailable. FDA labels are English US product information and are
explicitly marked as unsuitable for dosage decisions.

Run `python scripts/check_seed_sources.py` to check the bundled further-reading links and,
with WHO credentials configured, ICD codes. The codes require that live verification before
their source mapping can be considered confirmed. See [.env.example](.env.example) for all
source variables.

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
The workflow in `.github/workflows/ci.yml` runs all of it plus a Docker build.

## Limitations and possible next steps

- **The classifier is rule-based, not machine learning.** It does not understand context or
  negation ("kein Fieber"). The example entries were written together with the vocabulary, so
  their 16/16 result is a regression test, not an accuracy measurement. A real evaluation would
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
