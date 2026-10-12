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
Never connect Azure to Render's database: demo resets would interfere. Paid capacity is a blocker.
GitHub identity grants and application-secret transmission require confirmation of their exact scope
and destination before those operations; no grant is made by the preflight.

## Evidence boundaries

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
blocks deployment. RAG defaults off; enabling it requires separately verified current index coverage.

Tooling observed 2026-10-13: official Azure CLI ZIP 2.91.0 and Bicep 0.48.1, local ignored scratch only.
Azure CLI device-code login was denied with error 530035; no security policy was weakened. Account
protection cannot yet be claimed from CLI evidence. Neon requires sign-in before free-capacity checks.

On 2026-10-12 the portal showed an active trial with EUR 175.99 remaining and expiry 2026-10-20.
This is a dated observation. Current trial protection, isolated Neon capacity and live Azure checks
are pending. Never publish account identifiers, emails or credentials in examples/screenshots.

Primary references: [spending limits](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit),
[subscription policies](https://learn.microsoft.com/en-us/rest/api/resources/subscriptions/get),
[Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing).
