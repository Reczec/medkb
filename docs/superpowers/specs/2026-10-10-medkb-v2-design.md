# MedKB v2 – Design-Spec

Stand: 2026-10-10 · Status: zur Freigabe

## 1. Ziel

MedKB wird vom Diplomarbeits-Prototyp zu einer öffentlich gehosteten, vorzeigbaren Demo für
CV und Portfolio ausgebaut. Erfolg heißt: Ein Recruiter öffnet den Live-Link, klickt eine
Demo-Rolle an und sieht innerhalb von 30 Sekunden eine moderne, animierte Oberfläche, echte
Daten aus offiziellen Quellen und KI-Funktionen, die nachvollziehbar und sicher sind.

Der Kern der Diplomarbeit (Suche, regelbasierte Klassifikation, Archiv, Audit-Log) bleibt
erhalten und sichtbar.

### Vom Nutzer vorgegeben
- UI weniger generisch: Animationen, Motion, gestaltete Dropdowns, besseres Dashboard
- Rollen: Admin (alles) und lesende Rollen (z. B. neue Ärztin, Patient)
- Mehr realistische Einträge
- KI-Funktionen: Zusammenfassung, einfache Erklärung u. a.
- Echte, möglichst aktuelle Daten aus seriösen, bekannten Quellen
- Live-Link + GitHub; KI über ein kostenloses Modell
- Stack: React-Frontend auf dem bestehenden FastAPI-Backend

### Annahmen
- Keine Patientendaten, nirgends. Alle Inhalte sind Lehrbuch-/Demo-Inhalte.
- UI-Sprache Deutsch, Code und API Englisch (wie bisher).

### Nicht im Umfang
- Echte Nutzerverwaltung mit Registrierung, Passwort-Reset, E-Mail
- Vektor-/Embedding-Suche (Retrieval nutzt die bestehende Suche)
- Mehrsprachigkeit der UI
- Mobile App

## 2. Architektur

```
frontend/   React 18 + TypeScript + Vite
            Tailwind CSS, shadcn/ui (Radix), Framer Motion, Recharts,
            TanStack Query, React Router
app/        FastAPI (bestehend) + neue Module:
            auth.py, routers/auth.py, ai/ (provider, prompts, cache, ratelimit),
            sources/ (pubmed, icd11, openfda, cache), demo.py (Reset)
```

- Entwicklung: Vite-Dev-Server (Proxy `/api` → uvicorn :8000).
- Produktion: Multi-Stage-Dockerfile baut das Frontend, FastAPI liefert `frontend/dist` unter
  `/` aus (SPA-Fallback auf `index.html`), API unter `/api`.
- Das alte `app/static/` wird entfernt, sobald das React-Frontend alle Funktionen abdeckt.

## 3. Rollen und Authentifizierung

- Neue Tabelle `users`: `id`, `username` (unique), `password_hash` (bcrypt via `passlib` oder
  `pwdlib`), `role` (`admin` | `doctor` | `patient`), `display_name`, `created_at`.
- `POST /api/auth/login` (Benutzername + Passwort) → JWT (HS256, `JWT_SECRET`, 8 h gültig).
- `POST /api/auth/demo` `{role}` → JWT für den Demo-Nutzer dieser Rolle. Nur wenn
  `DEMO_MODE=true`, sonst 404.
- `GET /api/auth/me` → aktueller Nutzer.
- Token im `Authorization: Bearer`-Header; Frontend hält es im Speicher + `sessionStorage`.
- `X-Admin-Token` entfällt; `require_admin` wird zu `require_role(...)`.
- Seed legt drei Demo-Nutzer an (Admin, Dr. Demo, Patient Demo) mit zufälligem Passwort,
  wenn `DEMO_MODE=true`; ein Admin mit Passwort aus `ADMIN_PASSWORD` optional.
