---
name: update-pr
description: Push branch commits and update the existing PR body safely (prefer REST API)
license: MIT
---

## What I do

- Validate changes locally.
- Push the current branch (handles unset upstream).
- Detect the PR for the current branch.
- Regenerate the PR body from `.github/PULL_REQUEST_TEMPLATE.md` using the current `main...HEAD` diff.
- Update the PR body using GitHub REST API via `gh api` (fallback to `gh pr edit`).

## When to use me

Use this when you already have a PR open and need to refresh its description to match the latest branch changes.

## Process

1. Run `task validate`
2. Collect context:
   - `git diff main...HEAD --stat`
   - `git diff main...HEAD`
   - `git log main...HEAD --oneline`
3. Push current branch:
   - If upstream is not set: `git push -u origin HEAD`
   - Otherwise: `git push`
4. Detect PR:
   - Prefer: `gh pr view --json number,url --jq '.number, .url'`
   - Fallback: `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --json number,url --jq '.[0].number, .[0].url'`
5. Generate updated PR body (based on `.github/PULL_REQUEST_TEMPLATE.md`) and fill:
   - Proposed changes: bullets derived from `main...HEAD` diff (group by area; reference key paths)
   - Testing: include `task validate`
   - Migration steps (if any)
   - Screenshots placeholders
   - Types of changes: mark what applies
   - Checklist: mark what is true
6. Update PR body:
   - Prefer (REST, avoids GraphQL classic-projects failures):

```bash
owner="$(gh repo view --json owner --jq .owner.login)"
repo="$(gh repo view --json name --jq .name)"
gh api --method PATCH "repos/${owner}/${repo}/pulls/<PR_NUMBER>" \
  -f body="$(cat <<'EOF'
<filled template body>
EOF
)"
```

- Fallback:

```bash
gh pr edit <PR_NUMBER> --body "$(cat <<'EOF'
<filled template body>
EOF
)"
```
