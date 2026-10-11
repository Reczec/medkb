# Backlog

Follow-ups deferred from the stage 1 reviews (code review and design review, 2026-10-10). None blocks stage 2. Pick them up when touching the area, or batch them before stage 5.

## Behaviour

- Editor: Escape does nothing in the "Änderungen verwerfen?" dialog. Add `onOpenChange` → `blocker.reset()` in `frontend/src/features/editor/EditorPage.tsx`. There is also no `beforeunload` guard for closing the tab or reloading.
- Activity dates: `formatDay` in `frontend/src/lib/format.ts` parses `YYYY-MM-DD` as UTC midnight, so the date shows one day early west of UTC. Format with `timeZone: 'UTC'`. The buckets are UTC days.
- Backend `detail` texts for validation and some 404s are English; the UI shows them as they are.
- Archive restore shows no progress and does not guard against double submit. Defer `URL.revokeObjectURL` after the download click.
- `ThemeToggle` and `CategoryPicker` use `role="radio"` without arrow-key navigation. Either implement roving tabindex or switch to `aria-pressed` buttons.
- Command palette: the "Keine Einträge gefunden." message never shows, because the action items always match.
- Deleting an entry refetches it (404) before navigating away. Use `removeQueries(['document', id])`.
- Knowledge base list: with `keepPreviousData`, a failed refetch shows the error card above stale results.

## Auth (stage 2 review, 2026-10-11)

- A late 401 from a request sent with an old token clears a freshly issued token (`api.ts`): clear only if `tokenStore.get() === token`.
- If sessionStorage is blocked, the token is lost and every call is 401 without the expiry flow; keep an in-memory fallback in `lib/auth.ts`.
- `reset_demo` is not one transaction: readers can briefly see 0 entries, and a failure mid-way leaves the demo empty until the next run.
- SQLite reuses ids after the demo reset, so an editor opened before the reset can overwrite a restored example entry (PostgreSQL is fine).
- Tokens without `exp` are accepted (only our own signed ones): `options={"require": ["exp", "sub"]}`.
- Demo accounts and their tokens survive switching `DEMO_MODE` off.
- `upgrade_schema` can race when two instances start at once.
- Shutdown does not wait for a running reset thread.
- `tests/test_permissions.py` lists routes by hand; enumerate `app.routes` instead.
- Design ceiling: admin tabs are stock segmented controls, the users table shows roles as plain text, the activity feed and forbidden page have no in-world treatment.

## Build and ops

- `/assets` has no `Cache-Control: immutable` header (the comment in `app/spa.py` claims long caching). `HEAD /` returns 405.
- Move `shadcn` from dependencies to devDependencies. It is only needed at build time for `tailwind.css`.
- The CI docker job only builds the image. Also run it and curl `/api/health` and `/`.
- The main JS chunk is over 500 kB. Lazy-load the routes, the dashboard charts first.
- The README screenshots still show the old UI. Stage 5 replaces them with new screenshots and a demo GIF.

## Sources (stage 3 review, 2026-10-11)

- Live-check the bundled ICD-11 codes with WHO credentials using `scripts/check_seed_sources.py`; offline tests cannot confirm the code-to-diagnosis mapping.
- The design sidecar's Neurologie example uses a circle icon and its navigation snippet says "Dashboard". Synchronize these examples when next updating the design documentation.

## Design ideas (from the finish review, not defects)

- Dark theme rail is near-black. Consider a deep petrol so the shell identity survives in dark mode.
- On mobile the petrol shell disappears behind an off-white top bar. Consider petrol in the mobile top bar.
- The detail page leaves the lower half of the left column empty. The classification explanation could sit on the sheet as a margin note.
- Sheets never overlap like filed records; drawer and stack depth are unused.
