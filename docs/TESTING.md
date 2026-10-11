# Testing and verification gates

## Current validation

The planning foundation has a standard-library Python validator and unit tests. Run from repository root:

```sh
python3 tools/validate_planning.py
python3 -m unittest discover -s tools/tests -v
```

The validator checks required files, UTF-8/nonempty docs, relative Markdown file links, task ID uniqueness, statuses, dependency existence/cycles, required feature coverage, and evidence for verified_complete tasks. It ignores external URLs and does not validate Markdown anchors, source accuracy, legal compliance, secrets, application security or production readiness. Its tests include valid input and intentional broken planning fixtures. The workflow is validation-only and has no deployment job.

## Planned test layers

| Layer | Scope | Gate |
| --- | --- | --- |
| Static | lint, types, builds, OpenAPI/SDK diff, dependency/secret scans | Every implementation PR |
| Unit | policies, state transitions, validation, money, output schemas | Every domain change |
| Integration | real isolated PostgreSQL/PostGIS, migrations, constraints, sessions, outbox | Every API/database PR |
| Web E2E | login -> verified discovery -> request -> offer -> deal; moderator/admin denials | P2 onward, required before pilot |
| Mobile | physical device sessions, storage loss, permission denial, poor-network retries | P5 acceptance; emulator tests alone insufficient |
| AI evaluation | Bengali/English fixtures, unsafe content/injection, schema, cost caps, fallback | P6 with pinned prompt/model evaluation evidence |
| Operations | restore drill, load/soak, rollback/roll-forward, alerts | P7 staging release gate |

Use synthetic data; a disposable database per CI run with PostGIS enabled. Mock external paid services for routine tests, but record separate sandbox/provider delivery checks before launch. Make async time and session expiry controllable for deterministic tests.

## Critical acceptance cases

- Authentication: valid/invalid login, verification/reset token expiry and single use, rate limits, CSRF, admin MFA, revoked/expired sessions, deleted/suspended users, role change enforcement.
- Authorization: other users' private profiles/evidence/requests/deals cannot be read or changed; role and owner injection rejected; reviewers cannot approve themselves.
- Geography: longitude/latitude ordering, exact radius boundary, metres, invalid input, private address redaction, published/verified filters and EXPLAIN ANALYZE on realistic fixtures.
- Deals: simultaneous acceptance creates one deal; withdrawal/expiry races fail safely; replay returns original response; reused key with different body fails; unauthorized transitions rejected.
- Verification: expiry removes eligibility/badge, suspension is immediate, evidence remains private, approval is audited.
- AI: zero requests when disabled/budget exhausted; quota reservations prevent concurrent overspend; timeout/schema failure returns a safe fallback; no model output changes roles/verification/deals.
- Operations: migrate clean and previous schema, restore encrypted backup to isolated staging, observe alerts, execute rollback plan and verify logs contain no credentials.

## Release readiness

Set measured pilot latency/throughput targets in P1; proposed staging baseline is p95 API response under 500 ms for ordinary non-AI requests at agreed pilot load, with zero double-acceptance failures. Treat this as a target, not a result. Record hardware, dataset, concurrency and exclusions with measurements.

Before any production authorization: no unresolved critical/high findings; backup restoration demonstrated; monitoring/incident contacts assigned; retention/evidence policy approved; supported dependencies pinned; credentials rotated into deployment secret storage; budgets and trial expiry recorded; test failures/blockers disclosed. No production deployment is included in this task.
