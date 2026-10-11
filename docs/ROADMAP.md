# Phased development plan

All application phases are planned. Durations below are rough engineering estimates for one experienced developer, not committed dates; feedback, verification operations, provider delivery and store review can extend them. Security and tests are required in every phase.

| Phase | Indicative effort | Deliverables | Acceptance gate | Tasks |
| --- | --- | --- | --- | --- |
| P0 Planning | Current task | Architecture, agent rules, state, decisions, registry and validator | Documents validated locally; remote additions verified; PR reviewed/merged before phase closure | NS-001 |
| P1 Foundation | 1-2 weeks | pnpm workspace, API skeleton, environment validation, local PostGIS, migrations, API contracts and CI | Reproducible clean setup; health/readiness; migrate blank DB and restore fixture; lint/types/build/tests pass | NS-010, NS-011 |
| P2 Identity | 2-3 weeks | Register/login/logout/recovery, sessions, RBAC/object policies, admin MFA | Revocation, expiry, abuse limits, CSRF and cross-user denial tests pass | NS-020 |
| P3 Verified discovery | 2-3 weeks | Profiles/listings, evidence review, admin queues, geospatial search, public web | No private evidence leaks; badge expiry; real PostGIS geo/index checks; Bengali/English flows | NS-030, NS-031, NS-032 |
| P4 Agreements | 2-3 weeks | Requests, offers, deal states, notifications/outbox and dispute audit | Atomic offer acceptance; unique deal; idempotency; ownership and transition tests | NS-040 |
| P5 Mobile pilot | 2-3 weeks | Expo Android-first flows, secure session storage, location fallback | Physical device tests; session revoke; weak-network recovery; no duplicate submissions; accessibility | NS-050 |
| P6 Assisted AI | 1-2 weeks | Category/search assistance, provider description drafts, strict output contracts | Bengali/English evaluation; PII redaction; injection tests; budget cutoffs; core features work with AI off | NS-060 |
| P7 Release readiness | 2-3 weeks | Threat review, load tests, staging, restore drills, monitoring, runbooks and release artifact | Security and recovery gates signed off; hosting costs approved; staging verified; production remains a separate authorization | NS-070 |

P3 depends on P2; P4 depends on verified profiles and discovery; mobile can prototype after stable P2 contracts but closes after P4 journeys. AI starts after core workflows are usable. P7 testing begins during P1; its final gate cannot be bypassed by a demo.

## Milestones

- M0: planning proposal reviewed, merged and all documented checks pass.
- M1: a new developer can run the API and real PostGIS locally from documented commands.
- M2: a resident can sign in and an unauthorized user cannot edit another user's data.
- M3: a reviewer can verify a provider and a resident can discover only published eligible nearby services.
- M4: a resident and provider can agree a deal once, even with concurrent or retried requests.
- M5: the same journey works on a physical Android device with Bengali/English text and poor connectivity.
- M6: bounded AI assistance is evaluated and optional; no privileged action is delegated to the model.
- M7: staging evidence, recovery, security review and cost signoff support a separate launch decision.

## Definition of done

A task may be verified_complete only when its acceptance criteria are met, meaningful tests pass, evidence is recorded, docs match implementation, no secrets are included, and its required review/merge is complete. A planned endpoint, mock UI, passing docs validator or opened PR does not prove a product feature is complete.

## Open product inputs

Confirm pilot categories/service boundary, phone-versus-email login, evidence and expiry policy, moderation responsibility, adult/minor policy, support/dispute operations, target Android devices and anticipated users. Budget, AWS selected Region, plan type and trial expiry are also unresolved. Track resolutions in [DECISIONS.md](../DECISIONS.md); do not block independent local scaffolding on hosting decisions.
