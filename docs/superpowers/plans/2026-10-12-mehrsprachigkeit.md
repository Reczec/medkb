# Mehrsprachigkeit (Englisch primär, Deutsch umschaltbar) – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Oberfläche, Einträge, KI-Antworten und Servermeldungen sind auf Englisch (Standard) und Deutsch verfügbar, umschaltbar mit einem Klick.

**Architecture:**
- Deutsch bleibt die kanonische Sprache der Einträge (Klassifikation, Fachgebiete). Englisch ist eine optionale Fassung in vier neuen Spalten.
- Das Frontend wählt die Sprache (Wörterbücher `de`/`en`, `localStorage`), sendet sie als `Accept-Language` und zeigt je Feld Englisch mit Rückfall auf Deutsch.
- Das Backend liest den Header für Servermeldungen, KI-Anweisungen und ICD-11.

**Tech Stack:** wie bisher, keine neue Bibliothek.

**Spec:** `docs/superpowers/specs/2026-10-12-mehrsprachigkeit-design.md` (ergänzt `2026-10-10-medkb-v2-design.md`). **Gotchas:** `AGENTS.md`.

## Global Constraints

- Sprachen: `Lang = "en" | "de"`, Standard `en`. Speicherschlüssel `medkb:lang`. Header `Accept-Language` (`en` oder `de`, alles andere → `en`).
- Kanonisch deutsch: `title`, `content`, `sections`, `keywords`, `category`, `doc_type`. Englisch: `title_en` (String 200, nullable), `content_en` (Text, nullable), `sections_en` (JSON, nullable), `keywords_en` (JSON, Default `[]`). Weiterlesen-Link: `label_en` (optional). Gleiche Validierung wie die deutschen Felder.
- Abschnittsnamen englisch: Definition, Symptoms, Causes, Diagnostics, Therapy, Warning signs. `content_en` setzt der Server aus `sections_en` zusammen, genau wie `content`.
- Hinweistext: de „Prototyp mit Beispieldaten – keine medizinische Beratung.“, en „Prototype with example data – not medical advice.“ Notruf: en „In an emergency call 144 (Austria).“
- **KI-Cache:** Der Schlüssel für `de` bleibt wortgleich (Eingaben, `PROMPT_VERSION = "stage4-v3"`), damit die 376 vorgewärmten Antworten gültig bleiben. Für `en` kommt die Sprache in den Schlüssel.
- Entwürfe (`/api/ai/draft`) sind immer deutsch.
- Die deutschen Oberflächentexte werden nicht umformuliert; sie bilden `de` 1:1. Englisch: Satzschreibung, kein Title Case.
- Alles aus Etappe 1–5 bleibt: DESIGN.md (Farbe nie als Textfarbe), Test zuerst, ein Commit pro Aufgabe, keine echten Netz-/KI-Aufrufe in Tests, `ruff` und `oxlint` sauber.

## Review Focus

1. Ein Eintrag ohne englische Fassung (vom Admin deutsch angelegt) in der englischen Ansicht: deutscher Text mit sichtbarem Hinweis „Only available in German“, nie leer und nie „undefined“. Suche, Karten und KI funktionieren weiter. (Tasks 2, 7)
2. Sprachwechsel bei laufender KI-Antwort und im Editor mit ungespeicherten Änderungen: Der Editor behält seine Eingaben (kein Neumounten), eine laufende Antwort wird abgebrochen und nicht gemischt angezeigt. (Tasks 5, 9)
3. Servertexte kommen in der Anfragesprache; ohne Header gilt Englisch; kein Mix aus Gespeichertem und Übersetztem im Änderungsprotokoll. (Tasks 1, 3)
4. Deutsche KI-Antworten treffen den vorhandenen Cache weiter; englische und deutsche Antworten werden nie vertauscht. (Task 3)
5. Suche: ein englischer Begriff findet den Eintrag in beiden Oberflächen, ein deutscher ebenso; Begriffe mit JSON-Syntaxzeichen überspringen die Schlagwortspalten wie bisher. (Task 2)

---

## File Structure

