---
name: sprint-review
description: Summarise a sprint (milestone) from merged PRs and open issues into docs/sprints.
argument-hint: <milestone title or number>
disable-model-invocation: true
---

# /sprint-review <milestone>

1. Collect data:
   - `gh api repos/{owner}/{repo}/milestones --jq '.[] | {number,title,due_on,open_issues,closed_issues}'`
   - `gh issue list --milestone "<title>" --state all --json number,title,state,labels`
   - `gh pr list --state merged --search "milestone:\"<title>\"" --json number,title,additions,deletions,mergedAt`
     (fall back to PRs merged within the milestone dates).
   - `gh run list --branch main --limit 20 --json conclusion,name` for CI health.
2. Write `docs/sprints/<milestone-slug>.md`: goal, done (with PR links), carried over, metrics (PR count, median size,
   cycle time), contract changes, risks, demo notes, retro (keep / change / try), next sprint candidates.
3. Commit with `docs(sprint): review <milestone>` on a branch and open a PR via `/pr`.
