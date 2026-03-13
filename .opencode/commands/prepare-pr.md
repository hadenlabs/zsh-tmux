---
description: Prepare PR with description
agent: OpenRepoManager
---

1. Run `git diff main...HEAD --stat` to see changed files
2. Run `git log main...HEAD --oneline` to see commits
3. Load skill: git-release
4. Generate a PR description with:
   - Summary of changes
   - Testing notes
   - Migration steps (if any)
   - Screenshots (suggest placeholders)
5. Output the `gh pr create` command ready to paste
