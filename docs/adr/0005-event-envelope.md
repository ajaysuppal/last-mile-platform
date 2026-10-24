# ADR-0005: One versioned event envelope

**Status:** Accepted · 2026-10-24

## Context
Mobile, control tower, analytics and webhooks all consume the same facts. Ad-hoc payloads per producer make consumers
brittle.

## Decision
All events share one envelope: `event_id` (UUIDv7, producer-generated; for driver events generated on the device and
used as the idempotency key), `event_type`, `version`, `occurred_at` (device/simulated time), `recorded_at`
(server time), `source`, subject IDs (`order_id`, `package_id`, `route_id`, `stop_id`, `driver_id`, `vehicle_id`,
`merchant_id`, `facility_id`), `latitude`, `longitude` and `metadata`. The catalog lives in
`docs/events/asyncapi.yaml`. Changes are additive within a version; breaking changes bump `version` and need an ADR.

`merchant_id` and `facility_id` are platform extensions so webhook fan-out and per-facility analytics do not need joins.

## Consequences
+ One parser everywhere; device time and server time are both kept (needed for offline sync and rescue suppression).
− Some fields are null for many event types.
