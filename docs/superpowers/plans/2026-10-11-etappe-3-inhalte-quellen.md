# Etappe 3 – Datenmodell, Inhalte, externe Quellen – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Einträge werden strukturiert (Sektionen, englischer Fachbegriff, ICD-11-Code, Wirkstoffe, Weiterlesen) und tragen echte Live-Daten aus PubMed, WHO ICD-11 und openFDA. Die Wissensbasis wächst auf rund 45 Lehrbuch-Einträge in 16 Fachgebieten.

**Architecture:**
- `documents` bekommt sechs neue Spalten (über `ADDED_COLUMNS` auch in bestehenden Datenbanken).
- Liegen Sektionen vor, setzt der Server `content` daraus zusammen. Suche und Klassifikation bleiben dadurch unverändert.
- Ein neues Paket `app/sources/` kapselt die drei Fremd-APIs: synchrones `httpx`, 8 s Timeout, 24-h-Cache in der Tabelle `source_cache`.
- Der Router `/api/sources` (doctor, admin) liefert nie einen 5xx-Fehler wegen einer Fremd-API. Er antwortet immer 200 mit einem `status`.
- Im Frontend bekommt die Detailseite Tabs (Inhalt · ICD-11 · Studien · Medikamente), das Dashboard die Kachel „Neueste Studien“ und der Editor die neuen Felder.

**Tech Stack:** wie Etappe 2, dazu `httpx` (Laufzeit) und `respx` (Tests).

**Spec:** `docs/superpowers/specs/2026-10-10-medkb-v2-design.md`: Abschnitte 4 (ohne `ai_cache`/`ai_usage`, die gehören zu Etappe 4), 6 und 7 sowie die Quellen-Teile von 8, 9 und 10. **Gotchas:** `AGENTS.md`.

## Global Constraints

- **Neue Dokumentfelder** (Spec §4):
  - `term_en`: String(200), nullable. Erlaubte Zeichen: `^[A-Za-z0-9 ,'()\-]+$`, sonst 422.
  - `icd11_code`: String(20), nullable, wird großgeschrieben. Muster: `^[0-9A-Z]{4}(\.[0-9A-Z]{1,2})?$`.
  - `medications`: JSON-Liste, Default `[]`. Höchstens 10 Wirkstoffe zu je 2–60 Zeichen (`^[A-Za-z][A-Za-z \-]+$`), kleingeschrieben und ohne Duplikate.
  - `sections`: JSON, nullable. Felder `definition`, `symptoms`, `causes`, `diagnostics`, `therapy` und `red_flags`, jedes optional und höchstens 5000 Zeichen. Mindestens eines muss nicht leer sein.
  - `further_reading`: JSON-Liste aus `{label, url}`, Default `[]`, höchstens 8 Einträge. `label` hat 1–100 Zeichen, `url` muss mit `https://` beginnen.
  - `ai_generated`: bool, Default `false`. Wird nur beim Anlegen gesetzt.
- **Zusammensetzen von `content`.** Labels in fester Reihenfolge: Definition, Symptome, Ursachen, Diagnostik, Therapie, Warnzeichen. Pro nicht leerer Sektion `"{Label}\n{Text}"`, die Blöcke getrennt durch `"\n\n"`. Ein PATCH, das nur `content` schickt, setzt `sections = null`, der Eintrag wird damit zu Freitext.
- **Quellen** (Spec §6), alle unter `/api/sources`:
  - Rechte: nur doctor und admin. patient bekommt 403, ohne Login gibt es 401.
  - Timeout `SOURCES_TIMEOUT` = 8 s, Cache `SOURCE_CACHE_HOURS` = 24.
  - Antwort immer `{status, fetched_at, data}`. `status` ist einer von:
    - `ok`
    - `empty`: am Eintrag fehlt der Suchbegriff, oder es gibt keine Treffer
    - `unavailable`: Timeout, HTTP-Fehler oder unerwartetes Format
    - `not_configured`: ICD-Keys fehlen
  - Gecacht werden nur `ok` und `empty`, und zwar pro Abfrage (Quelle + Suchwert), nicht pro Dokument-ID.
- **Externe Endpunkte und Konfiguration:**
  - PubMed: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` mit `esearch.fcgi` und `esummary.fcgi`. Parameter `db=pubmed`, `retmode=json`, `sort=pub_date`, `tool=medkb`, optional `api_key=NCBI_API_KEY`.
  - ICD-11:
    - Token: `https://icdaccessmanagement.who.int/connect/token`, `grant_type=client_credentials`, `scope=icdapi_access`, Keys aus `ICD_CLIENT_ID`/`ICD_CLIENT_SECRET`.
    - Daten: `https://id.who.int/icd/release/11/{ICD_RELEASE}/mms/codeinfo/{code}`, danach die `stemId`.
    - Header `API-Version: v2`, `Accept-Language: {ICD_LANGUAGE}`, `Accept: application/json`.
    - Defaults: `ICD_RELEASE=2026-01`, `ICD_LANGUAGE=de` (Deutsch ist dort Prerelease).
    - Browser-Link: `https://icd.who.int/browse/{release}/mms/{language}#{entity_id}`.
  - openFDA: `https://api.fda.gov/drug/label.json?search=openfda.generic_name:"{wirkstoff}"&limit=1`. Eine 404-Antwort bedeutet „kein Label“, nicht `unavailable`.
- **16 Fachgebiete**, in dieser Reihenfolge (bei Gleichstand gewinnt das frühere, Allgemeinmedizin steht zuletzt): HNO, Augenheilkunde, Neurologie, Kardiologie, Pneumologie, Gastroenterologie, Endokrinologie, Urologie, Gynäkologie, Dermatologie, Orthopädie, Pädiatrie, Psychiatrie, Infektiologie, Innere Medizin, Allgemeinmedizin.
- **Inhalte:**
  - 44–48 Einträge, jedes Fachgebiet mit mindestens 2.
  - Diagnose- und Symptom-Einträge haben alle sechs Sektionen, alle anderen mindestens zwei.
  - Jeder Eintrag hat `term_en`, krankheitsbezogene Einträge zusätzlich `icd11_code`.
  - Quelle: „Redaktionelle Demo-Inhalte auf Lehrbuchniveau – keine medizinische Beratung“.
  - Weiterlesen-Links nur von gesundheit.gv.at, awmf.org, who.int, medlineplus.gov oder nih.gov. Jeder Link ist einmal live geprüft. Es gibt keine erfundenen URLs.
