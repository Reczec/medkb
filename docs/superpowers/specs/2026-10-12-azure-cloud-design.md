# MedKB on Azure — design

Date: 2026-10-12. Status: approved by the user on 2026-10-13; no Azure resources created.

## Intent and constraints

Deploy the existing MedKB application to Azure as a demonstrable Cloud/DevOps portfolio project
building on AZ-900: infrastructure as code, a tested container, secretless deployment authentication,
health verification, rollback and honest evidence. Work locally on main in the shared checkout;
document decisions, commands, verification and remaining limitations. The existing Render demo stays
the permanent portfolio link. Azure is a second, time-limited demo, not a production migration.

The user wants no additional personal payments and permits using existing Azure trial credit.
The portal showed an active subscription, Owner role, EUR 175.99 remaining (USD 200 in the subscription
banner), expiry 2026-10-20 and current cost 0.00. No resources exist in that subscription at inspection.
These are dated observations, not a continuing credit guarantee. Do not put account email, subscription
IDs, tenant IDs, database credentials or provider keys into committed example parameters or screenshots.

The account-specific spending protection has not yet been independently verified. Before provisioning,
verify the subscription offer and spending-limit status through the portal or Azure CLI. If no enforceable
trial protection can be established, stop before provisioning and report the specific uncertainty.
Never upgrade to pay-as-you-go, remove the spending limit, enable billing for the AI provider, or accept
new financial terms under this authorization. Azure free allowances are not a promise of zero consumption.
Budget alerts are notifications, not hard caps. Credit expiry can disable the Azure demo; document this
prominently rather than claim permanent free hosting. No automated follow-up scheduler is created.

Approval clarification, 2026-10-13: the user explicitly does not authorize consuming the whole trial
credit. The implementation plan proposes EUR 5 as the project's operating limit, with alerts at
50/80/100 percent and manual shutdown/cleanup at the limit or before trial expiry. This small limit
is subject to plan review. Billing delays mean it cannot guarantee a EUR 5 maximum; if that guarantee
is required, do not provision. The enforceable trial spending protection remains a separate prerequisite.

## Selected architecture and alternatives

Selected: Azure Container Apps Consumption, Bicep, GitHub Actions and public GHCR container images.
Use the existing multi-stage Dockerfile: FastAPI serves the built React frontend on port 8000. Deploy
one application in one isolated resource group in West Europe, subject to subscription availability.
Define a Consumption workload profile only, external HTTPS ingress, insecure HTTP disabled, target port
8000, 0.5 vCPU/1 GiB memory, minimum replicas 0 and maximum replicas 1. Single active revision mode
bounds normal operation to one demo instance; deployment can briefly overlap revisions. A temporary
second instance can restore the same demo corpus, so atomic PostgreSQL resets remain necessary.

App Service is a valid alternative, but the existing container fits Container Apps and scale-to-zero
more directly. Terraform is useful for multi-cloud work; Bicep offers native Azure validation without
introducing remote Terraform state and its storage/access lifecycle. Azure Container Registry and a
new Azure PostgreSQL server would add separately billable resources; omit both from this first demo.

No VNet, NAT gateway, private endpoint, custom domain, dedicated compute, paid Defender plan, paid
registry or Application Insights is introduced. Set environment log destination to none to avoid an
implicit Log Analytics resource; collect bounded live log-stream evidence and GitHub deployment logs.
Use Azure's existing platform metrics. Persistent searchable observability is an explicitly deferred
extension, not a capability this deployment claims.

## Data and existing functionality

Use an isolated PostgreSQL database or branch within existing verified free Neon capacity, with its own
connection credential. Never point Azure at Render's database: each startup/periodic demo reset would
otherwise change the other deployment. Inspect Neon capacity/plan before creating the isolated database;
if isolation requires extra payments, stop and present the concrete alternative. No silent plan upgrade.
Provisioning the external database is a documented prerequisite outside Azure Bicep.

Keep all 47 bilingual entries, demo roles, English default/German switch, explainable rule-based
classifier, provider quotas and prototype notices. No patient data or new product UI. Set DEMO_MODE=true
and DEMO_RESET_HOURS=3. Store JWT_SECRET persistently as an application secret so restarts preserve valid
logins. Azure's isolated AI usage/cache is independent of Render's; the upstream Gemini account quota
remains shared if its existing key is reused. Do not prewarm all document answers during deployment.

Enable RAG only after complete current German/English index coverage is verified in the isolated database.
Reuse validated local vectors only after checking every current chunk key, normalized dimensions and
signature, in a transaction with a final corpus check; otherwise use the existing explicit resumable index
CLI. No indexing at startup or from a public request. Default threshold remains development-selected 0.60.
Verify reset persistence and actual JSON/SSE answers. Quotas still count live smoke checks.

The filesystem is ephemeral. Archive downloads work within an instance, but stored archive files are
not guaranteed after scale-to-zero/revisions; document this existing demo limitation. Durable archive
storage would require a separate design and storage-cost review.

## Identity, secrets and networking

GitHub Actions uses azure/login with OIDC federation scoped to a protected GitHub Environment named
azure-demo. The subject is bound to this repository/environment, not arbitrary repositories or PRs.
Use a dedicated managed identity with Contributor scoped only to the Azure demo resource group;
manual bootstrap establishes the resource group and role assignment using the user's authorized account.
The recurring deployment identity cannot create its own broader role assignment. Initial federation and
role grants are security-sensitive operations: present exact scope for confirmation before creating them.
Use least-privilege workflow permissions: read contents, write id-token for deployment, write packages
only for the image publication job. Fork PRs cannot deploy or access application secrets.

