# Stage 4 completion record — AI assistance

Date: 2026-10-11. Request: implement the next stage and document all work. Scope: [stage 4 plan](../superpowers/plans/2026-10-11-etappe-4-ki.md) against [v2 spec](../superpowers/specs/2026-10-10-medkb-v2-design.md), PRODUCT and DESIGN. Native inline implementation; feature branch v2-stage4, baseline c422e54. The checkout is shared; baseline was clean and no foreign changes were overwritten.

## Implementation and commits

| Commit | Work | Validation |
|---|---|---|
| b462fa1 | Plan, interfaces, safety boundaries and review focus | Product/spec/source documentation read |
| 0926adc | Configurable OpenAI-compatible completion/stream provider |14 new tests RED→GREEN;500 backend,128 frontend,25 browser;Ruff71 |
| 75b27b3 | Persistent cache and atomic global/client UTC quotas |7 tests RED→GREEN, including concurrent final SQLite slot;507 backend,128 frontend,25 browser;Ruff73 |
| 40aeabf | Role endpoints, constrained prompts/output, PMID abstract transport, trusted explicit warmup |39 tests RED→GREEN;546 backend,128 frontend,25 browser;Ruff79 |
| 032547b | AI result panels, assistant, document/study controls, editor review/apply, dashboard usage |141 frontend,547 backend,25 browser;lint/typecheck/build/Ruff green |
| f97f251 | Five deterministic AI browser flows, visible saved provenance, configuration/docs and captures |Final check/review results below |

Each task ran pytest, Ruff check/format, frontend lint/typecheck/test/build/e2e. RED was observed before implementation: missing provider/store/routes/components, missing editor/tab controls, split-CRLF framing and reset-cache regression. A Radix tab test needed mousedown followed by click, matching existing test helpers. An async pytest test used asyncio.run because no asyncio pytest plugin is installed.

## What changed

Backend: app/ai separates provider, prompts, schemas, transactional store and validated execution. New ai_cache and ai_usage tables are created by create_all. HTTP clients close after requests; bounded output20,000 chars,4096 completion tokens, configured timeout30s. Provider failures expose only application error codes. Seven POST feature endpoints plus staff GETusage; anonymous401 and wrong role403 precede provider setup checks.

All roles can explain entries, read general warning signs and ask grounded questions. Staff can summarize entries/actual NCBI PMID abstracts. Admin can request a validated DocumentCreate draft or separate known-category/confidence opinion. A draft never inserts a document; provenance is forced true. Draft metadata URLs/source/category are not accepted from the model. Missing abstracts/providers fail honestly.

Questions normalize question words and reuse prior user topics for generic follow-ups, then use the existing AND keyword search's top five entries, six bounded history messages and role-specific prompts. No matches: no provider call or quota. Citations are server-owned IDs/titles; missing/out-of-range model indices fail. This does not establish factual support for every sentence. Quoted input/history is untrusted, prompts prohibit individual diagnoses/dosages and reference144; no patient data is permitted.

Frontend: /assistent and navigation/patient-home links; inline AI response sheets with source links, provenance and actionable error/retry states; patient explanation/warning controls and a staff-only summary tab; study abstract buttons; dashboard global UTC usage. Tokens are provisional until done. Text is rendered as React text, never model HTML. Requests abort on replacement/unmount; split UTF-8 and LF/CRLF SSE frames are tested. Admin reviews content and metadata before explicit apply; fields remain editable and require Save. AI category selection is a separate explicit action; the rule classifier remains unchanged. Draft generation is available only for new entries, preserving existing provenance on edits. Saved drafts show KI-generiert on detail pages.

## Decisions and deviations

