"""Run one headless turn of the factory in a project copy.

    python experiments/measurers/run_headless.py --name <run> --prompt-file <prompt.md> --out <out-1.json>
    python experiments/measurers/run_headless.py --name <run> --resume <session_id> --message "Gate A: ..." --out <out-2.json>
    python experiments/measurers/run_headless.py --name <run> --message-file <gate-a.md> --resume <session_id> --out <out-2.json>

Starts `claude -p` in <copy>/test-harness with the branch plugin, Sonnet, acceptEdits and the
tools the factory needs allowed; the JSON result (session_id, cost, num_turns, result text) is
written to --out and its head printed. CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 keeps background
roles alive. Nothing here touches the live checkout.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import paths

ROOT = paths.BASE
PLUGIN = str(paths.PACKAGE)
TOOLS = "Bash,Read,Write,Edit,MultiEdit,Glob,Grep,Agent,Task,SendMessage,TaskOutput,TaskStop,Monitor,WebFetch,NotebookEdit,ListAgents"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--prompt-file")
    ap.add_argument("--message")
    ap.add_argument("--message-file")
    ap.add_argument("--resume")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:                              # after parsing, so `--help` works with no config (F-14)
        paths.require_base()          # this script writes under BASE
    except paths.BaseNotSet as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    try:
        project = ROOT / paths.copy_folder(a.name, paths.BASELINES) / "test-harness"
    except ValueError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    if not project.is_dir():
        sys.stderr.write("no copy at %s: make it with prepare_copy.py --name %s (or name the baseline in the runs "
                         "table, QA_RUNS_TABLE)\n" % (project, a.name))
        return 2
    if a.prompt_file:
        text = Path(a.prompt_file).read_text(encoding="utf-8")
    elif a.message_file:
        text = Path(a.message_file).read_text(encoding="utf-8")
    else:
        text = a.message
    if not text:
        print("no prompt", file=sys.stderr)
        return 2
    cmd = [shutil.which("claude") or "claude", "-p", text, "--plugin-dir", PLUGIN, "--model", "sonnet",
           "--permission-mode", "acceptEdits", "--allowedTools", TOOLS, "--output-format", "json"]
    if a.resume:
        cmd += ["--resume", a.resume]
    env = dict(os.environ, CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="0")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {a.name}: start in {project}" + (f" (resume {a.resume[:8]})" if a.resume else ""))
    sys.stdout.flush()
    res = subprocess.run(cmd, cwd=str(project), env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out.write_text(res.stdout, encoding="utf-8")
    (out.with_suffix(".stderr.txt")).write_text(res.stderr, encoding="utf-8")
    print(f"[{time.strftime('%H:%M:%S')}] exit={res.returncode} after {int(time.time() - t0)}s -> {out}")
    try:
        d = json.loads(res.stdout)
    except ValueError:
        print("non-JSON stdout head:", res.stdout[:800])
        print("stderr head:", res.stderr[:800])
        return 1
    print(f"session={d.get('session_id')} turns={d.get('num_turns')} cost=${d.get('total_cost_usd', 0):.2f} "
          f"subtype={d.get('subtype')} error={d.get('is_error')}")
    print("RESULT:\n" + (d.get("result") or "")[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
