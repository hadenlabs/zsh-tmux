#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PY="${PYTHON:-python3}"

exec "${PY}" "${ROOT_DIR}/.infobot/skills/task-management/task_cli.py" "$@"
