#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

# Backward-compatible shim: task-management moved to `.infobot/`.
exec bash "${ROOT_DIR}/.infobot/skills/task-management/router.sh" "$@"
