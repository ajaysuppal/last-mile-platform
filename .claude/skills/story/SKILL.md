---
name: story
description: Turn a GitHub issue into a story spec (mini-PRD) and a feature branch. Use when starting work on an issue.
argument-hint: <issue-number>
disable-model-invocation: true
---

# /story <issue-number>

Goal: before writing code, produce a one-page spec the product owner can approve, and a clean branch.

1. Run `gh issue view $ARGUMENTS --json number,title,body,labels,milestone,url`.
   - Stop and say what is missing if the issue has no acceptance criteria (Given/When/Then) or no `area:*` label.
2. Read `CLAUDE.md`, the relevant ADRs in `docs/adr/`, `docs/events/asyncapi.yaml` and the modules the story touches.
3. Write `docs/stories/<number>-<kebab-slug>.md` from `docs/stories/_TEMPLATE.md`:
   context, user story, acceptance criteria copied verbatim, API delta (paths, request/response), events emitted/consumed,
   database changes, files to touch, existing code to reuse, test plan, out of scope, open questions.
4. `git fetch origin && git switch -c <type>/<number>-<kebab-slug> origin/main`
   where `<type>` is `feat`, `fix`, `chore`, `docs`, `test` or `refactor`.
5. Commit only the spec: `docs(story): spec for #<number>`.
6. Stop. Summarise the spec in 5 bullets plus one ELI5 sentence and wait for approval before implementing.
