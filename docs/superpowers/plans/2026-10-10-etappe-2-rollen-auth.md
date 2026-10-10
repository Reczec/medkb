# Etappe 2 – Rollen und Login – Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Drei Rollen (admin, doctor, patient) mit JWT-Login und Ein-Klick-Demo-Zugängen. Rechte werden im Backend erzwungen, die Oberfläche passt sich der Rolle an (Patienten-Startseite, ausgeblendete Admin-Funktionen). Die Demo-Datenbank setzt sich regelmäßig zurück.

**Architecture:** Das Backend bekommt eine `users`-Tabelle, `app/auth.py` (Passwort-Hash, JWT, Abhängigkeiten `current_user` und `require_role`) und `app/routers/auth.py`. Das bisherige `X-Admin-Token` (`app/security.py`, `ADMIN_TOKEN`) entfällt. Das Frontend hält das Token in `sessionStorage`, schickt es als `Authorization: Bearer`, stellt Nutzer und Rolle über einen `AuthProvider` bereit und schützt Routen mit Guards.

**Tech Stack:** wie Etappe 1, dazu `pyjwt` und `pwdlib[bcrypt]`.

**Spec:** `docs/superpowers/specs/2026-10-10-medkb-v2-design.md` (Abschnitt 3 sowie die Rollen-Teile von 8, 9, 10). **Gotchas:** `AGENTS.md`.

## Global Constraints

- Rollen: `admin` | `doctor` | `patient`. Anzeigenamen: „Admin“, „Dr. Demo“, „Patient Demo“.
- Rechte-Matrix (Spec §3), im Backend erzwungen:
  - **alle eingeloggten Rollen:** `GET /api/documents`, `GET /api/documents/{id}`, `GET /api/meta`, `GET /api/stats`
  - **doctor und admin:** `POST /api/classify`
  - **nur admin:** `POST`/`PATCH`/`DELETE /api/documents…`, `/api/archives…`, `/api/audit`, `GET /api/users`
  - **ohne Login:** nur `/api/health` und `/api/auth/*`
- Fehlercodes: fehlendes, ungültiges oder abgelaufenes Token → 401; falsche Rolle → 403.
- JWT: HS256, Secret `JWT_SECRET`, gültig 8 h. Claims: `sub` = User-ID, `role`, `exp`. Ist `JWT_SECRET` leer, wird beim Start ein Zufalls-Secret erzeugt und eine Warnung geloggt.
- `DEMO_MODE=true` aktiviert:
  - die drei Demo-Nutzer mit zufälligen Passwörtern,
  - `POST /api/auth/demo`,
  - einen Reset alle `DEMO_RESET_HOURS` (Default 24) sowie beim Start.

  Beim Reset werden Einträge und Audit-Log neu angelegt bzw. geleert. Nutzer und Archive bleiben.
- `ADMIN_PASSWORD` (optional) legt einen Login-Nutzer `admin` an bzw. aktualisiert ihn. Ohne Demo-Modus ist das der einzige Weg hinein.
- Patienten sehen nie Klassifikations-Scores, „regelbasiert“-Marker, Bearbeiten-Aktionen oder Admin-Bereiche.
- Alles aus Etappe 1 bleibt: UI-Texte Deutsch, Hinweis „keine medizinische Beratung“, `DESIGN.md`-Regeln, Test zuerst, ein Commit pro Aufgabe.

## Review Focus

1. Token läuft ab oder ist nach einem Server-Neustart ungültig (zufälliges Secret) → jeder API-Aufruf liefert 401 → einmaliger Sprung zur Login-Seite mit dem Hinweis „Sitzung abgelaufen“, keine Fehlerschleife. (Task 5)
2. Ein Patient ruft `/admin` oder `/wissen/neu` direkt per URL auf → Seite „Keine Berechtigung“ mit Link zur Startseite. Die API liefert 403, nie eine leere Seite. (Tasks 3 und 6)
3. `DEMO_MODE=false` → `/api/auth/demo` liefert 404, die Login-Seite blendet die Demo-Karten aus und zeigt nur das Formular. (Tasks 2 und 5)
4. Demo-Reset, während ein Admin editiert → Speichern liefert 404 → Toast „Eintrag existiert nicht mehr (Demo wurde zurückgesetzt)“, kein Absturz. (Task 6)
5. Falsches Passwort → 401 mit „Benutzername oder Passwort falsch“. Die Antwort verrät nicht, ob es den Benutzer gibt. (Task 2)

---

## File Structure

