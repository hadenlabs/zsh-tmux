---
description: Run a release bump using the release skill (major/minor/patch)
agent: OpenRepoManager
---

1. Load skill: release
2. Read the bump type from `$1` (expected: `major`, `minor`, or `patch`)
   - If `$1` is missing or not one of the expected values, ask the user to choose one of: `major` | `minor` | `patch`
3. Run: `task release:$1`
4. Confirm the new version and show the generated changelog entry (if produced by the task)
