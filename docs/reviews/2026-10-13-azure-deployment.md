# Azure deployment and remaining verification

Date: 2026-10-13. Status: **manual Azure deployment is live and application checks passed**.
GitHub OIDC delivery, compatible rollback/restoration and cold wake are verified.
Cost reporting remains delayed; the latest remaining-credit balance is still the dated portal observation.
Live demo: https://medkb-azure-demo.whiterock-973337bb.northeurope.azurecontainerapps.io
Approved spec/plan: [design](../superpowers/specs/2026-10-12-azure-cloud-design.md),
[implementation plan](../superpowers/plans/2026-10-13-azure-cloud.md).
Operator commands and constraints: [AZURE.md](../AZURE.md).
Full task ledger and implementation rulings: [execution ledger](2026-10-13-azure-execution-ledger.md).

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

## Historical blockers and evidence boundaries (superseded by live records below)

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

## Activation checklist (partially satisfied)

- [x] Complete normal Azure CLI login and run fresh protected-trial guard (2026-10-13).
- [ ] Refresh remaining credit/offer/expiry observation.
- [x] Verify free Neon capacity and Render database separation; create isolated `medkb_azure`/credential.
- [x] Confirm exact resource-group-scoped identity grant/federation and Azure secret destination.
- [x] Create marked demo group, identity, approved role grant, federation and GitHub environment variables.
- [x] Configure EUR 5 alerts at 50/80/100 percent; billing profile currency verified EUR.
- [x] Publish exact tested main image and verify anonymous public digest access.
- [x] Bootstrap safe app secrets, apply Bicep, inspect what-if property paths and ready digest (provider noise below).
- [x] Seed 47 entries; verify all roles, bilingual entry, patient write denial and HTML deep links.
- [x] Build/validate 271+271 current vectors; enable RAG, prove cited JSON/SSE and reset persistence.
- [x] Prove live rightmost-IP quota behavior; measure cold/warm latency without guaranteed claims.
- [x] Exercise compatible known-good rollback and restore current healthy digest.
- [ ] Timestamp actual credit/cost observations; inspect graph/replicas and clean up before 2026-10-20.

