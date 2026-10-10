# Etappe 1 – React-Frontend, Redesign und Dashboard – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das alte Vanilla-JS-UI durch ein animiertes React-Frontend mit neuem Dashboard ersetzen, das alle bestehenden Funktionen (Suche, Detail, Editor mit Live-Klassifikation, Archiv, Audit) abdeckt und von FastAPI ausgeliefert wird.

**Architecture:** Neues Verzeichnis `frontend/` (Vite + React + TS). Im Dev-Modus proxyt Vite `/api` auf uvicorn :8000. In Produktion baut ein Multi-Stage-Dockerfile das Frontend; FastAPI liefert `frontend/dist` mit SPA-Fallback aus. Backend-Änderungen beschränken sich auf `GET /api/stats` (Aktivitätsverlauf) und das Ausliefern der SPA. Auth bleibt in dieser Etappe beim `X-Admin-Token` (Etappe 2 ersetzt es).

**Nicht in Etappe 1** (kommt später laut Spec): Patienten-Startseite und Admin-Aktivitäts-Feed auf dem Dashboard (Etappe 2, braucht Rollen), Kachel „Neueste Studien" und weitere Detail-Tabs (Etappe 3), KPI „KI-Anfragen heute" (Etappe 4).

**Tech Stack:** React 19, TypeScript 5, Vite (aktuelle stabile Version via `create-vite`), Tailwind CSS v4 (`@tailwindcss/vite`), shadcn/ui (Radix), `motion` (Framer Motion, Import `motion/react`), Recharts, TanStack Query v5, React Router v7, `cmdk`, `sonner`, `@fontsource-variable/inter`, Vitest + Testing Library, Playwright, ESLint (flat config). Backend: FastAPI, SQLAlchemy 2, pytest.

**Spec:** `docs/superpowers/specs/2026-10-10-medkb-v2-design.md` (Abschnitte 2, 8, 9, 10, 12 – Etappe 1)

## Global Constraints

- UI-Texte Deutsch, Code/Bezeichner/API Englisch.
- Kein `innerHTML`/`dangerouslySetInnerHTML` mit Nutzerinhalten.
- Design: heller Standard, Off-White-Flächen, Akzent Teal/Petrol, eine Farbe pro Fachgebiet, Dark Mode; Schrift Inter, tabellarische Ziffern für Zahlen.
- Motion: Seitenübergänge, gestaffelte Listen mit Layout-Animation beim Filtern, hochzählende KPIs, einzeichnende Charts, animierte Popover/Dialoge, Live-Score-Balken im Editor; `prefers-reduced-motion` wird respektiert (Motion aus bzw. auf Opacity reduziert).
- Responsive bis 375 px Breite, kein horizontales Scrollen der Seite.
- Hinweis „Prototyp mit Beispieldaten – keine medizinische Beratung." bleibt sichtbar (Topbar oder Footer).
- Python ≥ 3.12, Node ≥ 20. Ruff-Regeln wie in `pyproject.toml`; alle bestehenden 74 Tests bleiben grün.
- UI-Arbeit (Tasks 4–9): vor dem Bauen den `impeccable`-Skill laden und die Designrichtung oben als Brief verwenden.

## Review Focus

1. Suchbegriffe mit Sonderzeichen (`%`, `_`, `"`, Umlaute) oder ohne Treffer → leerer Zustand mit Text „Keine Einträge gefunden", kein Fehler. (Task 6)
2. Backend nicht erreichbar oder 5xx → Fehlerkarte mit „Erneut versuchen" statt leerer Seite; Toast mit lesbarer Meldung aus `detail`. (Tasks 3, 5)
3. Falsches/fehlendes Admin-Token → klare Meldung „Admin-Token ungültig", Token-Eingabe bleibt offen; ein gespeichertes falsches Token wird verworfen. (Task 9)
4. Reload auf einer Deep-Link-Route wie `/wissen/12` in Produktion → SPA lädt; unbekannte `/api/...`-Pfade liefern weiterhin JSON-404, nicht `index.html`. (Task 10)
5. Sehr lange Titel/Inhalte und 20 Schlagwörter bei 375 px → Text bricht um bzw. wird gekürzt, nichts läuft aus der Karte. (Task 6, Playwright in Task 10)

---

## File Structure

