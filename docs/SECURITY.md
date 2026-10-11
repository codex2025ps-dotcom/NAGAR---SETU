# Authentication, authorization and security design

Status: proposed requirements; no authentication code exists yet. Implementation belongs to NS-020 and is a release gate.

## Credentials and session flow

1. Register/login over HTTPS; normalize login identifiers and validate request DTOs. Proposed pilot login is email/password, subject to product confirmation. Verify email before sensitive actions. Use generic recovery responses to reduce enumeration.
2. Use a maintained password library with Argon2id parameters benchmarked against current OWASP guidance. Store only salted password hashes. Never log a password, persist plaintext, use reversible encryption for passwords, or implement cryptography manually.
3. Successful login creates a cryptographically random opaque session token with at least 256 bits of entropy. PostgreSQL stores its SHA-256 hash, user ID, creation/last-use/expiry times and revocation state. Tokens are never stored in plaintext server-side; SHA-256 here applies to high-entropy tokens, not passwords.
4. Web uses a host-only Secure, HttpOnly, SameSite=Lax cookie with Path=/ and no Domain (use the __Host- prefix). Serve API under the same origin, for example /api/v1. Origin validation and CSRF tokens protect all unsafe cookie-authenticated methods, including login/logout. Do not put auth tokens in localStorage or URLs.
5. Mobile receives the token once in the HTTPS login response, stores it in Expo SecureStore and sends Authorization: Bearer. Avoid ordinary AsyncStorage, analytics events, crash dumps and debug logs. SecureStore is not a replacement for server revocation; handle device restore/reinstall and invalidated storage by reauthentication.
6. Each authenticated request hashes the supplied token, finds its active session and checks absolute/idle expiry plus current user status/roles. If cookies and bearer credentials conflict, reject the request. Rotate sessions after login/privilege changes and revoke old sessions. No JWT access or refresh-token pair is proposed initially.
7. Logout revokes the server record before clearing client storage. Suspension, password reset and compromised-session response revoke all relevant sessions. Browser and device storage failures must not leave a valid server session accidentally active.

Proposed initial limits: ordinary web sessions have 7-day absolute/24-hour idle expiry; mobile has 30-day absolute/7-day idle expiry; admin access has 12-hour absolute/30-minute idle expiry plus recent MFA for sensitive actions. These are initial policy choices to validate in P2, enforced server-side independently of cookie lifetime. Persist session last-use efficiently without extending absolute expiry. Never cache revocation or role changes beyond the documented enforcement requirement.

Password-reset tokens expire after 15 minutes; email-verification tokens after 24 hours. Generate them securely, hash them in the database, consume them once atomically, and keep them out of logs/referrers. Rate-limit requests and verification attempts. Use reviewed MFA libraries; encrypt MFA seeds with a runtime-managed key, hash one-use recovery codes, and require admin/moderator MFA before review or role administration. Do not ship a default admin password or role self-assignment path.

## Authorization policy

Default deny. Authentication runs before authorization. Every route explicitly declares public access or a policy; domain services also enforce object ownership and transition rules. Read roles from server state; never trust frontend claims. Return 401 for absent/invalid sessions and 403 for forbidden authenticated actions, with controlled 404 responses where needed to conceal resource existence.

Residents operate their own requests; providers operate their own profiles/offers; business owners manage only their businesses and permitted memberships. Moderators access assigned review queues and must not review their own profiles. Admin grants are audited, require recent MFA and cannot be created through ordinary profile update endpoints. Exact grant/review responsibilities are open product decisions; implement least privilege and test cross-user access.

## Threats and required controls

| Risk | Control | Required verification |
| --- | --- | --- |
| Credential stuffing/session theft | Per-identity and per-source rate limits, generic errors, secure cookies/storage, revocation | Expiry, logout, reset, suspension, repeated-login and device tests |
| IDOR/privilege escalation | Explicit policies, current roles, ownership checks, DTO allowlists | Cross-user edits/reads and role-injection requests fail |
| SQL injection/geo abuse | Parameterized SQL, bounded radius/paging, runtime validation | Malformed coordinates and injection payloads fail |
| Double deal acceptance | Transaction, locking, unique request constraint, idempotency | Concurrent acceptance and retry tests |
| Evidence leakage/malicious upload | Private bucket, short signed URLs, authorization, allowlisted MIME/size, scan/quarantine | Public enumeration/expired links fail; unsafe files rejected |
| XSS/CSRF | Escape output, restrictive CSP, origin allowlist, CSRF validation | Cookie-authenticated cross-site writes and stored payload tests |
| AI injection/data disclosure | Treat all model/retrieval text as untrusted, minimize/redact inputs, no privileged tools | Injection, schema rejection, leak checks, budget-off fallback |
| Secret/supply-chain leakage | Runtime secrets, protected environments, pinned CI actions, dependency scan | Secret scanning and lockfile/dependency review |

Request body limits, timeouts and shared rate-limit state must work across replicas before scaling. Restrict outbound fetches to approved endpoints to reduce SSRF; never let model outputs select arbitrary URLs. Public objects have a separate response schema from evidence and private user data.

## Privacy and evidence

Collect the least necessary contact/location information with clear purpose and consent. Define retention, deletion/export, moderator access logs, backup expiration and incident response before launch. Never seed production-like personal data into CI or prompts. Keep verification evidence private; display only the approved scope/date/expiry. The policy for identity evidence and applicable legal obligations needs qualified review before launch; this document does not claim legal compliance.

## Secret handling

Inject database credentials, mail/SMS credentials, object-storage keys, MFA encryption keys and AI keys at runtime. Only API/worker processes receive them. No browser public-variable prefix may contain a secret. Local .env files are ignored; commit examples with empty values only. Git ignore rules are not secret scanning. On a discovered leak, stop exposing it, redact reports, revoke/rotate the credential, and record remediation without copying the value.

Primary references: [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [Expo SecureStore](https://docs.expo.dev/versions/latest/sdk/securestore/).
