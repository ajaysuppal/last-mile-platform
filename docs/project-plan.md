# Project plan — team of 8, five one-week sprints

> **ELI5.** Eight people build one delivery company brain in five weeks. Everyone owns one department, agrees the
> "shape" of the messages between departments on day one, builds against fakes, and joins up every Friday in the
> simulator.

## 1. Approach

- **Contract-first:** freeze the event envelope and the `/v1` OpenAPI in week 1; each module builds against mocks.
- **Thin end-to-end slice first:** one order travels the whole loop in week 2, then each sprint deepens it.
- **One story = one branch = one PR:** issue → story spec → Conventional Commits → PR → CI → squash merge.
- **Simulator as the release gate:** every Friday demo runs a scenario; the end-to-end scenario runs in CI.

## 2. Roles (RACI agreed at kickoff)

| # | Role | Owns |
|---|---|---|
| 1 | Architect / product owner / delivery lead + merchant API | `/v1`, webhooks, event catalog, ADRs, CI/CD, backlog |
| 2 | Core platform | config, clock, database, event log, auth, audit |
| 3 | Routing & optimisation | travel-time model, VRP solver, wave planner |
| 4 | Carrier, capacity & assignment | drivers, vehicles, compliance, shifts, eligibility |
| 5 | Driver app + driver API | `/driver/v1`, geofence, POD, offline sync, mobile web app |
| 6 | Control tower | route monitor, exceptions, rescue, live map |
| 7 | Simulator & data | SimPy world, scenarios, calibration, OSM retrieval |
| 8 | Analytics & QA | KPIs, reports, contract/e2e/load tests |

Everyone also takes a rotating duty: reviewer of the week, demo driver, docs.

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Backlog and priorities | PO | PO | all | mentor |
| Contracts (API/events) | owning module | architect | consumers | all |
| Merge to `main` | author | code owner | reviewer | all |
| Sprint demo | demo driver | PO | all | mentor |

## 3. Sprints

| Sprint | Dates | Goal | Exit demo |
|---|---|---|---|
| S0 Foundations | 26 Oct – 1 Nov | Repo, CI, contracts, PRD, ADRs, core platform | `POST /v1/orders` writes an order and an `order.created` event |
| S1 Merchant & carrier | 2 – 8 Nov | API keys, idempotent orders, webhooks, fleet records, eligibility | merchant receives a signed webhook |
| S2 Planning & execution | 9 – 15 Nov | Wave planner, assignment, driver API and app | an order is planned, accepted, delivered with POD |
| S3 Operations & simulation | 16 – 22 Nov | Control tower, KPIs, simulator with incidents | breakdown → rescue in the simulator, live map |
| S4 Quality & extras | 23 – 29 Nov | Contract/e2e/load gates, calibration, ontology, assistant, release | `v1.0.0` demo of a simulated tricity day |

Ceremonies: Monday planning (30 min), async daily stand-up (issue comment or chat thread), Friday demo + retro
(30 min). Notes in `docs/sprints/`.

## 4. GitHub workflow

- **Board:** GitHub Projects with Status (Backlog → Ready → In progress → In review → Done), Iteration (1 week),
  Priority, Size and Area. Built-in automations move items to Done when the PR merges.
- **Issues:** forms for epic, user story (Given/When/Then), bug, spike, ADR. Definition of Ready: acceptance criteria,
  area label, milestone.
- **PRs:** Conventional title (linted), `Closes #n` (checked), ≤ 400 changed lines where possible, CI green, squash
  merge. `main` is protected by a ruleset (PR required, `ci` check required, linear history, no force-push).
- **Claude Code:** `/story`, `/commit`, `/pr`, `/sprint-review`, `/adr` skills keep specs, commits and PRs consistent.

## 5. Risks

| Risk | Mitigation |
|---|---|
| Modules block each other | Contracts frozen in S0; mocks and example events; simulator replays |
| Over-engineering | Modular monolith; Kafka/OSRM only behind adapters |
| Optimisation rabbit hole | Feasible routes first; improvements measured in the simulator |
| Unrealistic simulation | Calibrate on published data; label assumptions |
| Mobile connectivity | Offline queue + idempotent sync from day one |
| Untrusted AI actions | Assistant writes only after explicit human approval |
| Exam weeks / capacity | Cut line per sprint; stretch items marked |
