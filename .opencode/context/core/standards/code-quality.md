# Code Quality Standards

These are lightweight, repo-agnostic defaults. Prefer project-specific rules in `../project/` when present.

- Keep changes small and focused; avoid drive-by refactors.
- Prefer simple, explicit code over clever abstractions.
- Handle errors explicitly; return non-zero / throw with context.
- Avoid debug leftovers: `TODO`, `FIXME`, `console.log`, `set -x`.
- Keep files consistent with existing conventions in the repo.
