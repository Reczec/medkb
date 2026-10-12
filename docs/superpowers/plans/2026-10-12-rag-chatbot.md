# MedKB semantic RAG chatbot implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement task-by-task in this session; one fresh whole-branch review after implementation. User approved and tasks1–4 completed; task5 implementation is green, operator measurements and final review in progress. The completion record is the authoritative execution evidence.

**Goal:** Extend the bilingual MedKB assistant with measured semantic retrieval and excerpt-grounded answers.

**Architecture:** Separate chunking, native Gemini embedding transport, persisted index, hybrid retrieval and evaluation. Existing /api/ai/ask, AI answer provider, roles, streaming and quotas stay the integration boundary. JSON vectors and exact cosine search fit the small SQLite/Neon corpus without another service.

**Tech stack:** Python/FastAPI/SQLAlchemy/httpx (existing dependencies); React/TypeScript and existing i18n; Gemini gemini-embedding-001, 768 dimensions.

**Spec:** [RAG design](../specs/2026-10-12-rag-chatbot-design.md).

## Global constraints

- English default/German switch; new UI copy in both messages dictionaries; German canonical entries/classifier unchanged.
- No patient data, question/vector logging, real provider calls in automated tests, new dependency/service or public index-build endpoint.
- Fixed official Gemini embedding endpoint, model gemini-embedding-001 and 768 dimensions; validate finite nonzero unit vectors.
- Chunk body <=800 characters, overlap100, title prefix<=200; corpus<=5000 chunks; batches<=16; pause default4s; context<=6000 characters, <=5 documents, <=2 chunks/document.
- RAG_ENABLED=false, EMBEDDING_TIMEOUT=15, provisional RAG_MIN_SIMILARITY=0.45; explicit keyword fallback, 429 never bypassed. Existing global/client reservations count each provider request attempt.
- Full task check command: pytest; ruff check .; ruff format --check .; frontend npm run lint, npm run typecheck, npm test, npm run build, npm run e2e with absolute venv PYTHON.
- One commit/task; local Python3.11, CI3.12/3.13+Postgres. Shared checkout: inspect status before every commit. main pushes auto-deploy Render and reset demo entries.

## Review focus

1. Same/reset IDs with changed text or deleted entries: old chunks cannot become new evidence (Task2 regression).
2. Partial English translations: section fallback remains complete and correctly labeled (Task1/3 regression).
3. Wrong/malformed vector dimensions, NaN, zero norms and changed signature: never mix spaces or report semantic success (Task1/2 regression).
4. Failed provider/index quota or concurrent edit/build: no unbounded public calls, stale ready status or lost successful rows (Task2/3 regression).
5. Unrelated queries, history injection and relevant-but-insufficient excerpts: abstain/admit limits; no invented citations or metric claims (Task3/5 regression).

## File map and interfaces

- Create app/rag/__init__.py; app/rag/chunks.py: frozen Chunk(key, document_id, fingerprint, lang, title, section, text, offset), chunks(document,lang)->list[Chunk], signature(settings)->str.
- Create app/rag/embeddings.py: EmbeddingProvider Protocol.embed(texts:list[str], task:Literal['document','query'])->list[list[float]]; GeminiEmbeddings(settings); normalize(values,dimensions=768)->list[float]; get_embeddings(settings)->EmbeddingProvider.
- Modify app/models.py: Embedding(key:String64 PK, signature:String64 indexed, vector:JSON, created_at). New table via create_all; no existing-column migration needed.
- Modify app/config.py: rag_enabled, embedding_api_key, embedding_timeout, rag_min_similarity, rag_max_chunks; .env.example/docker-compose.yml forward these settings; render.yaml documents flag but keeps it off.
- Create app/rag/index.py: IndexStatus(total,ready), load_current(db,settings,lang)->list[tuple[Chunk,vector]]|None; build_index(db,settings,provider,pause=4)->BuildReport.
- Create app/rag/index_cli.py: explicit --pause, --limit-documents, --cleanup, no startup hooks; uses SessionLocal and the existing trusted global budget pattern.
- Create app/rag/retrieval.py: RetrievalResult(citations:list[dict], entries:list[dict], mode,reason,indexed_chunks); retrieve(db,body,lang,settings,provider,client_id)->RetrievalResult. Sync bounded index/math invoked in awaited worker; DB session never concurrently used.
- Modify app/routers/ai.py: integrate retrieve for ask, no-context response includes retrieval metadata, preserve request contract; app/ai/service.py accept optional retrieval metadata and include it in JSON/SSE done; normalize ask citations to actually used indices. app/ai/prompts.py retains safety rules, explicitly uses retrieved excerpts and insufficiency.
- Modify frontend/src/features/ai/client.ts and AIResponse.tsx: optional retrieval metadata and source section/excerpt disclosures; both dictionaries; existing shell/tokens retained.
- Create evaluation/rag/questions.json, schema/README; app/rag/evaluate.py and evaluation/rag/answer-review.csv template. Completion report docs/reviews/2026-10-12-rag-chatbot.md; update README/AGENTS/NEXT_STEPS.

