# MedKB – Digital Medical Knowledge Base

A small web application for storing, classifying, searching and archiving medical knowledge
entries (symptoms, diagnoses, descriptions, …). Python/FastAPI backend, SQLite or PostgreSQL,
plain HTML/CSS/JS frontend. The UI is in German, the code and API are in English.

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
- **Traceability**: change log of create / update / delete / archive actions (admin-only)
- **Dashboard** with entry counts per category; responsive, light/dark UI

| Search & dashboard | Classification suggestion | Admin: archives & change log |
|---|---|---|
| ![](docs/screenshots/search.png) | ![](docs/screenshots/editor-classification.png) | ![](docs/screenshots/admin-archive.png) |

## Architecture

```mermaid
flowchart LR
    UI["Browser UI<br/>HTML / CSS / JS"] -- "REST /api (JSON)" --> API["FastAPI app"]
    API --> SVC["services: CRUD, search, stats, audit"]
    API --> CLS["classifier: rules + scoring"]
    API --> ARC["archive: JSON export / restore"]
    SVC --> DB[("SQLite or PostgreSQL<br/>SQLAlchemy 2")]
    ARC --> DB
    ARC --> FS[("archives/*.json")]
```

```
app/
  main.py          FastAPI app, startup, static UI
  routers/         documents.py (public API), admin.py (archives, audit; token-protected)
  services.py      CRUD, search with relevance ranking, statistics, audit log
  classifier.py    rule-based classification and keyword extraction
  archive.py       JSON export / list / restore
  models.py, schemas.py, database.py, config.py, security.py
  seed.py, seed_data.py   example entries
  static/          index.html, style.css, app.js
tests/             pytest suite (classifier, document API, admin API)
```

## Quick start

Requires Python 3.12+.

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload
```

**macOS / Linux**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open <http://localhost:8000>. Interactive API docs are at <http://localhost:8000/docs>.
With the default `.env`, the example entries are inserted on first start and the admin
token is `change-me` (change it in `.env`).

### Docker (PostgreSQL)

```bash
cp .env.example .env      # set ADMIN_TOKEN
docker compose up --build
```

## API overview

| Method | Path | Description |
|---|---|---|
| GET | `/api/documents` | Search/list: `q`, `category`, `doc_type`, `limit`, `offset` |
| POST | `/api/documents` | Create (category/keywords are suggested automatically if omitted) |
| GET / PATCH / DELETE | `/api/documents/{id}` | Read, partial update (`reclassify: true` re-runs the classifier), delete |
| POST | `/api/classify` | Preview category and keywords without saving |
| GET | `/api/stats`, `/api/meta` | Dashboard numbers; categories and document types |
| POST / GET | `/api/archives` | *Admin.* Create an archive / list archives |
| GET | `/api/archives/{name}` | *Admin.* Download an archive |
| POST | `/api/archives/{name}/restore` | *Admin.* Replace all entries with an archive |
| GET | `/api/audit` | *Admin.* Change log |

Admin endpoints need the header `X-Admin-Token: <ADMIN_TOKEN>`.

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
```

74 tests cover the classifier, CRUD and validation, search (AND semantics, umlauts, ranking,
wildcard escaping, pagination), statistics, admin authentication, archive export/restore
(including corrupt files and path traversal) and the audit log. The suite passes on SQLite
and on PostgreSQL 16. The workflow in `.github/workflows/ci.yml` runs lint and tests on both.

## Limitations and possible next steps

- **The classifier is rule-based, not machine learning.** It does not understand context or
  negation ("kein Fieber"). The example entries were written together with the vocabulary, so
  their 16/16 result is a regression test, not an accuracy measurement. A real evaluation would
  need a labelled, independent test set.
- **Search is substring matching**, not PostgreSQL full-text or semantic search. That is fine
  for a prototype; for large data sets use full-text indexes (`tsvector`) or embeddings.
- **No user accounts.** Reading and editing entries is open; only the admin area is protected
  by a shared token. A real deployment needs authentication and role-based access.
- **Tables are created with `create_all`**; production use would add migrations (Alembic).
- **Restoring an archive replaces all entries and assigns new ids.**
- No patient data should ever be entered: the app has no encryption at rest, no access
  control for entries and no data-protection (GDPR) measures beyond what is listed here.

Ideas: full-text/semantic search, a trained classifier evaluated on labelled data,
user roles, versioning of single entries, import of archives into an empty database via CLI.

## License

MIT – see [LICENSE](LICENSE).
