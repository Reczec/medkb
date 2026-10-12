# Azure implementation and pending activation

Date: 2026-10-13. Status: local implementation reviewed and verified; live activation pending; **Azure is not deployed**.
Approved spec/plan: [design](../superpowers/specs/2026-10-12-azure-cloud-design.md),
[implementation plan](../superpowers/plans/2026-10-13-azure-cloud.md).
Operator commands and constraints: [AZURE.md](../AZURE.md).

## Delivered locally

- `6be0144`: fresh ARM spending-protection/expiry/target preflight; 12 initial tests.
- `eea27c7`: Bicep Consumption environment/app, secure secret preservation, digest-only deploy;
  10 tests including actual Bicep compilation.
- `bb92fdf`: opt-in GitHub delivery, exact successful main CI SHA, public GHCR/OIDC separation;
  11 executable guard and parsed YAML contract tests; actionlint clean.
- `8471d1c`: bounded revision/health checks, guarded cleanup and rollback instructions;
  9 operations tests and one real secret-list contract regression.
- `fe6a31c`: current bilingual RAG readiness, mandatory database TLS, preserved activation flag
  and explicit Azure-header quota regression; live acceptance remains pending.

Each completed task passed full pytest/ruff and frontend lint/typecheck/unit/build/e2e checks before
commit. Latest local checks: 895 backend tests passed, 1 skipped; 227 frontend unit tests and 38 e2e passed. Existing Starlette
deprecation and corrupt-vector SQLAlchemy identity warnings remain. No live model is used in tests.
Tool versions: official Azure CLI ZIP 2.91.0, Bicep 0.48.1, actionlint 1.7.12, installed only in
ignored plan scratch. Official GitHub action SHAs were resolved from vendor tags on this date.

## Decisions made during implementation

1. Fresh ARM GET replaces cached `az account show` for spending-policy evidence: the cached profile
   can omit `subscriptionPolicies`. Missing evidence blocks provisioning; cost if wrong is inability
   to deploy, not a financial upgrade.
2. Bicep rejected the planned secure array (BCP124). Use `@secure() object` wrapping `items` instead;
   cost if wrong is template rejection. Secret protection was never downgraded.
3. Added executable CI-event validation rather than only source-string tests, plus dev-only PyYAML
   for actual workflow permission contracts; cost if wrong is refused delivery.
4. Official CLI docs confirmed secret list defaults to names only. Captured `--show-values` preserves
   values; output/error bodies stay suppressed. Per-call timeouts keep revision polling bounded.
5. Live budget configuration moves to activation because no resource group/authenticated scope
   exists yet. Costs may not start before protection/isolation checks; alerts remain notifications.
6. Select a separate database named `medkb_azure` rather than an ambiguously named branch. Routine
   deploys preserve RAG and recheck actual current corpus/signature/vectors; errors block deployment.
   Cost if wrong: activation is refused; Render is never intentionally used as the Azure database.

## Live blockers and evidence boundaries

- Azure CLI device-code login denied with code **530035**. Normal browser login was then started;
  normal login succeeded on 2026-10-13. Fresh ARM verified Enabled, FreeTrial and spendingLimit=On.
  No tenant security policy, MFA or spending protection was weakened.
- The browser connection became unavailable after Azure login. Neon sign-in and free-plan capacity
  cannot yet be verified.
- Portal observations on 2026-10-12: active subscription, trial credit EUR 175.99 remaining,
  trial expires 2026-10-20. Remaining credit/expiry need a fresh observation; spending protection was verified separately on 2026-10-13.
- Fresh CLI resource-group inventory on 2026-10-13 returned an empty list.
- No Azure resources, isolated database, managed identity, federation or role grants created.
  No application credentials transmitted to Azure; no GHCR package published; workflow stays opt-in off.
- EUR 5 is the approved **credit-consumption operating target**, not an enforced hard cap.
  Budget scope/currency/address/support and delayed billing evidence remain pending. Personal cash
  charges, pay-as-you-go upgrades and removing spending limits are not authorized.

## Activation checklist (not yet satisfied)

- [x] Complete normal Azure CLI login and run fresh protected-trial guard (2026-10-13).
- [ ] Refresh remaining credit/offer/expiry observation.
- [ ] Verify free Neon capacity and Render database separation; create isolated `medkb_azure`/credential.
- [ ] Confirm exact resource-group-scoped identity grant/federation and Azure secret destination.
- [ ] Create marked demo group, identity, approved role grant, federation and GitHub environment variables.
- [ ] Configure EUR 5 alerts at 50/80/100 percent where supported; otherwise record manual-check fallback.
- [ ] Publish exact tested main image and verify anonymous public digest access.
- [ ] Bootstrap safe app secrets, apply Bicep, inspect no unintended what-if drift and ready digest.
- [ ] Seed 47 entries; verify roles, English/German, prototype notices and deep-link reload.
- [ ] Build/validate 271+271 current vectors; enable RAG, prove cited JSON/SSE and reset persistence.
- [ ] Prove live rightmost-IP quota behavior; measure cold/warm latency without guaranteed claims.
- [ ] Exercise compatible known-good rollback and restore current healthy digest.
- [ ] Timestamp actual credit/cost observations; inspect graph/replicas and clean up before 2026-10-20.

The permanent public demo remains [Render](https://medkb.onrender.com). No Azure live URL or
completed-deployment CV claim is justified until this checklist has real evidence.

## Independent review and single fix pass

A fresh gpt-6-astra reviewer inspected eee88a9..fe6a31c. Five findings were accepted:

- Critical: SQLAlchemy query `dbname` could override the validated URL path. Connection queries now
  allow only enforced TLS and optional required channel binding; destination overrides are rejected.
- Critical: captured output did not disable Azure CLI persistent logging. Child environment explicitly
  disables file and command logging, including when the parent enables them; synthetic secret-bearing
  failures stay suppressed.
- Important: normal what-if pretty output was incompatible with JSON parsing. Request `--no-pretty-print`
  and expose only resource IDs and change types, never resolved parameters or property deltas.
- Important: Windows batch arguments could be interpreted by a shell. Invoke the installed Azure Python
  module directly; validate subscription UUID and app name before any external request. The corrected
  read-only preflight succeeded live on 2026-10-13.
- Important: existing explicit broad file grants survived the previous ACL restriction. Replace the
  entire Windows DACL with the current identity's FullControl grant; the actual Everyone-grant
  regression failed before the fix and passed after it.

Twelve focused review regressions failed before implementation and passed afterward. The ACL test
was first corrected to use .NET directly because inherited PowerShell module paths prevented Get-Acl
loading; its actual pre-fix failure then confirmed the retained Everyone grant. No minor findings.

Reviewer declined live provisioning/OIDC/package/rollback/alerts, Neon capacity and effective identity,
real ingress spoofing, live RAG citations/reset persistence, billing and latency. Ruling for each:
retain these as unfulfilled operator acceptance checks, because mocks cannot establish platform facts;
cost if wrong is an unsupported deployment claim. Task 5 remains incomplete and the Azure workflow
remains disabled. No second review was requested; fixes are verified by RED-to-GREEN and full suites.
Final verification after the fix pass: 895 backend passed, 1 skipped, ruff check/format and actionlint
clean; frontend lint/typecheck/build green, 227 unit tests and 38 e2e passed. Actual Bicep compilation
was enabled in the backend run. GitHub CLI returned HTTP 401 Bad credentials during a read-only
repository-variable check; OIDC environment setup also requires a working GitHub session. No
GitHub settings were changed. These failures do not affect the successful Azure CLI trial login.