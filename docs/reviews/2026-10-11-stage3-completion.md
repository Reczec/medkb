# Stage 3 — completion and handoff (2026-10-11)

Original branch: `feat/v2-stage3`. Tasks 1–10 inherited from Claude; tasks 11–13 completed here. On 2026-10-11 the user authorized a local merge into `main`; the branch was integrated by fast-forward through `2977eda`. Nothing was pushed.

## Continuation commits

- `33f2a34`: task 11, latest PubMed studies on the staff dashboard; source mocks and seed-count adjustments moved forward to keep browser tests green.
- `450ed2f`: task 12, structured editor, source metadata, active-ingredient chips and section-aware classification preview.
- `912a892`: task 13, three browser flows, source configuration and agent documentation, synchronized 16-specialty palette in DESIGN.md and its JSON sidecar.
- `2977eda`: all three final software-review fixes, ten regression cases, backlog and this durable handoff.

The local integration includes every preceding stage 3 commit. The implementation plan, this record, AGENTS.md, README configuration and BACKLOG provide the continuation context for Claude or Codex. The plan-specific ignored execution scratch directory was removed after its decisions were preserved here; local visual-review captures remain under `.impeccable/review/`.

## Implemented

- Staff dashboard: latest PubMed studies grouped by specialty.
- Admin editor: English term, ICD-11 code, active ingredients, free text or six structured sections, section-aware classification preview.
- Browser coverage: physician studies and persistent tabs, patient warnings without source requests, structured entry creation; source calls mocked.
- AGENTS, source configuration README and the 16-specialty design system synchronized.

## Review and fixes

Fresh whole-branch software review of d89e736..912a892 identified three Important issues, no Critical or Minor:

1. Browser source results could survive changed document inputs or archive restoration. All source queries now invalidate after document mutations/restores; four mutation regressions observed RED then GREEN.
2. Malformed FDA nested metadata could escape as a server error. Nested metadata/list types are checked and all label interpretation stays within the source-error boundary; three endpoint regressions observed RED then GREEN, with recovery proving failures are not cached.
3. Malformed WHO entity language could raise a validation error. Entity model validation now translates to SourceUnavailable; three endpoint regressions observed RED then GREEN, with recovery proving failures are not cached.

Fresh substitute Impeccable finish reviewer: ship for the supported stage 3 UI scope after inspecting 16 desktop/phone light/dark captures. Shipped named reviewer unavailable; substitute agent used. Static synthetic-source review does not certify live sources, measured contrast or keyboard behavior. No material visual fixes.

## Verification boundaries

- WHO codes still need live verification with credentials through `scripts/check_seed_sources.py`.
- Clinical editorial accuracy was outside the offline software review.
- No live PostgreSQL concurrency test was run; transaction code and duplicate-insert regression were reviewed.
- AI and deployment remain stages 4 and 5.

## Rulings (including inherited Claude decisions)

