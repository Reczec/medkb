# RAG chatbot implementation and evaluation record

User approved the written spec/plan with “ja mach weiter bitte”. Work continued in the shared
local `main` checkout as requested. Baseline `c783e10`; no foreign changes were staged.

## Implementation

| Task | Commit | Verification |
|---|---|---|
| Approved spec and five-task plan | `17f0bfa` | Current product/design/deployment context inspected |
| Bilingual section chunks and embedding provider | `415417a` | 16 focused RED→GREEN; full checks green |
| Resumable content-aware persisted index | `77c2531` | 7 focused RED→GREEN; 805 backend, 224 frontend, 35 browser tests |
| Hybrid bounded retrieval and excerpt-grounded answers | `2ebb0d7` | 10 focused RED→GREEN; 815 backend, 224 frontend, 35 browser tests |
| Source disclosure UI and retrieval mode | `4948e22` | 3 new unit/browser scenarios RED→GREEN; 815 backend, 227 frontend, 38 browser tests |
| Frozen evaluation and documentation | `ed0a638` | 3 evaluation tests RED→GREEN; native transport regression RED→GREEN; 818 backend, 227 frontend, 38 browser tests |

Each task also passed Ruff check/format, frontend lint, typecheck, build and fresh-build browser
tests. Backend has one pre-existing skipped test. No live model is used by automated tests.
Local Python is 3.11; repository CI covers 3.12/3.13 and PostgreSQL separately.

Indexing uses fixed model `gemini-embedding-001`, 768 normalized dimensions, section chunks
<=800 characters with 100 overlap, title prefix<=200, batches<=16, and corpus bound 5000.
SHA keys bind language, actual section text, title/source and embedding space; document IDs and
reset timestamps do not own vector identity. Persisted vectors rebind to current documents,
reject changed signatures or malformed dimensions, resume successful batches and reuse unchanged
seed content across resets. English fallback is section by section. No new service/dependency,
patient-data workflow, public indexing endpoint or startup embedding job was added.

Runtime retrieval embeds the original question, adding the previous user topic for generic
follow-ups, then applies cosine relevance gating and RRF k=60 with keyword ranking. It supplies
up to five documents, two excerpts per document and 6000 context characters. Server-owned
citations include exact excerpts/sections and only indices actually referenced by the completed
answer. JSON/SSE terminal results carry mode and fallback reason. Partial streaming text remains
provisional. Existing roles, safety rules, classifier and document AI cache remain intact.

## Live operator measurement

Measurements use an isolated scratch SQLite database with 47 seed entries, not Neon or production.
The dataset was frozen before the first live probe:
`28ccfe70a6dd4f19f304f81d5bbfd92cb0c5ad56fa245a1c10b6e5bd0f49dd0d`.
Embedding-space signature:
`51ddda2b4449d1f1f772a7f7fc4a730e86ab85685e354eeb1588017f67cf9a9d`.
The bilingual corpus contains 542 chunks; the real index is complete 542/542. The first correctly
shaped 4-second build saved 288 and reported 254 failed chunks across 34 batches. A slower 15-second
resume saved all remaining 254 in 16 batches with zero failures; no successful vectors were lost.
The exact initial upstream-failure cause was not retained, so rate limiting is plausible but
not established. Development threshold selection and held-out results
will be recorded below after the operator run; until then no semantic-quality success is claimed.

The first live probe exposed a REST/SDK mismatch: `config` returned 400. The documented native
`embedContentConfig` was accepted 200 but model001 returned 3072 dimensions, which the adapter
correctly rejected. A controlled probe using still-supported top-level `taskType` and
`outputDimensionality` returned 768. The regression now asserts those effective native fields.
No secret, raw provider error body or query vector was printed or saved. Failed operator attempts
consumed their CLI reservations; the unsuccessful build was interrupted before restarting correctly.
Five bounded direct diagnostic probes outside the CLI reservation store checked transport status,
dimensions and one 16-item batch. They are separate operator actions, never application/test paths.
This compatibility boundary must be rechecked before changing model/schema.

