# ADR-0007: OR-Tools CVRPTW with a greedy fallback and a pluggable travel-time model

**Status:** Accepted · 2026-10-24

## Context
Routes must respect vehicle weight/volume capacity, customer time windows and shift ends. A road-network router (OSRM)
needs a pre-processed map, which is heavy for laptops and CI.

## Options
1. OSRM + VROOM in Docker. 2. **Google OR-Tools in-process + a travel-time model.** 3. Hand-written heuristic only.

## Decision
Option 2. The travel-time model is haversine distance × a circuity factor ÷ an hour-of-day speed profile per vehicle
type, with optional slowdown zones (traffic incidents). If `LASTMILE_OSRM_URL` is set, durations come from OSRM's
table service instead. OR-Tools solves a capacitated VRP with time windows (dimensions: time, weight, volume; orders
may be dropped with a penalty) under a time limit that scales with problem size. A greedy insertion heuristic is used
when OR-Tools is unavailable or returns no solution. Large waves are split by sweep angle around the facility.

## Consequences
+ Runs anywhere, deterministic in tests. + Real road times are one setting away.
− Straight-line based times are an approximation; documented as such in reports.
