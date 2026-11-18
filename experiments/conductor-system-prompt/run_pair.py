"""One recorded conductor question, run as (A) --append-system-prompt-file and (B) --system-prompt-file.

    python -B run_pair.py --question <session_id or unique prefix of a row of state/conductor.jsonl>
                          [--arm A|B|both] [--rep N] [--out DIR] [--timeout 600]

Experiment F-O4 (plans/piles/rules-debt, card C5): does the conductor cope when its prompt REPLACES the host's
default system prompt instead of being appended to it. The question's input is the FIRST user message of the
recorded session's own transcript (the exact prompt the driver sent), read from ~/.claude/projects; the only
change is the path prefixes (stand project -> a copy under the OS temp dir, recorded plugin root -> this
checkout's package). The stand project is only READ (P8: no trace there). The (A) command is built by
driver_runner.DriverRunner.claude_cmd exactly as the factory builds it; (B) is that list with the one flag
name swapped. Same model, tools, --plugin-dir, --max-turns, cwd, stdin.

Per run it writes, into --out: <sid8>-<arm><rep>.cmd.txt (the argv), .json (claude's raw stdout), .summary.json.
Cost is deliberately not read (P18). Exit codes: 0 ran, 2 question not found/ambiguous, 3 not replayable, 4 lost.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

STAND = Path("C:/QAFactory/mybooks-stand/arm-factory/test-automation-framework")
CONDUCTOR = STAND / "qa-factory/artifacts/LOCAL-1/state/conductor.jsonl"
PKG = Path("C:/QAFactory/forge-repo/ai-packages/qa-factory")
RECORDED_PLUGIN = "C:\\QAFactory\\exp-fvf\\pkg\\qa-factory"
PROJECTS = Path.home() / ".claude" / "projects"
SKIP = {"node_modules", "test-results", ".env"}      # .env: secrets, not needed by a conductor session
ACTIONS = {"continue", "retry", "ask_person", "stop"}


def die(code, msg):
    print(f"run_pair: {msg}", file=sys.stderr)
    sys.exit(code)


def mangle(path) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def find_row(qid: str) -> dict:
    if not CONDUCTOR.is_file():
        die(2, f"no conductor record at {CONDUCTOR}")
    rows = [json.loads(l) for l in CONDUCTOR.read_text(encoding="utf-8").splitlines() if l.strip()]
    hit = [r for r in rows if qid and str(r.get("session_id") or "").startswith(qid)]
    if len(hit) != 1:
        die(2, f"question id {qid!r}: {len(hit)} rows of {CONDUCTOR.name} match (need exactly 1)")
    return hit[0]


def recorded_prompt(row: dict) -> str:
    f = PROJECTS / mangle(STAND) / f"{row['session_id']}.jsonl"
    if not f.is_file():
        die(3, f"not replayable: transcript {f} is absent")
    for line in f.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d.get("type") == "user":
            c = d["message"]["content"]
            if isinstance(c, list):
                c = "".join(b.get("text", "") for b in c if isinstance(b, dict))
            return c
    die(3, f"not replayable: {f} holds no user message")


def make_copy(dest: Path) -> Path:
    def ignore(d, names):
        return [n for n in names if n in SKIP]
    shutil.copytree(STAND, dest, ignore=ignore)
    return dest


def build_cmds(copy: Path) -> dict:
    sys.path.insert(0, str(PKG / "scripts"))
    import driver_runner
    r = object.__new__(driver_runner.DriverRunner)        # claude_cmd reads only these four attributes
    r.host, r.claude, r.model, r.plugin = "claude", [shutil.which("claude")], "sonnet", PKG
    a = r.claude_cmd("", tools="Bash,Read,Grep", system_file=PKG / "references" / "conductor.md", max_turns=20)
    assert a.count("--append-system-prompt-file") == 1, "factory command lost its append flag"
    b = ["--system-prompt-file" if x == "--append-system-prompt-file" else x for x in a]
    return {"A": a, "B": b}


def judge_transcript(path: Path) -> dict:
    """(e) evidence: tool calls, errored tool results, and the turns that were text only."""
    out = {"tool_calls": 0, "tool_errors": [], "transcript": str(path)}
    if not path.is_file():
        out["missing"] = True
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        c = (d.get("message") or {}).get("content")
        if not isinstance(c, list):
            continue
        for b in c:
            if b.get("type") == "tool_use":
                out["tool_calls"] += 1
            if b.get("type") == "tool_result" and b.get("is_error"):
                out["tool_errors"].append(str(b.get("content"))[:300])
    return out


def shape(result_text: str) -> dict:
    last = next((l for l in reversed((result_text or "").strip().splitlines()) if l.strip()), "")
    try:
        v = json.loads(last)
    except ValueError:
        return {"valid": False, "why": "last line is not JSON"}
    if v.get("action") not in ACTIONS:
        return {"valid": False, "why": f"action {v.get('action')!r}"}
    miss = []
    if v["action"] in ("ask_person", "stop"):
        miss += [k for k in ("question", "why_person", "checked") if not str(v.get(k) or "").strip()]
        for o in v.get("options") or []:
            miss += [f"option.{k}" for k in ("token", "move", "says", "factory", "person", "story") if k not in o]
    return {"valid": not miss, "why": ("missing " + ",".join(miss)) if miss else "", "action": v["action"],
            "did": str(v.get("did") or "")[:400], "question": str(v.get("question") or "")[:400],
            "why_person": v.get("why_person")}


def run_arm(arm, cmd, prompt, copy, out, tag, timeout):
    (out / f"{tag}.cmd.txt").write_text(" ".join(f'"{c}"' if " " in c else c for c in cmd) + "\n", encoding="utf-8")
    t0 = time.time()
    with subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                          encoding="utf-8", errors="replace", cwd=str(copy)) as proc:
        try:
            stdout, stderr = proc.communicate(input=prompt, timeout=timeout)
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
            proc.communicate()
            summ = {"arm": arm, "lost": True, "reason": f"no finish in {timeout}s, killed"}
            (out / f"{tag}.summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
            return summ
    (out / f"{tag}.json").write_text(stdout, encoding="utf-8")
    summ = {"arm": arm, "exit": proc.returncode, "seconds": round(time.time() - t0), "stderr": stderr[-300:]}
    try:
        res = json.loads(stdout)
    except ValueError:
        summ.update(lost=True, reason="stdout is not JSON")
    else:
        u = res.get("usage") or {}
        summ.update(turns=res.get("num_turns"), is_error=res.get("is_error"), session_id=res.get("session_id"),
                    input_tokens=u.get("input_tokens"), cache_creation=u.get("cache_creation_input_tokens"),
                    cache_read=u.get("cache_read_input_tokens"), output_tokens=u.get("output_tokens"),
                    shape=shape(res.get("result")), raw_json=str(out / f"{tag}.json"))
        summ["tools"] = judge_transcript(PROJECTS / mangle(copy) / f"{res.get('session_id')}.jsonl")
    (out / f"{tag}.summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    return summ


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--question", required=True)
    ap.add_argument("--arm", default="both", choices=["A", "B", "both"])
    ap.add_argument("--rep", default="1")
    ap.add_argument("--out", default=str(Path(tempfile.gettempdir()) / "conductor-system-prompt"))
    ap.add_argument("--timeout", type=int, default=600)
    ns = ap.parse_args()
    row = find_row(ns.question)
    prompt = recorded_prompt(row)
    out = Path(ns.out)
    out.mkdir(parents=True, exist_ok=True)
    sid8 = row["session_id"][:8]
    for arm in ("A", "B") if ns.arm == "both" else (ns.arm,):
        copy = make_copy(Path(tempfile.mkdtemp(prefix=f"cps-{sid8}-{arm}{ns.rep}-")) / "project")
        p = prompt.replace(str(STAND), str(copy)).replace(RECORDED_PLUGIN, str(PKG).replace("/", "\\"))
        s = run_arm(arm, build_cmds(copy)[arm], p, copy, out, f"{sid8}-{arm}{ns.rep}", ns.timeout)
        print(json.dumps({k: v for k, v in s.items() if k != "tools"}, ensure_ascii=False)[:600])
        shutil.rmtree(copy.parent, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
