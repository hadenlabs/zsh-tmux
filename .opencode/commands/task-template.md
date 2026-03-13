---
description: Create a task template folder under .infobot/.tmp/tasks/ for a feature (task.json + subtask_01.json)
agent: OpenRepoManager
---

1. Read the feature name from `$1`.
2. If `$1` is missing, ask the user for the feature name (recommend `kebab-case`, e.g. `readme-refresh`).
3. Create a new task template:
   - Run `bash .infobot/skills/task-management/router.sh init <feature>`
4. Print the generated paths and the next commands to use:
   - `bash .infobot/skills/task-management/router.sh status <feature>`
   - `bash .infobot/skills/task-management/router.sh next <feature>`
