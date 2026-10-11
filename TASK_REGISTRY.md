# Task registry

Statuses: planned, in_progress, blocked, ready_for_review, verified_complete. Owners below are unassigned except the active planning task. Evidence must identify real checks/artifacts; design text is not implementation evidence. Update the table after each meaningful task.

| ID | Phase | Task | Status | Owner | Dependencies | Acceptance criteria | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NS-001 | P0 | Planning foundation | ready_for_review | Isha | - | Inspect repo; additive docs; validator and failure tests pass; remote additions verified; PR reviewed/merged for closure | Local validator PASS; 10 validator tests PASS; publication/CI evidence recorded in planning PR; review/merge pending |
| NS-010 | P1 | Backend API and monorepo foundation | planned | unassigned | NS-001 | Clean install, API health/readiness, contracts, lint/types/build/tests documented and passing | - |
| NS-011 | P1 | PostgreSQL and PostGIS foundation | planned | unassigned | NS-010 | Extension available, migrations/constraints tested on real DB, clean setup and restore fixture | - |
| NS-020 | P2 | User authentication and role-based access | planned | unassigned | NS-011 | Login/recovery/revoke/MFA/CSRF and object-denial tests pass; no default admin credentials | - |
| NS-030 | P3 | Business and service-provider profiles | planned | unassigned | NS-020 | Ownership, publication, consent, categories and scoped verification audit tests | - |
| NS-031 | P3 | Location-based discovery | planned | unassigned | NS-030 | Radius/index/privacy/boundary tests on real PostGIS; bounded paging and location fallback | - |
| NS-032 | P3 | Web and admin dashboard | planned | unassigned | NS-030, NS-031 | Review queues, suspension, audit, role-denial and Bengali/English E2E journeys | - |
| NS-040 | P4 | Requests, offers and deals | planned | unassigned | NS-031, NS-032 | Participant policies; states; concurrent one-deal acceptance; retry/idempotency; outbox checks | - |
| NS-050 | P5 | Mobile application | planned | unassigned | NS-040 | Physical Android journey; secure sessions; weak-network/location-denied/accessibility checks | - |
| NS-060 | P6 | AI integration | planned | unassigned | NS-040 | Evaluated Bengali/English assistance; quota/injection/schema/privacy tests; AI-off fallback | - |
| NS-070 | P7 | Testing, security and deployment readiness | planned | unassigned | NS-050, NS-060 | Staging/restore/load/security/cost evidence, runbooks; separate production authorization | - |

## Dependency and closure rules

Tasks may prototype independent parts early, but acceptance cannot close before dependencies are verified_complete. NS-001 remains ready_for_review until the planning PR is reviewed/merged and required checks are verified. Application tasks remain planned until actual code and acceptance evidence exist. NS-070 covers release readiness; it does not authorize a production deployment.