- **UI:**
  - Quellen werden sichtbar benannt („PubMed · NCBI“, „WHO ICD-11“, „openFDA · US-FDA-Produktinformation, englisch“), jeweils mit „abgerufen {relativ}“.
  - Patienten lösen keine Quellen-Abfragen aus.
- **Alles aus Etappe 1 und 2 bleibt:**
  - UI-Texte Deutsch.
  - Hinweis „keine medizinische Beratung“.
  - Die Regeln aus `DESIGN.md`: Fachgebietsfarbe nie als Textfarbe, `color-mix` nur in oklab.
  - Test zuerst, ein Commit pro Aufgabe.
  - Keine echten Netzwerkaufrufe in Tests.

## Review Focus

1. Fremd-APIs liefern Unerwartetes: Bei PubMed fehlt in `esummary` ein Feld, openFDA antwortet 404 für einen unbekannten Wirkstoff, der ICD-Token-Endpunkt antwortet mit falschen Keys 401, eine Antwort ist kein JSON oder läuft in den Timeout. Erwartet wird jeweils der passende `status` (`unavailable`, `empty` oder `ok` mit Lücken), nie ein 500 und nichts im Cache. (Tasks 5–7)
2. Die SQLite-Datenbank aus Etappe 2 oder ein altes Archiv ohne die neuen Felder. Der Start fügt die Spalten hinzu, alte Zeilen lesen sich als `[]`, `null` bzw. `false`, ein Restore setzt die Defaults. `DocumentOut` stürzt nie an `None` in Listenfeldern ab. (Tasks 1 und 2)
3. Ein Admin bearbeitet einen gegliederten Eintrag:
   - Nur `content` → `sections` wird `null`, der Text bleibt.
   - Nur `sections` → `content` wird neu zusammengesetzt.
   - Die Kategorie ändert sich nur bei `reclassify`.

   Die Detailseite zeigt danach die richtige Darstellung. (Tasks 1 und 12)
4. Zwei gleichzeitige Anfragen schreiben denselben Cache-Key (PostgreSQL `IntegrityError`) → beide antworten 200. Ändert sich `term_en`, wird nicht der alte Treffer ausgeliefert, weil der Key den Suchwert enthält. (Task 5)
5. Ein Patient öffnet einen Eintrag: keine Quellen-Tabs, keine Netzwerk-Anfrage an `/api/sources` (also auch keine 403 im Log), Sektionen und „Warnzeichen“-Hinweis sichtbar. Ein Arzt wechselt Tabs: Jede Quelle wird erst beim ersten Öffnen ihres Tabs geladen. (Task 10)

---

## File Structure

```
app/
  models.py              (mod) Document: term_en, icd11_code, medications, sections,
                               further_reading, ai_generated; SourceCache
  database.py            (mod) ADDED_COLUMNS für die sechs Spalten (mit Defaults)
  schemas.py             (mod) Sections, FurtherReadingLink, neue Felder in Create/Update/Out,
                               ArchiveEntry, ClassifyRequest (content oder sections),
                               SourceResult, Studies-/Icd11-/Medication-Ausgaben
  content.py             (neu) SECTION_LABELS, compose_content(sections) -> str
  services.py            (mod) Felder anlegen/ändern, content aus Sektionen
  archive.py             (mod) neue Felder exportieren/wiederherstellen
  classifier.py          (mod) 16 Fachgebiete
  seed_data/__init__.py  (neu, ersetzt seed_data.py) SOURCE, SEED_DOCUMENTS
  seed_data/<fach>.py    (neu) ein Modul pro Fachgebiet (16), je ENTRIES: list[dict]
  seed.py                (mod) alle Felder übernehmen
  config.py              (mod) ncbi_api_key, icd_client_id, icd_client_secret, icd_release,
                               icd_language, sources_timeout, source_cache_hours
  sources/__init__.py    (neu)
  sources/cache.py       (neu) cached(db, key, settings, fetch) -> SourceResult
  sources/pubmed.py      (neu) search_studies(...), CATEGORY_TERMS
  sources/icd11.py       (neu) lookup_code(...), Token-Cache
  sources/openfda.py     (neu) fetch_label(...)
  routers/sources.py     (neu) /api/sources/...
  main.py                (mod) Router einbinden
scripts/check_seed_sources.py (neu) prüft Weiterlesen-Links live, mit ICD-Keys auch die Codes
tests/
  conftest.py            (mod) autouse-Fixture `network` (respx, blockiert alles Unbekannte)
  test_document_fields.py (neu)
  test_schema_upgrade.py (mod)
  test_admin_api.py      (mod) Archiv mit neuen Feldern, altes Archiv
  test_classifier.py     (mod) 16 Fachgebiete
  test_seed_content.py   (neu) Inhaltsregeln
  test_sources_pubmed.py, test_sources_icd11.py, test_sources_openfda.py (neu)
  test_permissions.py    (mod) Quellen-Endpunkte
requirements.txt         (mod) httpx>=0.27,<1
requirements-dev.txt     (mod) respx>=0.21
.env.example, docker-compose.yml (mod) Quellen-Variablen
frontend/src/
  lib/types.ts           (mod) Document-Felder, Sections, SourceResult<T>, Study, Icd11Entry,
                               MedicationLabel
  lib/queries.ts         (mod) useStudies, useIcd11, useMedications, useLatestStudies
  lib/categories.ts      (mod) 16 Farben und Icons
  lib/sections.ts        (neu) SECTION_ORDER, SECTION_LABELS
  features/documents/SectionedContent.tsx (neu) Sektionen + Warnzeichen-Kasten
  features/documents/FurtherReading.tsx   (neu)
  features/documents/sources/SourcePanel.tsx  (neu) gemeinsamer Rahmen: Status, Provenienz
  features/documents/sources/StudiesPanel.tsx, Icd11Panel.tsx, MedicationsPanel.tsx (neu)
  features/documents/DocumentPage.tsx     (mod) Tabs für Staff, Sektionen für alle
  features/dashboard/LatestStudies.tsx    (neu)
  features/dashboard/DashboardPage.tsx    (mod)
  features/editor/EditorPage.tsx          (mod) Fachbegriff, ICD-11, Wirkstoffe, Abschnitte
  features/editor/SectionFields.tsx       (neu)
frontend/e2e/smoke.spec.ts (mod) 16 Fachgebiete, /api/sources per page.route gemockt
AGENTS.md, docs/BACKLOG.md (mod)
```

