# MedKB Azure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a temporary Azure portfolio demo with reproducible infrastructure, tested OIDC deployment, rollback and documented credit controls.

**Architecture:** Container Apps Consumption runs the existing image from public GHCR, backed by an isolated free Neon database. Bicep owns infrastructure; a secure deployment helper preserves application secrets. Render remains the permanent demo.

**Tech Stack:** Bicep, Azure CLI, GitHub Actions/OIDC, Python standard library, existing Docker/FastAPI/React/PostgreSQL stack.

**Spec:** `docs/superpowers/specs/2026-10-12-azure-cloud-design.md` (approved 2026-10-13).

## Global Constraints

- Work locally on `main`; one commit per task; preserve concurrent Claude changes.
- No additional personal payments, offer upgrades, removed spending limits or new financial terms.
- Proposed operating limit: EUR 5 credit consumption, alerts at 50/80/100 percent. Alerts do not enforce a cap; delayed billing can exceed this target. No provisioning if the user requires a guaranteed EUR 5 cap.
- Independently verify protected trial status before provisioning; current observed expiry is 2026-10-20.
- West Europe, Consumption only, 0.5 vCPU/1 GiB, replicas 0..1, Single revision, external HTTPS, port 8000, insecure HTTP disabled.
- No ACR, Azure PostgreSQL, Log Analytics, Application Insights, VNet/NAT/private endpoints, dedicated compute or paid Defender plan.
- Separate free Neon database; never use Render's database. `DEMO_MODE=true`, `DEMO_RESET_HOURS=3`, persistent JWT secret.
- RAG off until 271 current chunks per language are verified; threshold 0.60; no startup/public indexing or bulk answer prewarm.
- No real patient data; preserve languages, roles, classifier and prototype notices. No UI changes.
- All task commits require backend pytest/ruff and frontend lint/typecheck/test/build/e2e per AGENTS.md. Live checks are explicit operator checks, never paid model calls in tests.

## Review Focus

1. Missing or expired trial protection must block provisioning (Task 1).
2. Repeated Bicep deployment must preserve all existing app secrets without printing them (Task 2).
3. Fork, failed CI or mismatched SHA must never publish/deploy (Task 3).
4. Wrong subscription/resource group or malformed digest must block rollback/cleanup (Task 4).
5. Partial/stale RAG index and spoofed leftmost IP must not silently enable RAG or bypass quotas (Task 5).

---

## File map and shared verification

Create `scripts/azure/__init__.py`, `preflight.py`, `deploy.py`, `smoke.py`, `cleanup.py` and matching `tests/test_azure_*.py`: guarded operator commands and offline behavioral tests.
Create `infra/azure/main.bicep`, `infra/azure/parameters.example.json`: desired resource graph and nonsecret examples.
Create `.github/workflows/azure-deploy.yml`; modify `.github/workflows/ci.yml` and `.dockerignore`: validation and tested-commit publication.
Create `docs/AZURE.md`, `docs/reviews/2026-10-13-azure-deployment.md`; modify `README.md`, `docs/NEXT_STEPS.md`, `AGENTS.md`: operation and measured evidence.

At each task's green step run `.venv/Scripts/python.exe -m pytest`, `.venv/Scripts/python.exe -m ruff check .`, `.venv/Scripts/python.exe -m ruff format --check .`; from `frontend/` run `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, then set `PYTHON` to the absolute venv executable and run `npm run e2e`. Do not run shared database/e2e checks concurrently. Install missing Azure CLI/Bicep only from official vendor distribution; record versions and installation location.

### Task 1: Fail-closed operator preflight

**Files:** Create `scripts/azure/__init__.py`, `scripts/azure/preflight.py`, `tests/test_azure_preflight.py`, `docs/AZURE.md`.

**Interfaces:** Produces `validate_trial(account: dict, expires_on: str, today: date) -> None` and `validate_target(actual_subscription: str, expected_subscription: str, resource_group: str) -> None`; invalid conditions raise `ValueError`. CLI `python -m scripts.azure.preflight --subscription ID --resource-group NAME --expires-on YYYY-MM-DD` exits nonzero before writes on failure.

- [ ] Write tests: `validate_trial({"state": "Enabled", "subscriptionPolicies": {"spendingLimit": "Off"}}, "2026-10-20", date(2026,10,13))` raises; missing policy also raises; spendingLimit `On` plus valid date succeeds; date 2026-10-20 blocks. Mismatched subscription and resource group outside prefix `medkb-azure-demo-` raise.
- [ ] Run `pytest tests/test_azure_preflight.py -v`: expect missing module/functions failure.
- [ ] Implement read-only `az account show` capture, exact target comparison, enabled subscription and spendingLimit `On` checks. Verify the actual trial offer and expiry through portal as well; a CLI policy alone is not evidence of credit availability. Record dated redacted observations. Verify remaining free Neon capacity. No account upgrade, resource or identity creation here. Document EUR 5 target, billing delay, alerts and manual expiry cleanup.
- [ ] Run focused tests and shared verification; all pass. Record any unavailable tooling as a blocker, never substitute an unchecked deployment.
- [ ] Commit `feat: add guarded Azure deployment preflight` with these files.

