# CLAUDE.md — Last-Mile Platform

Read this before changing code. Keep it short; details live in `docs/`.

## What this is
A last-mile delivery orchestration platform: merchants (retailers) submit orders through an API → orders are planned
into routes → assigned to eligible driver + vehicle pairs → executed through a driver app (offline-tolerant) →
monitored in a control tower (risk, exceptions, rescue) → reported back to merchants via signed webhooks → measured
with KPIs. A SimPy simulator of the Chandigarh–Mohali–Panchkula tricity drives the whole system over HTTP.

## Commands
- `make setup` — install Python 3.12 and dependencies (uv)
- `make lint` / `make fmt` — ruff
- `make test` — pytest (SQLite, no external services)
- More targets (`make run`, `make demo`, `make sim`, `make e2e`) arrive with the platform modules.

## Architecture (see `docs/architecture.md` and `docs/adr/`)
- Modular monolith in `src/lastmile/` (one process; background workers run in the FastAPI lifespan).
- Simulator in `src/lastmile_sim/` talks to the platform **only over HTTP**.
- Every state change appends an event to the `events` table **in the same transaction** (no dual writes).
- Event envelope and catalog: `docs/events/asyncapi.yaml`. Contracts change additively; breaking changes need an ADR.

## Workflow (one story = one branch = one PR)
1. `/story <issue#>` — write `docs/stories/<n>-<slug>.md` from the issue and create `feat/<n>-<slug>`.
2. Write a failing test, implement the smallest change, run `make lint test`.
3. `/commit` — Conventional Commit from the staged diff (`type(scope): subject`).
4. `/pr` — run checks, update `docs/CURRENT_STATE.md`, open the PR with `Closes #n` and test evidence.
5. Squash-merge after `ci` is green. The PR title becomes the commit on `main`.

## Hard rules
- Never commit secrets, `.env`, raw third-party datasets, or any client/confidential document.
- Never push to `main` directly or force-push; `main` is protected.
- Never hold a database session open across network I/O (HTTP calls, LLM calls) — SQLite runs with one connection.
- Times are timezone-aware UTC in storage; business rules use the platform clock (`lastmile.clock`), never `datetime.now()`.
- New dependencies: say why, check the licence.

## Definition of Done
Issue linked · tests pass in CI · contracts/docs updated · `docs/CURRENT_STATE.md` updated · PR description explains
the change in plain language (an ELI5 line is welcome).