```
app/
  config.py            (mod) jwt_secret, jwt_hours=8, demo_mode, demo_reset_hours=24,
                             admin_password; admin_token entfernt
  models.py            (mod) User; AuditLog.actor (String(50), nullable)
  auth.py              (neu) hash_password, verify_password, create_token, decode_token,
                             current_user, require_role
  users.py             (neu) ensure_users(db, settings) -> None
  demo.py              (neu) reset_demo(db) -> int, demo_reset_loop(settings)
  routers/auth.py      (neu) /api/auth/login, /demo, /me, /options
  routers/users.py     (neu) GET /api/users
  routers/documents.py (mod) Rollen-Abhängigkeiten
  routers/admin.py     (mod) require_role("admin") statt require_admin
  services.py          (mod) log_audit(..., actor) für alle Aufrufer
  security.py          (gelöscht)
  main.py              (mod) Lifespan: Secret-Fallback, ensure_users, Demo-Reset und -Loop
tests/
  conftest.py          (mod) Rollen-Clients: client (admin), doctor_client, patient_client,
                             anon_client
  test_auth.py         (neu)
  test_permissions.py  (neu)
  test_demo_reset.py   (neu)
  test_admin_api.py    (mod) ohne X-Admin-Token
frontend/src/
  lib/auth.ts                (neu) Token-Speicher, AuthUser-Typ
  lib/api.ts                 (mod) Bearer-Header, 401 → Event `medkb:unauthorized`
  features/auth/AuthProvider.tsx  (neu) useAuth()
  features/auth/LoginPage.tsx     (neu)
  features/auth/guards.tsx        (neu) RequireAuth, RequireRole, ForbiddenPage
  features/home/PatientHome.tsx   (neu)
  features/dashboard/ActivityFeed.tsx (neu, admin)
  features/admin/UsersPanel.tsx   (neu)
  features/admin/AdminTokenGate.tsx (gelöscht)
  …bestehende Seiten (mod) rollenabhängig
frontend/e2e/smoke.spec.ts   (mod) Demo-Login je Rolle
```

---

### Task 1: Nutzer, Passwort-Hash, JWT

**Files:** `app/config.py`, `app/models.py`, `app/auth.py`, `requirements.txt` (`pyjwt>=2.9,<3`, `pwdlib[bcrypt]>=0.2,<1`), Test `tests/test_auth.py` (Unit-Teil)

**Interfaces:**
- Produces:
  - `User(id, username unique String(50), password_hash String(255), role String(10), display_name String(100), created_at)`
  - `hash_password(pw: str) -> str` und `verify_password(pw: str, hashed: str) -> bool`
  - `create_token(user: User, settings: Settings) -> str` und `decode_token(token: str, settings: Settings) -> dict`. `decode_token` wirft `jwt.InvalidTokenError` bei abgelaufenem oder manipuliertem Token.
  - `Role = Literal["admin", "doctor", "patient"]`

- [ ] **Step 1: Tests schreiben**
  - `test_password_roundtrip`: Hash ≠ Klartext, `verify` mit dem richtigen Passwort ist True, mit einem falschen False.
  - `test_token_roundtrip_carries_id_and_role`
  - `test_expired_token_is_rejected`: Settings mit `jwt_hours=-1`.
  - `test_token_signed_with_other_secret_is_rejected`
- [ ] **Step 2:** `pytest tests/test_auth.py` → FAIL (ImportError)
- [ ] **Step 3:** Implementieren. `admin_token` aus `Settings` entfernen; die Fixture `admin_disabled_client` fällt in Task 3 weg.
- [ ] **Step 4:** `pytest tests/test_auth.py` → PASS
- [ ] **Step 5:** Commit `feat(auth): users, password hashing and JWT helpers`

### Task 2: Auth-API und Nutzer-Seeding

**Files:** `app/users.py`, `app/routers/auth.py`, `app/main.py`, `tests/conftest.py`, `tests/test_auth.py`

