---
name: validate-pr
description: Find vulnerabilities or errors in a pull request (checks, scans, merge blockers) and propose fixes.
license: MIT
---

## What I do

- Ask which PR to validate (number or URL).
- List PRs assigned to you so you can pick quickly.
- Inspect CI/check failures, required checks, and merge blockers.
- Look for security signals when available (Code Scanning / dependency updates).
- Produce an actionable checklist to get the PR merge-ready.

## First question (required)

1. List PRs assigned to the current user:

```bash
gh pr list --assignee @me --state open --json number,title,url,headRefName,baseRefName,updatedAt --jq '.[] | "#\(.number)\t\(.headRefName) → \(.baseRefName)\t\(.updatedAt)\t\(.title)\t\(.url)"'
```

2. Ask: "Which PR do you want to validate? (number or URL)"

Notes:

- If the list is empty, fallback to:

```bash
gh pr list --author @me --state open --json number,title,url,headRefName,baseRefName,updatedAt --jq '.[] | "#\(.number)\t\(.headRefName) → \(.baseRefName)\t\(.updatedAt)\t\(.title)\t\(.url)"'
```

## Validation workflow (for PR <N>)

### 1) Quick PR status

```bash
gh pr view <N> --json number,url,title,state,isDraft,mergeable,baseRefName,headRefName,author,reviewDecision,labels,assignees
```

### 2) Checks / CI failures

```bash
gh pr checks <N>
```

If there are failing runs, inspect logs:

```bash
branch="$(gh pr view <N> --json headRefName --jq .headRefName)"
gh run list --branch "${branch}" --limit 10
```

Pick the failing run id and view:

```bash
gh run view <RUN_ID> --log-failed
```

### 3) Files changed (to scope the investigation)

```bash
gh pr diff <N> --stat
```

### 4) Security signals (best-effort)

Code scanning alerts for the PR merge ref (may require permissions; can be empty):

```bash
owner="$(gh repo view --json owner --jq .owner.login)"
repo="$(gh repo view --json name --jq .name)"
gh api "repos/${owner}/${repo}/code-scanning/alerts?ref=refs/pull/<N>/merge&state=open" --jq '.[] | "\(.rule.id)\t\(.rule.severity)\t\(.state)\t\(.html_url)"'
```

If the API call returns 403/404, report that security alerts are not accessible with current permissions and continue with checks/logs.

### 5) Output

Provide:

- The failing checks (name + link) and the root cause from logs.
- Any merge blockers (conflicts, required reviews, missing approvals).
- Any open code-scanning alerts (if accessible) with severity.
- Concrete next steps (commands to run locally and files to change).