---

### Task 1: Neue Dokumentfelder in Modell, Schema und Services

**Files:** `app/models.py`, `app/database.py`, `app/content.py`, `app/schemas.py`, `app/services.py`, `app/routers/documents.py` (ClassifyRequest), Tests `tests/test_document_fields.py`, `tests/test_schema_upgrade.py`

**Interfaces:**
- Produces:
  - Spalten am `Document`:
    - `term_en: str | None`
    - `icd11_code: str | None`
    - `medications: list[str]` (JSON, default list)
    - `sections: dict | None`
    - `further_reading: list[dict]` (JSON, default list)
    - `ai_generated: bool` (default False)
  - `ADDED_COLUMNS` um sechs Einträge erweitert. Typen: `VARCHAR(200)`, `VARCHAR(20)`, `JSON DEFAULT '[]'`, `JSON`, `JSON DEFAULT '[]'`, `BOOLEAN DEFAULT FALSE`.
  - `app/content.py`:
    - `SECTION_KEYS = ("definition", "symptoms", "causes", "diagnostics", "therapy", "red_flags")`
    - `SECTION_LABELS: dict[str, str]`
    - `compose_content(sections: Mapping[str, str | None]) -> str`
  - `schemas.Sections` (6 optionale Felder, Validator „mindestens eines nicht leer“, Werte gestrippt, leere Strings werden `None`) und `schemas.FurtherReadingLink(label, url)`.
  - `DocumentCreate`: `content` wird optional. Die neuen Felder `term_en`, `icd11_code`, `medications`, `sections`, `further_reading` und `ai_generated` kommen dazu. Ein Validator verlangt `content` oder `sections`. Sind `sections` gesetzt, ersetzt `compose_content` den Inhalt von `content`.
  - `DocumentUpdate`: dieselben Felder, ohne `ai_generated`. `null` ist erlaubt für `term_en`, `icd11_code` und `sections`. `medications`/`further_reading` dürfen nicht `null` sein.
  - `DocumentOut`: alle neuen Felder. Ein `field_validator(mode="before")` macht aus `None` bei `medications`/`further_reading` `[]` und bei `ai_generated` `False`.
  - `ClassifyRequest`: `content: str = ""` und `sections: Sections | None = None`. Eines von beiden ist Pflicht; mit Sektionen wird klassifiziert, was `compose_content` liefert.

- [ ] **Step 1: Tests schreiben** (`tests/test_document_fields.py`)
  - `test_create_with_sections_composes_content`: POST mit `sections={definition: "A", symptoms: "B"}` und ohne `content` → `content == "Definition\nA\n\nSymptome\nB"`, `sections` kommt zurück, `auto_classified` ist True.
  - `test_create_needs_content_or_sections` → 422.
  - `test_new_fields_roundtrip`:
    - Gesendet: `term_en="Migraine"`, `icd11_code="8a80.1"`, `medications=["Sumatriptan", "sumatriptan", "Ibuprofen"]` und ein https-Link.
    - Erwartet zurück: `icd11_code == "8A80.1"` und `medications == ["sumatriptan", "ibuprofen"]`.
  - `test_invalid_fields_are_rejected` (parametrisiert, jeweils 422):
    - `icd11_code="8A80.123"`
    - `term_en='x" OR 1'`
    - `medications=["1abc"]`
    - `further_reading=[{"label": "x", "url": "javascript:alert(1)"}]`
    - 9 Links
    - `sections={}`
  - `test_patch_content_drops_sections`: Nach dem PATCH mit nur `content` gilt `sections is None`, und `content` ist der neue Text.
  - `test_patch_sections_recomposes_content_without_reclassifying`: Ein Eintrag mit manueller Kategorie „HNO“ bekommt per PATCH neue Sektionen. Danach ist `content` neu, die Kategorie bleibt „HNO“.
  - `test_ai_generated_defaults_false_and_is_not_patchable`: PATCH `{"title": "Neu", "ai_generated": true}` → 200, `ai_generated` bleibt `False`, weil `DocumentUpdate` das Feld nicht kennt und unbekannte Felder ignoriert.
  - `test_classify_accepts_sections`: Sektionen mit „Tinnitus … Trommelfell“ → HNO.
  - In `tests/test_schema_upgrade.py`, `test_adds_document_columns_to_an_old_database`:
    - Alte `documents`-Tabelle ohne die sechs Spalten plus eine Zeile.
    - Danach `create_all` und `upgrade_schema` (zweimal).
    - Erwartet: die Spalten existieren, und die Zeile liest sich über `DocumentOut.model_validate` mit `medications == []` und `ai_generated is False`.
- [ ] **Step 2:** `pytest tests/test_document_fields.py tests/test_schema_upgrade.py` → FAIL
- [ ] **Step 3:** Implementieren. Das Audit-Detail führt geänderte Felder wie bisher auf, mit dem Feldnamen `sections`. `update_document` setzt `sections = None`, wenn `content` ohne `sections` gesendet wird.
- [ ] **Step 4:** `pytest` (ganze Suite) → PASS; `ruff check . && ruff format --check .`
- [ ] **Step 5:** Commit `feat(documents): structured sections, English term, ICD-11 code, medications, further reading`

### Task 2: Archiv mit neuen Feldern

**Files:** `app/archive.py`, `app/schemas.py` (`ArchiveEntry`), Test `tests/test_admin_api.py`

**Interfaces:**
- Consumes: Felder aus Task 1.
- Produces:
  - `ArchiveEntry` bekommt die sechs Felder mit den Defaults aus Task 1. `format_version` bleibt 1, weil alte Dateien gültig bleiben.
  - `restore_archive` schreibt alle Felder.

- [ ] **Step 1: Tests**
  - `test_archive_roundtrip_keeps_new_fields`:
    - Eintrag mit Sektionen, `term_en`, Code, Wirkstoffen und einem Link → Archiv → Löschen → Restore.
    - Erwartet: alle Felder gleich, `content` unverändert.
  - `test_old_archive_without_new_fields_restores_with_defaults`:
    - Handgeschriebene Datei im Format v1 mit nur den alten Feldern → Restore 200.
    - Erwartet: `sections is None`, `medications == []`, `ai_generated is False`.