Public GHCR images contain application code and the built frontend only. Check .dockerignore, exclude
local .env, operator files, databases, credentials and test artifacts. Pin each deployment to its image
digest; do not deploy an unqualified latest tag. Public image publication must be documented as a new
public artifact. GHCR package visibility is explicitly verified before Azure attempts its anonymous pull.

Application secrets: DATABASE_URL, JWT_SECRET and optional Gemini/WHO credentials are securely supplied
at bootstrap, never Bicep outputs, CLI command text, logs, git-tracked files or exposed workflow arguments.
Routine deployments preserve the existing secret configuration and update nonsecret infrastructure/image
inputs only. Bicep must avoid resetting preconfigured secrets; implementation tests cover that ownership
boundary. OIDC client/tenant/subscription identifiers use GitHub Environment variables, not repository
examples containing actual values. No long-lived Azure deployment password.

Keep uvicorn --no-proxy-headers. Set CLIENT_IP_HEADER=X-Forwarded-For only for Container Apps ingress:
Microsoft documents the rightmost address as provided by Azure. Verify current server parsing uses the
trusted rightmost value, add mocked backend regression coverage if required, and live-test spoofed
leftmost header values. Preserve Render's True-Client-IP configuration. No broad proxy trust change.

## Infrastructure and CI/CD boundaries

Planned files: infra/azure/main.bicep and environment/app modules as appropriate; example nonsecret
parameters; an Azure deployment workflow; bootstrap/deploy/smoke/rollback scripts under scripts/azure/;
deployment-contract tests; an operator guide and completion record in docs/. Follow existing style and
limit new dependencies. Pin actions and supported stable Azure resource APIs after checking current docs.

PRs compile/lint Bicep and validate deployment scripts/contracts without Azure credentials or provisioning.
The existing CI remains the gate for backend (SQLite/PostgreSQL), frontend and container smoke tests.
Publish/deploy only the successfully tested main commit. Handle workflow_run safely: successful CI,
expected repository and main branch, checkout the exact tested SHA, concurrency per environment and
no untrusted PR input in shell commands. Provide a manual retry path for the same verified commit.

Workflow builds the image, publishes to GHCR, records its digest, performs Bicep what-if, applies the
approved infrastructure and image update, waits for the active revision, and runs bounded HTTPS smoke
checks. Initial deployment must not automatically add secrets or grant permissions. No resource delete
in an ordinary workflow. Compare deployment outcomes to desired image digest and health; a successful
CLI exit alone is not completion.

Rollback redeploys an already-known working image digest/revision; inspect shared DB compatibility
before rollback because application rollback is not a database restore. A separate explicitly invoked
cleanup script validates subscription/resource group, previews resources and requires confirmation;
it never deletes unrelated Azure resources or the Render/Neon production database. Cleanup before
trial expiry is an operator task; automatic disablement is not equivalent to deletion.

## Acceptance and documentation

1. Bicep compiles, lint/contracts pass; idempotent what-if after deployment has no unintended changes.
2. An image of the tested commit is deployed by GitHub OIDC with resource-group-limited permissions.
3. Public HTTPS health is 200; demo roles work; 47 entries and both languages are present; deep links reload.
4. RAG has complete bilingual coverage and real cited JSON/SSE answers, retained after startup reset.
5. Header spoofing cannot change the quota identity; no credentials appear in source/image/logs/outputs.
6. Scale configuration is 0..1 on Consumption; demonstrate cold wake and record measured time separately
   from warm requests. No guaranteed latency claim. Observe rather than change settings solely to force sleep.
7. Demonstrate rollback to a known digest and recovery, then leave the chosen current revision healthy.
8. Record credit/cost observations with timestamps; note billing delays and the 2026-10-20 expiry. Avoid
   claiming zero cost until Azure reports it; distinguish credit consumption from personal cash charges.
9. Full project checks green per AGENTS.md, plus IaC/workflow validation and deliberate live operator checks.

README gains a truthful architecture explanation and Azure evidence, with Render as the durable demo.
The completion record lists task commits, tests, bootstrap/provision/deploy/rollback evidence, costing
boundaries and how to reproduce/clean up. Do not change CV claims to imply a permanent Azure service.

## Primary references checked 2026-10-12

- [Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing)
- [Ingress and trusted rightmost client IP](https://learn.microsoft.com/en-us/azure/container-apps/ingress-overview)
- [Container Apps Bicep schema](https://learn.microsoft.com/en-us/azure/templates/microsoft.app/containerapps)
- [Environment schema](https://learn.microsoft.com/en-us/azure/templates/microsoft.app/managedenvironments)
- [Logging options](https://learn.microsoft.com/en-us/azure/container-apps/log-options)
- [GitHub OIDC for Azure](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-azure)
- [Azure spending limit](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit)
- [Avoid charges with a free account](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/avoid-charges-free-account)

Next handoff: user reviews this written design, then write the implementation plan and obtain its
execution-method approval before implementation. Live provisioning additionally requires verified
cost protection and confirmation for scoped identity grants/secret transmission where applicable.
