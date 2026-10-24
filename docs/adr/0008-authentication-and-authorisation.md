# ADR-0008: API keys for merchants, JWT for staff and drivers, RBAC, audit

**Status:** Accepted · 2026-10-24

## Decision
- **Merchants (machines):** API keys `lmd_<env>_<id>_<secret>`; only a SHA-256 hash and the prefix are stored; scopes
  such as `orders:read`, `orders:write`, `webhooks:manage`; revocable; `last_used_at` tracked.
- **People:** `POST /auth/token` with email + password (argon2) returns a short-lived JWT (HS256, PyJWT) with `sub`
  and `role`. Roles: `admin`, `dispatcher`, `driver`, `merchant_user`. The user row is re-read on every request so
  deactivation takes effect immediately.
- **Tenancy:** every `/v1` query is filtered by the caller's merchant; another merchant's resource returns 404.
- **Audit:** key creation/revocation, order cancellation, rescue approval, re-sequencing and transfers write an
  `audit_log` row with actor, action, target and details.
- **Internal:** `/internal/*` (simulator control) requires `X-Internal-Token` and is disabled in `prod`.

## Consequences
+ Simple, standard, testable. − No OAuth/SSO in MVP.