- Demo-Reset: Bei `DEMO_MODE=true` wird die DB beim Start und alle 24 h (Hintergrund-Task)
  auf den Seed-Stand zurückgesetzt. KI- und Quellen-Cache bleiben erhalten.

### Rechte

| Funktion | patient | doctor | admin |
|---|---|---|---|
| Einträge lesen, suchen, Dashboard | ✓ (Laienansicht) | ✓ | ✓ |
| KI: Einfach erklärt, Wann zum Arzt? | ✓ | ✓ | ✓ |
| KI-Assistent (Fragen an die Wissensbasis) | ✓ (Laien-Ton) | ✓ | ✓ |
| KI: Fach-Zusammenfassung, Studien auf Deutsch | – | ✓ | ✓ |
| ICD-11, PubMed, openFDA | – | ✓ | ✓ |
| Klassifikations-Scores sehen | – | ✓ | ✓ |
| Anlegen, Bearbeiten, Löschen, Klassifizieren, KI-Entwurf | – | – | ✓ |
| Archiv, Audit-Log, Nutzerübersicht | – | – | ✓ |

Ohne Token: nur Login-Seite, `/api/auth/*` und `GET /api/health` (neu, für Render-Healthcheck). Alle anderen Endpunkte verlangen Login.
Rechte werden im Backend erzwungen; das Frontend blendet nur aus.

## 4. Datenmodell-Änderungen

`documents` erhält:
- `term_en` (String, nullable) – englischer Fachbegriff für Quellenabfragen
- `icd11_code` (String, nullable)
- `medications` (JSON-Liste von Wirkstoffnamen, englisch, Default `[]`)
- `sections` (JSON, nullable) – strukturierter Inhalt:
  `{definition, symptoms, causes, diagnostics, therapy, red_flags}` als Text. `content` bleibt
  das Volltextfeld für Suche/Klassifikation und wird aus den Sektionen zusammengesetzt, wenn
  vorhanden.
- `further_reading` (JSON-Liste `{label, url}`)
- `ai_generated` (bool, Default false) – Eintrag stammt aus KI-Entwurf

Neue Tabellen:
- `ai_cache`: `key` (sha256 aus feature + document_id + content-hash + model + role),
  `feature`, `document_id`, `model`, `output` (Text), `created_at`
- `source_cache`: `key` (source + query), `payload` (JSON), `fetched_at`
- `ai_usage`: `client_id` (gehashte IP), `day`, `count` – für das Rate-Limit

Schema weiterhin per `create_all`; Archiv-Export/-Import um die neuen Felder erweitert
(fehlende Felder in alten Archiven → Defaults).

## 5. KI

- Provider-Schnittstelle `AIProvider.complete(messages) -> str` und
  `stream(messages) -> AsyncIterator[str]`. Implementierung über die OpenAI-kompatible
  Chat-Completions-API mit `httpx`. Konfiguration: `AI_BASE_URL`, `AI_API_KEY`, `AI_MODEL`.
  Standard: Gemini Flash über Googles OpenAI-kompatiblen Endpunkt; Groq als dokumentierte
  Alternative. Ohne Key: Endpunkte antworten 503 `ai_not_configured`, UI zeigt Hinweis.
