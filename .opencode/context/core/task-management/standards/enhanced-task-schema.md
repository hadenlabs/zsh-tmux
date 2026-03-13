# Enhanced Task Schema (Minimal)

This is the minimum JSON schema expected by the task-management router in this repo.

Example:

```json
{
  "seq": "01",
  "title": "Implement X",
  "status": "pending",
  "parallel": true,
  "depends_on": ["00"],
  "deliverables": ["path/to/file"],
  "acceptance_criteria": ["Behavior works"]
}
```
