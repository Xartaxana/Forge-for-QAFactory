#!/usr/bin/env python3
"""clean_driver_state.py - drops what the driver's earlier life left in `state/driver-state.json` (t-2006 sec 3 step 10).

    python clean_driver_state.py --task-root <T>

Takes a BYTE COPY to `state/driver-state.before-walk.json` first (an existing copy is the first one and is kept: a second run never
overwrites it), then removes only the keys of DROP. `sessions` stays: a saved session of an old dispatch is never reused for a new id.
No `driver-state.json` (the driver never ran) is nothing to clean: exit 0, said. A file that is not a JSON object: exit 1, untouched.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

DROP = ("deferred", "deferred_seq", "code_close", "question_stop", "s6_reproved", "s6_manual_runner", "s6_probe_after", "package_pass")


def clean(task_root) -> tuple:
    """(exit code, words)."""
    state = Path(task_root).resolve() / "state" / "driver-state.json"
    if not state.is_file():
        return 0, f"{state} does not exist: nothing to clean"
    try:
        doc = json.loads(state.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return 1, f"{state} cannot be read as JSON ({type(exc).__name__}); left untouched"
    if not isinstance(doc, dict):
        return 1, f"{state} is not a JSON object; left untouched"
    backup = state.with_name("driver-state.before-walk.json")
    if not backup.exists():
        shutil.copyfile(state, backup)
    dropped = [k for k in DROP if k in doc]
    for key in dropped:
        del doc[key]
    state.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return 0, f"dropped {len(dropped)} key(s): {', '.join(dropped) or 'none'}; kept {len(doc)} (sessions: {'sessions' in doc}); copy: {backup.name}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-root", required=True)
    args = parser.parse_args(argv)
    code, words = clean(args.task_root)
    print(words)
    return code


if __name__ == "__main__":
    sys.exit(main())