- [ ] **Step 2:** `pytest tests/test_admin_api.py` → FAIL (der erste Test)
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** `pytest` → PASS
- [ ] **Step 5:** Commit `feat(archive): export and restore the new document fields`

### Task 3: Klassifikator mit 16 Fachgebieten

**Files:** `app/classifier.py`, `tests/test_classifier.py`, `frontend/src/lib/categories.ts`, `frontend/src/lib/categories.test.ts` (neu)

**Interfaces:**
- Produces:
  - `CATEGORIES` in der Reihenfolge der Global Constraints.
  - Das Frontend-Gegenstück `KNOWN_CATEGORIES` in derselben Reihenfolge.

- [ ] **Step 1: Tests**
  - Backend:
    - `test_sixteen_specialties_in_tie_order`: `CATEGORIES ==` Liste aus den Global Constraints.
    - `test_new_specialties_are_recognised` (parametrisiert, je ein typischer Satz):

      | Fachgebiet | Beispielsatz |
      |---|---|
      | Augenheilkunde | „Grauer Star: Linsentrübung, verschwommenes Sehen“ |
      | Pneumologie | „Asthma bronchiale mit Atemnot und Giemen“ |
      | Gastroenterologie | „Reflux, Sodbrennen, Speiseröhre“ |
      | Endokrinologie | „Diabetes, Blutzucker, Insulin“ |
      | Urologie | „Harnwegsinfekt, Brennen beim Wasserlassen, Blase“ |
      | Gynäkologie | „Endometriose, Regelschmerzen, Gebärmutter“ |
      | Infektiologie | „Borreliose nach Zeckenstich, Wanderröte“ |
      | Innere Medizin | „Eisenmangelanämie, Hämoglobin“ |

  - Frontend (`categories.test.ts`):
    - Alle 16 haben einen eigenen Ton.
    - Zwei benachbarte Töne liegen mindestens 20° auseinander.
    - `categoryStyle` liefert für jedes Fachgebiet L 0.62.
- [ ] **Step 2:** `pytest tests/test_classifier.py` und `npm test -- categories` → FAIL
- [ ] **Step 3: Vokabular umbauen**
  - Aus „Innere Medizin“ wandern:
    - Lunge (asthma, bronchitis, pneumonie, lungenentzündung, copd) → Pneumologie
    - Verdauung (magen, darm, sodbrennen, reflux, speiseröhre, gastritis, durchfall, verstopfung, leber, gallen, pankreas, colitis, crohn) → Gastroenterologie
    - Hormone/Stoffwechsel (diabetes, blutzucker, insulin, hba1c, schilddrüse, hashimoto, cholesterin, stoffwechsel) → Endokrinologie
  - Innere Medizin behält anämie, eisenmangel, gicht und niere (Nephrologie) und bekommt unter anderem hämoglobin, niereninsuffizienz, dialyse, rheuma, lupus, ödem.
  - Jedes neue Fachgebiet bekommt 15–30 Stämme mit `^` gegen Fehltreffer. Beispiele:
    - Augenheilkunde: „^auge“, „katarakt“, „glaukom“
    - Urologie: „^blase“, „harnweg“, „prostata“
  - Jedes neue Fachgebiet bekommt sein Farbschema:

    | Fachgebiet | Ton | Chroma | Icon |
    |---|---|---|---|
    | Gynäkologie | 0 | 0.13 | `Venus` |
    | Kardiologie | 22 | 0.17 | |
    | Dermatologie | 45 | 0.13 | |
    | Endokrinologie | 68 | 0.13 | `FlaskConical` |
    | Orthopädie | 90 | 0.12 | |
    | Gastroenterologie | 112 | 0.12 | `Soup` |
    | Innere Medizin | 135 | 0.12 | |
    | Pneumologie | 158 | 0.11 | `Wind` |
    | Infektiologie | 180 | 0.1 | `Microscope` |
    | Allgemeinmedizin | 202 | 0.1 | |
    | Augenheilkunde | 225 | 0.12 | `Eye` |
    | HNO | 248 | 0.13 | |
    | Psychiatrie | 270 | 0.09 | |
    | Neurologie | 292 | 0.15 | |
    | Urologie | 315 | 0.12 | `Droplets` |
    | Pädiatrie | 338 | 0.14 | |

    Die Abstände betragen gleichmäßig 22,5°. Ob es die Icon-Namen gibt, prüft das Typecheck gegen `lucide-react`. Fehlt einer, gilt ein naheliegender Ersatz, festgehalten als Ruling.
  - Die bestehenden Seed-Einträge „Diabetes mellitus Typ 2“ (künftig Endokrinologie) und „Sodbrennen und Reflux“ (künftig Gastroenterologie) bekommen im alten `seed_data.py` ein neues `expected_category`. Task 4 ersetzt die Datei.
- [ ] **Step 4:** `pytest`, `npm test`, `npm run typecheck` → PASS
- [ ] **Step 5:** Commit `feat(classifier): 16 specialties with their own vocabulary and colours`

### Task 4: Rund 45 strukturierte Lehrbuch-Einträge

**Files:**
- `app/seed_data.py` wird gelöscht und durch das Paket `app/seed_data/` ersetzt:
  - `__init__.py` mit `SOURCE` und `SEED_DOCUMENTS`
  - 16 Module, je eines pro Fachgebiet, z. B. `hno.py`, `augenheilkunde.py`
- `app/seed.py`
- `scripts/check_seed_sources.py`
- Test `tests/test_seed_content.py`

**Interfaces:**
- Consumes: Felder aus Task 1, Vokabular aus Task 3.
- Produces:
  - `SEED_DOCUMENTS: list[dict]` mit den Schlüsseln `title`, `doc_type`, `expected_category`, `term_en`, `icd11_code` (optional), `medications` (optional), `sections` und `further_reading`.
  - `seed_if_empty` übernimmt alle Felder. Die Kategorie wählt weiterhin der Klassifikator.