## Reviews and decisions

- Fresh Impeccable finish reviewer inspected eight EN/DE desktop/phone light/dark captures. Its
  one material fix was stale German assistant guidance. Both hints now explain general questions,
  five-entry excerpts and inspectable sources; refreshed German captures scored resolved, ship.
- Detector ran once on the changed AI component/client and returned no findings. The parent
  inspected all eight captures and the four refreshed German ones. Keyboard/phone browser tests
  verify disclosure expansion and absence of horizontal overflow.
- Fresh documenter preserved incumbent DESIGN.md/design.json and wrote the
  [design comparison](2026-10-12-rag-design-documentation.md), including pre-existing drift.
  Generic fresh agents substituted for named finish/documenter agents available in the skill.
- Fresh `gpt-6-astra` whole-branch review (`c783e10..ed0a638`) found no Critical issues, three
  Important issues and no Minor issues; its declined-to-judge list was empty. All three findings
  were accepted and fixed in one grouped pass with nine meaningful RED→GREEN regressions:
  - Keyword fallback now ranks the original question's section intent. Six English/German
    therapy, warning-sign and follow-up scenarios assert actual completion-prompt evidence.
    English diagnosis filler variants now preserve the previous user topic.
  - Evaluation checks corpus content and identity maps before/after retrieval. Same-ID replacement
    and new-ID reset regressions invalidate the run and null ranking metrics; changed citations
    cannot be scored through stale titles.
  - Cancellation shields and drains the bounded retrieval worker, including repeated cancellation,
    before the request session can close. The event-controlled test verifies no access after
    closure, no completion start and no transaction left open.
  No second code reviewer was used. Full-suite verification after the grouped changes is recorded
  below; the review itself used offline fake-provider reproductions and was read-only.

Development was measured once before this review (Hit@5=.90; generic diagnosis follow-up failed),
then repeated after the approved correctness fixes (Hit@5=1.00, MRR@5=1.00). Both raw reports are
retained. Only development data was used: the declared grid rejects both unrelated dev controls
at .55 and .60; the prespecified tie-break selects .60. The threshold decision was saved before
any held-out measurement, with its dev-file SHA256 and `held_out_at_decision=not_run`.
The release default/example threshold now equals this development-selected value.
The dev sweep's first threshold latency includes pacing; subsequent thresholds reuse real vectors
in memory and are not end-user latency measurements.

Rulings made during execution:

1. Use separate `ASK_PROMPT_VERSION=rag-v1`; keep document `PROMPT_VERSION=stage4-v3` because only
   the uncached ask prompt changed and the pinned German warmed-cache invariant must survive.
   Cost if wrong: bump all document cache versions and rewarm.
2. RRF order incorporates lexical rank before the final ID tie-break. Replace the incorrect test
   expecting globally sorted IDs with deterministic repeated retrieval. Cost if wrong: one ranking
   adjustment. Existing API citation tests retain old keys and additionally check excerpts.
3. Native model001 uses verified top-level REST fields instead of the planned SDK-style config.
   Both incorrect forms were rejected by dimensions/status before any relevance measurement.
   Cost if wrong after provider evolution: update the adapter contract and rebuild its signature.

## Release and remaining boundaries

`RAG_ENABLED=false` is retained in Render/default configuration. A code push alone does not
build production vectors or enable semantics. Public enablement requires the current Neon index,
the selected threshold and acceptable real evaluation, followed by live JSON/SSE and reset checks.
No Render secrets or production entries were changed by this work. Quotas remain global/client
and count upstream failures; operator allowance equals the global budget, not an unlimited budget.

Human answer-support review remains separate from mechanically valid citation indices. The blank
CSV rubric requires supported/total claims and appropriate abstention; this is not clinical
validation. Dataset fingerprints, failures and raw rankings make the small curated sample auditable.
The existing English document-cache warmup and refreshed README demo media remain independent
follow-ups. See [next steps](../NEXT_STEPS.md) and [evaluation commands](../../evaluation/rag/README.md).
