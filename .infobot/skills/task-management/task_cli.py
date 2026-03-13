#!/usr/bin/env python3

import json
import os
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from typing import NoReturn


def _now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _die(msg: str, code: int = 2) -> NoReturn:
    sys.stderr.write(msg + "\n")
    raise SystemExit(code)


def _tasks_dir(feature: str) -> str:
    return os.path.join(".infobot", ".tmp", "tasks", feature)


def _list_subtasks(feature: str):
    base = _tasks_dir(feature)
    if not os.path.isdir(base):
        _die(f"feature not found: {base}")
    files = []
    for name in os.listdir(base):
        if name.startswith("subtask_") and name.endswith(".json"):
            files.append(os.path.join(base, name))
    files.sort()
    return files


def _load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json_atomic(path: str, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def _seq_from_filename(path: str) -> str:
    name = os.path.basename(path)
    # subtask_01.json -> 01
    mid = name[len("subtask_") : -len(".json")]
    return mid


def _task_path(feature: str) -> str:
    return os.path.join(_tasks_dir(feature), "task.json")


def _subtask_path(feature: str, seq: str) -> str:
    seq = str(seq).zfill(2) if str(seq).isdigit() else str(seq)
    return os.path.join(_tasks_dir(feature), f"subtask_{seq}.json")


def _ordered_subtasks(feature: str):
    paths = _list_subtasks(feature)
    ordered = []
    for path in paths:
        obj = _load_json(path)
        seq = str(obj.get("seq") or _seq_from_filename(path))
        seq = str(seq).zfill(2) if str(seq).isdigit() else str(seq)
        ordered.append((seq, path, obj))
    ordered.sort(key=lambda item: item[0])
    return ordered


def _root_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _load_opencode_config():
    config_path = os.path.join(_root_dir(), "opencode.json")
    if not os.path.isfile(config_path):
        return {}
    try:
        return _load_json(config_path)
    except (json.JSONDecodeError, OSError):
        return {}


def _resolve_agent_model(agent_name: str) -> str | None:
    if not agent_name:
        return None
    config = _load_opencode_config()
    agents = config.get("agent") or config.get("agents") or {}
    agent = agents.get(agent_name)
    if not isinstance(agent, dict):
        return None
    model = agent.get("model")
    return str(model) if model else None


def _refresh_task_metadata(feature: str):
    task_path = _task_path(feature)
    if not os.path.isfile(task_path):
        return None

    task_obj = _load_json(task_path)
    ordered = _ordered_subtasks(feature)
    total = len(ordered)
    completed = sum(1 for _, _, obj in ordered if _is_completed(obj))

    task_obj["subtask_count"] = total
    task_obj["completed_count"] = completed

    if total > 0 and completed == total:
        task_obj["status"] = "completed"
        task_obj["completed_at"] = _now_iso()
    else:
        task_obj["status"] = "active"
        task_obj.pop("completed_at", None)

    _write_json_atomic(task_path, task_obj)
    return task_obj


def _is_completed(obj) -> bool:
    return str(obj.get("status", "")).lower() == "completed"


def _ready(subtasks_by_seq, obj) -> bool:
    if str(obj.get("status", "")).lower() != "pending":
        return False
    deps = obj.get("depends_on") or []
    if not isinstance(deps, list):
        return False
    for dep in deps:
        dep_seq = str(dep).zfill(2) if str(dep).isdigit() else str(dep)
        dep_obj = subtasks_by_seq.get(dep_seq)
        if not dep_obj or not _is_completed(dep_obj):
            return False
    return True


def _ready_for_seq(feature: str, seq: str) -> bool:
    subtasks_by_seq = {}
    for s, _, obj in _ordered_subtasks(feature):
        s = str(s).zfill(2) if str(s).isdigit() else str(s)
        subtasks_by_seq[s] = obj

    obj = subtasks_by_seq.get(seq)
    if not obj:
        return False
    return _ready(subtasks_by_seq, obj)


def _next_ready_seq(feature: str) -> str | None:
    subtasks_by_seq = {}
    ordered = []
    for seq, _, obj in _ordered_subtasks(feature):
        subtasks_by_seq[seq] = obj
        ordered.append((seq, obj))

    for seq, obj in ordered:
        if _ready(subtasks_by_seq, obj):
            return seq
    return None


def _normalize_items(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def _append_list(lines: list[str], label: str, values) -> None:
    lines.append(f"{label}:")
    items = _normalize_items(values)
    if not items:
        lines.append("- (none specified)")
        return

    for value in items:
        if isinstance(value, dict):
            path = value.get("path") or json.dumps(value, ensure_ascii=True)
            reason = value.get("reason")
            line_info = value.get("lines")
            details = []
            if line_info:
                details.append(f"lines {line_info}")
            if reason:
                details.append(str(reason))
            suffix = f" ({'; '.join(details)})" if details else ""
            lines.append(f"- {path}{suffix}")
        else:
            lines.append(f"- {value}")


def _subtask_user_prompt(feature: str, seq: str, task_obj, subtask_obj) -> str:
    prompt = subtask_obj.get("prompt")
    if isinstance(prompt, str) and prompt.strip():
        return prompt.strip()

    image_spec = subtask_obj.get("image_spec")
    if isinstance(image_spec, dict):
        prompt = image_spec.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            return prompt.strip()

    lines = []
    title = str(subtask_obj.get("title") or "").strip()
    objective = str(task_obj.get("objective") or "").strip()
    if title:
        lines.append(title)
    if objective:
        lines.append(f"Feature objective: {objective}")

    execution_notes = _normalize_items(subtask_obj.get("execution_notes"))
    acceptance = _normalize_items(subtask_obj.get("acceptance_criteria"))
    deliverables = _normalize_items(subtask_obj.get("deliverables"))
    run_spec = subtask_obj.get("run")

    if execution_notes:
        lines.append("")
        lines.append("Execution notes:")
        for note in execution_notes:
            lines.append(f"- {note}")

    if run_spec:
        lines.append("")
        lines.append("Requested execution:")
        if isinstance(run_spec, dict):
            command = run_spec.get("command")
            if command:
                lines.append(f"- Run `{command}`")
            for key, value in run_spec.items():
                if key == "command":
                    continue
                lines.append(f"- {key}: {value}")
        else:
            lines.append(f"- {run_spec}")

    if deliverables:
        lines.append("")
        lines.append("Deliverables:")
        for item in deliverables:
            lines.append(f"- {item}")

    if acceptance:
        lines.append("")
        lines.append("Acceptance criteria:")
        for item in acceptance:
            lines.append(f"- {item}")

    if not lines:
        lines.append(f"Complete subtask {feature} {seq}.")
    return "\n".join(lines)


def _resolve_opencode_bin() -> str:
    configured = os.environ.get("OPENCODE_BIN", "opencode")
    if os.path.isabs(configured):
        if os.path.isfile(configured) and os.access(configured, os.X_OK):
            return configured
        _die(f"opencode executable not found: {configured}")

    resolved = shutil.which(configured)
    if resolved:
        return resolved
    _die(f"opencode executable not found in PATH: {configured}")


def _subtask_prompt(feature: str, seq: str, task_obj, subtask_obj) -> str:
    preferred_agent = str(subtask_obj.get("suggested_agent") or "CoderAgent")
    runtime_model = str(
        subtask_obj.get("opencode_model") or _resolve_agent_model(preferred_agent) or ""
    ).strip()
    lines = [
        "Execute the following repository task using the task-manager workflow.",
        "",
        f"Feature: {feature}",
        f"Task file: {_task_path(feature)}",
        f"Subtask file: {_subtask_path(feature, seq)}",
        f"Objective: {task_obj.get('objective') or '(not specified)'}",
        f"Subtask: {seq} - {subtask_obj.get('title') or '(untitled)'}",
        f"Preferred execution agent: {preferred_agent}",
    ]
    if runtime_model:
        lines.append(f"Preferred execution model: {runtime_model}")

    acceptance = _normalize_items(subtask_obj.get("acceptance_criteria"))
    deliverables = _normalize_items(subtask_obj.get("deliverables"))
    context_files = _normalize_items(
        subtask_obj.get("context_files") or task_obj.get("context_files")
    )
    reference_files = _normalize_items(
        subtask_obj.get("reference_files") or task_obj.get("reference_files")
    )
    user_prompt = _subtask_user_prompt(feature, seq, task_obj, subtask_obj)

    lines.append("")
    lines.append("Task prompt:")
    lines.append(user_prompt)
    lines.append("")
    _append_list(lines, "Acceptance criteria", acceptance)
    lines.append("")
    _append_list(lines, "Deliverables", deliverables)
    lines.append("")
    _append_list(lines, "Context files", context_files)
    lines.append("")
    _append_list(lines, "Reference files", reference_files)
    lines.extend(
        [
            "",
            "Instructions:",
            "- Read the referenced task files before making changes.",
            "- Implement the subtask in this repository using the assigned agent.",
            "- Verify the deliverables and acceptance criteria.",
            (
                f"- When finished, mark the subtask complete with "
                f'`bash .infobot/skills/task-management/router.sh complete {feature} {seq} "<summary>"`.'
            ),
            "- If blocked, explain the blocker and leave the subtask in_progress.",
        ]
    )
    if preferred_agent == "Image Specialist":
        lines.extend(
            [
                "",
                "Image persistence requirements:",
                "- Generate the image by calling the OpenRouter API directly with `curl`.",
                "- Use the configured image model for this task when building the API request.",
                "- Authenticate with `OPENCODE_OPENROUTER_API_KEY`.",
                "- Request image output as base64 or data URL, decode it, and write the PNG to the deliverable path.",
                "- Do not stop after describing the image in chat; the PNG file must exist on disk before completing the subtask.",
            ]
        )
    return "\n".join(lines)


def _run_opencode_for_subtask(feature: str, seq: str, task_obj, subtask_obj) -> int:
    suggested_agent = str(subtask_obj.get("suggested_agent") or "CoderAgent")
    runtime_agent = str(subtask_obj.get("opencode_agent") or "OpenAgent")
    runtime_model = str(
        subtask_obj.get("opencode_model") or _resolve_agent_model(suggested_agent) or ""
    ).strip()
    opencode_bin = _resolve_opencode_bin()
    root_dir = _root_dir()
    task_path = _task_path(feature)
    subtask_path = _subtask_path(feature, seq)
    prompt = _subtask_prompt(feature, seq, task_obj, subtask_obj)

    command = [
        opencode_bin,
        "run",
        "--dir",
        root_dir,
        "--agent",
        runtime_agent,
    ]
    if runtime_model:
        command.extend(["--model", runtime_model])
    command.extend(
        [
            "--file",
            task_path,
            "--file",
            subtask_path,
            "--",
            prompt,
        ]
    )

    print(
        "executing\t{}\t{}\t{}\t{}\t{}\t{}".format(
            feature,
            seq,
            suggested_agent,
            runtime_agent,
            runtime_model or "(default-model)",
            shlex.join(command),
        )
    )
    completed = subprocess.run(command, cwd=root_dir, check=False)
    return completed.returncode


def cmd_execute(feature: str, seq: str | None = None, agent_id: str | None = None) -> int:
    feature = feature.strip()
    _refresh_task_metadata(feature)
    requested_seq = seq
    executed_any = False

    while True:
        resolved_seq = requested_seq or _next_ready_seq(feature)
        if not resolved_seq:
            if executed_any:
                _refresh_task_metadata(feature)
                return 0
            _die(f"no ready subtask found for feature: {feature}")

        resolved_seq = (
            str(resolved_seq).zfill(2)
            if str(resolved_seq).isdigit()
            else str(resolved_seq)
        )

        start_agent_id = agent_id or "opencode"
        start_result = cmd_start(feature, resolved_seq, start_agent_id)
        if start_result != 0:
            return start_result

        task_path = _task_path(feature)
        subtask_path = _subtask_path(feature, resolved_seq)
        if not os.path.isfile(task_path):
            _die(f"task not found: {task_path}")
        if not os.path.isfile(subtask_path):
            _die(f"subtask not found: {subtask_path}")

        task_obj = _load_json(task_path)
        subtask_obj = _load_json(subtask_path)
        result = _run_opencode_for_subtask(feature, resolved_seq, task_obj, subtask_obj)
        if result != 0:
            return result

        executed_any = True
        updated_subtask = _load_json(subtask_path)
        _refresh_task_metadata(feature)

        if not _is_completed(updated_subtask):
            print(f"waiting\t{feature}\t{resolved_seq}\tsubtask not completed")
            return 0

        if requested_seq:
            return 0

        requested_seq = None


def cmd_status(feature: str) -> int:
    _refresh_task_metadata(feature)
    paths = _list_subtasks(feature)
    rows = []
    for p in paths:
        obj = _load_json(p)
        seq = str(obj.get("seq") or _seq_from_filename(p))
        title = str(obj.get("title") or "")
        status = str(obj.get("status") or "unknown")
        rows.append((seq, status, title))

    for seq, status, title in rows:
        print(f"{seq}\t{status}\t{title}")
    return 0


def cmd_complete(feature: str, seq: str, summary: str) -> int:
    seq = str(seq).zfill(2) if str(seq).isdigit() else str(seq)
    path = _subtask_path(feature, seq)
    if not os.path.isfile(path):
        _die(f"subtask not found: {path}")

    obj = _load_json(path)
    obj["status"] = "completed"
    obj["completed_at"] = _now_iso()
    obj["completion_summary"] = summary
    _write_json_atomic(path, obj)
    _refresh_task_metadata(feature)
    print(f"completed\t{feature}\t{seq}")
    return 0


def cmd_start(feature: str, seq: str, agent_id: str | None = None) -> int:
    seq = str(seq).zfill(2) if str(seq).isdigit() else str(seq)
    path = _subtask_path(feature, seq)
    if not os.path.isfile(path):
        _die(f"subtask not found: {path}")

    obj = _load_json(path)
    status = str(obj.get("status", "")).lower()
    if status == "completed":
        _die(f"subtask already completed: {feature} {seq}")
    if status == "in_progress":
        print(f"in_progress\t{feature}\t{seq}")
        return 0
    if status != "pending":
        _die(f"subtask not startable from status: {status}")

    if not _ready_for_seq(feature, seq):
        _die(f"subtask not ready (deps/status): {feature} {seq}")

    obj["status"] = "in_progress"
    obj["started_at"] = _now_iso()
    if agent_id:
        obj["agent_id"] = agent_id
    _write_json_atomic(path, obj)

    print(f"started\t{feature}\t{seq}")
    return 0


def cmd_next(feature: str) -> int:
    seq = _next_ready_seq(feature)
    if seq:
        obj = _load_json(_subtask_path(feature, seq))
        title = str(obj.get("title") or "")
        print(f"{seq}\t{title}")
        return 0
    return 1


def cmd_parallel(feature: str) -> int:
    subtasks_by_seq = {}
    ordered = []
    for seq, _, obj in _ordered_subtasks(feature):
        subtasks_by_seq[seq] = obj
        ordered.append((seq, obj))

    any_out = False
    for seq, obj in ordered:
        if bool(obj.get("parallel")) and _ready(subtasks_by_seq, obj):
            title = str(obj.get("title") or "")
            print(f"{seq}\t{title}")
            any_out = True
    return 0 if any_out else 1


def cmd_init(feature: str) -> int:
    if not feature or feature.strip() == "":
        _die("usage: router.sh init <feature>")

    feature = feature.strip()
    base = _tasks_dir(feature)
    os.makedirs(base, exist_ok=True)

    task_path = os.path.join(base, "task.json")
    subtask_path = os.path.join(base, "subtask_01.json")

    if os.path.exists(task_path) or os.path.exists(subtask_path):
        _die(
            "task template already exists (refusing to overwrite): "
            f"{task_path} / {subtask_path}"
        )

    task_obj = {
        "id": feature,
        "name": feature,
        "status": "active",
        "objective": "",
        "context_files": [],
        "reference_files": [],
        "exit_criteria": [],
        "subtask_count": 1,
        "completed_count": 0,
        "created_at": _now_iso(),
    }

    subtask_obj = {
        "id": f"{feature}-01",
        "seq": "01",
        "title": "",
        "status": "pending",
        "depends_on": [],
        "parallel": True,
        "suggested_agent": "CoderAgent",
        "context_files": [],
        "reference_files": [],
        "acceptance_criteria": [],
        "deliverables": [],
    }

    _write_json_atomic(task_path, task_obj)
    _write_json_atomic(subtask_path, subtask_obj)

    print(f"created\t{task_path}")
    print(f"created\t{subtask_path}")
    return 0


def main(argv) -> int:
    if len(argv) < 2:
        _die("usage: router.sh <init|status|start|execute|complete|next|parallel> ...")
    cmd = argv[1]

    if cmd == "status":
        if len(argv) != 3:
            _die("usage: router.sh status <feature>")
        return cmd_status(argv[2])

    if cmd == "complete":
        if len(argv) < 5:
            _die('usage: router.sh complete <feature> <seq> "<summary>"')
        feature = argv[2]
        seq = argv[3]
        summary = " ".join(argv[4:]).strip()
        return cmd_complete(feature, seq, summary)

    if cmd == "start":
        if len(argv) not in (4, 5):
            _die("usage: router.sh start <feature> <seq> [agent_id]")
        feature = argv[2]
        seq = argv[3]
        agent_id = argv[4] if len(argv) == 5 else None
        return cmd_start(feature, seq, agent_id)

    if cmd == "next":
        if len(argv) != 3:
            _die("usage: router.sh next <feature>")
        return cmd_next(argv[2])

    if cmd == "execute":
        if len(argv) not in (3, 4, 5):
            _die("usage: router.sh execute <feature> [seq] [agent_id]")
        feature = argv[2]
        seq = argv[3] if len(argv) >= 4 else None
        agent_id = argv[4] if len(argv) == 5 else None
        return cmd_execute(feature, seq, agent_id)

    if cmd == "parallel":
        if len(argv) != 3:
            _die("usage: router.sh parallel <feature>")
        return cmd_parallel(argv[2])

    if cmd == "init":
        if len(argv) != 3:
            _die("usage: router.sh init <feature>")
        return cmd_init(argv[2])

    _die(f"unknown command: {cmd}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