- [ ] **Step 1: Tests** (`tests/test_seed_content.py`)
  - `test_entry_count_and_specialty_coverage`: 44 ≤ n ≤ 48, jedes der 16 Fachgebiete mindestens zweimal als `expected_category`.
  - `test_every_entry_validates`: `DocumentCreate(**fields)` für jeden Eintrag, ohne Fehler.
  - `test_diagnoses_and_symptoms_have_all_six_sections`, die übrigen haben mindestens zwei.
  - `test_every_entry_has_term_en_and_disease_entries_an_icd_code`: Diagnose und Symptom haben einen Code, Anamnese/Leitlinie/Beschreibung/Befund dürfen ohne sein.
  - `test_further_reading_only_from_trusted_hosts`: Hosts ⊆ {www.gesundheit.gv.at, register.awmf.org, www.awmf.org, www.who.int, medlineplus.gov, www.nih.gov, www.ninds.nih.gov, www.niddk.nih.gov, www.nei.nih.gov, www.nhlbi.nih.gov}. Jeder Eintrag hat mindestens einen Link.
  - `test_titles_are_unique`
  - Die bestehenden Tests bleiben unverändert:
    - `test_classifier.py` prüft `expected_category` für alle Einträge.
    - `test_keywords_are_real_words…` verwendet den Eintrag „Schlaganfall – Warnzeichen“, der deshalb bleibt.
    - `test_demo_reset.py` zählt die Einträge.
- [ ] **Step 2:** `pytest tests/test_seed_content.py` → FAIL
- [ ] **Step 3: Inhalte schreiben**
  - Die 18 bisherigen Themen bleiben und werden in Sektionen umgeschrieben, mit gleichen Titeln. e2e sucht „Anamnese bei Kopfschmerzen“.
  - Neu kommen rund 27 Themen dazu, mindestens 2 je neues Fachgebiet.
  - Lehrbuchniveau, je Sektion 1–3 Sätze, keine Dosierungen.
  - Warnzeichen enthalten bei Notfällen „Notruf 144“.
  - ICD-11-Codes aus dem ICD-11-Browser (Release 2026-01) übernehmen. Ist ein Code unsicher, lieber weglassen als raten.
- [ ] **Step 4: `scripts/check_seed_sources.py`**
  - Der Befehl `python scripts/check_seed_sources.py` ruft jede Weiterlesen-URL mit GET ab, mit Redirects und 10 s Timeout, und gibt Code und URL aus. Exit 1 bei einem Status ≠ 200.
  - Mit gesetzten `ICD_CLIENT_ID`/`SECRET` prüft er zusätzlich jeden Code über `app.sources.icd11.lookup_code`. Dieser Teil folgt erst nach Task 6; bis dahin läuft der Code-Abschnitt nur, wenn das Modul importierbar ist.
  - Einmal ausführen und alle toten Links ersetzen.
  - Kein CI-Job, weil er Netzwerk braucht.
- [ ] **Step 5:** `pytest`, Ruff → PASS. `python scripts/check_seed_sources.py` → alle 200.
- [ ] **Step 6:** Commit `feat(content): 46 structured textbook entries across 16 specialties`

### Task 5: Quellen-Cache, Router und PubMed

**Files:**
- `app/config.py`
- `app/models.py` (`SourceCache`)
- `app/schemas.py`
- `app/sources/__init__.py`, `app/sources/cache.py`, `app/sources/pubmed.py`
- `app/routers/sources.py`
- `app/main.py`
- `requirements.txt`, `requirements-dev.txt`
- `tests/conftest.py`, `tests/test_sources_pubmed.py`, `tests/test_permissions.py`

**Interfaces:**
- Produces:
  - `SourceCache(key String(300) PK, payload JSON, fetched_at DateTime(tz))`. Ein Demo-Reset löscht ihn nicht.
  - Neue Settings:
    - `ncbi_api_key: str = ""`
    - `icd_client_id: str = ""`, `icd_client_secret: str = ""`
    - `icd_release: str = "2026-01"`, `icd_language: str = "de"`
    - `sources_timeout: float = 8`
    - `source_cache_hours: float = 24`
  - `SourceStatus = Literal["ok", "empty", "unavailable", "not_configured"]`
  - `SourceResult[T](status, fetched_at: datetime | None, data: T | None)`, ein generisches Pydantic-Modell.
  - `Study(pmid, title, journal, year: int | None, authors: list[str], url)`. `authors` hat höchstens 3 Einträge, bei mehr Autoren folgt „et al.“. `url` hat die Form `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`.
  - `cached(db, key: str, settings, fetch: Callable[[], T | None]) -> SourceResult[T]`:
    - Ein frischer Cache-Treffer wird direkt zurückgegeben.
    - Sonst wird `fetch()` aufgerufen. `None` oder `[]` → `empty`, wird gecacht. Ein Wert → `ok`, wird gecacht.
    - `SourceUnavailable` → `unavailable`, wird nicht gecacht.
    - Speichern per `db.merge`. Ein `IntegrityError` wird per Rollback geschluckt.
  - `class SourceUnavailable(Exception)`
  - `search_studies(client: httpx.Client, query: str, settings, limit: int) -> list[Study]`. Wirft bei Transportfehlern, HTTP ≥ 400 und Formatfehlern `SourceUnavailable`.
  - `CATEGORY_TERMS: dict[str, str]`, je Fachgebiet ein MeSH-Begriff (z. B. Kardiologie → „Cardiovascular Diseases“).
  - Endpunkte (Staff):
    - `GET /api/sources/documents/{id}/studies` → `SourceResult[list[Study]]`. Query `"{term_en}" AND hasabstract`, Limit 5. Ohne `term_en` → `empty` ohne Netz. Cache-Key `pubmed:{query}:5`.
    - `GET /api/sources/latest-studies` → `SourceResult[list[LatestStudies]]` mit `LatestStudies(category, studies: list[Study])`. Die 2 Fachgebiete mit den meisten Einträgen, je 3 Studien, Query `"{CATEGORY_TERMS[c]}"[MeSH Major Topic] AND hasabstract`. Fällt eines der beiden aus → `unavailable`.
  - `tests/conftest.py`, autouse-Fixture `network`:
    - `respx.mock(assert_all_called=False)` mit einer Catch-all-Route, die `httpx.ConnectError` wirft.
    - Gibt den Router zurück, damit Tests eigene Routen davorsetzen können.
    - Leert vor jedem Test den ICD-Token-Cache. Der Teil kommt erst mit Task 6, sobald es das Modul gibt.

