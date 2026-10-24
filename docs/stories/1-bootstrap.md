# #1 — Bootstrap repo tooling, CI and Claude workflow

**Status:** Done · **Area:** platform · **Milestone:** M1 Foundations

## Context
Eight people (or one person plus Claude) need the same setup, the same quality bar and a repeatable
issue → spec → commit → PR flow before any feature work starts.

## User story
As a contributor I want one-command setup, CI and a story → commit → PR workflow so that every change lands clean and
reviewable.

## Acceptance criteria
- [x] `make setup && make test` installs with uv and passes.
- [x] PRs run the `ci` check (ruff lint + format, pytest); `ci` is the single required check on `main`.
- [x] `pr-checks` enforces Conventional PR titles and a linked issue.
- [x] Issue forms (epic, story, bug, spike, ADR), PR template, CODEOWNERS, Dependabot.
- [x] `CLAUDE.md`, `.claude/settings.json`, guard hooks and skills `/story`, `/commit`, `/pr`, `/sprint-review`, `/adr`.

## Design
- **Tooling:** uv (Python 3.12 pinned in `.python-version`), hatchling build, ruff (lint + format), pytest + pytest-asyncio.
- **CI:** `lint` and `test` jobs feed an aggregator job named `ci`, so the branch ruleset needs one stable check name.
- **Guard hooks:** stdlib-only Python so they work on macOS, Linux and Windows.

## Test plan
Smoke test imports the package; CI proves the toolchain on a clean runner.

## Out of scope
Application code (issue #3 onwards).
