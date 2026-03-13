---
description: Run goji smart commit (task validate, group changes, derive key/id from branch, commit with goji)
agent: OpenRepoManager
---

1. Load skill: goji-commit-smart
2. Run smart commits for the current branch:
   - Always run `task validate` first
   - Group changes into 1..N commits
   - Derive issue key/id from the branch name (per `infobot.toml`)
   - Create commits using goji conventions and sign-off
