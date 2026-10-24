# ADR-0003: SQLite by default, PostgreSQL supported

**Status:** Accepted · 2026-10-24

## Context
Contributors' laptops may not have Docker or a database server. The demo must run with only `uv` installed, yet the
design must hold up on a production database.

## Options
1. PostgreSQL only (Docker required).
2. **SQLite (WAL) by default, PostgreSQL via `LASTMILE_DATABASE_URL`, both tested in CI.**
3. In-memory stores.

## Decision
Option 2 with SQLAlchemy 2 (async) and Alembic migrations (`render_as_batch` for SQLite). Portable column types only:
UUIDs via `sqlalchemy.Uuid`, JSON via `sqlalchemy.JSON`, timestamps stored as UTC through a custom type, enums as
strings validated in code. Geospatial maths (haversine, H3 cells) is done in Python, so PostGIS is not required.

SQLite runs with a **single pooled connection**: every unit of work is serialised, which removes "database is locked"
races. Consequence: never hold a session across network I/O.

## Consequences
+ Zero-install local runs and fast tests. + Same code on PostgreSQL.
− SQLite caps write throughput; large simulations should use PostgreSQL.
