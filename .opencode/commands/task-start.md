---
description: Start working on the next ready subtask for a feature (marks it in_progress)
agent: OpenCoder
---

1. Read the feature name from `$1`.
2. If `$1` is missing:
   - List available features by enumerating directories under `.infobot/.tmp/tasks/` (one directory per feature).
   - If no features exist, ask the user for the feature name (recommend `kebab-case`, e.g. `readme-refresh`).
   - Otherwise, show a numbered list (`1..N`) and ask the user to select one to start.
3. Show current status:
   - Run `bash .infobot/skills/task-management/router.sh status <feature>`
4. Execute the next ready subtask through OpenCode:
   - Run `bash .infobot/skills/task-management/router.sh execute <feature>`
5. The router must:
    - resolve the next ready subtask,
    - mark it as `in_progress`, and
   - invoke `opencode run` through a primary runtime agent while passing the subtask's `suggested_agent` as the preferred executor in the prompt.
6. Prompt selection rules:
   - If the subtask has a `prompt`, use it as the primary execution prompt.
   - Otherwise, synthesize a prompt from the subtask metadata (`title`, `execution_notes`, `run`, `deliverables`, `acceptance_criteria`).
   - If `suggested_agent` has a configured model in `opencode.json`, pass that model to `opencode run`.
7. Sequential behavior:
   - If a subtask completes successfully and marks itself `completed`, continue automatically with the next ready subtask.
   - Stop when there are no more ready subtasks or when the current subtask remains `in_progress`.
