# Architecture decision records

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-modular-monolith.md) | Modular monolith with in-process workers | Accepted |
| [0003](0003-sqlite-default-postgres-supported.md) | SQLite by default, PostgreSQL supported | Accepted |
| [0004](0004-event-log-in-the-database.md) | Event log in the database (transactional outbox without a broker) | Accepted |
| [0005](0005-event-envelope.md) | One versioned event envelope | Accepted |
| [0006](0006-simulated-clock.md) | Platform clock that can run in simulated time | Accepted |
| [0007](0007-routing-solver.md) | OR-Tools CVRPTW with a greedy fallback and a pluggable travel-time model | Accepted |
| [0008](0008-authentication-and-authorisation.md) | API keys for merchants, JWT for staff and drivers, RBAC, audit | Accepted |
| [0009](0009-signed-webhooks.md) | Standard Webhooks signing, retries and delivery log | Accepted |
| [0010](0010-no-build-frontend.md) | Static web apps without a build step | Accepted |

New ADRs: run `/adr <title>` in Claude Code or copy the structure of an existing file.
