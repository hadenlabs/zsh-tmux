# Task Management Skill (Local)

This directory provides the minimal scripts referenced by bundled agents.

Commands:

- `bash .infobot/skills/task-management/router.sh init <feature>`
- `bash .infobot/skills/task-management/router.sh status <feature>`
- `bash .infobot/skills/task-management/router.sh start <feature> <seq> [agent_id]`
- `bash .infobot/skills/task-management/router.sh next <feature>`
- `bash .infobot/skills/task-management/router.sh parallel <feature>`
- `bash .infobot/skills/task-management/router.sh complete <feature> <seq> "summary"`

Backward compatibility:

- `bash .opencode/skills/task-management/router.sh ...` still works (shim).

Task files live under:

- `.infobot/.tmp/tasks/{feature}/subtask_XX.json`
