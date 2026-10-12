# Frozen MedKB RAG evaluation

`questions.json` was frozen before live embedding measurements on 2026-10-12: ten development
questions, two separate development controls, twenty held-out answerable questions (ten German,
ten English), four unrelated held-out controls and two safety controls. Labels use canonical
German titles and expected sections. Safety controls are not included in unrelated rejection
rates. These are curated, synthetic examples; no patient data or visitor questions are stored.

## Reproduce

Use an isolated, newly seeded database for measurements, not a reset of the production database.
In PowerShell from the repository root, with configured Gemini credentials in `.env`:

```powershell
$env:DATABASE_URL = 'sqlite:///./rag-evaluation.db'
.venv/Scripts/python.exe -m app.seed
.venv/Scripts/python.exe -m app.rag.index_cli --pause 15
.venv/Scripts/python.exe -m app.rag.evaluate --split dev --sweep --output evaluation/rag/dev.json
# Select and freeze the threshold using only dev results, then run test once:
.venv/Scripts/python.exe -m app.rag.evaluate --split test --threshold 0.60 --answers --output evaluation/rag/test.json
```

Replace the illustrative threshold with the recorded development decision. The declared grid is
0.35, 0.40, 0.45, 0.50, 0.55, 0.60. Maximize dev Hit@5 subject to rejecting both dev unrelated
controls; break ties with MRR@5, then the highest threshold. Never tune using held-out labels.
The dev sweep reuses real query vectors only in memory; conservative request reservations still
count each evaluation attempt. Trusted CLI operations retain the global daily budget. Regular
public requests retain both global and client quotas. A semantic answer uses one embedding and
one completion reservation. Provider failures consume their reserved attempts.

Sweep latency includes operator pacing on the first threshold and cached vectors thereafter;
only the separate held-out run measures uncached query latency without pacing inside its timer.
Corpus or identity changes invalidate the whole run and null ranking metrics; such a report is
not release evidence. Interrupted indexing retains valid batches; the live run needed 15-second
batch spacing to finish reliably rather than the CLI's default 4 seconds.

Default evaluation is retrieval-only. `--answers` generates grounded answers through the actual
answer service and a blank `.review.csv` rubric. `validated` means mechanically valid server
citation indices, not factual support or medical correctness. Human reviewers must fill supported
claims / total claims and appropriate abstention, using the saved excerpts and answers. No human
judgments are fabricated. Answers skipped for missing context/failures remain explicit.

## Metrics and interpretation

Both methods use the same frozen corpus. The baseline is the existing lexical top-five search;
hybrid candidates are the documents actually supplied as bounded runtime evidence. Hit@1/5
means any expected title occurs within that rank. Recall@5 averages the fraction of expected
titles retrieved per answerable question; MRR@5 averages the reciprocal first relevant rank
(zero when absent). Provider failures remain in the denominators, and a lexical fallback is not
counted as semantic success. Median/p95 use measured retrieval latency; p95 is nearest-rank.
Language breakdowns and raw rankings are included. Missing answerable cases and unrelated
acceptances remain visible. Safety controls require answer review; retrieving a document for
one is not itself a failed refusal.

Acceptance targets: held-out Hit@5 >=90%, MRR@5 >=0.75, no regression versus lexical Hit@5,
ranking improvements on at least three predeclared synonym cases, and at most one of four
unrelated controls accepted. This small editorial sample is portfolio evidence, not a clinical
validation, a representative patient sample, or a guarantee on new questions.

Reports include dataset/corpus SHA256 fingerprints, embedding-space signature, threshold,
index/chunk count, measured latencies and sanitized failures. Credentials and query vectors are
never written to reports. Automated tests use synthetic vectors and do not measure semantics.
Live runs are explicit operator actions. Free-tier availability and quotas depend on the account;
do not enable billing solely to run the benchmark. Keep `RAG_ENABLED=false` until a real current
index and acceptable measurements exist. Deploying code alone does not enable RAG.