```
app/i18n.py                 (neu) Lang, parse_language, request_language, MESSAGES, message()
app/content.py             (mod) SECTION_LABELS je Sprache, compose_content(sections, lang="de")
app/models.py              (mod) Document: title_en, content_en, sections_en, keywords_en
app/database.py            (mod) ADDED_COLUMNS
app/schemas.py             (mod) Create/Update/Out/ArchiveEntry, FurtherReadingLink.label_en
app/services.py            (mod) Felder anlegen/ändern, Suche über beide Sprachen
app/archive.py             (mod) neue Felder
app/auth.py, app/routers/* (mod) lokalisierte detail-Texte
app/ai/prompts.py          (mod) messages(feature, role, inputs, lang="de"), notice(lang)
app/ai/service.py, store.py (mod) lang durchreichen, cache_key(..., lang)
app/ai/retrieval.py        (mod) englische Stoppwörter
app/ai/prewarm.py          (mod) --lang
app/sources/icd11.py       (mod) Sprache je Anfrage
app/seed_data/*.py, links.py (mod) title_en, sections_en, keywords_en, label_en
tests/test_i18n.py, test_seed_translations.py (neu)
frontend/src/i18n/         (neu) messages.de.ts, messages.en.ts, I18nProvider.tsx, localized.ts,
                                 LanguageSwitch.tsx
frontend/src/lib/api.ts, format.ts, types.ts (mod)
frontend/src/test/utils.tsx (mod) I18nProvider, Option lang (Standard "de")
frontend/src/**            (mod) Texte → t()
frontend/e2e/*.ts          (mod) lang=de für bestehende Abläufe, i18n.spec.ts neu
README.md, AGENTS.md, docs/* (mod)
```

---

### Task 1: Sprachermittlung und lokalisierte Servermeldungen

**Files:** `app/i18n.py`, `app/auth.py`, `app/routers/auth.py`, `app/routers/ai.py`, `app/ai/store.py`, `app/ai/service.py`, `app/demo.py`, `app/spa.py`, Tests `tests/test_i18n.py`, `tests/test_auth.py`, `tests/test_ai_api.py`

**Interfaces:**
- Produces:
  - `Lang = Literal["en", "de"]`, `DEFAULT_LANG: Lang = "en"`.
  - `parse_language(header: str | None) -> Lang`: erster Eintrag, nur der Hauptteil (`de-AT;q=0.9` → `de`), sonst `en`.
  - `request_language(request: Request) -> Lang` (Dependency) und `RequestLang = Annotated[Lang, Depends(request_language)]`.
  - `message(code: str, lang: Lang) -> str` mit den Codes: `invalid_login`, `forbidden`, `ai_limit`, `ai_incomplete`, `ai_no_entries`, `ai_no_streaming`, `ai_no_abstract`. Unbekannter Code → `KeyError`.
- Consumes: bestehende `HTTPException`-Stellen. Der Code `ai_not_configured` bleibt ein Maschinencode.
- Das Protokoll `demo_reset` speichert einen englischen Text („Example data restored (47 entries)“); die Entwicklerseite in `spa.py` wird englisch.

- [ ] **Step 1: Tests**
  - `test_i18n.py`: `parse_language` für `None`, `""`, `de`, `de-AT,de;q=0.9`, `EN-gb`, `fr` (→ en), Müll.
  - `test_login_error_follows_the_header`: falsches Passwort mit `Accept-Language: de` → „Benutzername oder Passwort falsch“, mit `en` → „Wrong username or password“, ohne Header → englisch.
  - `test_forbidden_and_limit_messages_are_localized`: Patient ruft `/api/audit` (403) in beiden Sprachen; erschöpftes KI-Kontingent (429) in beiden Sprachen.
  - `test_every_message_exists_in_both_languages`: für jeden Code beide Sprachen, gleiche `{}`-Platzhalter.
  - Bestehende Tests, die deutsche Texte erwarten (`test_auth.py`, `test_ai_api.py` „keine passenden“), senden `Accept-Language: de`.
- [ ] **Step 2:** `pytest tests/test_i18n.py tests/test_auth.py tests/test_ai_api.py` → FAIL
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** `pytest`, `ruff check . && ruff format --check .` → PASS
- [ ] **Step 5:** Commit `feat(i18n): request language and localized server messages`

