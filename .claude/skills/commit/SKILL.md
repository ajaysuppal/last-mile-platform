---
name: commit
description: Write a Conventional Commit message for the staged changes and commit them.
disable-model-invocation: true
---

# /commit

1. Run `git diff --staged`. If nothing is staged, say so and stop.
2. Refuse to commit (and explain) if the staged diff contains a `.env` file, an API key (`lmd_live_`, `lmd_test_` followed by a
   long secret, `whsec_`, `sk-ant-`), a private key, or a database URL with a password.
3. Write the message:
   - Subject: `type(scope): imperative summary` ≤ 72 chars. Types: feat, fix, docs, refactor, test, chore, ci, perf, build.
     Scopes: core, merchant-api, webhooks, carrier, planning, driver, control-tower, analytics, sim, data, semantic,
     assistant, web, ci, docs, deps.
   - Body: why the change was needed and anything surprising (wrap at 72).
   - Footer: `Refs #<n>` using the issue number in the branch name, then the co-author trailer if Claude wrote the code.
4. Show the message, then `git commit -F -` with it.