**Interfaces:**
- Produces:
  - `ensure_users(db, settings)`: Bei `demo_mode` legt es `demo-admin`, `demo-doctor` und `demo-patient` mit Zufallspasswort an (idempotent). Bei gesetztem `admin_password` legt es den Nutzer `admin` (Rolle admin) an bzw. setzt sein Passwort.
  - `POST /api/auth/login {username, password}` → `{access_token, token_type: "bearer", user: {id, username, display_name, role}}`; bei falschen Daten 401 `"Benutzername oder Passwort falsch"`.
  - `POST /api/auth/demo {role}` → gleiche Antwort; 404, wenn `demo_mode` aus ist; 422 bei unbekannter Rolle.
  - `GET /api/auth/me` → user; ohne oder mit ungültigem Token 401.
  - `GET /api/auth/options` → `{demo_mode: bool}`, öffentlich.
  - Lifespan: Ist `jwt_secret` leer, wird `secrets.token_urlsafe(32)` gesetzt und gewarnt. Danach `ensure_users`.
  - `conftest.py`: Die Settings-Override bekommt `demo_mode=True` und `jwt_secret="test-secret"`. Die Fixture `client` meldet sich per Demo-Login als admin an (`client.headers["Authorization"]`); dazu kommen `doctor_client`, `patient_client` und `anon_client`. `ensure_users` läuft in der Fixture `clean_database`.

- [ ] **Step 1: Tests**
  - Demo-Login liefert für jede Rolle die passende Rolle in `/me`.
  - Ein Login mit falschem Passwort und einer mit unbekanntem Nutzer liefern dieselbe 401-Meldung.
  - Ein Login mit `admin_password` funktioniert.
  - `demo_mode=False`: `/demo` liefert 404 und `/options` liefert `{demo_mode: false}`.
  - `/me` ohne Token liefert 401.
- [ ] **Step 2:** FAIL. **Step 3:** Implementieren. **Step 4:** `pytest` (alle) → bestehende Tests grün; die Admin-Tests nutzen bis Task 3 noch den Header.
- [ ] **Step 5:** Commit `feat(auth): login, demo login, me and options endpoints`

### Task 3: Rechte erzwingen, Audit-Akteur, Nutzerliste

**Files:** `app/routers/documents.py`, `app/routers/admin.py`, `app/routers/users.py`, `app/services.py`, `app/archive.py`, `app/models.py`, `app/schemas.py` (`AuditOut.actor`, `UserOut`); `app/security.py` löschen; Tests `tests/test_permissions.py`, `tests/test_admin_api.py`, `tests/conftest.py`

**Interfaces:**
- Produces:
  - `log_audit(db, action, document_id, detail, actor: str | None)`. Die Router reichen `user.username` durch, bis in `create_archive` und `restore_archive`.
  - `GET /api/users` (admin) → `[{id, username, display_name, role, created_at}]`
  - `AuditOut.actor: str | None`

- [ ] **Step 1: Tests**
  - `tests/test_permissions.py` prüft die Rechte-Matrix aus den Global Constraints parametrisiert über alle Endpunkte × {anon: 401, patient, doctor, admin} → erwarteter Status (erlaubt: kein 401/403).
  - `test_audit_records_actor`: Ein Admin legt etwas an, das Audit-Log zeigt `actor == "demo-admin"`.
  - `test_users_list_has_no_password_hashes`
  - `test_admin_api.py`: Den Header-Tests werden Rollen-Tests (patient bzw. doctor → 403); `admin_disabled_client` entfällt.
- [ ] **Step 2:** FAIL. **Step 3:** Implementieren. **Step 4:** `pytest` → alles grün; `ruff`.
- [ ] **Step 5:** Commit `feat(auth): enforce roles on every endpoint, record the actor in the audit log`

### Task 4: Demo-Reset

**Files:** `app/demo.py`, `app/main.py`, Test `tests/test_demo_reset.py`

**Interfaces:**
- Produces:
  - `reset_demo(db) -> int` löscht alle Dokumente und das Audit-Log, legt die Seed-Einträge neu an, schreibt einen Audit-Eintrag `demo_reset` (actor `system`) und gibt die Anzahl der Einträge zurück.
  - `async demo_reset_loop(settings)` schläft `demo_reset_hours` und ruft dann `reset_demo` in einer neuen Session auf. Im Lifespan wird die Schleife per `asyncio.create_task` gestartet und beim Shutdown abgebrochen.
  - Beim Start mit `demo_mode` läuft `reset_demo` statt `seed_if_empty`.

- [ ] **Step 1: Tests**
  - Nach Änderungen setzt `reset_demo` auf genau `len(SEED_DOCUMENTS)` Einträge zurück, und das Audit-Log enthält nur `demo_reset`.
  - Nutzer bleiben erhalten (ein Login mit `admin_password` funktioniert nach dem Reset).
  - `demo_reset_loop` mit `demo_reset_hours=0.0001` und gepatchtem `reset_demo` ruft den Reset mindestens einmal auf; danach wird der Task abgebrochen.