### Task 2: Englische Inhaltsfelder, Archiv, Suche

**Files:** `app/models.py`, `app/database.py`, `app/content.py`, `app/schemas.py`, `app/services.py`, `app/archive.py`, Tests `tests/test_document_fields.py`, `tests/test_schema_upgrade.py`, `tests/test_admin_api.py`, `tests/test_documents_api.py`

**Interfaces:**
- Produces:
  - `SECTION_LABELS: dict[Lang, dict[str, str]]`, `compose_content(sections, lang: Lang = "de") -> str`.
  - `DocumentCreate`/`DocumentUpdate`: `title_en`, `content_en`, `sections_en`, `keywords_en` (alle optional; `null` leert). `sections_en` setzt `content_en` neu zusammen; `content_en` ohne `sections_en` setzt `sections_en = null` (wie auf Deutsch).
  - `DocumentOut` und `ArchiveEntry`: alle vier Felder, `keywords_en` Standard `[]`, `null` aus alten Zeilen wird `[]`.
  - `FurtherReadingLink.label_en: str | None = None`.
  - `ADDED_COLUMNS`: `title_en VARCHAR(200)`, `content_en TEXT`, `sections_en JSON`, `keywords_en JSON DEFAULT '[]'`.
  - Suche: Titel-Treffer in `title_en` zählen 3, `keywords_en` 2, `content_en` 1 (dieselben Gewichte, JSON-Syntaxschutz auch für `keywords_en`).

- [ ] **Step 1: Tests**
  - Anlegen mit `sections_en` ohne `content_en` → `content_en` mit englischen Abschnittsnamen („Definition\n…\n\nSymptoms\n…“).
  - PATCH nur `content_en` → `sections_en` null; PATCH `title_en: null` leert nur den Titel.
  - Ungültig (422): `title_en` mit 2 Zeichen, `sections_en: {}`, `keywords_en` mit 21 Wörtern.
  - Archiv-Roundtrip behält alle Felder und `label_en`; ein altes Archiv (nur deutsche Felder) stellt mit Standardwerten wieder her.
  - Schemaupgrade: alte `documents`-Tabelle erhält die vier Spalten, Zeile liest sich mit `keywords_en == []`.
  - Suche: Eintrag `title="Erkältung"`, `title_en="Common cold"` → Suche „cold“ findet ihn, „Erkältung“ ebenso; Titeltreffer in `title_en` schlägt einen Inhaltstreffer; ein Term mit `"` überspringt `keywords_en` ohne Fehler.
- [ ] **Step 2:** FAIL bestätigen
- [ ] **Step 3:** Implementieren (Abschnitte und Änderungslogik analog zu `sections`/`content`)
- [ ] **Step 4:** `pytest`, Ruff → PASS
- [ ] **Step 5:** Commit `feat(content): optional English version of entries, searchable and archived`

### Task 3: KI und ICD-11 in der Anfragesprache

**Files:** `app/ai/prompts.py`, `app/ai/service.py`, `app/ai/store.py`, `app/ai/retrieval.py`, `app/ai/prewarm.py`, `app/routers/ai.py`, `app/routers/sources.py`, `app/sources/icd11.py`, Tests `tests/test_ai_api.py`, `tests/test_sources_icd11.py`

**Interfaces:**
- Produces:
  - `prompts.messages(feature, role, inputs, lang: Lang = "de")`: Systemtext englisch mit „Answer in English/German.“ (Entwurf: immer Deutsch); `prompts.notice(lang)`.
  - `store.cache_key(feature, document_id, inputs, role, settings, lang: Lang = "de")`: für `de` identisch zum heutigen Schlüssel, für `en` mit angehängter Sprache.
  - `service.document_inputs(document, lang: Lang = "de")`: für `en` Titel, Inhalt und Abschnitte der englischen Fassung, wo vorhanden.
  - `service.execute(..., lang: Lang = "de")`; die Router reichen `RequestLang` durch. `ask` zitiert Titel und liefert Inhalt in der Anfragesprache; „keine passenden Einträge“ lokalisiert.
  - `retrieval.QUESTION_WORDS` enthält zusätzlich englische Frage- und Füllwörter.
  - `icd11.lookup_code(client, code, settings, language: str | None = None)` (Standard: `settings.icd_language`); der Endpunkt übergibt die Anfragesprache, der Cache-Schlüssel enthält sie.
  - `prewarm(db, settings, provider, limit=None, pause=0, lang: Lang = "de")`, CLI `--lang en|de|both`.

