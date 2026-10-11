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

- If sessionStorage is blocked, the token is lost and every call is 401 without the expiry flow; keep an in-memory fallback in `lib/auth.ts`.
- SQLite reuses ids after the demo reset, so an editor opened before the reset can overwrite a restored example entry (PostgreSQL is fine).
- Demo accounts and their tokens survive switching `DEMO_MODE` off.
- `upgrade_schema` can race when two instances start at once.
- Shutdown does not wait for a running reset thread.
- `tests/test_permissions.py` lists routes by hand; enumerate `app.routes` instead.
- Design ceiling: admin tabs are stock segmented controls, the users table shows roles as plain text, the activity feed and forbidden page have no in-world treatment.

## Build and ops

- Move `shadcn` from dependencies to devDependencies. It is only needed at build time for `tailwind.css`.
- The README screenshots still show the old UI. Stage 5 replaces them with new screenshots and a demo GIF.

## Sources (stage 3 review, 2026-10-11)

- The design sidecar's Neurologie example uses a circle icon and its navigation snippet says "Dashboard". Synchronize these examples when next updating the design documentation.

## Design ideas (from the finish review, not defects)

- Dark theme rail is near-black. Consider a deep petrol so the shell identity survives in dark mode.
- On mobile the petrol shell disappears behind an off-white top bar. Consider petrol in the mobile top bar.
- The detail page leaves the lower half of the left column empty. The classification explanation could sit on the sheet as a margin note.
- Sheets never overlap like filed records; drawer and stack depth are unused.

## AI (stage 4)


- Live provider smoke test done 2026-10-12 locally (all seven features). Re-check model availability and free-tier limits on the deployed service.
- Verify concurrent global/client reservations on PostgreSQL and trusted deployment proxy identity. Current concurrency regression uses SQLite; HMAC identities need stable JWT_SECRET.
- Cache has no automatic retention policy yet. Add bounded cleanup if real demo usage warrants it; successful content/role/model/prompt identities remain persisted across reset.
- Existing Impeccable surface brief mentions nine specialties; current DESIGN and code correctly contain sixteen. Treat this as pre-existing documentation drift, not a redesign request.

## Deployment (stage 5 review, 2026-10-12)

- `client_ip` takes the leftmost value of `CLIENT_IP_HEADER`; with `X-Forwarded-For` that value is client-controlled (README forbids it). Take the rightmost value or reject that header name.
- Two overlapping resets (a deploy's startup reset and the old instance's loop) can duplicate the entries until the next reset. On PostgreSQL, lock `documents` in SHARE ROW EXCLUSIVE mode first.
- Entry IDs change on every cold start (PostgreSQL sequences keep counting), so shared links to an entry break after the service sleeps. Seed with fixed IDs or `TRUNCATE ... RESTART IDENTITY`.
- An explicit request for `/index.html` is served without `no-cache`.
- The chunk-reload flag stays set if the reload lands on a non-lazy route; the next stale chunk then shows the error page instead of reloading.
- `autoDeployTrigger: commit` deploys even when CI fails; consider `checksPass`.
- The README GIF is 7.7 MB; an MP4 with a poster image would load faster.