### Task 1: Deterministic bilingual chunks and validated embeddings

**Tests:** tests/test_rag_chunks.py, tests/test_rag_embeddings.py. **Interfaces:** produces Chunk/chunks/signature and EmbeddingProvider/normalize for Task2/3.

- [ ] Write failing tests: long section covers first/last characters, every chunk<=800,100 overlap; section text not duplicated by composed content; partial English translation keeps German warning signs; reset timestamps/IDs do not change keys but text/model-signature changes do.
- [ ] Write transport failures: exact document/query task fields and config.outputDimensionality768, ordered batch result, wrong count/dimensions, bool/NaN/infinity/zero norm, invalid JSON/429/timeout, no key. Assert secret response bodies never enter public errors; one call/batch and batch<=16.
- [ ] Run focused tests and record meaningful RED before app/rag exists.
- [ ] Implement frozen chunk objects, stable SHA keys/version and current REST request shape with bounded httpx clients; no google SDK dependency. Store settings in config and .env.example. Validate before returning normalized vectors.
- [ ] Focused GREEN, full task checks; commit feat(rag): add bilingual chunks and embedding provider.

### Task 2: Resumable persisted index with freshness and quotas

**Tests:** tests/test_rag_index.py. **Consumes:** Task1 interfaces. **Produces:** load_current/build_index/IndexStatus/BuildReport.

- [ ] Write failing tests: new table existing DB; all ready vectors loaded only for current language/signature/content; reset reuses vectors; edit/delete/restore ID reuse ignores stale evidence; no FK prevents reset deletion.
- [ ] Test missing batch calls provider once and reserves once; second build calls none; partial failure preserves prior successful batches; concurrent insertion conflict doesn't erase success; editing during provider request cannot claim complete coverage; corrupt persisted vector causes incomplete index; corpus>5000 rejects before outbound calls.
- [ ] Test trusted CLI allowance preserves global cap and public client allowance; failed attempts count; missing key/empty corpus produce explicit reports; cleanup deletes only rows outside current corpus/signature and requires explicit flag.
- [ ] Observe RED; implement Embedding model, atomic conflict-safe batch storage, bounded loading, operator CLI with pause/default4 and no startup/public endpoint. Forward settings in Compose; Render flag remains false.
- [ ] Focused GREEN, full task checks; commit feat(rag): persist resumable content-aware embedding index.

### Task 3: Hybrid grounded retrieval in the existing assistant API

**Tests:** tests/test_rag_retrieval.py, tests/test_ai_api.py, tests/test_i18n.py. **Consumes:** Task1 provider, Task2 index, existing lexical retrieval and quota store. **Produces:** RetrievalResult/API metadata contract.

- [ ] Use hand-chosen fake vectors to test cosine ranking, distinct-document top5, top2 excerpts, deterministic ties, context<=6000, RRF60, and semantic threshold gating without lexical bypass. Assert similarity is not labeled medical confidence.
- [ ] Test original question intent/negation preserved; generic follow-up adds prior user topic, bounded800; empty generic input no calls. English fallback content/title follows actual documents; no stale/removed chunk supplied to prompt.
- [ ] Test disabled/incomplete/malformed/upstream failure visibly lexical with reason; valid semantic low similarity no-context and no completion; quota429 never falls back; semantic question/completion consumes two slots, failed calls count. Long provider work does not block health requests.
- [ ] Test auth before outbound calls, existing role tone and safe untrusted JSON prompt; JSON and SSE done include identical metadata; citations only contain referenced server indices/excerpts; out-of-range or missing marks fail honestly; cancellation has no partial successful cache.
- [ ] Observe RED; implement retrieve and integrate ask/service optional metadata; keep other AI features/cache version intact unless prompt changes require an explicit version bump and warmed-cache impact is documented.
- [ ] Focused GREEN, full task checks; commit feat(rag): ground assistant answers in hybrid retrieved excerpts.