- [ ] **Step 1: Tests**
  - Englische Anfrage: Systemtext enthält „Answer in English“, deutsche „Answer in German“; Entwurf bei `en` weiterhin „German“.
  - `test_german_cache_key_is_unchanged`: fester erwarteter Hash für eine feste Eingabe (aus dem heutigen Code berechnet).
  - Gleiche Anfrage in `en` und `de` ergibt zwei Cache-Einträge, Wiederholung je Sprache trifft den Cache (`cached: true`).
  - `document_inputs(doc, "en")` nutzt `title_en`/`sections_en`, fällt je Feld auf Deutsch zurück.
  - `ask`: „What helps with a cold?“ findet den Eintrag über den englischen Titel; Antwort lokalisiert, Zitat-Titel englisch.
  - ICD-Endpunkt: `Accept-Language: en` → WHO-Anfrage mit `Accept-Language: en`, Antwort `language == "en"`; getrennte Cache-Einträge je Sprache.
  - Prewarm `lang="en"` schreibt englische Schlüssel; `both` macht bei einem Eintrag 8 Varianten × 2 Sprachen = 16 Aufrufe (47 Einträge: 752).
- [ ] **Step 2:** FAIL bestätigen
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** `pytest`, Ruff → PASS
- [ ] **Step 5:** Commit `feat(ai): answers, cache and ICD-11 in the request language`

### Task 4: Englische Fassung der 47 Beispieleinträge

**Files:** `app/seed_data/<fach>.py` (16 Module), `app/seed_data/links.py`, `app/seed.py`, Test `tests/test_seed_translations.py`

**Interfaces:**
- Jeder Eintrag erhält `title_en`, `sections_en` (dieselben Schlüssel wie `sections`) und `keywords_en` (5–8 Begriffe). Die Link-Helfer liefern zusätzlich `label_en` („Austrian health portal: …“, „MedlinePlus (NIH): …“, „WHO fact sheet: …“). `seed.py` reicht die Felder an `DocumentCreate` durch.

- [ ] **Step 1: Tests** (`test_seed_translations.py`, parametrisiert je Eintrag)
  - `title_en` vorhanden und verschieden vom deutschen Titel (außer Namen wie „Burnout“).
  - `sections_en` hat exakt die Schlüssel von `sections`, kein Abschnitt leer.
  - `keywords_en` 5–8 Einträge ohne Duplikate.
  - Kein deutscher Text: weder `[äöüßÄÖÜ]` noch die Funktionswörter `und`, `der`, `die`, `das`, `nicht`, `bei`, `mit` als ganzes Wort in `title_en`, `sections_en`, `keywords_en`.
  - Jeder Weiterlesen-Link hat `label_en`.
  - Nach `reset_demo` sind `content_en` und `keywords_en` in der Datenbank gesetzt und die Suche „migraine“ findet „Migräne“.
- [ ] **Step 2:** FAIL (alle Einträge)
- [ ] **Step 3:** Übersetzen in drei Commits, je ein Drittel der Module. Redaktionell, Lehrbuchniveau, ohne Dosierungen. Fachbegriffe nach ICD-11 (englisch) und MedlinePlus; „Notruf 144“ → „emergency number 144 (Austria)“; „Telefonseelsorge 142“ → „Austrian crisis line 142“.
- [ ] **Step 4:** `pytest`, Ruff → PASS; `python scripts/check_seed_sources.py` unverändert grün
- [ ] **Step 5:** Commits `content: English version of entries (1/3)` … `(3/3)`

### Task 5: Übersetzungsschicht im Frontend

