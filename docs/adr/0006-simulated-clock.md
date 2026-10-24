# ADR-0006: Platform clock that can run in simulated time

**Status:** Accepted · 2026-10-24

## Context
A delivery day lasts 12+ hours; tests and demos need it in minutes. If the simulator accelerates time but the platform
uses the wall clock, SLA promises, time windows and risk calculations are wrong.

## Decision
All business code reads time from `lastmile.clock` (never `datetime.now()`). In `real` mode it is the UTC wall clock.
`POST /internal/sim/start {epoch, speed}` (internal token) switches to `epoch + (wall − start) × speed`. Workers sleep
in simulated seconds (`clock.sleep(sim_seconds)`). The simulator's SimPy loop uses the same formula, so both agree.

## Consequences
+ Deterministic, fast scenarios. + Same code in production (real mode).
− Retries of outbound webhooks use wall-clock backoff on purpose (network behaviour is not simulated).
