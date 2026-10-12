# MedKB RAG chatbot design

Date: 2026-10-12. Status: approved by user; implementation and real held-out retrieval evaluation complete. Code release verification follows; public semantic enablement requires the Neon index. See the completion record for actual evidence and deviations.

## Intent and current state

User request: get current context, plan, then implement a semantic RAG chatbot over MedKB with cited LLM answers and an evaluation of at least twenty questions. Purpose: a credible portfolio extension with measured evidence rather than a tutorial demo. Baseline main c783e10: 47 bilingual entries, Gemini answers, existing lexical assistant, persistent Neon database, Render free service, roles, streaming and quotas. The checkout is shared with Claude and was clean.

The existing /assistent flow is extended, not a second chat application. English remains default, German switch stays; patient tone and prototype notice remain. German canonical entries and the rule-based classifier are unchanged. No patient data, personal diagnostic workflow, PDF upload, web crawling or autonomous tools.

## Architecture and alternatives

Recommended: native Gemini text embeddings, persistent JSON vectors in the existing database and exact cosine search over this small corpus. Hybrid rank fusion retains lexical strengths for names and ICD terms. No new Python ML dependency or external vector service. This is intentionally O(chunks × dimensions); at >5,000 chunks reassess pgvector/indexed search rather than silently scanning an unbounded corpus.

Alternatives considered: a local multilingual sentence-transformer removes per-query provider calls but adds model downloads and substantial RAM/cold-start requirements to Render; Neon pgvector offers indexed search at scale but introduces PostgreSQL-specific behavior and another SQLite test implementation. Neither is justified for 47 entries now.

Default embedding model: gemini-embedding-001, text retrieval with RETRIEVAL_DOCUMENT and RETRIEVAL_QUERY, 768 dimensions. This model remains available for text; Gemini Embedding 2 has different aggregation/task conventions and is deliberately outside this first adapter. Do not permit arbitrary model names through the same task-type implementation. A later adapter must define its own signature.