- Default gemini-3.5-flash-lite, not legacy2.5Flash: official Google model docs restrict older models for new projects. BaseURL/key/model are configurable. [Compatibility](https://ai.google.dev/gemini-api/docs/openai), [model policy](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash), [pricing](https://ai.google.dev/gemini-api/docs/pricing), [Groq alternative](https://console.groq.com/docs/openai) checked during planning. Free tier availability/account limits are not guaranteed; Google lists free-tier input as product-improvement data.
- Cache key includes semantic entry snapshot, feature, stable seed identity or ordinary entry ID, role, provider/model and prompt version. Excludes IDs and reset timestamps from semantic snapshots: a regression initially showed unchanged seeds missing cache after reset; shared snapshot fixed it. Changed content remains a different identity. No ask/draft/classify cache; failed/incomplete output never cached.
- Quotas reserve global first and HMAC client second, then commit both;429 rolls both back and provides time to UTC midnight. Provider attempts consume quota even on failure, matching real upstream work. Direct client IP only; stable JWT_SECRET salts identity. Proxy trust is deployment work.
- Explicit trusted warmup temporarily uses the global budget as its own client budget, without modifying public30/day. Eight role/feature variants per entry =376 potential calls for47 entries. Missing key exits without requests; no automatic startup warmup. No live warmup was run.
- Inline panels instead of modal interruption preserve reference reading and ordinary filing-room design. No new tokens or imagery. DESIGN.md and design.json stay intact. Pre-existing brief/sidecar drift is reported in BACKLOG.
- Browser draft test cleans up its saved entry so the following seed-statistics tests remain independent. Captured fixture explanations/reference titles match the actual displayed seed entry; these are deterministic mocks, not real provider output.

## Verification and boundaries

Local Python3.11; project CI targets3.12/3.13. Latest implementation checks: pytest547, Ruff79 files, frontend141, lint/typecheck/build pass. Full browser run and reviews recorded after completion below. Existing warnings: oversized JS chunk, Vite config native-loader __dirname warning, FastAPI/httpx testclient deprecation; already documented follow-ups. Browser fixture backend uses throwaway SQLite and mocked source/AI endpoints.

No real AI key or WHO credentials supplied. Real provider output, model access/free quota, WHO diagnosis/code mappings, PostgreSQL concurrent quota behavior and trusted deployment proxy identity remain live-verification work. Prompt rules/valid source indices do not certify clinical correctness. No service registration/deployment was performed.

## Visual evidence and independent review

Four surfaces (patient explanation, staff summary, assistant, editor draft),1440×900/375×812, light/dark:16 full-page captures under ignored .impeccable/review/ai-*.png. All required files opened to validate evidence before review. Capture command: MEDKB_CAPTURE_AI=1 npm run e2e, with absolute venv PYTHON. Impeccable detector on changed AI/document/editor targets returned []. These verification screenshots are not new shipping image assets.

Code/finish reviewer findings and documenter outcome are appended here before completion. The named shipped reviewer types are unavailable through this harness's generic spawn API; fresh isolated agents receive the required contracts and the substitution is disclosed.

## Next steps

## Final independent review and fixes

Fresh isolated code review: no Critical findings; all five Important findings accepted and fixed in one grouped pass:

- PostgreSQL seed IDs change after reset: canonical source/title seed identity plus complete semantic snapshot now reuses unchanged cache entries. IDs and timestamps are excluded from snapshots; ordinary entries retain their ID identity. Reset regression forces a changed ID; RED then GREEN. Cache version is stage4-v2.
- Blocking PubMed work: fetch/cache runs in asyncio.to_thread with sequential session use. Concurrent health-request regression: RED then GREEN.
- Natural questions and generic follow-ups: bounded German question-word normalization and latest user-topic fallback. Three regression cases: RED then GREEN. Retrieval remains lexical.
- Compose configuration: all six AI settings forwarded; synthetic-key configuration validation RED then GREEN, without printing secrets.
- Assistant retry history: successful retries update conversation history and clear the submitted question. Frontend regression RED then GREEN.

Final full checks: 551 backend tests, 142 frontend tests, 30 browser tests; Ruff check/format (80 files), lint, typecheck and production build green. Docker CLI configuration validation passes; Docker Desktop daemon unavailable, so PostgreSQL runtime verification remains pending.

Minor accepted/deferred: staff “Einfach erklären” uses professional tone; tracked in BACKLOG. Review focus exclusions: real provider/model/free-tier access and quality without credentials, PostgreSQL concurrency/proxy runtime without deployment, and live WHO/clinical truth beyond deterministic contracts. None is claimed verified.

Fresh visual finish review disposition: ship, no material fixes. Sixteen desktop/phone light/dark captures reviewed; runtime behavior and every integration file were outside its scope. Named reviewer types unavailable: generic fresh isolated agents received their contracts. The [documenter report](2026-10-11-stage4-design-documentation.md) records unchanged DESIGN.md/design.json and rechecks behavior-only retry changes.

Integration follows the user's explicit local-main and push instructions. Grouped fixes are recorded as “fix(ai): address stage 4 review findings” in git log. No worktree created. Stage 4 ignored execution scratch is removed after preserving this record.

[Next steps](../NEXT_STEPS.md): configure one real provider smoke test, optionally warm seeded results, resolve auth/reset/archive follow-ups, then plan stage5 Render/Neon deployment and public demo evidence. [BACKLOG](../BACKLOG.md) retains deferred issues and live verification boundaries.

## Local integration

Fast-forwarded main from c422e54 to c65c0f1 after fetching origin/main and confirming no upstream changes. Full backend/frontend suites repeated on the identical merged implementation; all other final checks covered this same tree. Publication is recorded in the following documentation commit and remote verification. Earlier user instructions explicitly authorize local main and push.
