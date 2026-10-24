# Product Requirements — Last-Mile Platform

**Owner:** Ajay Kumar Suppal (product owner) · **Status:** v1 (MVP) · **Last updated:** 2026-10-24

> **ELI5.** Shops need parcels taken to customers' doors. This product is the "brain" that takes each shop's order,
> decides which driver carries it and in what order, guides the driver, watches for trouble, tells the shop what
> happened, and measures how well it all went. A built-in "video-game city" lets us test it without real vans.

## 1. Problem

Merchants that sell online hand parcels to a delivery operation that is hard to see into. Orders arrive through
ad-hoc channels, routes are planned by hand, drivers work from paper or chat messages, and when something goes
wrong (a van breaks down, a customer is not home, a driver loses signal underground) nobody notices until the
promised time has passed. Merchants learn about failures from angry customers instead of from the system.

## 2. Goal and success criteria

Deliver one reliable, observable **order → doorstep → merchant notified** loop, then improve it.

| Outcome | Measure (MVP target, measured in the simulator) |
|---|---|
| Orders are never lost or duplicated | 100 % of accepted orders reach a terminal state; 0 duplicates under retries |
| Deliveries are on time | On-time delivery (OTD) ≥ 90 % in the `demo` scenario |
| Merchants are informed | ≥ 99 % of merchant-facing events delivered as signed webhooks (after retries) |
| Operations can act early | At-risk routes flagged before they are late; rescue never causes a double delivery |
| Performance is measurable | KPIs available live and in an end-of-run report |

## 3. Personas

| Persona | Needs |
|---|---|
| **Merchant integration engineer** | A predictable REST API, API keys, idempotent writes, bulk upload, signed webhooks, clear errors |
| **Merchant operations user** | See orders and their timeline, cancel before pickup, ask questions in plain language |
| **Dispatcher** | A live map of routes and drivers, a prioritised exception queue, one-click rescue with approval |
| **Driver** | A simple phone app: accept route, pick up, scan, navigate stop to stop, prove delivery, works offline |
| **Fleet manager** | Driver, vehicle and compliance records; only eligible driver–vehicle pairs get work |
| **Operations analyst** | Trustworthy KPIs, plan vs actual, exportable event history |
| **Platform engineer** | One-command local run, CI gates, observable services, documented decisions |

## 4. Scope

### 4.1 In scope (MVP)

1. **Merchant API (`/v1`)** — API-key auth with scopes; create (idempotent), get, list, cancel orders; packages;
   SLA profiles (express, same-day, next-day) that compute the promised time; bulk ingestion (JSON / CSV);
   webhook endpoints with signed delivery, retries, delivery log and replay; merchant-scoped KPIs.
2. **Carrier & capacity** — carriers, drivers, vehicles (VIN, type, weight and volume capacity), compliance documents
   with expiry, shifts with vehicle selection, eligibility rules.
3. **Planning & assignment** — facility-based planning waves; vehicle routing with capacity, time windows and shift
   end; unplannable orders roll over and raise SLA-risk exceptions; plan preview.
4. **Driver execution (`/driver/v1`)** — accept route, arrive at pickup, scan packages, arrive at stop, capture proof
   of delivery (POD), deliver or fail with reason, complete route; geofence checks; idempotent events; offline batch
   sync with original timestamps; returns of undeliverable packages; a mobile web app.
5. **Control tower (`/ops/v1`)** — live route state with ETA-based risk; exception queue; two-phase rescue with
   suppression of already-completed work; stop re-sequencing and transfer; live map over server-sent events.
6. **Analytics** — on-time delivery, first-attempt success, deliveries per hour, dwell, doorstep time, failure and
   return rates, plan-vs-actual arrival error; event export.
7. **Simulator** — a discrete-event model of the Chandigarh–Mohali–Panchkula tricity that plays merchants, drivers,
   traffic, breakdowns, signal loss and GPS drift against the real API, calibrated on published delivery data.
8. **Knowledge layer** — JSON-LD representation of orders and events aligned with schema.org and EPCIS concepts,
   SHACL validation, a knowledge-graph export with SPARQL.
9. **Merchant assistant** — a chat assistant that answers order questions and performs create/cancel only after the
   merchant approves.

### 4.2 Out of scope (later)

Machine-learned ETA and risk models, computer vision on POD photos, automatic (unapproved) rescue in production,
dynamic pricing, customer-facing notifications (SMS/WhatsApp), native mobile apps, multi-region deployment.

