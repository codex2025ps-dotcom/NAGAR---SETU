# Instructions for Nagar Setu coding agents

## Mission and verified state

Build a cost-effective, secure, verified local platform for Raghunathganj. Read [PROJECT_STATE.md](PROJECT_STATE.md), [TASK_REGISTRY.md](TASK_REGISTRY.md), [DECISIONS.md](DECISIONS.md), and [the architecture](docs/ARCHITECTURE.md) first. Proposed designs are not implemented features. This task is documentation and validation only.

## Working rules

- Inspect the current branch, remote, file tree, existing instructions, and uncommitted changes before editing. Use targeted searches and read relevant code before making claims.
- Preserve existing files and user work. For the initial planning task, add files only. Future changes require authorization in the active task; never reset, force-push, overwrite unrelated work, or delete resources implicitly.
- Select one registered task and check its dependencies. Record owner, status, evidence, and remaining work. Use planned, in_progress, blocked, ready_for_review, or verified_complete; completion requires acceptance evidence and review/merge where specified.
- Work on a feature branch. Prefer small reviewable changes and additive migrations. Do not merge or deploy unless the user authorizes that action.
- Do not invent test results. Run appropriate checks, record commands and outcomes, and distinguish local validation, remote CI, integration tests, and production observations.
- Update state, task registry, and decisions when scope or implementation changes. Explain security and data-migration effects in the PR.
- Do not spawn or delegate to other agents unless the user authorizes it or a relevant task instruction requires it. Avoid duplicate concurrent work.

## Guidance preference

help_level: HIGH (selected by the user on 2026-10-12).

Before each meaningful step explain what it does and why. Suggest a better alternative when justified, explain tradeoffs, and flag best practices while executing the user's choice. Ask for missing inputs only when needed; continue independent authorized work. Conversational assistant nickname: ঈশা (Isha). Be truthful about being an AI assistant when identity matters.

## Architecture boundaries

- Use the proposed TypeScript pnpm monorepo and modular NestJS API unless an ADR explains a change. Client applications use the API; database access and secrets stay server-side.
- Shared contracts are public API types, not ORM entities. Validate input at runtime, authorize every object operation in the API, and default to deny.
- Role grants, verification approval, suspension, and offer acceptance are server-controlled and audited. A role or phone/email confirmation does not establish provider verification.
- Use PostgreSQL/PostGIS migrations and parameterized queries. Test geo behavior and concurrency against real PostGIS, not mocks alone.
- Keep AI optional, bounded, and behind the API. It cannot approve verification, grant roles, commit deals, or execute arbitrary tools.
- Apply [coding standards](docs/CODING_STANDARDS.md), [security requirements](docs/SECURITY.md), and [testing gates](docs/TESTING.md).

## Secrets and privacy

Never commit, print, send to AI, or embed passwords, live tokens, private keys, verification documents, or personal customer data. Commit only empty configuration examples. Use runtime secret injection and least-privilege service identities. Redact logs. Do not collect identity documents such as Aadhaar by default. Use synthetic test data.

## AWS guidance for this user's new AWS experience

This section carries forward user-provided constraints. The user's three-month trial is reported; paid-plan status, selected Region, spend limit, and budget are unconfirmed. Do not provision or deploy under this task.

- Before an AWS task, check available relevant AWS skills; use retrieve_skill if available, otherwise read the listed SKILL.md and follow its applicable guidance. The user's constraints override general skill advice.
- Say project instead of account, team member instead of IAM user, AWS Settings for settings.aws.com management, and selected Region instead of home Region. Human access is managed by AWS; do not assign team-member roles unless essential. Service-to-service IAM policies are still needed.
- Ask the user to confirm the Region in AWS Settings > View all projects > Overview > Additional Info > Region. If they cannot confirm, inspect ~/.aws/config without exposing credentials. Never infer the Region from the user's address or app location.
- All projects share one assigned Region. Create all Regional resources there, including Lambda and API Gateway. No Lambda@Edge, StackSets, cross-Region replication, multi-Region KMS, or Route 53 geolocation/latency/failover routing.
- CloudFront is global and actions may use us-east-1, pointing to origins in the selected Region. Only S3, Kinesis, CloudWatch Logs, and CloudWatch metrics dependencies required by global resources may also use us-east-1. Inventory those resource types in both Regions. Do not use that exception for ordinary app resources.
- Rekognition, Textract, Personalize, and App Runner are unavailable in eu-north-1 for this experience. Check service availability and plan eligibility before proposing a concrete deployment.
- Check whether the project is upgraded to the paid plan before development that uses AWS. For a failing service run `aws freetier get-account-plan-state`, then check the appropriate [Free/Paid supported-services list](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html). If unsupported, consult the unsupported list and explain that advanced features may be required; do not activate them silently.
- On sudden Access Denied for previously working operations, ask about spend limits and direct the user to AWS Settings > Billing. Only project owners can modify limits. Billing, invoices, and spend limits live in AWS Settings; budgets and cost optimization live in the AWS Billing and Cost Management console.
- Consult [project SCP/RCP documentation](https://docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html) for managed-policy restrictions; never attempt to bypass them.
- Before provisioning record the estimate, trial expiry, approved budget, cleanup plan, and Region. After successfully creating resources, ask whether to clean them up or retain them to control cost. No production deployment without explicit authorization.
