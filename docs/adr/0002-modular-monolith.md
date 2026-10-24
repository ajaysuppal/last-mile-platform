# ADR-0002: Modular monolith with in-process workers

**Status:** Accepted · 2026-10-24

## Context
The platform has many domains (orders, carrier, planning, execution, control tower, analytics, webhooks). Splitting them
into microservices early multiplies deployment, networking and consistency problems for a small team and a five-week
timeline.

## Options
1. Microservices per domain with a message broker.
2. **One deployable with strict module boundaries; background workers as asyncio tasks.**
3. Monolith without boundaries.

## Decision
Option 2. Each domain lives in its own package under `src/lastmile/` and owns its tables. Modules communicate through
service functions and the event log, not by reaching into each other's tables for writes. Workers (planner, webhook
sender, route monitor, batch worker, live feed) start in the FastAPI lifespan and can be disabled
(`LASTMILE_WORKERS_ENABLED=false`) for tests.

## Consequences
+ One command runs everything; transactions span a module and its events.
+ A module can later be extracted behind the same event contracts.
− CPU-heavy work (route solving) shares the process; mitigated with solver time limits and a worker thread.
