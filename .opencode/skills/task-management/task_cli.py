#!/usr/bin/env python3

"""Backward-compatible shim.

The canonical task-management implementation lives under `.infobot/`.
This file delegates to it so existing tooling referencing `.opencode/` keeps working.
"""

import os
import runpy
import sys


def main() -> int:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    target = os.path.join(
        root_dir, ".infobot", "skills", "task-management", "task_cli.py"
    )
    if not os.path.isfile(target):
        sys.stderr.write(f"infobot task_cli not found: {target}\n")
        return 2
    sys.argv[0] = target
    runpy.run_path(target, run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
