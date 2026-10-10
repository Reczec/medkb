# Backlog

Follow-ups deferred from the stage 1 reviews (code review and design review, 2026-10-10). None blocks stage 2. Pick them up when touching the area, or batch them before stage 5.

## Behaviour

- Editor: Escape does nothing in the "Änderungen verwerfen?" dialog. Add `onOpenChange` → `blocker.reset()` in `frontend/src/features/editor/EditorPage.tsx`. There is also no `beforeunload` guard for closing the tab or reloading.
- Activity dates: `formatDay` in `frontend/src/lib/format.ts` parses `YYYY-MM-DD` as UTC midnight, so the date shows one day early west of UTC. Format with `timeZone: 'UTC'`. The buckets are UTC days.
- `AdminTokenGate` drops a stored token on any error. Drop it only on 401. A token that expires mid-session ends in an error card with no way back to the gate, and backend `detail` texts are English. Most of this goes away with stage 2 auth.
- Archive restore shows no progress and does not guard against double submit. Defer `URL.revokeObjectURL` after the download click.
- `ThemeToggle` and `CategoryPicker` use `role="radio"` without arrow-key navigation. Either implement roving tabindex or switch to `aria-pressed` buttons.
- Command palette: the "Keine Einträge gefunden." message never shows, because the action items always match.
- Deleting an entry refetches it (404) before navigating away. Use `removeQueries(['document', id])`.
- Knowledge base list: with `keepPreviousData`, a failed refetch shows the error card above stale results.

## Build and ops

- `/assets` has no `Cache-Control: immutable` header (the comment in `app/spa.py` claims long caching). `HEAD /` returns 405.
- Move `shadcn` from dependencies to devDependencies. It is only needed at build time for `tailwind.css`.
- The CI docker job only builds the image. Also run it and curl `/api/health` and `/`.
- The main JS chunk is over 500 kB. Lazy-load the routes, the dashboard charts first.
- The README screenshots still show the old UI. Stage 5 replaces them with new screenshots and a demo GIF.

## Design ideas (from the finish review, not defects)

- Dark theme rail is near-black. Consider a deep petrol so the shell identity survives in dark mode.
- On mobile the petrol shell disappears behind an off-white top bar. Consider petrol in the mobile top bar.
- The detail page leaves the lower half of the left column empty. The classification explanation could sit on the sheet as a margin note.
- Allgemeinmedizin's hue (196) equals the primary teal, so its tab can read as an action colour.
- Sheets never overlap like filed records; drawer and stack depth are unused.
