# Etappe 5 – Öffentliche Demo (Render + Neon), README, Demo-GIF – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** MedKB läuft öffentlich unter einem Live-Link. Ein Recruiter klickt eine Demo-Rolle und sieht in Sekunden echte Inhalte, Quellen und KI. Das README zeigt Live-Link, Screenshots, Demo-GIF und Architektur.

**Architecture:**
- Ein Docker Web Service auf Render (Free) liefert API und gebautes Frontend. Die Datenbank ist Neon Postgres (Free); Renders eigenes Free-Postgres läuft nach 30 Tagen ab.
- Vorher werden die für einen öffentlichen Betrieb relevanten Backlog-Punkte geschlossen:
  - Token-Härtung
  - atomarer Demo-Reset
  - echte Client-IP hinter Renders Proxy für das KI-Kontingent
  - Cache-Header
  - kleineres JS-Bundle

**Tech Stack:** wie Etappe 4; `render.yaml` (Blueprint), ffmpeg für das GIF (lokal installiert).

**Spec:** `docs/superpowers/specs/2026-10-10-medkb-v2-design.md` §11, §12.5; offene Punkte `docs/BACKLOG.md`, `docs/NEXT_STEPS.md`. **Gotchas:** `AGENTS.md`.

## Global Constraints

- Hosting-Fakten (geprüft 2026-10-12):
  - Render Free:
    - schläft nach 15 min ohne eingehende Anfrage, Aufwachen dauert etwa 1 min
    - 750 Instanzstunden pro Workspace und Monat
    - flüchtiges Dateisystem (Archive gehen bei Neustart verloren)
  - Neon Free:
    - 0,5 GB Speicher, 100 CU-Stunden pro Projekt und Monat
    - pausiert nach 5 min, Aufwachen in Sekunden
- Secrets nur in Render-Umgebungsvariablen, nie im Repo: `DATABASE_URL`, `AI_API_KEY`, optional `ICD_CLIENT_ID`/`ICD_CLIENT_SECRET`, `NCBI_API_KEY`. `JWT_SECRET` erzeugt Render (`generateValue: true`) und bleibt über Deploys stabil.
- Öffentliche Demo:
  - `DEMO_MODE=true`, `DEMO_RESET_HOURS=3`, weil jeder Besucher Admin sein kann
  - KI-Tagesgrenzen bleiben bei 500 global und 30 pro Client
- Konten anlegen und Secrets eintragen macht der Nutzer selbst; der Agent liefert Schritt-für-Schritt-Anleitung und prüft danach.
- Alles aus Etappe 1–4 bleibt: UI Deutsch, Hinweis „keine medizinische Beratung“, DESIGN.md, Test zuerst, ein Commit pro Aufgabe, keine echten Netz-/KI-Aufrufe in Tests.

## Review Focus

1. Zwei Besucher hinter Renders Proxy teilen sich nicht dasselbe KI-Kontingent, und ein Besucher kann sein Kontingent nicht durch einen selbst gesetzten Header zurücksetzen. Dafür zählt nur der konfigurierte Header von Renders Edge. (Task 2)
2. Ein Demo-Reset während laufender Lesezugriffe zeigt nie eine leere Wissensdatenbank. Ein Fehler mitten im Reset lässt den alten Stand stehen. (Task 1)
3. Kaltstart nach Schlaf: Render weckt den Dienst, die Neon-Verbindung baut sich neu auf, `create_all`/`upgrade_schema`/Reset laufen einmal. Der erste Aufruf liefert die Seite, kein 502-Dauerzustand. Healthcheck `/api/health` antwortet ohne Datenbankzugriff. (Tasks 5, 7)
4. Ein abgelaufenes oder ohne `exp` signiertes Token wird abgewiesen. Eine späte 401 einer alten Anfrage meldet einen frisch eingeloggten Nutzer nicht ab. (Task 1)
5. Nach einem Deploy liefern alte Browser-Tabs keine 404 auf gelöschte Asset-Hashes in einer Endlosschleife. `index.html` wird nie lange gecacht, Hash-Assets dagegen immutable. (Task 3)

