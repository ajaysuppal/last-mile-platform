---
name: pr
description: Verify the branch, update CURRENT_STATE, and open a pull request with the template filled in.
disable-model-invocation: true
---

# /pr

1. Run `make lint` and `make test`. If either fails, stop and fix — never open a red PR.
   Capture the last ~15 lines of test output as evidence.
2. If routes or events changed, regenerate `docs/api/openapi.json` (`uv run lastmile openapi`) and update
   `docs/events/asyncapi.yaml`.
3. Append a dated bullet to `docs/CURRENT_STATE.md` describing what now works; commit it (`docs: update current state`).
4. Build the PR body from `.github/PULL_REQUEST_TEMPLATE.md`: summary (plus one ELI5 sentence), `Closes #<n>`,
   link to the story spec, contract changes ticked, test evidence pasted.
5. `git push -u origin HEAD`, then
   `gh pr create --base main --title "<conventional title>" --body-file <tmpfile> --label <area labels>`.
6. Print the PR URL. Do not merge — merging happens after `ci` is green (squash only).
