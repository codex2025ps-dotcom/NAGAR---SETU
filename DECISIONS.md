# Architecture decisions

Statuses: proposed, accepted, superseded. Accepted constraints come from the user's explicit request; stack proposals require review. This log is not evidence of implementation.

| ID | Status | Decision | Rationale / tradeoff |
| --- | --- | --- | --- |
| ADR-001 | proposed | TypeScript pnpm monorepo with NestJS, Next.js and Expo | Shared API contracts and lower context-switching; requires framework compatibility checks in P1 |
| ADR-002 | proposed | Modular monolith with one PostgreSQL/PostGIS database | Transactional deals and lower operating overhead; split only on measured scaling needs |
| ADR-003 | accepted | PostgreSQL plus PostGIS | User requirement; enforce indexed metre-based geo queries and extension validation |
| ADR-004 | proposed | Drizzle plus explicit SQL migrations | Typed common queries; spatial and concurrency correctness need reviewed SQL/integration tests |
| ADR-005 | proposed | Revocable opaque sessions in PostgreSQL | Immediate revoke/current roles; per-request lookup cost; auth library evaluated before P2 |
| ADR-006 | proposed | Web/admin share Next.js; mobile uses Expo | Faster initial admin delivery and Android-first pilot; native UI/accessibility still needs device work |
| ADR-007 | proposed | Manual scoped verification, with audit and expiry | Establishes review responsibility; requires operational evidence/moderation policy |
| ADR-008 | proposed | Optional server-side AI, no privileged actions | Limits spend and injection effects; core platform works with AI off |
| ADR-009 | accepted | Preserve existing files; additive planning first; no production deployment | Explicit user scope; all application functionality remains planned |
| ADR-010 | accepted | No exposed secrets or credentials; verified completion only | Explicit user requirement; tests/evidence must match claims |
| ADR-011 | accepted | HIGH guidance; user reports three-month AWS trial | User responses on 2026-10-12; trial is not proof of paid-plan eligibility or Region |

## Open decisions

| ID | Required input / decision | Needed by | Interim handling |
| --- | --- | --- | --- |
| OPEN-001 | AWS selected Region, plan type, exact trial expiry, allowance, spend limit and monthly budget | Before provisioning | Keep hosting unprovisioned; check AWS Settings and authenticated plan state |
| OPEN-002 | Pilot email/password vs phone OTP and reviewed auth/MFA library | P1/P2 | Proposed email baseline; no SMS expenses; compare managed identity alternative |
| OPEN-003 | Evidence types, reviewer roles, expiry, retention, disputes and privacy obligations | P3 | No sensitive ID collection by default; no badge without reviewed evidence |
| OPEN-004 | Pilot categories/service boundary and anticipated traffic | P1/P3 | Synthetic fixtures; bounded geo queries; no asserted jurisdiction boundary |
| OPEN-005 | Hosting provider and resilience/RPO/RTO budget | P7, before staging resources | Container portability; provisional targets only |
| OPEN-006 | AI provider, model, data-processing terms and hard quota | P6 | AI off; mock adapters only |
| OPEN-007 | Mail/SMS/map provider, delivery permissions/licensing and recurring costs | P2/P3 | No assumed free production integration |
| OPEN-008 | Mobile device baseline, age policy, support and moderation ownership | P3/P5 | Android-first proposal; no production launch until agreed |

## Recording changes

For each material decision add context, options, chosen behavior, consequences, status, date and task/PR evidence. Supersede old decisions explicitly rather than erasing their reasoning. Do not turn a proposed choice into accepted merely because a scaffold uses it. [Architecture](docs/ARCHITECTURE.md) and [roadmap](docs/ROADMAP.md) must stay consistent with this log.