```
app/
  services.py          (mod) get_stats: + activity
  schemas.py           (mod) DayCount, StatsOut.activity
  spa.py               (neu) mount_frontend(app, dist_dir)
  main.py              (mod) nutzt mount_frontend statt StaticFiles(app/static)
  static/              (entfernt in Task 10)
tests/
  test_stats_activity.py (neu)
  test_spa.py            (neu)
frontend/
  package.json, vite.config.ts, tsconfig.json, tsconfig.app.json, tsconfig.node.json,
  eslint.config.js, index.html, components.json, playwright.config.ts
  src/main.tsx                 Providers (QueryClient, Router, Theme, Toaster)
  src/App.tsx                  Routen
  src/index.css                Tailwind + Design-Tokens (CSS-Variablen hell/dunkel)
  src/lib/api.ts               fetch-Wrapper, ApiError, errorMessage()
  src/lib/types.ts             TS-Typen zu den Pydantic-Schemas
  src/lib/queries.ts           TanStack-Query-Hooks
  src/lib/categories.ts        Farbe + Icon pro Fachgebiet
  src/lib/format.ts            Datum/Zahl (de-AT)
  src/lib/scores.ts            toScoreBars()
  src/lib/utils.ts             cn() (shadcn)
  src/hooks/useDebounced.ts
  src/hooks/useReducedMotion.ts (Re-Export von motion)
  src/components/ui/*          shadcn-Komponenten (generiert)
  src/components/layout/AppShell.tsx, Sidebar.tsx, Topbar.tsx, ThemeToggle.tsx,
                        CommandPalette.tsx, PageTransition.tsx
  src/components/feedback/ErrorState.tsx, EmptyState.tsx
  src/components/motion/CountUp.tsx
  src/features/dashboard/DashboardPage.tsx, KpiCard.tsx, CategoryDonut.tsx,
                          DocTypeBars.tsx, ActivityChart.tsx, RecentList.tsx
  src/features/documents/KnowledgeBasePage.tsx, SearchFilters.tsx, DocumentCard.tsx,
                          DocumentPage.tsx, ClassificationExplainer.tsx
  src/features/editor/EditorPage.tsx, ScoreBars.tsx, KeywordInput.tsx
  src/features/admin/AdminPage.tsx, AdminTokenGate.tsx, ArchivesPanel.tsx, AuditTable.tsx
  src/**/*.test.ts(x)          Vitest
  e2e/smoke.spec.ts            Playwright
Dockerfile                     (mod) Multi-Stage
.github/workflows/ci.yml       (mod) + Frontend-Job
.gitignore / .dockerignore     (mod) node_modules, frontend/dist, playwright-report
```

Routen: `/` Dashboard · `/wissen` Liste · `/wissen/neu` Editor · `/wissen/:id` Detail · `/wissen/:id/bearbeiten` Editor · `/admin` Admin · `*` 404-Seite.

---

### Task 1: Aktivitätsverlauf in `/api/stats`

**Files:**
- Modify: `app/schemas.py` (StatsOut), `app/services.py` (get_stats)
- Test: `tests/test_stats_activity.py`

**Interfaces:**
- Produces: `StatsOut.activity: list[DayCount]`, `DayCount(date: datetime.date, count: int)`. JSON: `"activity": [{"date": "2026-10-10", "count": 2}, ...]` – genau 30 Einträge, ältester zuerst, letzter = heute (UTC), Tage ohne Änderungen mit `count: 0`. Gezählt werden alle `AuditLog`-Zeilen (create/update/delete/archive/restore).

- [ ] **Step 1: Failing tests schreiben**

```python
from datetime import UTC, datetime, timedelta
from tests.conftest import make_doc

def test_activity_has_30_days_oldest_first_ending_today(client):
    activity = client.get("/api/stats").json()["activity"]
    assert len(activity) == 30
    today = datetime.now(UTC).date()
    assert activity[-1]["date"] == today.isoformat()
    assert activity[0]["date"] == (today - timedelta(days=29)).isoformat()
    assert all(day["count"] == 0 for day in activity)

def test_activity_counts_audit_entries_of_today(client):
    doc = make_doc(client)
    client.patch(f"/api/documents/{doc['id']}", json={"title": "Neuer Titel"})
    assert client.get("/api/stats").json()["activity"][-1]["count"] == 2

def test_activity_ignores_entries_older_than_30_days(client, db_session):
    db_session.add(AuditLog(action="create", detail="alt",
                            timestamp=datetime.now(UTC) - timedelta(days=31)))
    db_session.commit()
    assert sum(d["count"] for d in client.get("/api/stats").json()["activity"]) == 0
```

Dafür eine Fixture `db_session` in `tests/conftest.py` ergänzen (`with SessionLocal() as s: yield s`).