- [ ] **Step 1: Tests** (`tests/test_sources_pubmed.py`, respx-Antworten mit realistischem esearch/esummary-JSON)
  - `test_studies_are_parsed_newest_first`: Titel, Journal (`fulljournalname`), Jahr aus `pubdate` „2026 Sep 3“, 4 Autoren werden zu 3 plus „et al.“, PMID-Link.
  - `test_document_without_term_is_empty_without_network`: Keine Route aufgerufen.
  - `test_second_call_is_served_from_cache`: Die respx-Route wird genau einmal aufgerufen.
  - `test_stale_cache_is_refetched`: `fetched_at` liegt 25 h zurück.
  - `test_changed_term_uses_a_new_cache_entry`
  - `test_upstream_failure_is_unavailable_and_not_cached` (parametrisiert):
    - Timeout
    - HTTP 500
    - kein JSON
    - `esearchresult` fehlt

    Jeweils 200 mit `status == "unavailable"`, kein Cache-Eintrag.
  - `test_api_key_is_sent_when_configured`
  - `test_latest_studies_uses_the_two_largest_specialties`
  - `test_cache_survives_demo_reset`
  - `test_concurrent_store_of_same_key_does_not_fail`: `cached` zweimal mit derselben Session-Factory, der zweite Aufruf trifft einen vorhandenen Key.
  - `tests/test_permissions.py`: Die drei Quellen-Endpunkte aus Tasks 5–7 und `latest-studies` kommen mit `STAFF` in `ENDPOINTS`. Die Endpunkte aus Tasks 6/7 trägt die jeweilige Task nach.
- [ ] **Step 2:** `pytest tests/test_sources_pubmed.py tests/test_permissions.py` → FAIL
- [ ] **Step 3:** Implementieren
  - Ein `httpx.Client(timeout=settings.sources_timeout)` pro Anfrage, als FastAPI-Dependency `http_client`. Tests können ihn darüber überschreiben; respx fängt ohnehin ab.
  - Endpunkte sind sync (`def`).
- [ ] **Step 4:** `pytest`, Ruff → PASS
- [ ] **Step 5:** Commit `feat(sources): PubMed studies with a 24 h cache`

### Task 6: WHO ICD-11

**Files:** `app/sources/icd11.py`, `app/schemas.py`, `app/routers/sources.py`, `tests/conftest.py`, `tests/test_sources_icd11.py`, `tests/test_permissions.py`

**Interfaces:**
- Produces:
  - `Icd11Entry(code, title, definition: str | None, url, release, language)`
  - `lookup_code(client, code: str, settings) -> Icd11Entry | None`:
    - Ablauf: Token holen, `codeinfo/{code}` abfragen, dann die `stemId` (mit `http://` → `https://`).
    - Titel und Definition kommen aus `{"@value": ...}`.
    - Eine 404 bei `codeinfo` ergibt `None`.
  - Token-Cache: Modulvariable `_token: tuple[str, float] | None` mit `expires_in - 60` s Gültigkeit. Dazu `reset_token_cache()` für Tests.
  - `GET /api/sources/documents/{id}/icd11` → `SourceResult[Icd11Entry]`:
    - Fehlen die Keys → `not_configured`, ohne Netz.
    - Ohne Code → `empty`.
    - Cache-Key `icd11:{release}:{language}:{code}`.
  - `.env.example` und `docker-compose.yml` bekommen `ICD_CLIENT_ID`, `ICD_CLIENT_SECRET`, `ICD_RELEASE` und `ICD_LANGUAGE`, außerdem `NCBI_API_KEY`.

- [ ] **Step 1: Tests**
  - `test_not_configured_without_keys`: Keine Route aufgerufen.
  - `test_lookup_returns_title_definition_and_browser_link`:
    - Token, codeinfo und Entity werden gemockt.
    - Prüft die Header `API-Version: v2` und `Accept-Language: de`.
    - Link: `https://icd.who.int/browse/2026-01/mms/de#{entity_id}`.
  - `test_token_is_reused_until_expiry`: Zwei Codes, ein einziger Token-Aufruf.
  - `test_wrong_credentials_are_unavailable`: Token-Endpunkt antwortet 401.
  - `test_unknown_code_is_empty`: `codeinfo` antwortet 404.
  - `test_entity_without_definition_is_ok_with_null_definition`
  - Permission-Matrix: Endpunkt ergänzen.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** `pytest`, Ruff → PASS
- [ ] **Step 5:** Commit `feat(sources): WHO ICD-11 lookup via OAuth client credentials`

### Task 7: openFDA

**Files:** `app/sources/openfda.py`, `app/schemas.py`, `app/routers/sources.py`, `tests/test_sources_openfda.py`, `tests/test_permissions.py`

**Interfaces:**
- Produces:
  - `MedicationLabel(ingredient, brand_names: list[str], indications: str | None, warnings: str | None, adverse_reactions: str | None, url)`:
    - Jeder Text ist auf 600 Zeichen gekürzt, an einer Wortgrenze, mit „…“.
    - `warnings` kommt aus `boxed_warning`, ersatzweise aus `warnings_and_cautions`, dann aus `warnings`.
    - `url`: `https://open.fda.gov/apis/drug/label/`
  - `fetch_label(client, ingredient: str, settings) -> MedicationLabel | None`. Eine 404 ergibt `None`.
  - `MedicationsOut(found: list[MedicationLabel], missing: list[str])`
  - `GET /api/sources/documents/{id}/medications` → `SourceResult[MedicationsOut]`:
    - Pro Wirkstoff ein eigener Cache-Eintrag, `openfda:{ingredient}`.
    - Leere `medications` → `empty`.
    - Fällt ein einzelner Wirkstoff aus → `unavailable`. Nicht gefundene Wirkstoffe landen in `missing`, der Status bleibt `ok`.
    - `fetched_at` ist der älteste Zeitstempel der Teile.

- [ ] **Step 1: Tests**
  - `test_label_fields_are_extracted_and_truncated`
  - `test_boxed_warning_is_preferred`
  - `test_unknown_ingredient_goes_to_missing`
  - `test_each_ingredient_is_cached_separately`
  - `test_upstream_error_is_unavailable`
  - `test_no_medications_is_empty_without_network`
  - Permission-Matrix ergänzen.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** `pytest`, Ruff → PASS
- [ ] **Step 5:** Commit `feat(sources): openFDA drug labels per active ingredient`

### Task 8: Frontend-Typen, Abfragen und gegliederte Detailansicht

