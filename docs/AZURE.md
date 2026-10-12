# Temporary Azure demo — operator guide

Status: implementation in progress; no Azure deployment is claimed. Render remains the permanent
demo at https://medkb.onrender.com. The approved Azure trial expires **2026-10-20**.

## Cost controls

The user approved a **EUR 5 credit-consumption operating target**, not spending the whole trial credit.
Budget warnings at 50/80/100 percent notify; they do not stop resources. Billing updates are delayed,
so EUR 5 is not a guaranteed maximum. No personal cash charges, upgrades to pay-as-you-go, removed
spending limits or new financial terms are authorized. No recurring monitoring has been scheduled.

Before any resource creation, verify the actual free-trial offer, remaining credit and expiry in the
portal, then run the read-only guard with your real subscription ID (never commit it):

```powershell
.venv/Scripts/python.exe -m scripts.azure.preflight --subscription YOUR_SUBSCRIPTION --resource-group medkb-azure-demo-portfolio --expires-on 2026-10-20
```

The guard reads fresh ARM subscription policies, requires `state=Enabled` and `spendingLimit=On`,
checks the exact subscription and demo group prefix, and blocks on/after the expiry date. It does not
prove that trial credit remains: inspect that separately. A missing policy is a blocker.

Use only Consumption, replicas 0..1 and no separately charged registry/database/log workspace.
Check resource-group costs during this temporary demo; stop and clean up at the operating target
or before trial expiry. Trial disablement does not delete resources. Platform free grants are not
a guarantee that all associated charges are zero.

## External prerequisites

Install Azure CLI/Bicep from Microsoft's official distribution; record versions. Verify Neon is still
on the free plan and has spare capacity before creating a separate database/branch and credential.
Create a separate database named `medkb_azure` with its own role/credential. Never connect Azure to
Render's database: demo resets would interfere. The deployment helper rejects other database names
and SQLite URLs. Require `sslmode=require` or stronger; fallback to plaintext is refused. Verify the
Render database is different before bootstrap. Paid capacity is a blocker.
GitHub identity grants and application-secret transmission require confirmation of their exact scope
and destination before those operations; no grant is made by the preflight.

## Infrastructure and secure parameter ownership

`infra/azure/main.bicep` uses Microsoft.App API 2025-07-01, a Consumption-only environment with
log destination `none`, and one HTTPS app on port 8000 with 0.5 vCPU/1 GiB, scale 0..1 and Single
revision mode. It creates no identity/role grants or paid supporting services. Bicep's secure types
are string/object, so the secret list is wrapped in `@secure() appSecrets object` under `items`.

Run `python -m scripts.azure.deploy --help`. Default is what-if; `--apply` performs the deployment.
Both use the exact `ghcr.io/reczec/medkb@sha256:<64 lowercase hex>` image. For initial bootstrap,
provide `--bootstrap-secrets-file .superpowers/azure-bootstrap.json`, an array of Azure secret objects
with `name` and `value`: required names `database-url`, `jwt-secret`; optional `ai-api-key`,
`embedding-api-key`, `icd-client-id`, `icd-client-secret`, `ncbi-api-key`. Never commit actual values.
The helper restricts local file permissions before reading/writing. The source is deleted only after
successful apply; transient parameter files are deleted even on failure. It passes paths rather than
secret values in CLI arguments and suppresses raw CLI bodies/errors. Review the nonsecret Bicep graph
and compiled template; what-if response bodies are not printed because they can contain credentials.

Routine deployments read and preserve every existing secret through captured CLI output, including
unknown secret names and Key Vault references, and reference recognized settings through environment
variables. They do not need application keys in GitHub Secrets. A missing/duplicate required secret
blocks deployment. RAG defaults off on bootstrap and routine deployments preserve its existing flag.
Every enabled deployment rechecks current bilingual coverage against the isolated database before
Azure writes; `--disable-rag` explicitly turns it off. Database inspection failures are redacted.

## RAG index preparation

After initial startup seeds the isolated database, prepare its index explicitly. The shipped resumable
operator command is `python -m app.rag.index_cli --pause 15`, with `DATABASE_URL` set securely to the
isolated database and existing provider credentials loaded locally. This calls the embedding provider
only for missing chunks and respects the global AI budget; do not run it in tests or bulk-prewarm answers.
Expect 542 current unique vectors, 271 per language. Then deploy with `--rag-enabled`; the helper reads
the current corpus keys, checks stored signatures and normalized 768-dimensional vectors, and requires
both languages to report 271/271. Partial or stale vectors block activation. A read-only transaction
is used for the PostgreSQL check. Demo reset persistence must still be demonstrated live.

Reuse of existing local vectors is allowed only through a separately validated transactional import
with exact current keys/signature/dimensions and a final corpus check. No general importer is shipped
in this Azure change; the supported fallback is the existing resumable index command above.

Tooling observed 2026-10-13: official Azure CLI ZIP 2.91.0 and Bicep 0.48.1, local ignored scratch only.
Azure CLI device-code login was denied with error 530035; no security policy was weakened. Normal browser login succeeded on 2026-10-13; fresh ARM evidence confirmed an enabled FreeTrial
subscription with spendingLimit=On. The browser connection then became unavailable; Neon sign-in
and free capacity cannot yet be verified.