## 5. Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | A merchant authenticates with a hashed, scoped API key; a key is shown once at creation and can be revoked. |
| FR-2 | `POST /v1/orders` requires an `Idempotency-Key`; replays return the original response; a reused key with a different body is rejected. |
| FR-3 | Orders are validated (service area, time window, package sizes, phone format) and normalised before acceptance. |
| FR-4 | Each order gets a promised-by time from its SLA profile, computed in the local time zone (Asia/Kolkata). |
| FR-5 | Orders can be cancelled until pickup. |
| FR-6 | Bulk ingestion accepts up to 1 000 orders per batch and reports per-row results. |
| FR-7 | Merchant-facing events are delivered to registered webhook endpoints, signed per the Standard Webhooks spec, retried with backoff, logged, and replayable. |
| FR-8 | Drivers can only start a shift with a vehicle they are eligible to drive (licence class, valid documents, vehicle available). |
| FR-9 | Planning waves produce routes that respect vehicle capacity (weight and volume), time windows and the driver's shift end. |
| FR-10 | A published route is offered to its driver; a route not accepted in time raises a no-show exception and is re-planned. |
| FR-11 | Driver events are idempotent by client event ID and accepted out of order; offline batches keep device timestamps. |
| FR-12 | Arrival or delivery outside the geofence radius is accepted but flagged and raises an exception. |
| FR-13 | Failed packages return to the facility; they are re-attempted while attempts remain, otherwise returned to the merchant. |
| FR-14 | The control tower computes a risk state for every active route and raises exceptions for late/at-risk routes, no-shows, breakdowns, stale heartbeats, failed deliveries and geofence violations. |
| FR-15 | Rescue is proposed, approved, then dispatched; a delivery recorded on the device before the hand-over always wins and voids the rescue leg. |
| FR-16 | Every state change emits an immutable, versioned event in the same transaction. |
| FR-17 | KPIs are available live (all, per facility, per merchant) and in a run report. |
| FR-18 | Sensitive actions (key creation, cancellation, rescue approval, re-sequencing) are written to an audit log. |

## 6. Non-functional requirements

| Area | Requirement |
|---|---|
| Reliability | No dual writes: state and event commit together. Consumers are idempotent and resume from a stored offset. |
| Idempotency | All write APIs that can be retried are idempotent (orders, batches, driver events, webhook deliveries). |
| Performance | Laptop, SQLite: order intake p95 < 300 ms at 20 requests/s; planning wave of 300 stops < 5 s. PostgreSQL for higher load. |
| Security | Hashed API keys and passwords (argon2), JWT for staff/drivers, role-based access, encrypted webhook secrets, no secrets in the repo, SSRF guard on webhook URLs. |
| Privacy | Webhook payloads and exports exclude recipient phone numbers; POD photos stored outside the database. |
| Observability | Health and readiness probes, Prometheus metrics (requests, events, consumer lag, webhook outcomes, solver time), request IDs in logs. |
| Portability | Runs with only `uv` installed (SQLite); PostgreSQL supported and tested in CI; Docker image provided. |
| Testability | Unit, integration, property-based contract tests and an end-to-end simulation run in CI. |

## 7. KPIs (definitions)

| KPI | Definition |
|---|---|
| On-time delivery (OTD) | Delivered orders whose delivery time ≤ promised-by (or window end) ÷ delivered orders |
| First-attempt success | Orders delivered on the first attempt ÷ orders with at least one attempt |
| Deliveries per hour (DPH) | Delivered stops ÷ driver hours on active routes |
| Dwell time | Mean time from stop arrival to delivery outcome |
| Doorstep time | Mean time from stop arrival to proof-of-delivery capture |
| Failure rate | Failed attempts ÷ all attempts |
| Return rate | Returned orders ÷ orders that reached a terminal state |
| Plan vs actual | Mean absolute error between planned and actual stop arrival (minutes) |
| Webhook success | Webhook deliveries that succeeded ÷ deliveries that reached a final state |

## 8. Release plan

MVP is delivered as 16 pull requests across five milestones (see `docs/project-plan.md`); each milestone ends with a
working demo in the simulator.

## 9. Risks and assumptions

- Simulator realism depends on calibration; until real-data calibration runs, parameters are labelled assumptions.
- SQLite is a single-writer database; the default demo scale is chosen to fit it, larger runs use PostgreSQL.
- The assistant requires an Anthropic API key to run live; all of its tests run without one.
