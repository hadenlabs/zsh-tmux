# Task Management Skill (Infobot)

This directory provides the task-management router used by Infobot.

Commands:

- `bash .infobot/skills/task-management/router.sh init <feature>`
- `bash .infobot/skills/task-management/router.sh status <feature>`
- `bash .infobot/skills/task-management/router.sh start <feature> <seq> [agent_id]`
- `bash .infobot/skills/task-management/router.sh execute <feature> [seq] [agent_id]`
- `bash .infobot/skills/task-management/router.sh next <feature>`
- `bash .infobot/skills/task-management/router.sh parallel <feature>`
- `bash .infobot/skills/task-management/router.sh complete <feature> <seq> "summary"`

Task files live under:

- `.infobot/.tmp/tasks/{feature}/subtask_XX.json`

Execution behavior:

- `execute` uses each subtask as the OpenCode prompt source.
- Set `suggested_agent` in the subtask JSON to choose which agent runs it.
- The router invokes OpenCode through a primary runtime agent (`OpenAgent` by default) and passes `suggested_agent` as the preferred agent inside the prompt.
- If the selected `suggested_agent` has a model configured in `opencode.json`, the router also passes that model to `opencode run`.
- If the subtask defines `prompt`, that text is passed through directly.
- For `Image Specialist`, the task prompt now explicitly requires persisting the generated image via OpenRouter API + base64 decode so the PNG is written to disk.
- If there is no explicit `prompt`, the router builds one from fields like `title`, `execution_notes`, `run`, `deliverables`, and `acceptance_criteria`.
- When a subtask marks itself `completed`, `execute` automatically continues with the next ready subtask until it reaches a blocker or finishes the feature.