## Evidence boundaries

On 2026-10-12 the portal showed an active trial with EUR 175.99 remaining and expiry 2026-10-20.
This is a dated observation. Current trial protection was verified on 2026-10-13. Updated credit balance, isolated Neon capacity
and live Azure checks are pending. Never publish account identifiers, emails or credentials in examples/screenshots.

Primary references: [spending limits](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit),
[subscription policies](https://learn.microsoft.com/en-us/rest/api/resources/subscriptions/get),
[Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing).

## GitHub OIDC bootstrap and delivery gate

The Azure workflow is **disabled by default**. Set repository variable `AZURE_DEMO_ENABLED=true`
only after manual bootstrap, cost protection, isolated database and package visibility checks succeed.
The first image can be built/published manually from a successful main CI commit; the regular workflow
does not create its own permissions or application secrets. GHCR packages are often initially private:
verify the MedKB package visibility in GitHub. Anonymous manifest inspection must succeed before Azure.

Create protected environment `azure-demo` restricted to main, with a required reviewer where the
repository plan supports it. Exact federation: issuer `https://token.actions.githubusercontent.com`,
subject `repo:Reczec/medkb:environment:azure-demo`, audience `api://AzureADTokenExchange`.
Create a dedicated user-assigned managed identity `medkb-azure-demo-deployer` in the demo group;
assign Contributor **only** to `/subscriptions/YOUR_SUBSCRIPTION/resourceGroups/medkb-azure-demo-portfolio`.
Confirm that exact access grant before executing bootstrap; do not grant subscription-wide access.
The deploying identity cannot grant itself roles. No long-lived Azure password is stored.

Environment variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`,
`AZURE_RESOURCE_GROUP`, `AZURE_APP_NAME`, `AZURE_TRIAL_EXPIRES_ON`. Their actual values stay outside git.
Routine deployment reads existing Azure app secrets with its resource-group-scoped identity.

Successful **push** CI for the exact main SHA is required, including backend SQLite/PostgreSQL,
frontend/e2e, Docker and the added Azure-contract job. PR/fork/failed/in-progress events are refused.
Manual dispatch accepts only a full 40-character SHA with successful push CI for the same repository
and main branch. Validation runs before package-write or id-token jobs. The published image is pinned
by digest. The deploy job alone has id-token permission and the image job alone has packages-write.
Workflow concurrency prevents overlapping deployment runs. Official action SHAs were resolved from
their published tags on 2026-10-13; Bicep/actionlint versions are 0.48.1/1.7.12.

## Health, rollback and cleanup

After apply, the helper waits at most 180 seconds for matching latest/ready revision names and the
desired digest, then at most 180 seconds for HTTPS `/api/health` to return `{"status":"ok"}`. Each
revision CLI request is limited to the remaining poll budget. A CLI success alone is not live proof.
Standalone: `python -m scripts.azure.smoke https://YOUR_APP.azurecontainerapps.io`.

Record the last healthy digest and review database compatibility before rollback. Use the same
deployment command with that digest and `--apply`; it runs the same trial guard and health verification.
This does not restore database contents. Record rollback evidence and return to the chosen current digest.

Before trial expiry (2026-10-20) or at the EUR 5 operating target, inspect costs then preview cleanup:

```powershell
python -m scripts.azure.cleanup --subscription YOUR_SUBSCRIPTION --expected-subscription YOUR_SUBSCRIPTION --resource-group medkb-azure-demo-portfolio --expected-resource-group medkb-azure-demo-portfolio
```

Deletion additionally requires `--delete` and typing the exact group name at the prompt. The group
must bear tag `project=medkb-azure-demo`; bootstrap must set it. Review every listed resource before
confirming. Only this group is deleted; Neon/Render are not touched. Cleanup still works after trial
expiry if Azure permits access; it does not require an unexpired trial. Resource deletion may take
time and reported costs may arrive later. Scale-to-zero is not equivalent to cleanup or a hard cost cap.

Budget setup is pending live authentication/resource-group creation. In Cost Management, select the
**demo resource-group scope**, create a monthly budget for **5 in the actual billing currency**, and
set actual-cost notifications at 50/80/100 percent. If the billing currency is not EUR, do not silently
equate amounts: confirm a corresponding limit before creation. Confirm the notification address and
Azure destination before entering it. Record the scope/currency/thresholds and whether the trial
offer supports budgets. If unsupported, document that and inspect costs manually during operation.
No automatic deletion, billing upgrade or recurring monitor is installed by this guide.

## Demo limitations

Filesystem archives are ephemeral across scale-to-zero/revisions; no durable storage is added.
Logs have no persistent searchable workspace: use bounded log streams, deployment logs and platform
metrics. Cold-wake latency needs a measured live observation and is not promised. If the existing
Gemini key is reused, its upstream quota is shared with Render even though database quotas/cache are
isolated. RAG reset persistence, real cited JSON/SSE answers, spoofed-IP checks, rollback and costing
are pending until recorded in the deployment review. Never imply permanent Azure hosting in the CV.