**Files:** `frontend/src/i18n/*`, `frontend/src/lib/api.ts`, `frontend/src/lib/format.ts`, `frontend/src/lib/types.ts`, `frontend/src/main.tsx`, `frontend/src/test/utils.tsx`, `frontend/index.html`, Tests `frontend/src/i18n/*.test.tsx`, `frontend/src/lib/api.test.ts`, `frontend/src/lib/format.test.ts`

**Interfaces:**
- Produces:
  - `messages.de.ts`: `export const de = {…} as const`; `export type MessageKey = keyof typeof de`. `messages.en.ts`: `export const en: Record<MessageKey, string>`. Beide starten mit den Schlüsseln der gemeinsamen Teile (Fachgebiete `category.<Name>`, Dokumenttypen `docType.<Name>`, Rollen, Abschnitte, Hinweis, Notruf).
  - `I18nProvider({ lang?: Lang, children })`: liest/schreibt `medkb:lang` (Standard `en`, Speicher gesperrt → nur Arbeitsspeicher), setzt `document.documentElement.lang` und `setApiLanguage`.
  - `useI18n(): { lang, setLang, t, locale }`; `t(key, params?)` ersetzt `{name}`; mit `params.count` wählt es `key_one`/`key_other` (`Intl.PluralRules`).
  - `LanguageSwitch({ tone?: 'rail' | 'surface' })`: zwei Schaltflächen `EN`/`DE` mit `aria-pressed`, Gruppenname `Language`/`Sprache`.
  - `format.ts`: `formatDate(iso, lang)`, `formatDay(iso, lang)`, `formatRelative(iso, lang, now?)`, `formatNumber(n, lang)`; Locale `en-GB`/`de-AT`.
  - `api()` sendet `Accept-Language`; Fehlertext-Fallback „Error {status}“/„Fehler {status}“.
  - `renderWithProviders(ui, { lang = 'de', … })` umhüllt mit `I18nProvider`.

- [ ] **Step 1: Tests**
  - Vollständigkeit: `Object.keys(en)` gleich `Object.keys(de)`; je Schlüssel dieselben `{platzhalter}`; `_one`/`_other` stehen paarweise.
  - `t`: Platzhalter, Plural (`count: 1` / `count: 2`), unbekannter Schlüssel liefert den Schlüssel (kein Absturz).
  - Provider: Standard `en`; gespeicherte Wahl `de` wird gelesen; `setLang('de')` schreibt `localStorage` und `<html lang>`; ohne Speicherzugriff keine Ausnahme.
  - `LanguageSwitch` wechselt die Sprache und lässt den umgebenden Zustand unberührt (ein Feld behält seinen Wert).
  - `api()` sendet `Accept-Language: en` bzw. `de`.
  - `format`: `formatDate` und `formatRelative` je Sprache.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren; `index.html` `lang="en"`
- [ ] **Step 4:** `npm run lint && npm run typecheck && npm test` → PASS
- [ ] **Step 5:** Commit `feat(i18n): translation layer, language switch and locale-aware formatting`

### Task 6: Rahmen und Anmeldung übersetzen

**Files:** `components/layout/{Sidebar,Topbar,CommandPalette,AppShell,ThemeToggle}.tsx`, `features/auth/{LoginPage,guards}.tsx`, `features/{RouteError,NotFoundPage}.tsx`, `lib/auth.ts`, `components/feedback/*`, Tests je Komponente

**Interfaces:** Alle Texte über `t()`. Der Umschalter sitzt in der Seitenleiste unter dem Theme-Umschalter und auf der Login-Seite (Desktop-Rail, Handy-Leiste). `ROLE_LABELS` wird zu Schlüsseln `role.admin` usw.

- [ ] **Step 1: Tests** (je Datei `lang="de"` unverändert, dazu Englisch)
  - Login in `en`: Überschrift „Sign in“, drei Rollenkarten „Open as doctor/patient/admin“, Hinweiszeile englisch; der Umschalter wechselt zu Deutsch und zurück.
  - Seitenleiste in `en`: „Home“, „Knowledge base“, „AI assistant“, „Sign out“; Befehlspalette „Search entries, symptoms, diagnoses …“.
  - 403-Seite und NotFound in `en`.
