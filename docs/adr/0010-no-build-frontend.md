# ADR-0010: Static web apps without a build step

**Status:** Accepted · 2026-10-24

## Context
The control tower, merchant portal and driver app are needed for demos, but the environment has no Node.js, and a
frontend build chain would slow everyone down.

## Decision
Plain HTML + modern JavaScript modules + CSS served by FastAPI from `src/lastmile/web/`. Maps use Leaflet from a
pinned CDN version with OpenStreetMap tiles (attributed). Live updates use server-sent events. The driver app keeps an
offline queue in `localStorage` and syncs through `/driver/v1/sync`.

## Consequences
+ Zero tooling; view-source friendly. − No component framework; keep pages small.
