---
name: adr
description: Scaffold the next architecture decision record in docs/adr.
argument-hint: <decision title>
disable-model-invocation: true
---

# /adr <title>

1. Find the highest number in `docs/adr/` and use the next one (4 digits).
2. Create `docs/adr/<NNNN>-<kebab-title>.md` with sections: Status (Proposed), Context, Options considered (at least two,
   with trade-offs), Decision, Consequences (good and bad), Links.
3. Fill Context and Options from the conversation and the code; leave Decision for the human if it is not settled.
4. Add the ADR to the index table in `docs/adr/README.md`.
