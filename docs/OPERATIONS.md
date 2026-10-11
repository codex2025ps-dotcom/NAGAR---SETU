# Hosting, costs and operations

## Current state

No infrastructure, cloud resources or deployed services were created. The user reports a three-month AWS trial. Exact expiry, credits/allowance, paid-plan status, selected Region, spend limit and monthly budget remain unconfirmed. A trial does not establish zero cost or production suitability.

## Cost-effective path

Develop locally first with Docker and PostgreSQL/PostGIS; no paid model or SMS dependency is needed for routine tests. Begin with one API, one web application and one database. Keep web/admin together. Avoid Kubernetes, microservices, Redis, a vector database and always-on workers until measured requirements justify them. Use PostgreSQL search/category filters first; AI improves an already functioning platform.

For staging, compare a small persistent VM running containers with a managed PostgreSQL/PostGIS service. A VM may lower the direct bill but requires patching, backups, restore tests and outage handling. Managed PostgreSQL reduces operational work but creates a recurring baseline cost; confirm PostGIS support, extension permissions and selected-Region availability. A single VM with a co-located database is acceptable only for disposable development/staging, not assumed production resilience.

Future production recommendation: stateless API/web containers, privately reachable managed PostgreSQL with PostGIS, private object storage, HTTPS ingress, and same-Region backups. Availability sizing and hosting provider remain open until the budget and recovery targets are approved. Multi-AZ within the selected Region may be considered; it is not multi-Region deployment. No hosting resources or configuration are supplied now.

## Estimate before provisioning

Record selected Region, instance/container hours, vCPU/RAM and storage, database/backup retention, public IPv4/ingress/egress, object operations, mail/SMS delivery, maps/geocoding licences, logs, AI token usage, mobile build/store fees and applicable taxes. Use current provider pricing; do not assume the trial covers each item. Record an approved monthly total, alert thresholds and shutdown/cleanup owners. Re-evaluate before trial expiry; do not leave trial-funded resources running indefinitely.

AI has per-user/per-day quotas plus a hard global spend/token cap, max input/output lengths, timeout and feature flag. Reserve usage atomically before dispatch, account for concurrent requests and reconcile actual usage afterward. Refuse new AI calls on exhaustion; ordinary workflows remain available. Do not record unredacted prompts. A model provider and pricing are still open decisions.

## AWS new-experience prerequisites

Follow [AGENTS.md](../AGENTS.md) for the complete user constraints. Confirm the selected Region at AWS Settings > View all projects > Overview > Additional Info > Region; if the user cannot, inspect ~/.aws/config safely. Check paid-plan status using `aws freetier get-account-plan-state` when authenticated AWS work begins. Use the applicable [supported-services list](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html) and project policy restrictions. Do not activate advanced features without authorization.

Create Regional resources only in the confirmed selected Region. Do not use Lambda@Edge, StackSets, cross-Region replication/routing, multi-Region keys or cross-Region AI inference. Only global-service dependencies permitted in AGENTS.md can use us-east-1. Do not guess ap-south-1 from Raghunathganj's location. Service availability must also be checked for the actual selected Region.

Use service identities and runtime secret injection, never embedded AWS keys. If VM hosting is chosen, require IMDSv2, encrypted durable disks, least-privilege instance profiles and managed access rather than open SSH. For burstable EC2 candidates, estimate CPU-credit surplus costs and architecture compatibility. Do not rely on ephemeral instance-store disks for database durability. User restrictions take precedence over generic multi-Region recommendations in skills.

Spend limits can pause a project. For sudden Access Denied on previously working operations, ask about spend limits and direct the user to AWS Settings > Billing; only the project owner can change a limit. Billing/invoices/spend limits use AWS Settings; budgets and optimization use the AWS Billing and Cost Management console. After creating resources in a future authorized task, ask whether to retain or clean them up.

## Deployment and recovery gates

GitHub Actions initially validates docs only. Future CI adds lint/types/tests/build, scanning and disposable DB migration tests. Staging deployment is a separately authorized task; use a dedicated environment, short-lived credentials/OIDC where supported, and no production credentials in PR jobs. Protect production with a manual approval gate and a tested rollback/roll-forward plan; do not automatically deploy from main.

Secrets, database and verification files need encryption in transit and at rest. Monitor API error/latency, DB capacity, authentication abuse, outbox lag, verification queue and AI consumption. Set log/backup retention and redact personal content. Define incident contacts and pilot recovery targets before P7. Provisional targets: RPO <=24 hours and RTO <=4 hours, to be approved and demonstrated by restore exercises; no current system meets these targets because none exists.
