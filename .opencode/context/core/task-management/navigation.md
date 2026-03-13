# Task Management

This repo includes a minimal task-management CLI used by agent prompts:

- `.infobot/skills/task-management/router.sh`

Backward compatibility:

- `.opencode/skills/task-management/router.sh` (shim)

Schema notes:

- Subtasks live under `.infobot/.tmp/tasks/{feature}/subtask_XX.json`
- Fields supported by the CLI:
  - `title` (string)
  - `status` (pending|in_progress|completed)
  - `depends_on` (array of seq strings like "01")
  - `parallel` (boolean)

See: `standards/enhanced-task-schema.md`