### Task 2: Bounded infrastructure and preserved secrets

**Files:** Create `infra/azure/main.bicep`, `infra/azure/parameters.example.json`, `scripts/azure/deploy.py`, `tests/test_azure_deploy.py`; modify `.dockerignore`, `docs/AZURE.md`.

**Interfaces:** Consumes Task 1 guards. Produces `validate_digest(image: str) -> None`, `build_parameters(image: str, secrets: list[dict], rag_enabled: bool) -> dict`; CLI `python -m scripts.azure.deploy --subscription ID --resource-group NAME --app NAME --image ghcr.io/reczec/medkb@sha256:HEX --expires-on DATE [--apply] [--bootstrap-secrets-file PATH]`. Default is what-if; apply is explicit. Bootstrap file is ignored, locally permission-restricted, and deleted after successful transfer.

- [ ] Write tests asserting digest must contain exactly 64 hexadecimal characters; secret values survive `build_parameters` unchanged and never occur in captured console output. Compile Bicep to JSON and assert only Container Apps environment/app resources, Consumption profile, CPU 0.5, memory `1Gi`, min/max 0/1, revision `Single`, targetPort 8000, allowInsecure false, logs destination `none`, secure secret-array parameter and no secret outputs.
- [ ] Run `pytest tests/test_azure_deploy.py -v`: expect missing helper/template failure.
- [ ] Implement Bicep with stable Microsoft.App API `2025-07-01` after checking both resource schemas. Parameters: app/environment names, location default `westeurope`, digest image, `@secure() appSecrets array`, `ragEnabled bool=false`. Environment variables reference application secrets; preserve uvicorn `--no-proxy-headers`, set Azure `CLIENT_IP_HEADER=X-Forwarded-For`. Include existing quota/provider settings from application config explicitly; no Render-only values.
- [ ] Implement helper: preflight before writes; bootstrap secrets from restricted file, routine secrets from captured `az containerapp secret list` output. Pass secure parameters via restricted temporary JSON file (path only in command), never print values or raw subprocess errors containing them, delete in `finally`. Missing required DATABASE_URL/JWT_SECRET blocks. What-if and apply consume the same parameters. Output only public hostname/image/revision. Exclude `.env.*`, operator files and `.impeccable/` from Docker context. Examples contain placeholders only.
- [ ] Run compiled-template and helper tests, Bicep lint/build and shared verification. Mock CLI subprocesses; no Azure writes in tests.
- [ ] Commit `feat: define bounded Azure infrastructure and secure deployment`.

### Task 3: Tested-commit GitHub delivery

**Files:** Create `.github/workflows/azure-deploy.yml`, `tests/test_azure_workflow.py`; modify `.github/workflows/ci.yml`, `docs/AZURE.md`.

**Interfaces:** Consumes Task 2 CLI. Produces a public GHCR digest built from the exact successful CI SHA; environment `azure-demo` variables `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_APP_NAME`, `AZURE_TRIAL_EXPIRES_ON` (no committed real identifiers).

- [ ] Write workflow contract tests: successful `CI` workflow_run, repo `Reczec/medkb`, main branch and checkout of event head_sha required; fork/failed run rejected; image/deploy jobs have separate packages-write/id-token-write permissions; deployment concurrency and protected environment required. Manual dispatch verifies successful CI for its selected main SHA before publication.
- [ ] Run `pytest tests/test_azure_workflow.py -v`: expect absent workflow failure.
- [ ] Add credential-free PR Bicep/helper validation. Pin official actions to verified commit SHAs; use actionlint. Build existing Dockerfile, publish SHA-tagged GHCR image, deploy its returned digest only. Never interpolate untrusted event strings into shell code. Verify package public visibility before anonymous Azure pull. Deployment performs preflight, what-if, apply, active revision/digest comparison and bounded health checks. Routine job never creates role grants or supplies new application secrets.
- [ ] Document manual bootstrap: exact repository/environment federation subject, dedicated user-assigned managed identity, Contributor only on this demo resource group; obtain required confirmation of exact access grant before execution. Scope confirmation and secret destination confirmation are separate from plan approval. No subscription-wide Contributor or long-lived Azure password.
- [ ] Run contract tests, actionlint, Bicep build and shared verification; commit `ci: deploy tested MedKB images to Azure with OIDC`.

### Task 4: Health, rollback and narrowly scoped cleanup