- [ ] **Step 2–4:** FAIL → Implementieren → `lint`/`typecheck`/`test` grün
- [ ] **Step 5:** Commit `feat(i18n): shell, navigation and login in English and German`

### Task 7: Wissensdatenbank, Eintrag, Quellen übersetzen (mit Inhaltsrückfall)

**Files:** `features/documents/**`, `features/documents/sources/**`, `i18n/localized.ts`, `lib/categories.ts`, `components/specialty/*`, Tests

**Interfaces:**
- Produces: `localized(document, lang) -> { title, content, sections, keywords, fallback: boolean }`: je Feld englisch, sonst deutsch; `fallback` ist `true`, wenn in `en` weder Titel noch Inhalt eine englische Fassung haben. `FurtherReadingLink` nutzt `label_en`.
- `DocumentCard`, `DocumentPage`, `SectionedContent` (Abschnittsnamen aus `t`), `FurtherReading`, Quellenpanels, `SpecialtyStrip`, Filter und `ClassificationExplainer` nutzen `t()` und `localized()`. Fachgebiete und Typen über `category.*`/`docType.*`.
- `ClassificationExplainer` ergänzt in `en`: „The rule-based classifier works on German text; matched terms are German word stems.“

- [ ] **Step 1: Tests**
  - `localized`: vier Fälle (beide Fassungen, nur Deutsch, Teilfassung, Sprache `de`).
  - `DocumentPage` in `en`: englischer Titel und englische Abschnitte, Weiterlesen-Beschriftung `label_en`; ohne englische Fassung deutscher Text mit „Only available in German“ (Rolle `status`).
  - `DocumentCard` zeigt den englischen Titel und „Cardiology“ am Reiter; Suche im Wissensdatenbank-Test sendet unveränderte Query.
  - Quellenpanels in `en`: „PubMed is currently unreachable.“, „abgerufen“ → „retrieved 5 minutes ago“, ICD-Hinweis „German version: WHO prerelease“ nur bei `de`.
- [ ] **Step 2–4:** FAIL → Implementieren → grün
- [ ] **Step 5:** Commit `feat(i18n): knowledge base, entries and sources in both languages`

### Task 8: Dashboard, Startseite, Admin übersetzen

**Files:** `features/dashboard/**`, `features/home/*`, `features/admin/**`, `lib/audit.ts`, Tests

**Interfaces:** `AUDIT_ACTIONS` liefert Schlüssel statt Texte; das Änderungsprotokoll zeigt `detail` unverändert. Die Schnellsuchen der Patientenstartseite sind je Sprache eigene Begriffe („Headache“, „Cough“, „Back pain“, „High blood pressure“). Die Diagrammachse und der Satz „47 entries in 16 specialties …“ nutzen `t` mit `count` und `formatNumber`.

- [ ] **Step 1: Tests**
  - Dashboard in `en`: Überschrift „Overview“, Zusammenfassungssatz mit Plural („1 change“/„3 changes“).
  - Patientenstartseite: englische Schnellsuchen verlinken auf `/wissen?q=Headache`; Notfallhinweis „In an emergency call 144 (Austria).“
  - Admin: Tabs, Tabellenköpfe, Aktionsnamen in `en`; Rollen in der Nutzertabelle.
- [ ] **Step 2–4:** FAIL → Implementieren → grün
- [ ] **Step 5:** Commit `feat(i18n): dashboard, home and admin in both languages`

### Task 9: Editor und KI-Oberfläche, englische Fassung im Editor

**Files:** `features/editor/**`, `features/ai/**`, `features/ai/client.ts`, Tests

**Interfaces:**
- Der Editor erhält einen aufklappbaren Bereich „English version“ (Titel, Text oder Abschnitte, Schlagwörter), gesendet als `title_en`, `content_en`/`sections_en`, `keywords_en`; Leeres wird als `null` gesendet. Die Live-Klassifikation nutzt weiter nur den deutschen Text. Die Vorschau der zusammengesetzten Abschnitte nutzt `SECTION_LABELS` der jeweiligen Sprache.
- KI-Panels: Bedienelemente und Fehlertexte über `t()`; die Antwort kommt vom Server in der Anfragesprache. Ein Sprachwechsel verwirft das Ergebnis des Panels und bricht eine laufende Anfrage ab (`AbortController`); „KI-generiert“ → „AI-generated“.
- Der Entwurfsknopf nennt: „Draft is written in German.“