### Task 4: Bilingual source evidence and transparent fallback UI

**Tests:** frontend/src/features/ai/AIViews.test.tsx, client.test.ts, frontend/e2e/rag.spec.ts. **Consumes:** Task3 response contract.

- [ ] Read DESIGN.md and applicable Impeccable extension workflow before UI changes. Add failing tests in both languages for hybrid label, fallback reason, safely rendered source excerpts, disclosure keyboard behavior and links with stable server indices.
- [ ] Add browser mocks for semantic answer, lexical fallback and no-context; test patient/doctor roles, English default/German switch, phone375 width, and streaming done. Preserve every existing source-network interception.
- [ ] Observe RED; add localized retrieval line and source disclosures inside current AIResponse/Assistant flow, no new tokens/routes. Render excerpt as text, not arbitrary HTML. Leave old result fixtures compatible when metadata is absent.
- [ ] Capture desktop/mobile light/dark results, inspect accessibility/wrapping and reduced motion; run focused GREEN and full task checks. Commit feat(frontend): show RAG source excerpts and retrieval mode.

### Task 5: Reproducible evaluation, reviews and handoff

**Tests:** tests/test_rag_evaluation.py; fixture dataset under evaluation/rag. **Consumes:** Tasks1–3 runtime retrieval and seed corpus, existing quota/provider answer execution.

- [ ] Freeze 10 dev,20 held-out answerable (10 DE/10 EN),6 held-out controls before first real measurement. Include the spec's20 candidate questions after validating labels/sections. Add dev-only unrelated controls with distinct wording. Mark safety controls separately from unrelated no-answer controls.
- [ ] Write failing tests for dataset validation (unique IDs, known titles/sections, no dev/test duplicates), exact Hit@1/5/Recall@5/MRR@5 formulas on synthetic rankings, provider-failure denominators, no-answer and safety denominators, corpus/dataset fingerprints, deterministic report and latency percentiles.
- [ ] Implement python -m app.rag.evaluate --split dev|test --output PATH [--answers] [--pause 4]. Default retrieval-only; lexical baseline and hybrid measured on identical frozen corpus. Store safe benchmark outputs, never credentials. Any mocked run is labeled synthetic and not semantic quality evidence.
- [ ] Optional real operator run only with configured Gemini free-tier credentials/budget: index; measure dev; select threshold from declared grid; freeze; measure held-out once. Targets Hit@5>=0.90, MRR@5>=0.75, hybrid no worse than baseline and improvements on>=3 declared synonym cases, <=1/4 unrelated controls accepted. Record failures without rewriting test labels or tuning on held-out results.
- [ ] Optional20-answer run produces blank human support-review rubric plus mechanical citation-index validity; do not invent human judgments or equate citations with clinical correctness. If credentials/quota absent, document pending real evaluation and keep RAG disabled.
- [ ] Full task checks; README explains architecture, measured vs pending evidence, reproducible commands and free-tier limits; update AGENTS/NEXT_STEPS and completion record with each task/commit/RED→GREEN/review ruling. Commit test(rag): add frozen retrieval evaluation and documentation.
- [ ] Fresh whole-branch review under executing-plans; one grouped material-fix pass with regression tests and full checks; fresh visual finish/documentation review if required by Impeccable. Preserve deferred minors and review substitutions in durable report.
- [ ] Integrate according to user's local-main instruction after green checks. A main push triggers public deployment; only enable RAG after real index/evaluation. Verify deployed API metadata/index persistence if release is executed, without changing unrelated Render secrets. Leave no foreign changes staged.

## Self-review and execution handoff

The plan covers every spec area with a bounded interface and owns all five review risks in tests. Real embedding quality, free-tier limits and human factual-support labels are explicit measured/pending boundaries. No fake-vector result can satisfy semantic acceptance. UI runtime keeps legacy compatibility while operator tooling makes index state explicit.

Proposed execution: native, task-by-task in this chat, then fresh final review. Review this spec and plan before implementation: provider choice, two-slot semantic request budget, explicit fallback, twenty-question evidence and release enablement are the main decisions.
