---
description: Validate a PR for errors/vulnerabilities (asks for PR; lists assigned PRs)
agent: OpenRepoManager
---

1. Load skill: validate-pr
2. If `$1` is provided (PR number or URL), validate that PR; otherwise list PRs assigned to `@me` and ask which PR to validate.
