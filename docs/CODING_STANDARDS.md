# Coding standards

These are requirements for future application code. Configuration is not installed yet.

## Language and boundaries

Use TypeScript strict mode; prohibit unexplained any and ignored type errors. Choose one lint/formatter configuration in P1 and enforce it in CI. Pin supported runtime/package-manager versions and commit the dependency lockfile; CI uses frozen installs. Use NestJS feature modules with thin controllers, domain services and database adapters. Avoid circular imports and arbitrary direct table writes across modules.

API routes use /api/v1, validated allowlisted DTOs, OpenAPI contracts and consistent errors with request IDs. Do not expose stack traces, database rows, credential columns or internal provider errors. Separate public response schemas from private/admin schemas. Use bounded cursor pagination and explicit request limits. Version breaking API changes and regenerate clients rather than hand-editing generated files.

## Database and migrations

Use parameterized queries, foreign keys, checks and unique constraints. Review spatial SQL explicitly. Use timestamptz/UTC, UUIDs and INR paise integers; never floating-point money. Write additive expand/contract migrations; do not silently drop data or rewrite applied migrations. Backfill separately with checkpoints and a rollback/roll-forward plan. Runtime DB role cannot create/drop schema; migration identity is distinct.

Transactions enforce deal and verification invariants. Include concurrent update tests and idempotency keys on replayable mutations. Validate latitude/longitude and metres consistently. Do not replace PostGIS with approximate frontend distance sorting for correctness-critical decisions.

## Frontends and localization

Call the API through the generated client. Share contracts/business vocabulary across web and mobile; share UI only where platform accessibility stays correct. Localize Bengali/English strings, INR and Asia/Kolkata date rendering. Include loading/empty/error/permission-denied states, keyboard/screen-reader support and small-screen layouts. Retry writes only with server-supported idempotency.

## Security and observability

Follow [SECURITY.md](SECURITY.md). Authorization belongs in the API and services even when the UI hides controls. Structured logs carry request IDs, event names and safe IDs; redact tokens, login inputs, addresses, evidence URLs and model prompts. Audit role/verification/deal actions separately with retention and controlled access.

Bound retries with backoff, timeouts and jitter. Never blindly retry non-idempotent mutations. External adapters are replaceable; failures return a safe user-facing state. AI outputs must pass runtime schema validation before display and cannot bypass domain authorization.

## Changes and review

Small PRs link a task ID, describe the concrete behavior, and record validation commands/results, migration effects, security implications and remaining limits. Preserve unrelated work. Update architecture decisions for material changes. A task needs failing-path tests and appropriate integration checks, not tests that merely repeat implementation. Do not claim success based only on compilation or mocked dependencies.