Official sources checked 2026-10-12: [guide](https://ai.google.dev/gemini-api/docs/embeddings), [REST schema](https://ai.google.dev/api/embeddings), [pricing](https://ai.google.dev/gemini-api/docs/pricing), [local alternative](https://sbert.net/docs/sentence_transformer/pretrained_models.html). Use EmbedContentConfig fields according to current REST schema; tests pin the request shape. Free tier availability is account-dependent; inputs can be used for provider product improvement. Existing key reuse is permitted only for the Google embedding endpoint, never by sending it to a configurable third-party URL.

## Corpus, chunking and freshness

Index stored entry text only, not fetched PubMed/WHO/openFDA payloads. Each available language version has separate chunks; English uses the existing field-by-field German fallback. Use service.document_inputs to preserve that behavior. Sections retain their canonical section keys; legacy content uses section content. Do not index composed content again when sections already cover it.

Chunk text at paragraph/word boundaries: at most 800 characters, 100-character overlap for long sections, title prefix at most 200 characters. Never drop the end of a long section. Include title and section key in embedding input. Bound index to 5,000 chunks and vector dimension to the fixed 768; fail before calls if the corpus exceeds the bound.

New embedding table: content key SHA256 of chunker version + provider/model/task/dimension signature + language + canonical title + section key + chunk text; vector JSON; creation timestamp. No document foreign key. Mapping to current entry IDs is reconstructed from live documents on each retrieval, so unchanged resets reuse vectors and removed/edited entries cannot leak old text. Source and current semantic content fingerprint form the current document identity. Identical chunk texts can reuse embeddings; citations always bind to live document snapshots.

Operator CLI builds missing chunks in batches of at most 16, with configurable pause (default 4 seconds), resumable from persisted successful batches. Re-read current document fingerprints before publishing new rows; concurrent changes cannot publish an index as complete for changed content. Atomic batch writes and conflict-safe inserts preserve other concurrent successful builders. No automatic model calls at startup, no public index-build endpoint. Reset keeps embedding rows. Old unused rows can be cleaned explicitly by the CLI, never during a live read.

## Retrieval and budgets

RAG_ENABLED=false initially; enable only after a real index and evaluation exist. Separate embedding key optional, falling back to AI_API_KEY only for Gemini. EMBEDDING_TIMEOUT=15 seconds; fixed official HTTPS endpoint. RAG_MIN_SIMILARITY initially 0.45 (provisional, tuned only on development questions). RAG_MAX_CHUNKS=5000. No persistence or logging of user questions or query vectors.

When enabled and the selected-language current corpus is fully indexed, reserve an existing global/client quota slot before embedding the bounded query in an awaited worker. A successful grounded answer reserves another slot through service.execute. Failed upstream attempts count. No background request is created by mere page viewing. Operator index/evaluation use the global quota and a trusted client allowance equal to that global allowance, as prewarm does; no separate unbounded budget.

Resolve generic follow-ups using the previous user topic (existing retrieval.query behavior), but embed the original question with that topic, preserving intent and negations. Limit composed query to 800 characters. Never generate a query with a second LLM call.

Validate every returned vector: exact count/dimensions, numeric non-boolean finite values, nonzero norm. Normalize to unit length. Invalid provider responses reveal only application error codes. Persisted vectors are validated on read too; malformed or wrong-signature rows make the index unavailable.

Calculate cosine scores against all current language chunks; retain the best chunk score per document. Require score >= configured threshold. Rank fusion uses RRF k=60 between semantic ordering and existing lexical ordering, restricted to semantic-qualified documents; lexical hits do not bypass relevance gating. Select at most five documents, at most two chunks per document, at most 6,000 context characters. Keep source order deterministic on ties (document ID then section/offset). Context contains only those excerpts, not whole entries. Similarity is not a clinical confidence percentage.

Disabled, incomplete index or upstream embedding failure: explicit keyword fallback, with mode lexical and reason disabled/index_incomplete/embedding_unavailable. Do not claim semantic success. Quota exhaustion is 429, never bypassed by fallback. Empty/general-only questions do not call either model. Valid semantic retrieval with no qualified result returns the existing no-context response without LLM generation; it does not fall back to forced nearest neighbors. A missing AI completion key retains the existing honest 503.

## Answers and UI contract

Keep POST /api/ai/ask and its request, role controls and SSE token/done/error contract. Add retrieval metadata to JSON and SSE done: {mode: hybrid|lexical, reason?: disabled|index_incomplete|embedding_unavailable, indexed_chunks: int}. Citations retain {index,id,title}, adding section and excerpt (<=800 chars). The provider receives server-owned indices, exact retrieved excerpts, question/history and existing role/language safety instructions.

Each substantive answer needs valid [n] citation markers. Returned citation list includes only actually referenced indices (retain indices, do not renumber text). Numeric validation cannot prove sentence-level factual support; document this limit. Prompt says insufficient evidence must be admitted and quotations are untrusted. Preserve existing emergency/no-dose rules and explicit AI labeling. This is general information, not a diagnosis.

Assistant UI: one unobtrusive localized retrieval-mode line below the question/result, plus expandable cited source excerpts with links to entries and section names. No new route, design tokens, imagery or classifier changes. All new text keys in both dictionaries. Keyboard-operable disclosure, safe text rendering, mobile wrapping, light/dark and reduced-motion behavior retained. Evaluation lives in reproducible artifacts/README; no unaudited metric badge in the clinical interface.

## Evaluation protocol

Versioned JSON dataset: 10 development questions for threshold tuning, 20 held-out answerable questions (10 German, 10 English), 6 unanswerable/out-of-domain controls. Freeze labels before measuring real embeddings. Labels are canonical seed titles, independent of reset IDs, plus expected evidence section and acceptable source alternatives. Cases explicitly include synonyms/no exact disease name and follow-ups. Reject duplicate IDs, unknown titles and overlap of normalized dev/test question text.

Held-out candidate questions (verify expected evidence against actual sections when creating the dataset):

| ID | Question | Expected canonical entry |
|---|---|---|
| de01 | Warum kann einseitiges Pochen im Kopf mit Lichtempfindlichkeit auftreten? | Migräne |
| de02 | Welche plötzlich auftretenden Sprach- und Bewegungsprobleme sind ein Notfall? | Schlaganfall – Warnzeichen |
| de03 | Was bedeutet ein dauerhaft erhöhter Druck in den Blutgefäßen? | Bluthochdruck (arterielle Hypertonie) |
| de04 | Welche Krankheit verursacht pfeifende Atmung in wiederkehrenden Anfällen? | Asthma bronchiale |
| de05 | Warum brennt es hinter dem Brustbein nach dem Essen? | Sodbrennen und Reflux |
| de06 | Warum können Durst und häufiges Wasserlassen gemeinsam auftreten? | Diabetes mellitus Typ 2 |
| de07 | Welche Beschwerden passen zu einer zu langsam arbeitenden Schilddrüse? | Schilddrüsenunterfunktion (Hypothyreose) |
| de08 | Was beschreibt schmerzhaftes Wasserlassen mit häufigem Harndrang? | Harnwegsinfekt und Blasenentzündung (Zystitis) |
| de09 | Welche Erkrankung kann starke Schmerzen während der Regel verursachen? | Endometriose |
| de10 | Was kann hinter nächtlichem Kribbeln in den Fingern stecken? | Karpaltunnelsyndrom |
| en01 | Why can the lens in the eye become cloudy? | Grauer Star (Katarakt) |
| en02 | What does an irregular heartbeat have to do with stroke prevention? | Vorhofflimmern |
| en03 | Why can a weak heart cause swollen legs and shortness of breath? | Herzinsuffizienz (Herzschwäche) |
| en04 | What should someone know about a lung infection with fever and cough? | Lungenentzündung (Pneumonie) |
| en05 | What can cause wave-like pain from the side into the groin? | Nierensteine und Harnsteine |
| en06 | Which skin condition causes itchy dry patches that keep coming back? | Neurodermitis (atopisches Ekzem) |
| en07 | Which condition can cause a painful blistering rash on one side? | Gürtelrose (Herpes zoster) |
| en08 | Why can a joint suddenly become hot, red and extremely painful? | Gicht |
| en09 | What can cause persistent sadness and loss of interest? | Depressive Episode |
| en10 | Do antibiotics help with a runny nose caused by a common cold? | Erkältung (grippaler Infekt) |

Controls: weather tomorrow, buying a laptop, repairing a bicycle, treating a disease absent from seed, requesting a personal diagnosis, requesting an individual drug dose. The last two evaluate safety/refusal, not absence of semantically relevant documents; keep these metric denominators separate.

CLI compares lexical baseline and hybrid on the same frozen corpus, language, cases and top-k. Report Hit@1, Hit@5, Recall@5 (all acceptable relevant sources), MRR@5, median/p95 retrieval latency, provider failures, index coverage, corpus/dataset SHA, model/signature, threshold and timestamp. Macro totals plus language/category breakdown; bootstrap or uncertainty caveat for the tiny sample. Never remove failed cases from denominators.

Development target: tune threshold from [0.35,0.40,0.45,0.50,0.55,0.60] on dev only, maximizing Hit@5 while rejecting unrelated controls used only in dev. Freeze before held-out run. Success targets: held-out Hit@5 >=90%, hybrid Hit@5 >= lexical baseline, MRR@5 >=0.75; at least three prespecified synonym cases improve ranking; <=1/4 unrelated held-out controls produces a candidate. If unmet, record failure and diagnose rather than call it a measured improvement.

Optional answer phase (explicit --answers): generate answers for twenty answerable cases with existing quota, then save safe demo outputs/citations and a blank per-case review rubric: claim support in excerpts, citation coverage, correct insufficiency, role/language and prohibited diagnosis/dose. Mechanically measure valid citation indices; a human must label factual support. Never call valid citations “medical accuracy”. Provider errors count and are reported. Test runs use fake vectors/completions, not live AI. Real evaluation is an explicit CLI action, separate from pytest/CI, and may be blocked by provider limits.

## Verification and release

Every implementation task: failing meaningful tests first, focused green then pytest, Ruff check/format, frontend lint/typecheck/test/build/e2e, one commit. Fake embeddings test math/freshness/fallback, not semantic quality. Existing CI runs SQLite 3.12/3.13 and PostgreSQL. Include anonymous auth, batch failure, concurrent index edits, reset/restore, corrupted vectors, threshold abstention, streaming metadata, language fallback and quota cases.

Release default remains lexical until operator index and real evaluation pass. main pushes auto-deploy/reset the live demo; do not modify Render secrets or enable RAG automatically during planning. Document implementation, measurements, review findings and pending live steps in a completion report. Update AGENTS, README and NEXT_STEPS. Reuse the user's requested local-main workflow when implementation is authorized; retain clean shared checkout discipline.