- T5 conftest token-cache reset needs T6 module. Ruling: add the reset to the fixture in T6 — module does not exist before — cost if wrong: none.
- T4 script ICD check needs T6 lookup_code. Ruling: T4 ships link check only; T6 adds the ICD part — cost if wrong: none.
- Task 4: Ruling: seed entries get `content` = compose_content(sections) in app/seed_data/__init__.py — keeps test_classifier/test_demo_reset unchanged as the plan requires — cost if wrong: none.
- Task 4: Ruling: 47 entries (plan said ~46, range 44–48) — 3 per specialty, 2 for Allgemeinmedizin — cost if wrong: none.
- Task 4: Ruling: ICD-11 codes written from the WHO classification without live verification (no ICD keys yet); scripts/check_seed_sources.py verifies them once keys exist — cost if wrong: a wrong code shows "empty" in the ICD-11 tab until fixed.
- Task 5: Ruling: shared app/sources/http.py (http_client dependency + get_json) not in the file map — all three clients need the same timeout/error mapping — cost if wrong: none.
- Task 5: Ruling: Study has `authors` (≤3) + `more_authors: bool` instead of a literal "et al." list element — typed, the UI appends "et al." — cost if wrong: one field rename.
- Task 5: Ruling: the network fixture lets unmatched requests get respx's empty 200 (→ "unavailable") instead of a catch-all ConnectError route — respx matches routes in insertion order, so a catch-all would shadow per-test routes — cost if wrong: an unmocked call in a test shows as "unavailable" instead of failing loudly.
- Task 5: Ruling: store() inserts first and falls back to UPDATE on IntegrityError (deterministic conflict path, tested) instead of db.merge — cost if wrong: none.
- Task 5: Ruling: SourceResult uses Generic[T] + noqa UP046, not PEP 695 — local venv is Python 3.11 — cost if wrong: none.
- Task 6: Ruling: Icd11Entry.language and the browser link use the language WHO actually answered in (title @language), not the requested one — German is a prerelease and may fall back to English — cost if wrong: none.
- Task 6: Ruling: an entity without a title counts as "unavailable" (extra test) — a nameless code is not usable — cost if wrong: none.
- Task 7: Ruling: live smoke showed NCBI 429 on the dashboard burst — added a process-wide NCBI throttle (0.4 s, 0.12 s with key) and one retry after 1 s on 429 (tests RED→GREEN) — cost if wrong: up to ~2 s slower first load of the tile.
- Task 7: Ruling: PubMed without sort parameter (default "most recent" = newest additions) instead of plan's sort=pub_date — pub_date ranked future-dated 2027 issues first — cost if wrong: order differs slightly from publication date.
- Task 7: Ruling: openFDA fetches 10 labels and picks single-ingredient → prescription → with-indication (plan said limit=1) — limit=1 returned combination/homeopathic labels live — cost if wrong: none.
- Task 7: Ruling: removed "ferrous sulfate" from the Eisenmangelanämie seed — openFDA only has homeopathic/OTC labels for it — cost if wrong: no medication tab on that entry.
- Task 8: Ruling: test fixtures share PLAIN_FIELDS from src/test/utils.tsx for the six new Document fields — one place instead of seven literals — cost if wrong: none.
- Task 9: Ruling: SourcePanel takes the TanStack query object (+ shortName, notConfiguredText, caption) instead of separate result/isPending/error/onRetry props — one prop, no drift between them — cost if wrong: none. StudyItem is exported for the dashboard tile (Task 11).
- Task 10: Ruling: lazy loading via Radix mounting only the active tab plus gcTime 10 min on source queries, instead of a visited-set — same behaviour, less state — cost if wrong: none.
- Task 11: Ruling: move the existing e2e source mocks and seed-count adjustments from Task 13 into Task 11 — AGENTS requires green e2e after every task and no real source requests in tests — cost if wrong: only commit grouping changes. Task 13 still adds the new flows and docs.
- Task 13: Ruling: use an absolute PYTHON path for e2e instead of the relative plan example — Playwright starts uvicorn from the repository root — cost if wrong: local command wording only.
- Final: Ruling: leave live ICD-code validity explicitly unconfirmed until WHO credentials exist — software and source status handling are tested, the source mapping is not — cost if wrong: a seed diagnosis may show an empty or incorrect WHO match.
- Final: Ruling: clinical editorial accuracy needs domain/source review beyond the offline software review — demo content remains labeled synthetic with no medical-advice claim — cost if wrong: an example text may contain a clinical inaccuracy.
- Final: Ruling: PostgreSQL concurrency is assessed from transaction code and the duplicate-insert regression, without a live PostgreSQL run — no configured PostgreSQL test environment — cost if wrong: a production concurrency edge may remain.
- Final: Ruling: AI and deployment readiness stay in stages 4 and 5 — the stage 3 handoff authorizes this stage only — cost if wrong: those features remain unfinished as documented.

## Deferred minors

- Final: minor (deferred): preexisting design.json snippets approximate the Neurologie icon as a circle and name the navigation Dashboard instead of the current label.

## Final checks

Full post-fix checks passed: pytest 486 tests, Ruff check and format (68 files), frontend lint/typecheck, Vitest 128 tests (24 files), production build, Playwright 25 tests. Existing warnings remain: FastAPI/httpx deprecation, Vite config __dirname, and the main JS chunk over 500 kB (already in BACKLOG).

## Local integration verification

After the authorized fast-forward into `main`, all checks were rerun successfully: pytest 486 tests; Ruff check and format (68 files); frontend lint, typecheck, Vitest 128 tests, production build and Playwright 25 tests. No conflicts occurred. The fully merged local `feat/v2-stage3` branch was deleted after verification; its commits remain in `main`. No worktree was created or removed, and no remote branch or repository was changed. This integration record, its AGENTS.md link and the plan's completion status are committed separately on `main`.