---

## File Structure

```
app/auth.py                 (mod) decode_token verlangt exp und sub
app/demo.py                 (mod) reset_demo in einer Transaktion
app/seed.py, app/services.py (mod) commit-Parameter für den atomaren Reset
app/config.py               (mod) client_ip_header
app/routers/ai.py           (mod) Client-IP aus konfiguriertem Header
app/spa.py                  (mod) Cache-Control, HEAD /, Sicherheits-Header
frontend/src/lib/api.ts     (mod) 401 löscht nur das eigene Token
frontend/src/App.tsx        (mod) Routen per React.lazy
Dockerfile                  (mod) PORT aus der Umgebung
render.yaml                 (neu) Blueprint
.github/workflows/ci.yml    (mod) Container starten, /api/health und / prüfen
scripts/record_demo.mjs     (neu) Playwright-Video der Demo-Tour → ffmpeg → docs/media/demo.gif
README.md                   (mod) Live-Link, GIF, Screenshots, Architektur, Kaltstart-Hinweis
docs/media/*                (neu) Screenshots, GIF
AGENTS.md, docs/NEXT_STEPS.md, docs/BACKLOG.md (mod)
```

---

### Task 1: Token-Härtung und atomarer Demo-Reset

**Files:** `app/auth.py`, `app/demo.py`, `app/seed.py`, `app/services.py`, `frontend/src/lib/api.ts`, Tests `tests/test_auth.py`, `tests/test_demo_reset.py`, `frontend/src/lib/api.test.ts`

**Interfaces:**
- `decode_token` nutzt `options={"require": ["exp", "sub"]}`.
- `create_document(db, data, actor=None, commit=True)` und `seed_if_empty(db, force=False, commit=True)`.
- `reset_demo(db)` löscht, befüllt und schreibt den Audit-Eintrag mit genau einem `commit()`; im Fehlerfall `rollback()` und die Exception geht weiter.
- `api.ts`: Bei 401 wird das Token nur gelöscht, wenn `tokenStore.get()` noch das gesendete Token ist.

- [ ] **Step 1: Tests**
  - `test_token_without_exp_is_rejected`: Mit dem Secret signiertes `{sub, role}` ohne `exp` → `/api/auth/me` 401.
  - `test_reset_is_one_transaction`:
    - `seed_if_empty` wird so gepatcht, dass es nach dem 5. Eintrag wirft.
    - Erwartet: Exception; danach unverändert die alten Einträge und das alte Log.
  - `test_reader_never_sees_an_empty_base_during_reset`: Eine zweite Session zählt Dokumente, während `reset_demo` vor dem Commit steht, und sieht mehr als 0. Das gilt für SQLite und für den PostgreSQL-CI-Job.
  - `api.test.ts` → `'a late 401 for an old token keeps the new token'`.
- [ ] **Step 2:** FAIL bestätigen
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** `pytest`, Ruff, Frontend lint/typecheck/test → grün
- [ ] **Step 5:** Commit `fix: atomic demo reset, tokens require exp, late 401 keeps a new login`

### Task 2: Echte Client-IP hinter Renders Proxy

**Files:** `app/config.py`, `app/routers/ai.py`, `tests/test_ai_api.py`

**Interfaces:**
- `client_ip_header: str = ""` (Env `CLIENT_IP_HEADER`). Leer → `request.client.host`. Gesetzt → der erste Wert dieses Headers; fehlt er, gilt `request.client.host`.
- Welcher Header vertrauenswürdig ist, wird in Task 7 live geprüft (Kandidat `True-Client-IP` von Renders Cloudflare-Edge). Bis dahin bleibt der Default leer.

