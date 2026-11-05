"""Which paths a role reached for and did not find — the raw evidence behind FR-15.

    python read_misses.py [<run>]

`<run>` defaults to default_right of the runs table (QA_RUNS_TABLE); without a table it is required.

`known_paths` and the brief's file list are the answer to a miss: a path the work needs is given,
not searched for. Written because the plan carried "11 misses" from a partial count and the
transcripts of an earlier run held **129 over 644 reads** across 74 paths - the top of that list
was one file hunted at two levels. Run it after the next run: the number is the measure of whether
the fixes made since worked, and the list says what to give a role next.

No test of its own (FR-28): it counts what the transcripts say and prints it.
"""
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

import paths

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
run = sys.argv[1] if len(sys.argv) > 1 else paths.DEFAULT_RIGHT
if not run:
    print("read_misses.py: the run is required: it has no default without a runs table (QA_RUNS_TABLE); "
          "usage: read_misses.py <run>", file=sys.stderr)
    raise SystemExit(2)
PROJECT = paths.BASE / paths.copy_folder(run, paths.BASELINES) / "test-harness"
root = paths.transcript_dir(PROJECT)
print("transcripts:", root, root.is_dir())

misses = collections.Counter()
by_role = collections.Counter()
total_reads = 0
for main in sorted(glob.glob(str(root / "*.jsonl")), key=os.path.getmtime):
    role = "?"
    pending = {}
    for line in Path(main).open(encoding="utf-8", errors="replace"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        message = row.get("message") or {}
        if row.get("type") == "user" and role == "?":
            content = message.get("content")
            text = content if isinstance(content, str) else " ".join(
                part.get("text", "") for part in content if isinstance(part, dict))
            found = re.search(r"qa-[a-z\-]+", text or "")
            role = found.group(0) if found else "?"
        if row.get("type") == "assistant":
            for block in message.get("content", []) or []:
                if isinstance(block, dict) and block.get("type") == "tool_use" \
                        and block.get("name") in ("Read", "Glob", "Grep"):
                    pending[block.get("id")] = (block.get("name"),
                                                (block.get("input") or {}).get("file_path")
                                                or (block.get("input") or {}).get("path") or "")
                    if block.get("name") == "Read":
                        total_reads += 1
        if row.get("type") == "user":
            for block in message.get("content", []) or []:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                tool, path = pending.get(block.get("tool_use_id"), ("", ""))
                if not tool:
                    continue
                body = block.get("content")
                text = body if isinstance(body, str) else " ".join(
                    part.get("text", "") for part in body if isinstance(part, dict))
                if block.get("is_error") or re.search(r"does not exist|no such file|not found",
                                                      str(text or ""), re.I):
                    if path:
                        misses[path] += 1
                        by_role[role] += 1

print(f"Read calls: {total_reads}; misses: {sum(misses.values())} over {len(misses)} paths\n")
for path, count in misses.most_common(40):
    print(f"{count:3}  {path}")
print("\nby role:", dict(by_role))