**Files:**
- `frontend/src/lib/types.ts`, `lib/sections.ts`, `lib/queries.ts`
- `features/documents/SectionedContent.tsx`, `features/documents/FurtherReading.tsx`, `features/documents/DocumentPage.tsx`
- Tests `features/documents/SectionedContent.test.tsx`, `DocumentPage.test.tsx`

**Interfaces:**
- Consumes: API aus Tasks 1 und 5–7.
- Produces:
  - `Document` mit den neuen Feldern:
    - `Sections = Partial<Record<SectionKey, string | null>>`
    - `FurtherReadingLink { label: string; url: string }`
  - `SourceResult<T> { status: 'ok' | 'empty' | 'unavailable' | 'not_configured'; fetched_at: string | null; data: T | null }`
  - `Study`, `LatestStudies`, `Icd11Entry`, `MedicationLabel`, `MedicationsOut`
  - `SECTION_ORDER` und `SECTION_LABELS` (gleiche Labels wie in `app/content.py`)
  - Hooks:
    - `useStudies(id, enabled)`, `useIcd11(id, enabled)`, `useMedications(id, enabled)`, jeweils mit `staleTime: 10 min`
    - `useLatestStudies(enabled)`
  - `<SectionedContent sections={…} />`:
    - Pro Sektion ein `h2` mit Label und Text.
    - `red_flags` steht als eigener Kasten „Warnzeichen“ am Ende, mit Icon. Steht dort „144“, bekommt der Kasten den Hinweis „Im Notfall: 144“. Ohne Fachgebietsfarbe, mit einem destructive-Ton aus den Tokens.
  - `<FurtherReading links={…} />` in der Seitenleiste:
    - Externe Links mit `rel="noreferrer noopener"` und `target="_blank"`.
    - Daneben der Host, z. B. „gesundheit.gv.at“.
  - Details zeigen „Fachbegriff (en)“ und „ICD-11“, wenn vorhanden.

- [ ] **Step 1: Tests**
  - `SectionedContent`:
    - rendert Sektionen in fester Reihenfolge und überspringt leere
    - Warnzeichen-Kasten mit „144“-Hinweis
  - `DocumentPage`:
    - Ein Eintrag mit `sections` zeigt die Überschriften „Symptome“ und „Therapie“, ohne `sections` die Absätze wie bisher.
    - „Weiterlesen“-Links öffnen in einem neuen Tab.
    - Die Fixture `document5` bekommt die neuen Felder.
- [ ] **Step 2:** `npm test` → FAIL
- [ ] **Step 3:** Implementieren. Typografie nach DESIGN.md:
  - Sektionsüberschriften `text-base font-semibold`, kein zweiter 30px-Titel („One Title“).
  - Lesebreite `max-w-[68ch]`.
- [ ] **Step 4:** `npm run lint && npm run typecheck && npm test` → PASS
- [ ] **Step 5:** Commit `feat(frontend): structured entry view with warning signs and further reading`

### Task 9: Quellen-Panels

**Files:** `features/documents/sources/SourcePanel.tsx`, `StudiesPanel.tsx`, `Icd11Panel.tsx`, `MedicationsPanel.tsx`, Test `features/documents/sources/SourcePanels.test.tsx`

**Interfaces:**
- Consumes: Hooks und Typen aus Task 8.
- Produces:
  - `<SourcePanel source="PubMed · NCBI" result={…} isPending error onRetry>{(data) => …}</SourcePanel>`, ein gemeinsamer Rahmen für alle Panels:
    - Kopfzeile mit dem Quellennamen und „abgerufen {formatRelative}“.
    - Bei `isPending`: Skeleton.
    - Bei `empty`: Text je Quelle über die Prop `emptyText`.
    - Bei `unavailable`: „{Quelle} ist gerade nicht erreichbar.“ mit dem Button „Erneut versuchen“.
    - Bei `not_configured`: „ICD-11 ist auf diesem Server nicht eingerichtet (WHO-API-Zugang fehlt).“
    - Bei `error`: `ErrorState`.
  - `StudiesPanel({documentId, enabled})`:
    - Liste mit Titel als externem PubMed-Link, Journal · Jahr und Autoren.
    - Zahlen in `tabular`.
  - `Icd11Panel({documentId, enabled})`:
    - Code groß in Monospace, dazu Titel und Definition.
    - Link „Im ICD-11-Browser öffnen“.
    - Hinweis „Deutsche Fassung: WHO-Prerelease“, wenn `language === 'de'`.
  - `MedicationsPanel({documentId, enabled})`:
    - Pro Wirkstoff eine aufklappbare Karte mit Anwendungsgebiet, Warnhinweisen und Nebenwirkungen.
    - Banner „US-FDA-Produktinformation, englisch – nicht für Dosierungsentscheidungen“.
    - `missing` steht als Zeile „Kein FDA-Label gefunden für: …“.

- [ ] **Step 1: Tests**, pro Panel und Status (`mockFetch`):
  - `ok` rendert die Daten und die Provenienz
  - `empty`, `unavailable` mit Retry (zweiter Fetch erfolgt), `not_configured` (ICD)
  - `enabled=false` → kein Fetch
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** lint, typecheck, test → PASS
- [ ] **Step 5:** Commit `feat(frontend): PubMed, ICD-11 and openFDA panels with honest status states`

### Task 10: Detailseite mit Tabs je Rolle

**Files:** `features/documents/DocumentPage.tsx`, `DocumentPage.test.tsx`

**Interfaces:**
- Consumes: Panels aus Task 9, `SectionedContent` aus Task 8.
- Produces:
  - Staff (doctor, admin) bekommt `Tabs` (shadcn) mit „Inhalt“, „ICD-11“, „Studien“ und „Medikamente“ über dem Blatt. Der Reiter Medikamente erscheint nur, wenn `medications.length > 0`.
  - Ein Panel lädt erst, wenn sein Tab einmal aktiv war: `enabled` wird nach dem ersten Öffnen dauerhaft true.
  - Der aktive Tab steht in `?tab=` (ersetzt den History-Eintrag), damit er einen Reload übersteht.
  - Patient: keine Tabs, nur Inhalt. Die Panels werden nie gerendert.