- [ ] **Step 1: Tests**
  - Ohne Einstellung hat ein gefälschtes `True-Client-IP` keine Wirkung: Das Kontingent ist nach 30 Aufrufen erschöpft, auch mit wechselndem Header.
  - Mit `client_ip_header="true-client-ip"` haben zwei verschiedene Header-Werte getrennte Kontingente.
- [ ] **Step 2–4:** RED → Implementieren → GREEN, ganze Suite
- [ ] **Step 5:** Commit `feat(ai): client identity from a configured proxy header`

### Task 3: Auslieferung härten

**Files:** `app/spa.py`, `tests/test_spa.py`

**Interfaces:**
- Header nach Anfrage:
  - `/assets/*`: `Cache-Control: public, max-age=31536000, immutable`
  - `index.html` und SPA-Fallback: `Cache-Control: no-cache`
- `HEAD /` → 200.
- Alle Antworten bekommen `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` und `X-Frame-Options: DENY`.
- Ein unbekanntes `/assets/alt-123.js` liefert 404 statt `index.html`, damit alte Tabs nicht HTML als JS laden.

- [ ] **Step 1: Tests** für jede Zeile oben (`test_spa.py`, mit einem temporären `dist`)
- [ ] **Step 2–4:** RED → Implementieren → GREEN
- [ ] **Step 5:** Commit `feat(spa): caching and security headers for public hosting`

### Task 4: Schnellerer erster Aufruf

**Files:** `frontend/src/App.tsx`, ggf. `frontend/vite.config.ts`, `frontend/src/App.test.tsx` (neu, falls nötig)

**Interfaces:** Seiten werden per `React.lazy` + `Suspense` geladen, mit Skeleton als Fallback: Dashboard (Recharts), Wissensdatenbank, Eintrag, Editor, Admin, Assistent, Login bleibt eager. Der Router fängt Lade-Fehler eines Chunks ab: ein einmaliger Reload, danach `RouteError`.

- [ ] **Step 1:** Test: Navigation zu einer lazy Route rendert erst Skeleton, dann die Seite. Die bestehenden Seiten-Tests bleiben grün.
- [ ] **Step 2–3:** Implementieren
- [ ] **Step 4:** `npm run build` → keine Warnung „larger than 500 kB“; Größe des Haupt-Chunks im Commit notieren. `npm run e2e` grün.
- [ ] **Step 5:** Commit `perf(frontend): lazy-load routes`

### Task 5: Deploy-Konfiguration

**Files:** `Dockerfile`, `render.yaml`, `.github/workflows/ci.yml`, `tests/test_deploy_config.py`

**Interfaces:**
- Dockerfile: `CMD` bindet an `${PORT:-8000}` (shell form via `sh -c`); der Healthcheck nutzt dieselbe Variable.
- `render.yaml`:
  - `type: web`, `runtime: docker`, `plan: free`, `healthCheckPath: /api/health`, `autoDeploy: true`
  - envVars:
    - `DATABASE_URL` (sync: false)
    - `JWT_SECRET` (generateValue: true)
    - `DEMO_MODE=true`, `DEMO_RESET_HOURS=3`
    - `AI_API_KEY` (sync: false)
    - `ICD_CLIENT_ID`/`ICD_CLIENT_SECRET`/`NCBI_API_KEY` (sync: false)
    - `CLIENT_IP_HEADER` (leer, bis Task 7 ihn bestätigt)
- CI-Job `docker`: Image bauen, mit `-e PORT=9000 -e DEMO_MODE=true -e JWT_SECRET=…` starten, auf `/api/health` warten (max 60 s), dann `/api/health` und `/` prüfen; `/` muss `MedKB` enthalten.
- `test_deploy_config.py`: `render.yaml` enthält jeden Schlüssel, den `Settings` für die Demo braucht. Ein Secret steht nie als Wert darin, nur mit `sync: false` oder `generateValue`. Das Parsing läuft ohne PyYAML über eine einfache Zeilensuche.

