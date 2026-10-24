# ADR-0009: Standard Webhooks signing, retries and delivery log

**Status:** Accepted · 2026-10-24

## Decision
- Endpoints are registered per merchant with a list of event types; a `whsec_…` secret is shown once and stored
  encrypted (Fernet).
- A fan-out consumer turns merchant-relevant events into `webhook_deliveries` (unique per endpoint + event, so a
  replayed event never duplicates a delivery).
- A sender claims due deliveries, POSTs them **without holding a database session**, and records the result.
  Headers follow the Standard Webhooks spec: `webhook-id` (event ID), `webhook-timestamp`, `webhook-signature:
  v1,<base64 HMAC-SHA256 of "id.timestamp.body">`.
- Retries: 0 s, 10 s, 1 min, 5 min, 30 min, 2 h (configurable), then `dead`. HTTP 410 disables the endpoint.
- Payloads exclude recipient phone numbers. Private-network URLs are rejected outside development.

## Consequences
+ Merchants can verify authenticity with off-the-shelf libraries. + At-least-once delivery with full audit.
− Consumers must dedupe on `webhook-id`.