- Funktionen (Endpunkte unter `/api/ai`):
  - `POST /documents/{id}/explain` – Laiensprache (B1)
  - `POST /documents/{id}/red-flags` – Warnzeichen, Notruf-Hinweis 144
  - `POST /documents/{id}/summary` – Fach-Zusammenfassung (doctor, admin)
  - `POST /studies/summarize` – PubMed-Abstracts → 2–3 Sätze Deutsch (doctor, admin)
  - `POST /ask` – Frage an die Wissensbasis: Top-5-Treffer der bestehenden Suche als Kontext,
    Antwort nur aus diesem Kontext mit Quellenmarken `[n]`; wenn nichts passt, sagt sie das.
    Ton abhängig von der Rolle. Gesprächsverlauf bis 6 Nachrichten wird mitgeschickt.
  - `POST /draft` – Entwurf für einen Eintrag aus Titel (+ Vorschlag term_en, icd11_code,
    medications) (admin)
  - `POST /classify` – KI-Zweitmeinung zur Kategorie, Antwort als JSON, im Editor neben der
    Regel-Klassifikation („Regeln vs. KI") (admin)
- Streaming per SSE für explain, summary, ask, draft.
- System-Prompt: keine individuellen Diagnosen, keine Dosierungsempfehlungen, Hinweis
  „keine medizinische Beratung", bei Notfallzeichen Notruf 144.
- Cache: dokumentbezogene Ergebnisse in `ai_cache`; Seed-Einträge werden per CLI-Befehl
  (`python -m app.ai.prewarm`) vorab befüllt. `ask` wird nicht gecacht.
- Rate-Limit: pro gehashter IP 30 nicht gecachte KI-Aufrufe/Tag, global `AI_DAILY_LIMIT`
  (Default 500). Überschreitung → 429 mit freundlicher Meldung.

## 6. Externe Quellen

Alle unter `/api/sources`, nur doctor/admin, Timeout 8 s, Cache 24 h in `source_cache`,
Fehler → 200 mit `{status: "unavailable"}` statt Exception.

- `GET /documents/{id}/studies` – PubMed E-utilities (`esearch` + `esummary`, optional
  `NCBI_API_KEY`), Suchbegriff `term_en`, die 5 neuesten Treffer: Titel, Journal, Jahr,
  Autoren, PMID-Link.
- `GET /documents/{id}/icd11` – WHO ICD-11 API (OAuth2 Client Credentials,
  `ICD_CLIENT_ID`/`ICD_CLIENT_SECRET`), Code + Titel + Definition + Link zum Browser.
  Ohne Keys: `{status: "not_configured"}`.
- `GET /documents/{id}/medications` – openFDA Drug Label pro Wirkstoff aus `medications`:
  Anwendungsgebiet, Warnhinweise, Nebenwirkungen (gekürzt), klar als US-FDA-Daten markiert.
- Dashboard-Kachel „Neueste Studien" nutzt PubMed für die Fachgebiete mit den meisten
  Einträgen.

## 7. Inhalte

- Ca. 45 Einträge, 16 Fachgebiete (9 bestehende + 7 neue): Allgemeinmedizin, Innere Medizin,
  Kardiologie, Neurologie, HNO, Dermatologie, Orthopädie, Pädiatrie, Psychiatrie, Pneumologie,
  Gastroenterologie, Endokrinologie, Urologie, Gynäkologie, Augenheilkunde, Infektiologie.
  Jedes Fachgebiet hat mindestens zwei Einträge.
- Jeder Eintrag mit Sektionen (Definition, Symptome, Ursachen, Diagnostik, Therapie,
  Warnzeichen), `term_en`, `icd11_code`, `medications` wo sinnvoll, `further_reading` auf
  gesundheit.gv.at, AWMF, WHO, NIH.
- Kennzeichnung: „Redaktionelle Demo-Inhalte auf Lehrbuchniveau – keine medizinische
  Beratung".
- Klassifikator-Vokabular um die neuen Fachgebiete erweitert; Regressionstest prüft weiter
  `expected_category` aller Seed-Einträge.

## 8. Frontend

- Seiten: Login (3 Demo-Karten + Formular), Dashboard (rollenabhängig), Wissensdatenbank
  (Suche, Filter, Liste), Eintrag (Detail mit Tabs), Editor (admin), KI-Assistent (Chat),
  Admin (Archive, Audit-Log, Nutzer).
- Layout: Seitenleiste (einklappbar, mobil als Drawer), Kopfzeile mit Rollen-Badge,
  Theme-Umschalter, Befehlspalette (Strg+K).
- Design: heller Standard, Off-White-Flächen, Akzent Teal/Petrol, Farbe pro Fachgebiet,
  Dark Mode; Schrift Inter (oder Geist), tabellarische Ziffern.
- Motion (Framer Motion): Seitenübergänge, gestaffelte Listen mit Layout-Animation beim
  Filtern, hochzählende KPIs, einzeichnende Charts, animierte Popover/Dialoge, Live-Score-
  Balken der Klassifikation im Editor, gestreamte KI-Texte mit Skeletons;
  `prefers-reduced-motion` respektiert.
- Dashboard doctor/admin: KPI-Karten (Einträge, Fachgebiete, Auto-Klassifikationsquote,
  KI-Anfragen heute), Donut nach Fachgebiet, Balken nach Dokumenttyp, Änderungen über Zeit,
  Kachel „Neueste Studien", zuletzt bearbeitet; admin zusätzlich Aktivitäts-Feed + Archiv.
- Startseite patient: großes Suchfeld, Themenkacheln, Einstieg in den KI-Assistenten.
- Eintrag doctor: Tabs Inhalt · KI-Zusammenfassung · ICD-11 · Studien · Medikamente;
  Seitenleiste mit Schlagwörtern, Kategorie, Klassifikations-Erklärung.
  Eintrag patient: Laientext zuerst („Einfach erklärt"), „Wann zum Arzt?", Originaltext
  aufklappbar.
- Neue Backend-Endpunkte für das Dashboard: `GET /api/stats` erweitert um
  Änderungen pro Tag (letzte 30 Tage) und KI-Anfragen heute.

## 9. Fehlerbehandlung

- Einheitliches Fehlerformat `{detail, code}`; Frontend zeigt Toasts.
- 401 → zurück zum Login; 403 → „Keine Berechtigung" (sollte durch Ausblenden selten sein).
- KI/Quellen nicht konfiguriert oder nicht erreichbar → Platzhalter-Karte mit Erklärung, kein
  Absturz.
- Rate-Limit → 429 mit Restzeit.

## 10. Tests und CI

- Backend (pytest): bestehende Tests an Rollen angepasst; neu: Auth (Login, Demo-Login,
  abgelaufenes Token, Rechte je Rolle pro Endpunkt), KI mit Fake-Provider (Cache-Treffer,
  Rate-Limit, Rollen-Ton, `ask` mit Quellenmarken), Quellen mit gemockten HTTP-Antworten
  (`respx`), Demo-Reset, Archiv mit neuen Feldern.
- Frontend: ESLint, `tsc --noEmit`, Vitest für Hilfsfunktionen und Hooks, Playwright-Smoke:
  Demo-Login je Rolle, Suche, Detailseite, Admin legt Eintrag an.
- CI: bestehende Python-Jobs + Frontend-Job + Docker-Build.

## 11. Deployment

- Render Web Service (Docker) + Neon Postgres (Free). Env: `DATABASE_URL`, `JWT_SECRET`,
  `DEMO_MODE=true`, `AI_*`, `ICD_*`, optional `NCBI_API_KEY`, `AI_DAILY_LIMIT`.
- Free-Tier schläft nach 15 min (Kaltstart ~30–50 s) – im README erwähnt.
- `render.yaml` im Repo; Secrets nur in Render.
- README: Live-Link, Demo-GIF, Architekturdiagramm, Bezug zur Diplomarbeit.

## 12. Etappen

1. Frontend-Grundgerüst + Redesign + Dashboard auf bestehender API (Admin-Bereich vorerst
   noch über `X-Admin-Token`; `/api/stats` wird hier schon erweitert)
2. Rollen und Auth (inkl. Demo-Login, Demo-Reset)
3. Datenmodell-Erweiterung, neue Inhalte, externe Quellen
4. KI-Funktionen
5. Deployment, README, Demo-GIF

Jede Etappe endet mit grünen Tests und einem Commit.