- [ ] **Step 2: Laufen lassen, FAIL erwarten**

Run: `pytest tests/test_stats_activity.py -v` → FAIL (`KeyError: 'activity'`)

- [ ] **Step 3: Implementieren**

`DayCount` in `schemas.py`; in `get_stats` die AuditLog-Zeilen ab `today-29` laden (nur `timestamp`-Spalte) und in Python pro UTC-Datum zählen (DB-unabhängig, funktioniert auf SQLite und PostgreSQL; naive Timestamps aus SQLite als UTC behandeln, `_as_utc` wiederverwenden).

- [ ] **Step 4: Alle Tests laufen lassen**

Run: `pytest` → 77 passed. `ruff check . && ruff format --check .` → sauber.

- [ ] **Step 5: Commit** — `feat(api): add 30-day activity series to /api/stats`

---

### Task 2: Frontend-Grundgerüst

**Files:**
- Create: `frontend/` (Vite-Template `react-ts`), `frontend/vite.config.ts`, `frontend/src/index.css`, `frontend/components.json`, `frontend/src/lib/utils.ts`, `frontend/eslint.config.js`
- Modify: `.gitignore`, `.dockerignore`

**Interfaces:**
- Produces: `npm run dev` (Port 5173, Proxy `/api` → `http://127.0.0.1:8000`), `npm run build` (→ `frontend/dist`), `npm run lint`, `npm run typecheck` (`tsc -b --noEmit`), `npm test` (`vitest run`), `npm run e2e` (`playwright test`). Pfad-Alias `@/` → `src/`. Design-Tokens als CSS-Variablen in `index.css`: `--background, --foreground, --card, --muted, --border, --primary (Teal), --primary-foreground, --ring, --radius` jeweils für `:root` und `.dark`.

