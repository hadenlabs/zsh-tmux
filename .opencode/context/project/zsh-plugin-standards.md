# zsh-ai Plugin Standards

Based on `AGENTS.md` in this repo.

- File layout uses a factory `main.zsh` that loads `base.zsh` + OS-specific file (`osx.zsh` | `linux.zsh`).
- Public functions: `ai::action`.
- Internal functions: `ai::internal::action`.
- Variables: `AI_VARIABLE_NAME`.
- `.zsh` files must start with `#!/usr/bin/env ksh`.
- Files under `docs/` must be written in English.