- [ ] **Step 1: Tests**
  - Editor in `en`: Beschriftungen englisch; Eingaben im Bereich „English version“ landen im POST/PATCH-Körper; leerer Bereich sendet keine `_en`-Felder.
  - Sprachwechsel mit ungespeicherten Änderungen: Feldwerte bleiben (Review Focus 2).
  - Sprachwechsel während einer streamenden KI-Antwort: kein Mischtext, Anfrage abgebrochen, Panel leer.
  - KI-Panels in `en`: Fehlercodes `ai_not_configured` und 429 in englischen Texten.
- [ ] **Step 2–4:** FAIL → Implementieren → grün
- [ ] **Step 5:** Commit `feat(i18n): editor English version and AI panels in both languages`

### Task 10: Browser-Tests und Dokumentation

**Files:** `frontend/e2e/*.spec.ts`, `frontend/e2e/i18n.spec.ts`, `README.md`, `AGENTS.md`, `docs/NEXT_STEPS.md`, `docs/superpowers/specs/2026-10-10-medkb-v2-design.md`

- [ ] **Step 1: e2e**
  - Bestehende Abläufe setzen `localStorage['medkb:lang']='de'` über `addInitScript` (in `loginAs` und `ai.spec.ts`).
  - Neu `i18n.spec.ts`: Ohne Vorwahl ist die Login-Seite englisch; „Open as doctor“ führt zu „Overview“; der Wechsel zu Deutsch gilt nach Reload und auf dem Eintrag „Migräne“ (Titel, Abschnitte); „Migraine“ im Suchfeld findet den Eintrag; ein Eintrag ohne englische Fassung zeigt den Hinweis; der Handy-Login zeigt den Umschalter ohne Überlauf.
- [ ] **Step 2:** `npm run build` und `npm run e2e` (absoluter `PYTHON`-Pfad) → grün
- [ ] **Step 3: Doku**
  - README: Funktionsliste „English and German“, Demo-Hinweis, Konfiguration (`Accept-Language`).
  - AGENTS: Hinweis in Working rules („UI text English, German switch: new texts go to both dictionaries“), Gotchas (Sprache in Tests, `lang="de"` Standard der Testhilfe, KI-Cache-Schlüssel).
  - v2-Spec §1: „Nicht im Umfang“ verweist auf die neue Spec.
  - Aufnahmen: `frontend/scripts/record-demo.mjs` auf Englisch; README-Screenshots und GIF neu.
- [ ] **Step 4:** Alle Prüfungen (`pytest`, Ruff, `lint`, `typecheck`, `test`, `build`, `e2e`) grün
- [ ] **Step 5:** Commit `test(e2e): English default and language switch; docs and media`

### Task 11: Veröffentlichen und live prüfen (mit dem Nutzer)

- [ ] **Step 1:** PR, CI grün, Merge nach `main`, Render deployt.
- [ ] **Step 2: Live-Abnahme:**
  - Standard englisch auf `/login`.
  - Demo je Rolle; Wechsel DE ↔ EN bleibt nach Reload.
  - Eintrag „Migraine“ in beiden Sprachen; PubMed, ICD-11 (`en` und `de`), openFDA.
  - KI: ein Aufruf je Sprache.
  - Suche „cold“ und „Erkältung“.
- [ ] **Step 3: Englischer KI-Cache:** nach dem nächsten UTC-Tageswechsel `python -m app.ai.prewarm --lang en --pause 4` gegen die Neon-Datenbank (376 Aufrufe, das heutige Budget reicht nicht).
- [ ] **Step 4:** Ergebnis in `docs/reviews/2026-10-12-mehrsprachigkeit.md`, README-Live-Hinweis, AGENTS-Status.
- [ ] **Step 5:** Commit `docs: bilingual release verified live`
