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

On 2026-10-12 the portal showed an active trial with EUR 175.99 remaining and expiry 2026-10-20.
This is a dated observation. Current trial protection, isolated Neon capacity and live Azure checks
are pending. Never publish account identifiers, emails or credentials in examples/screenshots.

Primary references: [spending limits](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit),
[subscription policies](https://learn.microsoft.com/en-us/rest/api/resources/subscriptions/get),
[Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing).