The permanent public demo remains [Render](https://medkb.onrender.com). Manual Azure deployment is
demonstrated, including protected OIDC delivery and compatible image rollback. It is temporary hosting.

## Live application verification, 2026-10-13

The ready revision serves bootstrap image digest
`sha256:870ac92c70b93a9aba09cb54f0c72410b375fe19a53e33cd4eaecd87a1d9d8af`.
Consumption configuration is 0..1 replicas, 0.5 vCPU / 1 GiB, Single revision, 300-second cooldown,
with no Log Analytics destination. HTTPS returned 200. Warm health requests took 0.140 and 0.032
seconds; these are not cold-start measurements.

The isolated Neon database contains 47 entries and 271 valid current chunks per language. All
three demo roles authenticate; patients cannot write. German JSON and English SSE RAG answers
returned hybrid retrieval and one citation each. Different spoofed IP prefixes produced the same
quota identity. A real database demo reset preserved both language indexes, AI quota and the cached
document explanation; a subsequent explanation was served from cache. Chat answers intentionally
are not cached: the initial operator script incorrectly expected this, then was corrected without
changing product code. Six small live LLM answers were used across both runs; automated tests use fakes.

GitHub run [38322206724](https://github.com/Reczec/medkb/actions/runs/38322206724) passed its trusted
SHA verification, but image publication failed with `permission_denied: write_package`.
Public package visibility permits anonymous pulls; it does not grant Actions write access. The user
confirmed adding repository Actions access and failed jobs were rerun. OIDC deployment is not yet proven.
The repository opt-in variable is now enabled; the environment requires Reczec's deployment review.

After CLI replica inventory confirmed zero replicas, one health request returned 200 in 22.937
seconds; the next returned 200 in 0.157 seconds. This is one cold-wake observation, not a latency SLA.
The concurrently approved OIDC job failed before any deployment with AADSTS700213: its actual
subject includes immutable owner/repository IDs. The existing federation was updated to match
`repo:OWNER@OWNER-ID/REPO@REPO-ID:environment:azure-demo`, keeping the same repository, environment,
issuer, audience and resource-group-only role. No wildcard or additional grant was introduced.
This matches [GitHub's immutable subject documentation](https://docs.github.com/en/actions/reference/security/oidc).
The failed deployment job was rerun and **all three jobs succeeded**, including OIDC login,
guarded what-if/apply, exact ready digest and HTTPS health verification.

## Rollback, drift and final state

CI image digest `sha256:7575fc0f92edb82bf4f5eab3fc88f696f59ee61334be8f5cb2fdfa82e35ce104`
was deployed from tested main commit `7d166746429ec3f319b077164c0f9090ea7dc00e`.
The operator then deployed the healthy bootstrap digest `870ac92c…` and verified its ready revision
and HTTPS health, before restoring the CI digest and repeating both checks. Final revision
`medkb-azure-demo--0000003` is ready, latest and provisioning Succeeded. Both images contain the same
application/schema; their intervening changes are infrastructure/documentation. This image rollback
does not restore database state. RAG remains enabled and its current coverage is checked before every apply.

Final resource inventory contains only the user-assigned identity, Consumption environment and app.
No Azure registry, database, storage or paid logging workspace was created. A repeat what-if reports
Modify for environment/app and Ignore for identity; it is **not a zero-diff preview**. Safe property-path
inspection shows service-populated ingress/scale/environment defaults, secure secret comparison and
probe-array ordering. Actual Startup/Readiness settings match Bicep after sorting by type. No additional
resource creation or deletion was proposed. Secret values are captured/preserved without logging them.
One preview failed while delivery was in progress; the final non-mutating preview completed successfully.

The final 2026-10-13 resource-group ActualCost query returned no rows. The EUR 5 budget exists with
50/80/100 percent notifications; current spend is not yet available. This is billing delay, not proof
of zero cost. Credit REST lookups returned 404, so EUR 175.99 remains only the 2026-10-12 portal
observation. Fresh protected-trial policy remains On. Check actual remaining credit/costs manually
in the portal and remove the demo resources before 2026-10-20; alerts do not enforce a hard cap.

Final checks rerun locally: backend with the explicit Bicep compiler, ruff check/format, actionlint,
frontend lint/typecheck, 227 unit tests, production build and 38 browser tests. One existing backend
skip is unrelated to Bicep. No live model calls occur in automated tests.

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
cost if wrong is an unsupported deployment claim. At review time Task 5 was incomplete and the Azure
workflow disabled. The later live results above supersede that state. No second review was requested;
fixes are verified by RED-to-GREEN and full suites.
Final verification after the fix pass: 895 backend passed, 1 skipped, ruff check/format and actionlint
clean; frontend lint/typecheck/build green, 227 unit tests and 38 e2e passed. Actual Bicep compilation
was enabled in the backend run. GitHub CLI returned HTTP 401 Bad credentials during a read-only
repository-variable check; OIDC environment setup also requires a working GitHub session. No
GitHub settings were changed. These failures do not affect the successful Azure CLI trial login.

`c6d6069` contains the verified review corrections. The authorized `git push origin main` was attempted but failed with invalid username/token; all Azure commits remain local. Reauthenticate GitHub before retrying push and configuring the deployment environment.


Activation retry on 2026-10-13: browser transport remains closed. GitHub auth diagnosis confirmed an invalid GITHUB_TOKEN override and no stored CLI login without it. Normal gh web login was started with the override removed only in that child process; user confirmation remains pending. No Azure resources or GitHub grants created.

## Earlier bootstrap checkpoint (superseded by final state above)

- GitHub workflow/package scopes were explicitly approved and confirmed; main through 3f39a39 pushed,
  all six CI jobs succeeded. Subsequent region commit requires its own successful CI before publication.
- Official Neon CLI 8.4.1 installed without lifecycle scripts in ignored scratch; login succeeded.
  OS keyring unsupported, so the session is in an owner-only ignored directory. No secrets committed.
- Verified existing organization plan Free and one existing MedKB project. Created a distinct free
  medkb-azure-demo project, fixed 0.25 CU, own medkb_azure database/medkb_azure_owner role. Actual SQL
  current_database/current_user matched exactly. Seeded 47 entries and imported 542 existing normalized
  current-signature vectors transactionally; final coverage de=271/271 and en=271/271. No model requests.
- User explicitly approved database/role creation, RG-scoped Contributor/OIDC and app secret transfer.
  Marked group created; West Europe rejected new customers. North Europe identity creation succeeded.
  Ruling: default application region changes to North Europe, an allowed European fallback under the
  design's availability condition; cost if wrong: provisioning fails with spending protection retained.
- Assigned dedicated managed identity Contributor only on the demo group, exact repository/environment
  issuer/subject/audience federation. No subscription-level role assignment.
- GitHub azure-demo restricts branches to main and requires Reczec review. Automatic approval initially
  rejected self-approval; user explicitly approved it, then configuration succeeded. Autodeploy is off.
- Group-scoped budget nominal amount 5, actual alerts 50/80/100 percent to the signed-in account.
  API currentSpend was null: current cost and billing currency still need evidence; alerts are no cap.
- North Europe contract observed RED on the old compiled default, then GREEN; full verification:
  895 backend passed/1 skip, ruff clean, 227 frontend unit/38 e2e passed, frontend lint/typecheck/build green.
- Container Apps provider registration and first image bootstrap in progress; app not deployed yet.

### Live template correction and first image

The actual provider rejected literal appLogsConfiguration.destination='none', although schema/SDK
wording describes logical 'none'. Official CLI implementation serializes that choice to null.
Ruling: leave optional destination unset (empty appLogsConfiguration), preserving disabled logging
without creating Log Analytics; cost if wrong is provider refusal. Compiled regression observed RED
then GREEN. The corrected live what-if proposes exactly environment/app Create and identity Ignore.

The tested main 3688002 CI succeeded, local container health passed, and its image was published as
sha256:870ac92c70b93a9aba09cb54f0c72410b375fe19a53e33cd4eaecd87a1d9d8af. User set GHCR visibility
Public. A fresh anonymous registry token request and exact manifest GET returned HTTP 200; package
API independently confirmed public visibility. Temporary Docker registry credential was removed.

Azure billing account type MicrosoftCustomerAgreement, active profile currency EUR: budget amount 5
is confirmed EUR 5. Cost query returned no rows, budget currentSpend null; this is not evidence of a
final zero invoice. Protected trial remains enabled; no offer upgrade or spending-limit removal.
Final unset-logging verification: 895 backend passed/1 skipped, ruff clean, frontend lint/typecheck/build green, 227 unit tests and 38 e2e passed. Trial-credit REST endpoints returned 404; latest remaining-credit observation stays dated 2026-10-12 rather than falsely refreshed.