- [ ] **Step 2:** FAIL. **Step 3:** Implementieren. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(demo): periodic demo reset`

### Task 5: Frontend – Login, Token, Guards

**Files:** `src/lib/auth.ts`, `src/lib/api.ts`, `src/features/auth/{AuthProvider,LoginPage,guards}.tsx`, `src/App.tsx`, `src/main.tsx`; Tests `src/features/auth/*.test.tsx`, `src/lib/api.test.ts`

**Interfaces:**
- Produces:
  - `AuthUser {id, username, display_name, role}`
  - `tokenStore.get()`, `tokenStore.set(token)`, `tokenStore.clear()` (sessionStorage `token`)
  - `api()` setzt `Authorization: Bearer <token>`, sobald ein Token vorhanden ist. Bei 401 löscht es das Token und feuert `window` `medkb:unauthorized`. Die Option `admin` und `ADMIN_TOKEN_KEY` entfallen.
  - `useAuth()` → `{user, status: 'loading' | 'anonymous' | 'authenticated', login(username, password), loginDemo(role), logout()}`. Beim Start mit vorhandenem Token wird `/api/auth/me` geladen. `medkb:unauthorized` setzt den Status auf anonym und merkt sich den Hinweis „Sitzung abgelaufen“.
  - Routen: `/login` ist öffentlich. Alles andere liegt unter `<RequireAuth>`, das nach `/login?next=…` umleitet. `<RequireRole roles={[…]}>` zeigt bei falscher Rolle die `ForbiddenPage` („Keine Berechtigung“).
  - `LoginPage`:
    - Links die Marke und der Satz „Medizinische Wissensdatenbank – Prototyp mit Beispieldaten“.
    - Drei Demo-Karten im Karteireiter-Stil: **Admin** (Einträge pflegen, Archiv, Protokoll), **Ärztin / Arzt** (Fachansicht mit Klassifikation), **Patient:in** (einfache Sprache, nur lesen). Ein Klick meldet an und leitet zu `next` oder `/` weiter.
    - Darunter ein aufklappbares Formular „Mit Benutzername anmelden“.
    - Die Demo-Karten erscheinen nur, wenn `/api/auth/options` `demo_mode` liefert.

- [ ] **Step 1: Tests**
  - api: Der Bearer-Header wird gesendet; bei 401 wird das Token gelöscht und das Event gefeuert.
  - LoginPage: Ein Klick auf „Als Ärztin / Arzt ansehen“ ruft `POST /api/auth/demo {role: "doctor"}` auf und navigiert zu `/`. Mit `demo_mode: false` gibt es keine Demo-Karten, das Formular ist sichtbar.
  - Ein falsches Passwort zeigt „Benutzername oder Passwort falsch“.
  - RequireAuth leitet ohne Token nach `/login?next=%2Fwissen` um.
  - RequireRole zeigt „Keine Berechtigung“ für einen Patienten auf `/admin`.
  - Ein 401 während einer Sitzung → die Login-Seite zeigt „Sitzung abgelaufen“.
- [ ] **Step 2:** FAIL. **Step 3:** Implementieren (`impeccable` laden, Designsprache aus `DESIGN.md`). **Step 4:** PASS, lint, typecheck.
- [ ] **Step 5:** Commit `feat(frontend): login page with demo roles, token handling and route guards`

### Task 6: Rollenabhängige Oberfläche

**Files:**
- Ändern: `Sidebar.tsx`, `Topbar.tsx`, `CommandPalette.tsx`, `DocumentPage.tsx`, `DocumentCard.tsx`, `EditorPage.tsx`, `AdminPage.tsx`, `DashboardPage.tsx`
- Neu: `features/admin/UsersPanel.tsx`, `features/dashboard/ActivityFeed.tsx`
- Löschen: `features/admin/AdminTokenGate.tsx`
- Tests dazu.

**Interfaces:**
- Consumes: `useAuth()` (Task 5)
- Produces:
  - **Navigation:** Den Eintrag „Admin“ gibt es nur für admin. Unten in der Seitenleiste stehen ein Nutzer-Chip (Anzeigename und Rolle) und „Abmelden“.
  - **Aktionen:** „Neuer Eintrag“ (Topbar und Palette) gibt es nur für admin.
  - **Detailseite:** Bearbeiten und Löschen nur für admin. Den `ClassificationExplainer` sehen nur doctor und admin.
  - **Karten:** Der Marker „regelbasiert/manuell“ auf `DocumentCard` erscheint nicht für patient.
  - **Admin-Seite:** Sie hat die Tabs Archive, Änderungsprotokoll (mit Spalte „Wer“) und Nutzer.
  - **Admin-Dashboard:** Unter „Zuletzt bearbeitet“ steht der `ActivityFeed`: die letzten 8 Audit-Einträge mit Akteur und relativer Zeit.
  - **Routen-Rechte:** `/wissen/neu`, `/wissen/:id/bearbeiten` und `/admin` liegen unter `RequireRole admin`.
  - **Editor:** Ein 404 beim Speichern zeigt den Toast „Eintrag existiert nicht mehr (Demo wurde zurückgesetzt)“.

- [ ] **Step 1: Tests**
  - Ein Patient sieht auf der Detailseite weder „Bearbeiten“ noch „Klassifikation“.
  - Ein Doctor sieht „Klassifikation“, aber nicht „Bearbeiten“.
  - Die Sidebar zeigt „Admin“ nur für admin; „Abmelden“ ruft `logout` auf.
  - Die Admin-Seite listet die Nutzer.
  - Ein 404 beim Speichern im Editor zeigt den Demo-Reset-Toast.
- [ ] **Step 2:** FAIL. **Step 3:** Implementieren. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(frontend): role-aware navigation, detail page, admin users and activity feed`

### Task 7: Patienten-Startseite

**Files:** `src/features/home/PatientHome.tsx`, `src/App.tsx` (Index-Route: patient → `PatientHome`, sonst `DashboardPage`), Test

**Interfaces:**
- Produces: Die Startseite für Patient:innen:
  - Begrüßung „Wonach suchst du?“.
  - Ein großes Suchfeld, das bei Enter zu `/wissen?q=…` führt.
  - Themen als Karteireiter (der `SpecialtyStrip` aus `/api/stats`).
  - Die zuletzt bearbeiteten Einträge als Blätter (`RecentList`).
  - Ein Hinweis „Bei Notfällen sofort 144 anrufen“.
  - Keine Statistik-Zahlen und keine Diagramme.
  - Platzhalter-Karte „Frag den KI-Assistenten – kommt bald“ ohne Funktion. Sie verschwindet in Etappe 4 wieder bzw. wird ersetzt.

- [ ] **Step 1: Tests**
  - Ein Patient auf `/` sieht „Wonach suchst du?“ und kein „Änderungen der letzten 30 Tage“.
  - Enter im Suchfeld navigiert zu `/wissen?q=husten`.
  - Ein Doctor auf `/` sieht das Dashboard.
- [ ] **Step 2:** FAIL. **Step 3:** Implementieren. **Step 4:** PASS.
- [ ] **Step 5:** Commit `feat(frontend): patient home`

### Task 8: E2E, Doku, Konfiguration

**Files:** `frontend/e2e/smoke.spec.ts`, `frontend/playwright.config.ts` (env `DEMO_MODE=true`, `JWT_SECRET=e2e-secret`, ohne `ADMIN_TOKEN`), `.env.example`, `docker-compose.yml`, `README.md`, `AGENTS.md`, `docs/BACKLOG.md` (Admin-Token-Punkte streichen)

- [ ] **Step 1: E2E**
  - Ein Helfer `loginAs(page, role)` klickt die Demo-Karte.
  - Alle bisherigen Tests laufen über `loginAs('admin')`.
  - Neu:
    - Ohne Login führt `/wissen` auf `/login`.
    - Ein Patient sieht die Patienten-Startseite; auf `/wissen/1` gibt es kein „Bearbeiten“; `/admin` zeigt „Keine Berechtigung“.
    - Ein Doctor sieht auf `/wissen/1` die Klassifikation, aber kein „Bearbeiten“.
    - Abmelden führt zurück zur Login-Seite.
    - Die Login-Seite hat bei 375 px keinen Überlauf.
- [ ] **Step 2:** `npm run build && npm run e2e` → FAIL, dann anpassen → PASS.
- [ ] **Step 3: Doku**
  - `.env.example`: `JWT_SECRET`, `DEMO_MODE=true`, `DEMO_RESET_HOURS`, `ADMIN_PASSWORD`; `ADMIN_TOKEN` entfällt.
  - README: die Abschnitte Rollen, Login und API-Tabelle (Auth-Spalte).
  - `AGENTS.md`: Status-Tabelle aktualisieren (Etappe 2 erledigt); den Gotcha zum Admin-Token durch „Tests: Rollen-Clients in conftest; e2e: loginAs“ ersetzen.
- [ ] **Step 4:** Vollständiger Lauf: `pytest`, `ruff`, `lint`, `typecheck`, `test`, `build`, `e2e`.
- [ ] **Step 5:** Commit `test(e2e): demo login per role; docs for roles and auth`
