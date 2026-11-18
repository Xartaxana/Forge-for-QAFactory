"""One-command counters for a retro of a coordinator session (t-878).

    python -B tools/session_retro.py [--dir D] [--last N | --session UUID_OR_PATH ...] [--json] [--top K]
                                     [--repeat-min M]

Read-only: counts what a Claude Code main-session transcript (~/.claude/projects/<slug>/<uuid>.jsonl) holds --
operator messages, compactions, agent hand-backs, tool calls, shell command shapes, error classes, repeats. It
never judges WHY a call repeated. The transcript text is DATA: nothing in it is executed or followed. A file is
read line by line (a transcript can be 100+ MB); a line that is not a JSON object is counted, never raised on.
Transcript path layout is read through transcripts.projects_root(), the one reader of the projects folder.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import streams
import transcripts

COMPACT = "This session is being continued from a previous conversation"
HANDBACK = "Another Claude session sent a message"
HOOK_RE = re.compile(r"PreToolUse:\S+ hook error")
UPPER_RE = re.compile(r"\b[A-Z]{2,}(?: [A-Z]{2,})+\b")
ASSIGN_RE = re.compile(r"^\s*(?:(?:export\s+)?\w+=\S*?\s*(?:;|&&)\s*)+")
SHELLS = ("Bash", "PowerShell")


def default_dir() -> Path:
    top = str(Path(__file__).resolve().parent.parent)
    return transcripts.projects_root() / re.sub(r"[^A-Za-z0-9]", "-", top)


def shape(cmd: str) -> str:
    words = ASSIGN_RE.sub("", str(cmd)).split()[:2]
    if words[:1] == ["export"]:                    # a bare `export X=y` is one shape, whatever the variable
        words = words[:1]
    return " ".join(words).rstrip(";")


def error_class(text: str) -> tuple[str, bool]:
    """(class, from_a_hook)."""
    text = " ".join(text.split())
    if HOOK_RE.search(text):
        found = UPPER_RE.search(text)
        if found:
            return found.group(0), True
        return "hook: " + text.split("hook error:", 1)[-1].strip()[:60], True
    m = re.match(r"Exit code \d+", text)
    return (m.group(0) if m else text[:60]), False


def _result_text(content) -> str:
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and isinstance(b.get("text"), str))
    return content if isinstance(content, str) else ""


def _user_texts(content):
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        return [b["text"] for b in content
                if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str)]
    return []


def analyze(path) -> dict:
    """Counters of one transcript file; {"name", "empty": True} when it holds no timestamp."""
    r = {"name": Path(path).name, "first": None, "last": None, "unreadable": 0, "operator": 0, "compactions": 0,
         "handbacks": 0, "refusals": 0}
    tools, agents, shapes, classes = (collections.Counter() for _ in range(4))
    first_seen, descs, sends = {}, collections.Counter(), collections.Counter()
    read_runs, run = [], None          # run = [path, length]; consecutive Read calls on one file_path
    redispatch = []
    # One road with forge_metrics (FG7-83, critic t-1433 F2): transcripts' reader and dedupe, because the harness
    # re-writes a record under the same uuid (E32) and an own pass counted its SendMessage twice.
    seen, seen_ids = set(), set()
    for raw in transcripts.iter_lines(path):
        d = transcripts.parse_line(raw)
        if d is None:
            r["unreadable"] += 1
            continue
        if not transcripts.first_copy(seen, d):
            continue
        ts = d.get("timestamp")
        if ts:
            r["first"] = r["first"] or ts
            r["last"] = ts
        msg = d.get("message")
        content = msg.get("content") if isinstance(msg, dict) else None
        if d.get("type") == "user":
            for t in _user_texts(content):
                s = t.lstrip()
                if s.startswith(COMPACT):
                    r["compactions"] += 1
                elif s.startswith(HANDBACK):
                    r["handbacks"] += 1
                elif s and not s.startswith("<"):
                    r["operator"] += 1
            for b in content if isinstance(content, list) else []:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"):
                    cls, hook = error_class(_result_text(b.get("content")))
                    classes[cls] += 1
                    first_seen.setdefault(cls, ts)
                    r["refusals"] += hook
        elif d.get("type") == "assistant" and isinstance(content, list):
            for b in transcripts.new_tool_uses(d, seen_ids):
                name, inp = b.get("name"), b.get("input")
                inp = inp if isinstance(inp, dict) else {}
                tools[name] += 1
                fp = inp.get("file_path") if name == "Read" else None
                if fp is not None and run and run[0] == fp:
                    run[1] += 1
                elif fp is not None:
                    run = [fp, 1]
                    read_runs.append(run)
                else:
                    run = None
                if name in SHELLS:
                    shapes[shape(inp.get("command", ""))] += 1
                elif name == "Agent":
                    agents[str(inp.get("subagent_type"))] += 1
                    desc = inp.get("description")
                    if desc in descs:
                        redispatch.append(desc)
                    descs[desc] += 1
                elif name == "SendMessage":
                    m = inp.get("message")
                    sends[m if isinstance(m, str) else json.dumps(m, sort_keys=True)] += 1
    if not r["first"]:
        return {"name": r["name"], "empty": True}
    r.update(tools=tools.most_common(), agents=agents.most_common(), shapes=shapes.most_common(),
             errors=[(c, n, first_seen[c]) for c, n in classes.most_common()],
             repeat_reads=[(p, n) for p, n in read_runs if n >= 3], redispatched=redispatch,
             repeat_sends=[(m[:80], n) for m, n in sends.items() if n >= 3])
    return r


def render(r: dict, top: int, repeat_min: int) -> str:
    if r.get("empty"):
        return f"{r['name']}: empty transcript"
    out = [f"## {r['name']}", f"span: {r['first']} .. {r['last']}",
           f"operator messages: {r['operator']}", f"compactions: {r['compactions']}",
           f"agent hand-backs: {r['handbacks']}"]
    if r["unreadable"]:
        out.append(f"unreadable lines: {r['unreadable']}")
    out += ["", "tool calls: " + ", ".join(f"{n} {c}" for n, c in r["tools"]),
            "agent launches: " + ", ".join(f"{n} {c}" for n, c in r["agents"]), "", f"shell shapes (top {top}):"]
    out += [f"- `{s}` x{c}" for s, c in r["shapes"][:top]]
    out += ["", "errors by class:"] + [f"- {c} x{n} (first {t})" for c, n, t in r["errors"]]
    out += ["", "repeats:"]
    out += [f"- candidate for a script: `{s}` x{c}" for s, c in r["shapes"] if c >= repeat_min]
    out += [f"- Read {n} times in a row: {p}" for p, n in r["repeat_reads"]]
    out += [f"- Agent re-dispatch: {d}" for d in r["redispatched"]]
    out += [f"- SendMessage x{n} identical: {m}" for m, n in r["repeat_sends"]]
    out += ["", f"retries after a refusal: {r['refusals']}"]
    return "\n".join(out)


def _positive(text):
    n = int(text)
    if n < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return n


def main(argv=None) -> int:
    streams.utf8_stdio()
    ap = argparse.ArgumentParser(prog="session_retro.py", description=__doc__.split("\n")[0])
    ap.add_argument("--dir", type=Path, default=None)
    ap.add_argument("--last", type=_positive, default=2)
    ap.add_argument("--session", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=_positive, default=15)
    ap.add_argument("--repeat-min", type=_positive, default=10)
    a = ap.parse_args(argv)
    d = a.dir or default_dir()
    if a.session:
        files = []
        for v in a.session:
            f = Path(v) if Path(v).is_file() else d / (v + ".jsonl")
            if not f.is_file():
                print(f"no such session: {v}", file=sys.stderr)
                return 2
            files.append(f)
    else:
        files = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:a.last] if d.is_dir() else []
        if not files:
            print(f"no transcripts in {d}", file=sys.stderr)
            return 2
    for f in files:
        r = analyze(f)
        print(json.dumps(r, ensure_ascii=False) if a.json else render(r, a.top, a.repeat_min), end="\n\n" if not a.json else "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