- [ ] **Step 1:** `npm create vite@latest frontend -- --template react-ts`, dann Abhängigkeiten installieren: `tailwindcss @tailwindcss/vite motion recharts @tanstack/react-query react-router cmdk sonner lucide-react @fontsource-variable/inter clsx tailwind-merge` und dev: `vitest @testing-library/react @testing-library/jest-dom jsdom @playwright/test`.
- [ ] **Step 2:** `npx shadcn@latest init` (Stil „new-york", Basisfarbe neutral, CSS-Variablen an), danach `npx shadcn@latest add button card badge input textarea select dialog alert-dialog dropdown-menu tabs tooltip skeleton command sheet separator table scroll-area popover`.
- [ ] **Step 3:** Tokens in `index.css` auf die Designrichtung setzen (Off-White `oklch(0.985 0.003 200)`-Bereich, Primary Teal ~`oklch(0.55 0.11 195)`), Inter als `--font-sans`, `font-variant-numeric: tabular-nums` als Utility `.tabular`.
- [ ] **Step 4:** Vitest in `vite.config.ts` konfigurieren (`environment: "jsdom"`, `setupFiles` mit jest-dom). Ein Platzhalter-Test `src/lib/utils.test.ts` prüft `cn("a", false && "b", "c") === "a c"`.
- [ ] **Step 5: Verifizieren** — `npm run lint && npm run typecheck && npm test && npm run build` → alles grün, `frontend/dist/index.html` existiert.
- [ ] **Step 6:** `.gitignore`/`.dockerignore` um `frontend/node_modules/`, `frontend/dist/`, `frontend/playwright-report/`, `frontend/test-results/` ergänzen.
- [ ] **Step 7: Commit** — `feat(frontend): scaffold Vite React TS app with Tailwind and shadcn/ui`

---

### Task 3: API-Client, Typen, Query-Hooks, Hilfsfunktionen

**Files:**
- Create: `src/lib/api.ts`, `src/lib/types.ts`, `src/lib/queries.ts`, `src/lib/categories.ts`, `src/lib/format.ts`, `src/lib/scores.ts`, `src/hooks/useDebounced.ts`
- Test: `src/lib/api.test.ts`, `src/lib/categories.test.ts`, `src/lib/scores.test.ts`

**Interfaces:**
- Produces:
  - `class ApiError extends Error { status: number }`
  - `async function errorMessage(res: Response): Promise<string>` – `detail` als String → direkt; `detail` als Array (Pydantic) → `"feld: msg; feld: msg"` (loc ohne erstes Element); kein JSON → `"Fehler {status}"`.
  - `async function api<T>(path: string, opts?: { method?: string; body?: unknown; admin?: boolean }): Promise<T>` – setzt `Content-Type` bei Body, `X-Admin-Token` aus `sessionStorage["adminToken"]` bei `admin: true`, wirft `ApiError`, gibt bei 204 `undefined` zurück.
  - `types.ts`: `Document, DocumentList, DocumentCreate, DocumentUpdate, ClassifyResponse, Meta, Stats (inkl. activity: {date: string; count: number}[]), AuditEntry, ArchiveInfo, RestoreResult` – Felder exakt wie `app/schemas.py`.
  - `queries.ts`: `useMeta()`, `useStats()`, `useDocuments(params: {q?: string; category?: string; docType?: string; offset: number; limit: number})` (mit `placeholderData: keepPreviousData`), `useDocument(id)`, `useClassify(title, content)` (nur aktiv ab title≥1 und content≥10 Zeichen), `useCreateDocument()`, `useUpdateDocument(id)`, `useDeleteDocument()`, `useArchives()`, `useCreateArchive()`, `useRestoreArchive()`, `useAudit(limit)`. Mutationen invalidieren `["documents"]`, `["stats"]`, `["audit"]`.
  - `categoryStyle(name: string): { color: string; soft: string; icon: LucideIcon }` – feste Zuordnung für die 9 bestehenden Fachgebiete (HNO, Neurologie, Innere Medizin, Kardiologie, Dermatologie, Orthopädie, Pädiatrie, Psychiatrie, Allgemeinmedizin); unbekannt → neutrales Grau + `Stethoscope`.
  - `toScoreBars(scores: Record<string, number>, max?: number): {name: string; score: number; share: number}[]` – absteigend sortiert, `share` = score / größter Score (0–1), Kategorien mit 0 weggelassen, höchstens `max` (Default 5).
  - `formatDate(iso: string): string` (de-AT, `dateStyle: "medium", timeStyle: "short"`), `formatRelative(iso)` („vor 3 Min.", via `Intl.RelativeTimeFormat("de-AT")`).
  - `useDebounced<T>(value: T, ms: number): T`.

- [ ] **Step 1: Failing tests**

```ts
// api.test.ts
it("reads a string detail", async () => {
  expect(await errorMessage(new Response(JSON.stringify({ detail: "Document not found." }), { status: 404 }))).toBe("Document not found.");
});
it("joins pydantic error details", async () => {
  const body = { detail: [{ loc: ["body", "title"], msg: "too short" }, { loc: ["body", "content"], msg: "missing" }] };
  expect(await errorMessage(new Response(JSON.stringify(body), { status: 422 }))).toBe("title: too short; content: missing");
});
it("falls back to the status for non-JSON bodies", async () => {
  expect(await errorMessage(new Response("<html>", { status: 502 }))).toBe("Fehler 502");
});
it("throws ApiError with status and sends the admin token", async () => { /* fetch mocken, sessionStorage setzen, Header + ApiError.status === 401 prüfen */ });

// scores.test.ts
it("sorts, normalises and drops zero scores", () => {
  expect(toScoreBars({ HNO: 2, Kardiologie: 8, Neurologie: 0, Dermatologie: 4 })).toEqual([
    { name: "Kardiologie", score: 8, share: 1 },
    { name: "Dermatologie", score: 4, share: 0.5 },
    { name: "HNO", score: 2, share: 0.25 },
  ]);
});
it("returns an empty list when every score is 0", () => expect(toScoreBars({ HNO: 0 })).toEqual([]));

// categories.test.ts
it("has a distinct colour for every known category", () => { /* 9 Namen → 9 verschiedene color-Werte */ });
it("falls back for unknown categories", () => expect(categoryStyle("Xyz").icon).toBe(Stethoscope));
```

- [ ] **Step 2:** `npm test` → FAIL (Module fehlen)
- [ ] **Step 3:** Implementieren wie unter Interfaces.
- [ ] **Step 4:** `npm test && npm run typecheck` → PASS
- [ ] **Step 5: Commit** — `feat(frontend): add API client, types, query hooks and helpers`

---

### Task 4: App-Shell, Navigation, Theme, Befehlspalette, Fehler-/Leerzustände

**Files:**
- Create: `src/main.tsx`, `src/App.tsx`, `src/components/layout/{AppShell,Sidebar,Topbar,ThemeToggle,CommandPalette,PageTransition}.tsx`, `src/components/feedback/{ErrorState,EmptyState}.tsx`, `src/components/motion/CountUp.tsx`, `src/features/NotFoundPage.tsx`
- Test: `src/components/layout/ThemeToggle.test.tsx`, `src/components/motion/CountUp.test.tsx`, `src/components/layout/CommandPalette.test.tsx`

**Interfaces:**
- Consumes: `useDocuments`, `categoryStyle` (Task 3)
- Produces:
  - `<AppShell>` mit `<Outlet/>`; Sidebar-Einträge: Dashboard (`/`), Wissensdatenbank (`/wissen`), Admin (`/admin`). Einklappbar auf Desktop (Zustand in `localStorage["sidebar"]`), auf < 768 px als `Sheet`-Drawer.
  - `<PageTransition>`: `AnimatePresence mode="wait"`, Schlüssel = `location.pathname`, Fade + 8 px Slide, 200 ms; bei reduced motion nur Opacity.
  - Theme: `"light" | "dark" | "system"` in `localStorage["theme"]`, Klasse `dark` auf `<html>`; Default `system`.
  - `<CommandPalette>`: öffnet mit Strg+K / ⌘K und über einen Suchknopf in der Topbar; Eingabe (debounced 200 ms) sucht via `useDocuments({q, limit: 8})`; Enter öffnet `/wissen/:id`; feste Aktionen „Neuer Eintrag", „Zum Dashboard", „Theme wechseln".
  - `<CountUp value={n} />`: zählt in 800 ms von 0 hoch (motion `animate`), bei reduced motion sofort Endwert.
  - `<ErrorState error onRetry />` (Titel „Daten konnten nicht geladen werden", Meldung aus `ApiError.message`, Button „Erneut versuchen"), `<EmptyState title text action? />`.
  - Toasts über `sonner` (`toast.success/error`), global im Provider.
  - Topbar zeigt Hinweis „Prototyp mit Beispieldaten – keine medizinische Beratung."

- [ ] **Step 1: Failing tests** — ThemeToggle: Klick auf „Dunkel" setzt `document.documentElement.classList.contains("dark") === true` und `localStorage.theme === "dark"`. CountUp: mit gemocktem `useReducedMotion → true` steht sofort `42` im DOM. CommandPalette: `fireEvent.keyDown(window, {key: "k", ctrlKey: true})` → Dialog mit Platzhalter „Einträge durchsuchen…" sichtbar.
- [ ] **Step 2:** `npm test` → FAIL
- [ ] **Step 3:** Implementieren (impeccable-Skill laden; Designrichtung aus Global Constraints).
- [ ] **Step 4:** `npm test && npm run lint && npm run typecheck` → PASS; manuell `npm run dev` + uvicorn: Navigation, Theme, Strg+K funktionieren, Seitenwechsel animiert.
- [ ] **Step 5: Commit** — `feat(frontend): app shell with animated navigation, theme and command palette`

---

### Task 5: Dashboard

**Files:**
- Create: `src/features/dashboard/{DashboardPage,KpiCard,CategoryDonut,DocTypeBars,ActivityChart,RecentList}.tsx`
- Test: `src/features/dashboard/DashboardPage.test.tsx`

**Interfaces:**
- Consumes: `useStats`, `categoryStyle`, `CountUp`, `ErrorState`, `formatRelative`
- Produces: Route `/`.
  - KPI-Karten: „Einträge" (`total`), „Fachgebiete" (Anzahl Kategorien mit count > 0), „Auto-Klassifikationsquote" (`round(auto_classified/total*100)` %, bei total 0 → „–"), „Änderungen (30 Tage)" (Summe `activity`). Mit `CountUp`, Karten gestaffelt eingeblendet (60 ms Abstand).
  - `CategoryDonut`: Recharts `PieChart` (innerRadius), Farben aus `categoryStyle`, Mitte zeigt Gesamtzahl; Klick auf ein Segment → `/wissen?category=<name>`.
  - `DocTypeBars`: horizontale Balken je Dokumenttyp.
  - `ActivityChart`: `AreaChart` über `activity`, Tooltip mit Datum (de-AT) und Anzahl.
  - `RecentList`: 5 zuletzt geänderte Einträge mit Fachgebiets-Punkt, relativer Zeit, Link zu `/wissen/:id`.
  - Lade-Zustand: Skeletons in Kartenform; Fehler: `ErrorState` mit `refetch`.
  - Charts animieren nur, wenn nicht reduced motion (`isAnimationActive`).

- [ ] **Step 1: Failing tests** (Query-Client mit vorbefüllten Daten bzw. gemocktem `fetch`):
  - Stats `{total: 16, auto_classified: 12, categories: [...3 mit count>0, 6 mit 0], activity: 30 Tage mit Summe 5}` → Texte „16", „75 %", „3", „5" sichtbar (reduced motion gemockt).
  - `total: 0` → Quote zeigt „–".
  - `fetch` liefert 500 → „Daten konnten nicht geladen werden" und Button „Erneut versuchen" sichtbar.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren.
- [ ] **Step 4:** PASS; manuell im Browser hell/dunkel und bei 375 px prüfen.
- [ ] **Step 5: Commit** — `feat(frontend): animated dashboard with KPIs and charts`

---

### Task 6: Wissensdatenbank – Suche, Filter, Liste

**Files:**
- Create: `src/features/documents/{KnowledgeBasePage,SearchFilters,DocumentCard}.tsx`
- Test: `src/features/documents/KnowledgeBasePage.test.tsx`

**Interfaces:**
- Consumes: `useDocuments`, `useMeta`, `useDebounced`, `categoryStyle`, `EmptyState`, `ErrorState`
- Produces: Route `/wissen`. Zustand in der URL: `?q=&category=&type=&page=` (page ab 1, Seitengröße 10). Suche debounced 300 ms. Filter als shadcn-`Select` (animiert öffnend) mit Option „Alle Fachgebiete"/„Alle Typen". Aktive Filter als entfernbare Badges. Liste mit `motion` `layout` + `AnimatePresence` (gestaffeltes Einblenden, Gleiten beim Filtern). `DocumentCard`: Titel (max. 2 Zeilen, `line-clamp-2`), Fachgebiets-Badge in Kategoriefarbe, Typ, Auszug (`line-clamp-3`), bis zu 5 Schlagwörter + „+N", `break-words`. Trefferzeile „1–10 von 23 Einträgen". Pagination „Zurück/Weiter". Leer: `EmptyState` „Keine Einträge gefunden" mit Button „Filter zurücksetzen".

- [ ] **Step 1: Failing tests:**
  - Eingabe `kopf` → nach Debounce wird `fetch` mit `q=kopf` aufgerufen (Fake-Timer).
  - Eingabe `100% "Ohr_"` → Request-URL enthält korrekt kodiertes `q`, Antwort `{items: [], total: 0}` → „Keine Einträge gefunden".
  - `?category=HNO` in der Start-URL → Request enthält `category=HNO`, Badge „HNO" sichtbar; Klick auf das ✕ entfernt den Parameter.
  - Karte mit 300-Zeichen-Titel und 20 Schlagwörtern rendert „+15".
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren.
- [ ] **Step 4:** PASS
- [ ] **Step 5: Commit** — `feat(frontend): searchable, filterable knowledge base list with layout animations`

---

### Task 7: Eintrags-Detailseite

**Files:**
- Create: `src/features/documents/{DocumentPage,ClassificationExplainer}.tsx`
- Test: `src/features/documents/DocumentPage.test.tsx`

**Interfaces:**
- Consumes: `useDocument`, `useClassify`, `useDeleteDocument`, `toScoreBars`, `categoryStyle`, `formatDate`
- Produces: Route `/wissen/:id`. Kopf mit Titel, Fachgebiets-Badge, Typ, „automatisch klassifiziert"/„manuell gesetzt". Inhalt als Fließtext (Absätze an `\n\n`). Seitenleiste: Schlagwörter, Quelle, erstellt/geändert, `ClassificationExplainer` (ruft `/api/classify` mit Titel+Inhalt, zeigt Top-5 `toScoreBars` und `matched_terms` als Chips). Aktionen „Bearbeiten" (→ `/wissen/:id/bearbeiten`) und „Löschen" (`AlertDialog` „Eintrag endgültig löschen?", danach Toast + `/wissen`). 404 → `EmptyState` „Eintrag nicht gefunden" mit Link zur Liste. Tabs-Gerüst nur mit „Inhalt" (weitere Tabs kommen in Etappe 3/4).

- [ ] **Step 1: Failing tests:** Detail rendert Titel und Badge; Klassifikations-Balken für `{Kardiologie: 10, Innere Medizin: 2}` zeigen beide Namen; API 404 → „Eintrag nicht gefunden"; Löschen → Bestätigungsdialog, nach Bestätigen `DELETE /api/documents/5` aufgerufen.
- [ ] **Step 2:** FAIL · **Step 3:** Implementieren · **Step 4:** PASS
- [ ] **Step 5: Commit** — `feat(frontend): document detail page with classification explainer`

---

### Task 8: Editor mit Live-Klassifikation

**Files:**
- Create: `src/features/editor/{EditorPage,ScoreBars,KeywordInput}.tsx`
- Test: `src/features/editor/EditorPage.test.tsx`, `src/features/editor/KeywordInput.test.tsx`

**Interfaces:**
- Consumes: `useMeta`, `useDocument`, `useClassify`, `useCreateDocument`, `useUpdateDocument`, `useDebounced`, `toScoreBars`
- Produces: Routen `/wissen/neu` und `/wissen/:id/bearbeiten`. Felder: Titel, Typ (`Select`), Inhalt (`Textarea`, auto-grow), Fachgebiet (`Select` mit erster Option „Automatisch (Vorschlag: X)"), Schlagwörter (`KeywordInput`), Quelle. Neben dem Formular (mobil darunter) `ScoreBars`: Titel+Inhalt debounced 400 ms an `/api/classify`; Balken animieren ihre Breite (`motion` `animate={{width}}`), Gewinner hervorgehoben, Text „Vorschlag: Kardiologie (Konfidenz 83 %)" bzw. „Zu wenig Fachbegriffe – Fallback Allgemeinmedizin" bei `fallback`. Button „Vorgeschlagene Schlagwörter übernehmen". Speichern: Create sendet `category` nur bei manueller Wahl; Update sendet nur geänderte Felder, bei Wechsel zurück auf „Automatisch" `reclassify: true`. Validierungsfehler (422) erscheinen per Toast mit `errorMessage`-Text. Ungespeicherte Änderungen: `useBlocker` fragt „Änderungen verwerfen?".
- `KeywordInput`: Enter oder Komma fügt hinzu, Backspace im leeren Feld entfernt das letzte, Duplikate (case-insensitive) ignoriert, max. 20, max. 50 Zeichen.

- [ ] **Step 1: Failing tests:** KeywordInput: „Fieber, fieber, Husten" → zwei Chips; 21. Eintrag wird nicht hinzugefügt. Editor: Tippen in Titel/Inhalt → nach Debounce Request an `/api/classify`; Anzeige „Vorschlag: Kardiologie"; Speichern ohne Kategorie-Wahl → Body ohne `category`; Wechsel zurück auf „Automatisch" im Bearbeiten-Modus → Body enthält `reclassify: true`; 422-Antwort → Toast mit „title: …".
- [ ] **Step 2:** FAIL · **Step 3:** Implementieren · **Step 4:** PASS
- [ ] **Step 5: Commit** — `feat(frontend): editor with live animated classification`

---

### Task 9: Admin-Bereich (Archiv, Änderungsprotokoll)

**Files:**
- Create: `src/features/admin/{AdminPage,AdminTokenGate,ArchivesPanel,AuditTable}.tsx`
- Test: `src/features/admin/AdminPage.test.tsx`

**Interfaces:**
- Consumes: `useArchives`, `useCreateArchive`, `useRestoreArchive`, `useAudit`, `api`
- Produces: Route `/admin`. `AdminTokenGate`: Passwortfeld „Admin-Token", speichert in `sessionStorage["adminToken"]`, prüft sofort mit `GET /api/audit?limit=1`; 401 → Token wird gelöscht, Meldung „Admin-Token ungültig"; 503 → „Admin-Funktionen sind deaktiviert (ADMIN_TOKEN fehlt)". Danach Tabs „Archive" und „Änderungsprotokoll". Archive: Liste (Name, Datum, Größe, Anzahl), „Archiv erstellen", Download (Blob über `api(..., admin)`), „Wiederherstellen" mit `AlertDialog` („Ersetzt alle Einträge; vorher wird automatisch eine Sicherung erstellt"). Audit: Tabelle mit Zeit (relativ + Tooltip absolut), Aktion als farbiges Badge (create grün, update blau, delete rot, archive/restore violett), Dokument-Link, Detail. „Abmelden" löscht das Token.

- [ ] **Step 1: Failing tests:** falsches Token (401) → „Admin-Token ungültig" und `sessionStorage.adminToken` leer; richtiges Token → Tab „Archive" sichtbar und Header `X-Admin-Token` gesendet; Wiederherstellen → Dialog, nach Bestätigen `POST /api/archives/<name>/restore`.
- [ ] **Step 2:** FAIL · **Step 3:** Implementieren · **Step 4:** PASS
- [ ] **Step 5: Commit** — `feat(frontend): admin area for archives and audit log`

---

### Task 10: Auslieferung durch FastAPI, Docker, CI, Smoke-Tests, altes UI entfernen

**Files:**
- Create: `app/spa.py`, `tests/test_spa.py`, `frontend/playwright.config.ts`, `frontend/e2e/smoke.spec.ts`
- Modify: `app/main.py`, `Dockerfile`, `.github/workflows/ci.yml`, `README.md` (Quick start: Frontend-Dev und Build)
- Delete: `app/static/`

**Interfaces:**
- Produces: `mount_frontend(app: FastAPI, dist_dir: Path) -> None` – wenn `dist_dir/index.html` existiert: `/assets` als `StaticFiles`, Catch-all `GET /{path:path}` liefert eine existierende Datei aus `dist_dir` (Pfad mit `resolve()` gegen Traversal geprüft) oder sonst `index.html`; Pfade, die mit `api/` beginnen, → JSON 404 `{"detail": "Not Found"}`. Wenn `dist` fehlt: `GET /` liefert eine kurze HTML-Seite „Frontend nicht gebaut – `cd frontend && npm run build`", API läuft normal. Settings: `frontend_dist: Path = Path("frontend/dist")`.

- [ ] **Step 1: Failing tests** (`tests/test_spa.py`, eigene `FastAPI()`-Instanz + `tmp_path` mit `index.html` und `assets/app.js`):

```python
def test_deep_link_serves_index(spa_client): assert "<div id=\"root\">" in spa_client.get("/wissen/12").text
def test_asset_is_served(spa_client): assert spa_client.get("/assets/app.js").headers["content-type"].startswith("text/javascript")
def test_unknown_api_path_is_json_404(spa_client):
    r = spa_client.get("/api/does-not-exist"); assert r.status_code == 404 and r.json() == {"detail": "Not Found"}
def test_path_traversal_does_not_leak_files(spa_client, tmp_path):
    (tmp_path / "secret.txt").write_text("TOP-SECRET")  # liegt neben dist/, nicht darin
    assert "TOP-SECRET" not in spa_client.get("/..%2Fsecret.txt").text
def test_missing_dist_shows_hint(tmp_path):
    app = FastAPI(); mount_frontend(app, tmp_path / "nope")
    assert "Frontend nicht gebaut" in TestClient(app).get("/").text
```

- [ ] **Step 2:** `pytest tests/test_spa.py -v` → FAIL
- [ ] **Step 3:** `app/spa.py` implementieren; `main.py` ruft `mount_frontend(app, settings.frontend_dist)` nach den API-Routern; `app/static/` löschen.
- [ ] **Step 4:** `pytest` → alle grün; `ruff check . && ruff format --check .`
- [ ] **Step 5: Playwright** — `playwright.config.ts` startet `webServer` mit uvicorn (SQLite-Datei in tmp, `SEED_DEMO_DATA=true`, `ADMIN_TOKEN=e2e-token`) gegen das gebaute Frontend. `e2e/smoke.spec.ts`:
  - Dashboard zeigt „Einträge" und eine Zahl > 0.
  - Suche „kopfschmerz" → Karte „Anamnese bei Kopfschmerzen" → Detailseite zeigt Neurologie.
  - Neuer Eintrag mit Herz-Text → Vorschlag „Kardiologie" → Speichern → Detailseite.
  - Admin mit `e2e-token` → Archiv erstellen → erscheint in der Liste.
  - Viewport 375×812: Liste und Detail ohne horizontales Scrollen (`document.documentElement.scrollWidth <= 375`).
  Run: `npm run build && npx playwright install chromium && npm run e2e` → 5 passed.
- [ ] **Step 6: Dockerfile** — Stage 1 `node:22-alpine`: `npm ci && npm run build` in `frontend/`; Stage 2 wie bisher, zusätzlich `COPY --from=frontend /frontend/dist ./frontend/dist`. Verifizieren: `docker build -t medkb .` (falls Docker lokal fehlt, übernimmt die CI den Build).
- [ ] **Step 7: CI** — neuer Job `frontend`: Node 22, `npm ci`, `lint`, `typecheck`, `test`, `build`, Playwright (Chromium) gegen Python 3.12; Job `docker`: `docker build .`.
- [ ] **Step 8:** README-Quick-Start um Frontend ergänzen (Dev: zwei Terminals; Prod: `npm run build` dann uvicorn).
- [ ] **Step 9: Commit** — `feat: serve React frontend from FastAPI, multi-stage Docker, CI and e2e smoke tests`

---

## Abschluss Etappe 1

- [ ] `pytest`, `ruff`, `npm run lint/typecheck/test/e2e` alle grün
- [ ] Manuelle Sichtprüfung hell/dunkel, Desktop/375 px, reduced motion (DevTools-Emulation)
- [ ] Push auf `main`, CI grün