- [ ] **Step 1:** Test schreiben → FAIL
- [ ] **Step 2:** Implementieren; lokal `docker build` ist mangels Daemon evtl. nicht möglich → CI-Job ist der Beleg
- [ ] **Step 3:** `pytest` grün; nach Push CI-Job `docker` grün
- [ ] **Step 4:** Commit `build: Render blueprint, PORT-aware image, container smoke test in CI`

### Task 6: README, Screenshots, Demo-GIF

**Files:** `scripts/record_demo.mjs`, `docs/media/*`, `README.md`

**Interfaces:**
- `node scripts/record_demo.mjs` startet gegen einen laufenden Server (`BASE_URL`, Default `http://127.0.0.1:8000`) eine Playwright-Tour mit Video (1280×800). KI- und Quellen-Antworten sind wie in e2e gemockt, damit das GIF reproduzierbar ist. Die Tour:
  1. Login als Ärztin
  2. Dashboard
  3. Suche „Migräne“
  4. Eintrag mit Reitern Studien und ICD-11
  5. KI-Zusammenfassung
  6. Wechsel zu Patient
  7. „Warnzeichen erklären“
  8. KI-Assistent mit Quelle
- Danach ffmpeg mit Palette, 12 fps, 960 px Breite → `docs/media/demo.gif`, Zielgröße unter 8 MB.
- Screenshots: Dashboard, Eintrag (Arzt), Patientenansicht, Assistent, Editor mit KI-Entwurf; Desktop hell und dunkel plus ein Handy-Bild → `docs/media/*.png`. Die alten README-Bilder werden entfernt.
- README auf Deutsch, mit englischer Kurzfassung oben:
  - Live-Link und Demo-Rollen
  - Kaltstart-Hinweis (bis ~1 min)
  - GIF
  - Architekturdiagramm (Mermaid)
  - Funktionen je Rolle
  - echte Quellen (PubMed, WHO ICD-11, openFDA, Gemini)
  - Sicherheits- und Datenschutzgrenzen
  - Bezug zur Diplomarbeit
  - lokales Setup, Tests

- [ ] **Step 1:** Skript schreiben, GIF und Screenshots erzeugen, Bilder ansehen und prüfen (lesbar, keine leeren Zustände)
- [ ] **Step 2:** README schreiben; jeden Befehl darin einmal ausführen
- [ ] **Step 3:** Commit `docs: README with live demo, GIF and screenshots`

### Task 7: Deploy und Live-Abnahme (mit dem Nutzer)

**Nutzer:**
1. Neon-Konto und Projekt anlegen, Connection-String kopieren.
2. Render-Konto, „New → Blueprint“ und dieses Repo verbinden.
3. Die Secrets im Render-Dashboard eintragen: `DATABASE_URL`, `AI_API_KEY`, optional ICD.

**Agent:** Anleitung mit Screenshots-Hinweisen, danach Live-Abnahme gegen die echte URL:
- `/api/health`
- Demo-Login je Rolle
- Suche
- Eintrag mit Studien und openFDA
- ICD-11 (falls Keys)
- jede KI-Funktion einmal
- Kaltstart-Zeit messen
- Header aus Task 3
- Client-IP-Header bestimmen: `/api/ai/usage` mit zwei Netzen, oder ein temporärer Debug-Log nur der Header-Namen. Dann `CLIENT_IP_HEADER` setzen und mit einem gefälschten Header gegenprüfen.

- [ ] **Step 1:** Abnahme-Checkliste in `docs/reviews/2026-10-12-stage5-deployment.md` mit Ergebnis je Punkt
- [ ] **Step 2:** README-Live-Link einsetzen; AGENTS-Status Etappe 5 „done“; NEXT_STEPS und BACKLOG aktualisieren
- [ ] **Step 3:** Commit `docs: stage 5 live verification`