**Files:** Create `scripts/azure/smoke.py`, `scripts/azure/cleanup.py`, `tests/test_azure_operations.py`; modify `scripts/azure/deploy.py`, `docs/AZURE.md`, `.github/workflows/azure-deploy.yml`.

**Interfaces:** Produces `check_health(url: str, timeout_seconds: int=180) -> None` and `validate_cleanup_target(subscription: str, expected_subscription: str, resource_group: str, expected_resource_group: str) -> None`. Smoke CLI takes HTTPS URL. Cleanup CLI requires exact expected subscription/group, previews resources, then requires the typed group name; default performs no deletion. Rollback uses Task 2 deploy CLI with a recorded known-good digest.

- [ ] Write tests: HTTP URL rejected, repeated 503 times out within bounded polling, healthy JSON succeeds; wrong subscription/group refuses cleanup before delete; absent confirmation never deletes; malformed rollback digest raises via Task 2 guard. Use fake clock/HTTP/CLI fixtures.
- [ ] Run `pytest tests/test_azure_operations.py -v`: expect missing module failure.
- [ ] Implement bounded polling of existing health endpoint and revision image checks. Document rollback compatibility review, known-good digest and post-rollback health; application rollback does not restore the database. Cleanup targets only the explicitly confirmed demo group; no Neon/Render deletion and no normal workflow deletes. Document setting app max replicas/scale behavior is not a hard spend cap; delete own resources to end their future charges, allowing for billing delay.
- [ ] Add EUR 5 resource-group budget with 50/80/100 percent alerts where the actual trial offer supports it; use portal configuration with separately confirmed notification address, record its effective currency and scope. If unsupported, record the limitation and require manual portal cost checks during the temporary demo. Do not claim an enforced cap or schedule automatic follow-ups.
- [ ] Run focused tests and shared verification; commit `feat: add Azure health rollback and cleanup operations`.

### Task 5: Isolated data, live proof and complete handoff

**Files:** Create `tests/test_azure_rag_readiness.py`, `docs/reviews/2026-10-13-azure-deployment.md`; modify `scripts/azure/preflight.py`, `tests/test_ai_api.py`, `README.md`, `docs/NEXT_STEPS.md`, `AGENTS.md`, `docs/AZURE.md`.

**Interfaces:** Add `validate_rag_readiness(coverage: dict[str, tuple[int,int]]) -> None`: each of `de`, `en` must have expected/current counts `(271,271)` for the current corpus signature; current signature verification is performed by existing RAG index code before constructing coverage. Non-ready index leaves `ragEnabled=false`.

- [ ] Write tests: `{ "de": (271,271), "en": (271,270) }` and absent language raise; complete coverage succeeds. Add backend request regression proving `X-Forwarded-For: attacker, trusted` selects `trusted` quota identity and changing only leftmost cannot bypass it; preserve existing Render header tests.
- [ ] Run targeted tests: expect missing readiness validator failure; verify IP regression passes if current parsing already satisfies contract. No unnecessary production IP change.
- [ ] Implement readiness guard and document reuse of validated vectors only with current keys/signature/dimensions and transactional final corpus check; otherwise use existing resumable index CLI. Check the existing importer/index API before selecting the supported command; no new public endpoint. Isolated database must have complete index before re-deploying with RAG true.
- [ ] Execute authorized provisioning only after cost preflight and separately required scoped-grant/secret confirmations. Provision free isolated Neon database, bootstrap secrets safely, create resource group/identity and deploy tested digest. Verify 47 entries, all roles, English/German, deep-link reload, JSON/SSE citations and persistence after reset; record real Azure rightmost-header behavior. No live model in automated tests.
- [ ] Observe cold wake and measured warm latency, verify resource graph/replicas, no unintended what-if drift, exercise known-good rollback and restore desired healthy digest. Record timestamped credit/cost observations, alerts, expiry, package visibility, ephemeral archives, logs limitation and shared AI upstream quota. If any live check is blocked, report it explicitly and leave completion status pending.
- [ ] Run all project checks plus Bicep/actionlint/contracts. Update README with actual Azure link/evidence and Render as durable link; record task commits and reproduction/cleanup commands without credentials or personal identifiers. Commit `docs: verify and document the temporary Azure demo`; push only verified commits.

## Self-review and execution handoff

Checked 2026-10-13: all spec sections map to Tasks 1–5; five review failure modes have owning tests; helpers use consistent interfaces; infrastructure secrets have a single preservation path; live access grants remain explicit operator gates. Documentation-only planning has not created resources or consumed Azure credit.

Recommended execution: Native, because five tasks share deployment guards and CLI interfaces; finish with the executing-plans skill's independent whole-change review. User reviews this plan, including the proposed EUR 5 operating limit, before implementation. The amount is not a guaranteed maximum and does not authorize personal cash charges.
