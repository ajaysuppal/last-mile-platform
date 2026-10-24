# ADR-0004: Event log in the database (transactional outbox without a broker)

**Status:** Accepted · 2026-10-24

## Context
Every state change must produce an immutable event for other modules, merchants (webhooks), the control tower and
analytics. Writing to a database and then publishing to a broker is a dual write: a crash in between loses the event.

## Options
1. Database + broker (Kafka/Redis Streams) with a transactional outbox and relay.
2. **The outbox *is* the log: an append-only `events` table read by consumers that store their offset.**
3. Change-data-capture (Debezium).

## Decision
Option 2. Producers call `append_event(session, …)` inside the business transaction. Each consumer reads
`seq > offset ORDER BY seq`, applies its effects and advances `consumer_offsets` **in one transaction**, which gives
effectively-once processing for database effects. Consumers are gap-aware: on PostgreSQL a sequence gap (an in-flight
or rolled-back transaction) is waited on briefly before being skipped. An in-process notifier wakes consumers right
after commits.

A Redis Streams or Kafka adapter can be added later by relaying the same rows; contracts do not change.

## Consequences
+ No lost or phantom events; no extra infrastructure. + Full history for analytics and replay.
− Polling a table; fine at MVP scale. − The table grows; archive/partition later.