- [ ] **Step 1: Tests**
  - Arzt: Tabs sichtbar. Vor dem Klick auf „Studien“ gibt es keinen Aufruf an `/api/sources/documents/5/studies`, danach genau einen. Zurück auf „Inhalt“ und wieder auf „Studien“ → kein zweiter Fetch, dafür sorgt `staleTime`.
  - Patient: kein Tablist, kein Aufruf an `/api/sources`.
  - `?tab=icd11` öffnet direkt das ICD-11-Panel.
  - Ein Eintrag ohne Wirkstoffe hat keinen Reiter „Medikamente“.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren. Der Tab-Inhalt bleibt auf dem Blatt unter dem `FileTab`. Motion: Wechsel per Überblendung, Reduced Motion wird respektiert.
- [ ] **Step 4:** lint, typecheck, test → PASS
- [ ] **Step 5:** Commit `feat(frontend): entry tabs for content, ICD-11, studies and medications`

### Task 11: Dashboard-Kachel „Neueste Studien“

**Files:** `features/dashboard/LatestStudies.tsx`, `DashboardPage.tsx`, `DashboardPage.test.tsx`

**Interfaces:**
- Consumes: `useLatestStudies` und `SourcePanel` (Status-Rahmen).
- Produces: Die Kachel gibt es nur für Staff. Pro Fachgebiet ein `FileTab` (Farbe nur am Reiter), darunter 3 Studien mit Link. Die Kachel steht neben „Zuletzt bearbeitet“.

- [ ] **Step 1: Tests**
  - Arzt sieht die Kachel mit zwei Fachgebieten und Links.
  - Patient-Startseite: kein Aufruf an `latest-studies`.
  - `unavailable` → Hinweis statt Absturz.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** lint, typecheck, test → PASS
- [ ] **Step 5:** Commit `feat(dashboard): latest PubMed studies for the largest specialties`

### Task 12: Editor mit Fachbegriff, ICD-11, Wirkstoffen und Abschnitten

**Files:** `features/editor/EditorPage.tsx`, `features/editor/SectionFields.tsx`, `EditorPage.test.tsx`, `lib/queries.ts` (useClassify mit Sektionen)

**Interfaces:**
- Consumes: API aus Task 1, `KeywordInput` (für die Wirkstoffe wiederverwendet).
- Produces:
  - Der Formularzustand bekommt `termEn`, `icd11Code`, `medications: string[]`, `mode: 'text' | 'sections'` und `sections: Sections`.
  - `mode` ist `sections`, wenn der Eintrag Sektionen hat; neue Einträge starten mit `text`. Umschalten über einen Segmented Control „Freitext / Abschnitte“ mit `aria-pressed`-Buttons, kein `role=radio`. Siehe BACKLOG.
  - Beim Wechsel Freitext → Abschnitte landet der Freitext in `definition`. Beim Wechsel Abschnitte → Freitext wird `compose` im Client nur zur Vorschau genutzt; gesendet wird `content`, und das Backend setzt `sections = null`.
  - Senden:
    - Im Modus `sections` gehen `sections` raus und kein `content`.
    - Im Modus `text` geht `content` raus und kein `sections`.
    - `term_en`/`icd11_code` gehen als `null`, wenn sie leer sind.
  - Live-Klassifikation: `useClassify(title, {content} | {sections})`.
  - `<SectionFields value onChange />`: sechs `Textarea`s mit Labels aus `SECTION_LABELS`.
  - `further_reading` und `ai_generated` sind nicht editierbar. PATCH lässt sie unberührt.
  - Ruling: Weiterlesen-Pflege kommt erst bei Bedarf.

- [ ] **Step 1: Tests**
  - Ein neuer Eintrag im Abschnitte-Modus sendet `sections` ohne `content`. Die Klassifikations-Vorschau ruft `/api/classify` mit `sections` auf.
  - Beim Bearbeiten eines gegliederten Eintrags sind die Abschnitte vorbefüllt.
  - Ungültiger ICD-Code „8A80.123“ → die Feldfehlermeldung kommt aus der 422-Antwort, das Formular bleibt.
  - Wirkstoffe hinzufügen/entfernen → PATCH enthält `medications`.
  - Die bestehenden Editor-Tests bleiben grün.
- [ ] **Step 2:** FAIL
- [ ] **Step 3:** Implementieren
- [ ] **Step 4:** lint, typecheck, test → PASS
- [ ] **Step 5:** Commit `feat(editor): English term, ICD-11 code, active ingredients and section mode`

### Task 13: e2e, Doku, Abschluss

**Files:** `frontend/e2e/smoke.spec.ts`, `frontend/playwright.config.ts` (falls nötig), `AGENTS.md`, `docs/BACKLOG.md`, `.env.example`, `README.md` (nur Abschnitt Konfiguration)

- [ ] **Step 1: e2e anpassen**
  - In `beforeEach` fängt `page.route('**/api/sources/**', …)` alle Quellen-Abfragen mit festen JSON-Antworten ab. Der Playwright-Server ruft so nie PubMed auf.
  - Erwartete Zahl der Fachgebiets-Tabs: 9 → 16.
  - Neuer Test „Arzt öffnet Studien-Tab“: Die Studie aus dem Mock ist sichtbar, mit der Provenienz „PubMed · NCBI“.
  - Neuer Test „Patient sieht Warnzeichen“: Die Detailseite eines Seed-Eintrags zeigt „Warnzeichen“ und keine Tabs.
  - Neuer Test „Editor im Abschnitte-Modus legt einen Eintrag an“.
- [ ] **Step 2:** `npm run build` und `PYTHON=../.venv/Scripts/python.exe npm run e2e` → PASS
- [ ] **Step 3: Doku**
  - `AGENTS.md`: Etappe 3 auf „done“. Neue Gotchas:
    - respx-Fixture `network` blockiert jedes Netz in Tests
    - `page.route` für `/api/sources` in e2e
    - der ICD-Token-Cache
    - Seed-Inhalte in `app/seed_data/<fach>.py`
    - `scripts/check_seed_sources.py`
  - `.env.example`: Quellen-Variablen mit einer Anleitung für die WHO-Registrierung auf `icd.who.int/icdapi`.
  - BACKLOG: offene Minors.
- [ ] **Step 4:** Vollständige Prüfung:
  - `pytest`
  - `ruff check . && ruff format --check .`
  - in `frontend/`: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run e2e`
- [ ] **Step 5:** Commit `test(e2e): sources, sections and 16 specialties; docs for stage 3`
