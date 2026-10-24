# #2 — PRD, architecture, ADRs and event catalog

**Status:** Done · **Area:** docs · **Milestone:** M1 Foundations

## Context
Before modules are built in parallel, everyone needs the same picture of the product, the boundaries between
modules, and the message formats between them.

## User story
As a product owner I want a PRD, architecture views and recorded decisions so that everyone builds the same platform.

## Acceptance criteria
- [x] `docs/prd/PRD.md` — problem, goals, personas, scope, functional and non-functional requirements, KPIs.
- [x] `docs/architecture.md` — context and container diagrams, event flow, order lifecycle, rescue suppression, clock.
- [x] ADRs 0001–0010 with an index.
- [x] `docs/events/asyncapi.yaml` — envelope and the full event catalog.
- [x] `docs/project-plan.md` — roles, sprints, ceremonies, GitHub workflow, risks.

## Design
Diagrams are Mermaid so they render on GitHub and stay diffable. The PRD and plan are written in our own words.

## Test plan
Docs only; CI still runs lint and tests.

## Out of scope
OpenAPI document — generated from code once the API exists (`docs/api/openapi.json`).
